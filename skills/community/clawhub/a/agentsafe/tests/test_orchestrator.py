"""Orchestrator end-to-end acceptance with fully faked externals."""

import httpx
import pytest
import respx

from agentsafe.agents.validation import ValidationAgent
from agentsafe.analyzers.bytecode import (
    BytecodeAnalysis,
    BytecodeAnalyzer,
    BytecodeClass,
    BytecodeClassification,
    BytecodeToolRun,
)
from agentsafe.analyzers.source import SourceAnalysis, SourceAnalyzer, ToolRun
from agentsafe.config import LLMProviderConfig
from agentsafe.explorer import ContractNotVerifiedError, EtherscanClient, SourceBundle, SourceFile
from agentsafe.llm.router import LLMRouter
from agentsafe.orchestrator import AuditOrchestrator, OrchestratorError
from agentsafe.rpc import EthRpcClient
from agentsafe.schemas import Finding, FindingStatus

ADDR = "0x" + "ab" * 20
RPC = "https://rpc.test"
ETH = "https://api.etherscan.test/v2/api"

CODE = "0x6080604052" + "ff" * 300

BUNDLE = SourceBundle(
    is_verified=True,
    contract_name="Vault",
    compiler_version="v0.8.19+commit.7dd6d404",
    files=[SourceFile(path="V.sol", content="contract Vault {}")],
)

SLITHER_FINDING = Finding(
    title="[slither] reentrancy-eth",
    severity="high",
    status=FindingStatus.TOOL_DETECTED,
    source=["slither"],
    detector_id="reentrancy-eth",
    description="Reentrancy in withdraw()",
    evidence="withdraw() calls receiver before state update",
    file_path="V.sol",
    line_start=10,
)


class FakeExplorer(EtherscanClient):
    def __init__(self, verified: bool = True, fail: bool = False):
        super().__init__("k", base_url=ETH, sleeper=_ns)
        self.verified, self.fail = verified, fail

    async def get_verified_source(self, address):
        if self.fail:
            raise RuntimeError("explorer down")
        if not self.verified:
            raise ContractNotVerifiedError(address)
        return BUNDLE


class FakeSourceAnalyzer(SourceAnalyzer):
    def __init__(self, findings, error: bool = False):
        super().__init__()
        self.findings, self.error = findings, error

    async def analyze(self, bundle):
        if self.error:
            raise RuntimeError("source analysis crashed")
        return SourceAnalysis(
            runs=[
                ToolRun(tool="slither", executed=True, findings=self.findings),
                ToolRun(tool="aderyn", executed=True, findings=[]),
            ],
            partial_failure=False,
        )


