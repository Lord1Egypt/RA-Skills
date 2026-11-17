"""Audit orchestrator: the full pipeline with stage tracking + hard deadline.

    validate address -> fetch source/bytecode -> classify -> static tools
    -> bounded LLM agents -> validation -> merge -> report

Partial failures never erase partial results. Every stage updates a
StageStatus via the progress callback; the whole run is wrapped in a hard
overall deadline (AUDIT_TIMEOUT_SECONDS).
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Callable, Sequence
from datetime import UTC

from agentsafe import report as report_mod
from agentsafe.agents.base import AnalysisMaterial, BaseAgent, split_segments
from agentsafe.agents.validation import ValidationAgent
from agentsafe.analyzers.bytecode import BytecodeAnalyzer, BytecodeClass
from agentsafe.analyzers.source import SourceAnalyzer
from agentsafe.explorer import ContractNotVerifiedError, EtherscanClient
from agentsafe.llm.router import AuditBudget, LLMRouter, LLMRouterError
from agentsafe.rpc import EthRpcClient
from agentsafe.schemas import (
    AuditReport,
    Finding,
    FindingStatus,
    LLMUsage,
    StageState,
    StageStatus,
    normalize_address,
)

logger = logging.getLogger("agentSAFE.orchestrator")

STAGES = (
    "validate_address",
    "fetch_source",
    "classify",
    "static_analysis",
    "bytecode_analysis",
    "llm_agents",
    "cross_validation",
    "merge_report",
)


class OrchestratorError(RuntimeError):
    def __init__(self, message: str, *, error_code: str = "orchestrator_error") -> None:
        super().__init__(message)
        self.error_code = error_code


class AuditOrchestrator:
    def __init__(
        self,
        *,
        rpc: EthRpcClient,
        explorer: EtherscanClient,
        source_analyzer: SourceAnalyzer,
        bytecode_analyzer: BytecodeAnalyzer,
        router: LLMRouter | None,
        agents: Sequence[BaseAgent],
        validation_agent: ValidationAgent,
        total_timeout_seconds: float = 900.0,
        llm_max_calls: int = 12,
        llm_deadline_seconds: float = 600.0,
        clock: Callable[[], float] | None = None,
    ) -> None:
        self._rpc = rpc
        self._explorer = explorer
        self._source = source_analyzer
        self._bytecode = bytecode_analyzer
        self._router = router
        self._agents = list(agents)
        self._validation = validation_agent
        self._total_timeout = total_timeout_seconds
        self._llm_max_calls = llm_max_calls
        self._llm_deadline = llm_deadline_seconds
        self._clock = clock or time.monotonic

    async def run(
        self,
        address: str,
        task_id: str | None = None,
        progress: Callable[[StageStatus], None] | None = None,
    ) -> AuditReport:
        started = self._clock()
        stages: list[StageStatus] = [StageStatus(name=n, state=StageState.PENDING) for n in STAGES]
        idx = {s.name: i for i, s in enumerate(stages)}

        def stage(name: str) -> StageStatus:
            return stages[idx[name]]

        def emit(st: StageStatus) -> None:
            if progress:
                progress(st)

        def start(name: str) -> None:
            st = stage(name)
            st.state = StageState.RUNNING
            st.started_at = _utcnow()
            emit(st)

        def done(name: str, *, error_code: str | None = None, detail: str | None = None) -> None:
            st = stage(name)
            st.finished_at = _utcnow()
            st.error_code = error_code
            st.detail = detail
            st.state = StageState.FAILED if error_code else StageState.COMPLETED
            emit(st)

        def skip(name: str, why: str) -> None:
            st = stage(name)
            st.state = StageState.SKIPPED
            st.detail = why
            st.finished_at = _utcnow()
            emit(st)

        errors: list[str] = []
        limitations: list[str] = []
        tools_executed: list[str] = []
        tools_failed: list[str] = []
        tool_versions: dict[str, str] = {}
        findings: list[Finding] = []
        budget: AuditBudget | None = None
        is_verified = False

        try:
            async with asyncio.timeout(self._total_timeout):
                # -- 1. validate ------------------------------------------------
                start("validate_address")
                try:
                    addr = normalize_address(address)
                except ValueError as exc:
                    done("validate_address", error_code="invalid_address", detail=str(exc))
                    raise OrchestratorError(
                        f"invalid_address: {exc}", error_code="invalid_address"
                    ) from exc
                done("validate_address")

                # -- 2. fetch source (explorer) --------------------------------
                start("fetch_source")
                bundle = None
                try:
                    bundle = await self._explorer.get_verified_source(addr)
                    is_verified = True
                    done("fetch_source")
                except ContractNotVerifiedError:
                    done("fetch_source")  # not an error: closed-source path
                except Exception as exc:
                    done("fetch_source", error_code="explorer_error", detail=str(exc))
                    errors.append(f"etherscan: {exc}")
                    limitations.append(
                        "verified-source lookup failed; continuing with bytecode path"
                    )

                # -- 3. bytecode fetch + classify -------------------------------
                start("classify")
                code = await self._rpc.get_code(addr)
                if not code or code == "0x":
                    done(
                        "classify",
                        error_code="not_a_contract",
                        detail="address has no runtime code (EOA)",
                    )
                    raise OrchestratorError(
                        f"not_a_contract: {addr} has no runtime bytecode",
                        error_code="not_a_contract",
                    )
                from agentsafe.analyzers.bytecode import classify_bytecode

                classification = classify_bytecode(code)
                cls = classification.bytecode_class
                notes = "; ".join(classification.notes) if classification.notes else ""
                done("classify", detail=f"{cls.value}: {notes}" if notes else cls.value)

                if cls == BytecodeClass.MINIMAL_PROXY_EIP1167 and classification.proxy_target:
                    limitations.append(
                        "EIP-1167 minimal proxy: the implementation at "
                        f"{classification.proxy_target} should be audited separately"
                    )
                if cls in (BytecodeClass.PROXY_EIP1967, BytecodeClass.BEACON_PROXY_EIP1967):
                    limitations.append(
                        "proxy pattern detected: implementation address resolution "
                        "and admin controls require separate review"
                    )

                # -- 4. verified-source static analysis -------------------------
                start("static_analysis")
                source_runs = []
                if bundle is not None:
                    try:
                        source_result = await self._source.analyze(bundle)
                        source_runs = source_result.runs
                        for r in source_result.runs:
                            if r.version:
                                tool_versions[f"{r.tool}_version"] = r.version
                            if r.executed and not r.error:
                                tools_executed.append(r.tool)
                            else:
                                tools_failed.append(r.tool)
                                errors.append(f"{r.tool}: {r.error or 'no result'}")
                        if source_result.partial_failure:
                            limitations.append(
                                "static analysis had partial failures; "
                                "missing tool results are not evidence of safety"
                            )
                    except Exception as exc:
                        errors.append(f"source analysis: {exc}")
                        tools_failed.extend(["slither", "aderyn"])
                        done("static_analysis", error_code="source_analysis_error", detail=str(exc))
                    else:
                        done("static_analysis")
                else:
                    skip("static_analysis", "no verified source (closed-source path)")

                # -- 5. bytecode tools (always run: independent second opinion) --
                start("bytecode_analysis")
                byte_result = None
                try:
                    byte_result = await self._bytecode.analyze(code)
                    for br in byte_result.runs:
                        if br.version:
                            tool_versions[f"{br.tool}_version"] = br.version
                        if br.executed and not br.error:
                            tools_executed.append(br.tool)
                        else:
                            tools_failed.append(br.tool)
                            errors.append(f"{br.tool}: {br.error or 'no result'}")
                except Exception as exc:
                    errors.append(f"bytecode analysis: {exc}")
                    tools_failed.extend(["mythril", "heimdall"])
                    done("bytecode_analysis", error_code="bytecode_analysis_error", detail=str(exc))
                else:
                    done("bytecode_analysis")

                # -- 6. bounded multi-agent LLM analysis ------------------------
                start("llm_agents")
                segments: dict[str, str] = {}
                pseudo = False
                if bundle is not None:
                    segments = split_segments(bundle.files)
                elif byte_result is not None:
                    segments = byte_result.pseudo_source_segments()
                    pseudo = True
                    if not segments:
                        limitations.append(
                            "no pseudo-source could be recovered; LLM bytecode "
                            "analysis skipped (not evidence of safety)"
                        )

                llm_usage = LLMUsage()
                if self._router is not None and segments and self._agents:
                    budget = self._router.start_audit(
                        max_calls=self._llm_max_calls,
                        deadline_seconds=min(
                            self._llm_deadline,
                            self._total_timeout - (self._clock() - started) - 5.0,
                        ),
                    )
                    material = AnalysisMaterial(
                        kind="source" if bundle else "bytecode",
                        segments=segments,
                        is_pseudo_source=pseudo,
                        bytecode=code if bundle is None else None,
                    )
                    for agent in self._agents:
                        try:
                            ares = await agent.analyze(budget, material)
                        except LLMRouterError as exc:
                            errors.append(f"{agent.name}: {exc}")
                            continue
                        findings.extend(ares.findings)
                        errors.extend(ares.errors)
                        if ares.skipped_reason:
                            limitations.append(f"{agent.name}: {ares.skipped_reason}")
                    u = budget.usage_summary()
                    llm_usage = LLMUsage(
                        total_calls=u["total_calls"],
                        total_prompt_tokens=u["prompt_tokens"],
                        total_completion_tokens=u["completion_tokens"],
                        providers_used=u["providers_used"],
                        models_used=u["models_used"],
                        failed_calls=u["failed_calls"],
                    )
                    done("llm_agents", detail=f"{llm_usage.total_calls} calls")
                else:
                    skip("llm_agents", "no LLM router/agents configured or no material")

                # -- 7. cross validation ----------------------------------------
                start("cross_validation")
                tool_findings = [
                    f for r in (source_runs if bundle is not None else []) for f in r.findings
                ]
                if byte_result is not None:
                    tool_findings.extend(byte_result.findings)
                llm_findings = [f for f in findings if f.status == FindingStatus.LLM_SUGGESTED]
                if llm_findings:
                    outcome = self._validation.validate(llm_findings, tool_findings)
                    validated = {
                        id(f): nf for f, nf in zip(llm_findings, outcome.findings, strict=True)
                    }
                    findings = [validated.get(id(f), f) for f in findings]
                    done(
                        "cross_validation",
                        detail=f"cross_checked={outcome.cross_checked} "
                        f"manual_review={outcome.manual_review}",
                    )
                else:
                    skip("cross_validation", "no LLM findings to validate")

                # -- 8. merge + report -------------------------------------------
                start("merge_report")
                if tools_failed:
                    limitations.append(
                        "partial failures: some analysis tools failed or did not "
                        "run; their missing output is not evidence of safety"
                    )
                final = report_mod.build_report(
                    address=addr,
                    task_id=task_id,
                    is_verified_source=is_verified,
                    raw_findings=[*tool_findings, *findings],
                    tools_executed=tools_executed,
                    tools_failed=tools_failed,
                    tool_versions=tool_versions,
                    llm_usage=llm_usage,
                    limitations=limitations,
                    errors=errors,
                    execution_time_seconds=self._clock() - started,
                )
                done("merge_report")
                return final

        except TimeoutError as exc:
            raise OrchestratorError(
                f"audit_timeout: exceeded hard deadline of {self._total_timeout:.0f}s",
                error_code="audit_timeout",
            ) from exc


def _utcnow():
    from datetime import datetime

    return datetime.now(UTC)