class FakeBytecodeAnalyzer(BytecodeAnalyzer):
    def __init__(self, findings=None, error: bool = False, fail_all: bool = False):
        super().__init__()
        self.findings = findings or []
        self.error, self.fail_all = error, fail_all

    async def analyze(self, bytecode):
        if self.error:
            raise RuntimeError("bytecode analysis crashed")
        runs = [
            BytecodeToolRun(
                tool="mythril",
                executed=not self.fail_all,
                findings=self.findings,
                error=None if not self.fail_all else "not installed",
            ),
            BytecodeToolRun(
                tool="heimdall", executed=True, pseudo_sources={"decompiled.sol": "pseudo"}
            ),
        ]
        return BytecodeAnalysis(
            classification=BytecodeClassification(BytecodeClass.NORMAL, len(bytecode) // 2 - 1),
            runs=runs,
        )


async def _ns(_):
    return None


def _router():
    prov = LLMProviderConfig(
        name="p", base_url="https://llm.test/v1", api_key="sk", model="m", rpm_limit=60
    )
    import time

    return LLMRouter(
        [prov],
        global_rpm=600,
        request_timeout_seconds=5,
        max_retries_per_call=0,
        http_client=httpx.AsyncClient(),
        sleeper=_ns,
        clock=lambda: time.monotonic(),
    )


def _orchestrator(
    explorer, source_analyzer, bytecode_analyzer, router=None, agents=(), timeout=900.0
):
    return AuditOrchestrator(
        rpc=EthRpcClient(RPC, sleeper=_ns),
        explorer=explorer,
        source_analyzer=source_analyzer,
        bytecode_analyzer=bytecode_analyzer,
        router=router,
        agents=list(agents),
        validation_agent=ValidationAgent(),
        total_timeout_seconds=timeout,
        llm_max_calls=5,
        llm_deadline_seconds=60.0,
    )


def _stub_rpc(code: str):
    respx.post(RPC).mock(
        return_value=httpx.Response(200, json={"jsonrpc": "2.0", "id": 1, "result": code})
    )


class TestVerifiedSourcePath:
    @respx.mock
    async def test_full_pipeline_produces_report(self):
        from agentsafe.agents.fund_flow import FundFlowAgent

        _stub_rpc(CODE)
        orch = _orchestrator(
            FakeExplorer(verified=True),
            FakeSourceAnalyzer([SLITHER_FINDING]),
            FakeBytecodeAnalyzer(findings=[]),
            router=None,  # no LLM configured: agents skipped honestly
            agents=[FundFlowAgent(_router())],
        )
        stages: list = []

        def progress(st):
            stages.append((st.name, st.state.value))

        report = await orch.run(ADDR, task_id="task-x", progress=progress)
        assert report.is_verified_source is True
        assert report.task_id == "task-x"
        assert any(f.detector_id == "reentrancy-eth" for f in report.findings)
        assert "slither" in report.summary.tools_executed
        assert "mythril" in report.summary.tools_executed
        assert report.llm_usage.total_calls == 0  # router None -> agents skipped
        assert any(s == "llm_agents" and v == "skipped" for s, v in stages)

    @respx.mock
    async def test_invalid_address_fails_fast(self):
        orch = _orchestrator(FakeExplorer(), FakeSourceAnalyzer([]), FakeBytecodeAnalyzer())
        with pytest.raises(OrchestratorError, match="invalid_address"):
            await orch.run("0x123")

    @respx.mock
    async def test_eoa_rejected(self):
        _stub_rpc("0x")
        orch = _orchestrator(FakeExplorer(), FakeSourceAnalyzer([]), FakeBytecodeAnalyzer())
        with pytest.raises(OrchestratorError, match="not_a_contract"):
            await orch.run(ADDR)


class TestClosedSourcePath:
    @respx.mock
    async def test_unverified_contract_uses_bytecode(self):
        _stub_rpc(CODE)
        orch = _orchestrator(
            FakeExplorer(verified=False),
            FakeSourceAnalyzer([SLITHER_FINDING]),  # must NOT run
            FakeBytecodeAnalyzer(findings=[]),
        )
        report = await orch.run(ADDR)
        assert report.is_verified_source is False
        assert "mythril" in report.summary.tools_executed
        assert "slither" not in report.summary.tools_executed

    @respx.mock
    async def test_explorer_failure_falls_back_to_bytecode(self):
        _stub_rpc(CODE)
        orch = _orchestrator(
            FakeExplorer(fail=True),
            FakeSourceAnalyzer([]),
            FakeBytecodeAnalyzer(findings=[]),
        )
        report = await orch.run(ADDR)
        assert report.is_verified_source is False
        assert any("etherscan" in e for e in report.errors)
        assert any("bytecode path" in lim for lim in report.limitations)


class TestPartialFailure:
    @respx.mock
    async def test_source_tool_crash_still_reports_bytecode(self):
        _stub_rpc(CODE)
        myth_finding = Finding(
            title="[mythril] Integer Overflow",
            severity="high",
            status=FindingStatus.TOOL_DETECTED,
            source=["mythril"],
            detector_id="SWC-101",
            description="overflow",
            evidence="bytecode offset 100: ADD",
        )
        orch = _orchestrator(
            FakeExplorer(verified=True),
            FakeSourceAnalyzer([], error=True),
            FakeBytecodeAnalyzer(findings=[myth_finding]),
        )
        report = await orch.run(ADDR)
        assert any(f.detector_id == "SWC-101" for f in report.findings)
        assert "slither" in report.summary.tools_failed
        assert any("source analysis" in e for e in report.errors)

    @respx.mock
    async def test_all_bytecode_tools_missing_recorded_not_clean(self):
        _stub_rpc(CODE)
        orch = _orchestrator(
            FakeExplorer(verified=False),
            FakeSourceAnalyzer([]),
            FakeBytecodeAnalyzer(fail_all=True),
        )
        report = await orch.run(ADDR)
        assert "mythril" in report.summary.tools_failed
        assert any(
            "partial failures" in lim or "not evidence of safety" in lim
            for lim in report.limitations
        )


class TestHardDeadline:
    @respx.mock
    async def test_deadline_exceeded_raises(self):
        _stub_rpc(CODE)

        class HangingAnalyzer(FakeSourceAnalyzer):
            async def analyze(self, bundle):
                import asyncio as _a

                await _a.sleep(99999)  # real block: must hit the hard deadline
                raise RuntimeError()

        import time

        # Verified source -> the pipeline actually reaches the source
        # analyzer, which hangs until the hard deadline fires.
        orch = AuditOrchestrator(
            rpc=EthRpcClient(RPC, sleeper=_ns),
            explorer=FakeExplorer(verified=True),
            source_analyzer=HangingAnalyzer([]),
            bytecode_analyzer=FakeBytecodeAnalyzer([]),
            router=None,
            agents=[],
            validation_agent=ValidationAgent(),
            total_timeout_seconds=0.05,
            clock=lambda: time.monotonic(),
        )
        with pytest.raises(OrchestratorError, match="audit_timeout"):
            await orch.run(ADDR)


class TestValidationFlow:
    @respx.mock
    async def test_llm_findings_get_validated(self):
        _stub_rpc(CODE)
        router = _router()
        llm_finding = Finding(
            title="Unprotected withdraw",
            severity="high",
            status=FindingStatus.LLM_SUGGESTED,
            source=["fund_flow"],
            description="hypothesis",
            evidence="withdraw() calls receiver",
            file_path="V.sol",
            line_start=10,
            confidence=0.7,
        )

        class OneShotAgent:
            name = "fund_flow"

            async def analyze(self, budget, material):
                from agentsafe.agents.base import AgentResult

                return AgentResult(agent="fund_flow", findings=[llm_finding])

        orch = _orchestrator(
            FakeExplorer(verified=True),
            FakeSourceAnalyzer([SLITHER_FINDING]),
            FakeBytecodeAnalyzer(),
            router=router,
            agents=[OneShotAgent()],
        )
        report = await orch.run(ADDR)
        assert report.llm_usage.total_calls == 0  # OneShotAgent bypassed router
        cross = [f for f in report.findings if f.status is FindingStatus.CROSS_CHECKED]
        # withdraw hypothesis is supported by slither reentrancy at same spot
        assert cross, report.findings
        assert cross[0].metadata["validation"]["supporting_detector"] == "reentrancy-eth"
