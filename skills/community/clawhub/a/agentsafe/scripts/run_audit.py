#!/usr/bin/env python
"""Worker entry point: run inside the GitHub Actions ephemeral runner.

Usage:
    python scripts/run_audit.py --address 0x... --task-id <id> --output report.json

Reads configuration from environment (.env not used on the worker; the
workflow injects secrets as env vars). Writes report.json on success and on
partial failure; exits 3 only on hard failure. Never prints secrets.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path

# Allow running from a repo checkout without installation.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from agentsafe.agents.access_control import AccessControlAgent  # noqa: E402
from agentsafe.agents.business_logic import BusinessLogicAgent  # noqa: E402
from agentsafe.agents.fund_flow import FundFlowAgent  # noqa: E402
from agentsafe.agents.validation import ValidationAgent  # noqa: E402
from agentsafe.analyzers.bytecode import BytecodeAnalyzer  # noqa: E402
from agentsafe.analyzers.source import SourceAnalyzer  # noqa: E402
from agentsafe.config import Settings, validate_runtime_settings  # noqa: E402
from agentsafe.explorer import EtherscanClient  # noqa: E402
from agentsafe.llm.router import LLMRouter  # noqa: E402
from agentsafe.orchestrator import AuditOrchestrator, OrchestratorError  # noqa: E402
from agentsafe.rpc import EthRpcClient  # noqa: E402
from agentsafe.schemas import StageStatus  # noqa: E402

logger = logging.getLogger("agentSAFE.worker")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="agentSAFE audit worker")
    p.add_argument("--address", required=True, help="EVM contract address (mainnet)")
    p.add_argument("--task-id", required=True, help="task_id issued by the MCP service")
    p.add_argument("--output", default="report.json", help="output report path")
    return p.parse_args()


def build_orchestrator(settings: Settings) -> AuditOrchestrator:
    rpc = EthRpcClient(settings.INFURA_ETH_ENDPOINT)
    explorer = EtherscanClient(settings.ETHERSCAN_API_KEY)
    source_analyzer = SourceAnalyzer()
    bytecode_analyzer = BytecodeAnalyzer()
    providers = settings.llm_providers()
    router = LLMRouter(
        providers,
        global_rpm=settings.LLM_GLOBAL_RPM,
        request_timeout_seconds=settings.LLM_REQUEST_TIMEOUT_SECONDS,
        max_retries_per_call=settings.LLM_MAX_RETRIES_PER_CALL,
        default_max_output_tokens=settings.LLM_MAX_OUTPUT_TOKENS,
    )
    agents = [AccessControlAgent(router), FundFlowAgent(router), BusinessLogicAgent(router)]
    return AuditOrchestrator(
        rpc=rpc,
        explorer=explorer,
        source_analyzer=source_analyzer,
        bytecode_analyzer=bytecode_analyzer,
        router=router,
        agents=agents,
        validation_agent=ValidationAgent(),
        total_timeout_seconds=settings.AUDIT_TIMEOUT_SECONDS,
        llm_max_calls=settings.LLM_MAX_CALLS_PER_AUDIT,
        llm_deadline_seconds=min(600.0, settings.AUDIT_TIMEOUT_SECONDS * 0.66),
    )


async def run(args: argparse.Namespace) -> int:
    settings = Settings()
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL, logging.INFO),
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )
    # httpx INFO lines would log the Etherscan URL with its API key.
    logging.getLogger("httpx").setLevel(logging.WARNING)
    # Worker needs RPC + Etherscan + LLM, but NOT GitHub dispatch credentials.
    validate_runtime_settings(settings, require_github=False)

    stages_written: list[StageStatus] = []

    def progress(st: StageStatus) -> None:
        stages_written.append(st)
        logger.info(
            "stage %s -> %s%s", st.name, st.state.value, f" ({st.detail})" if st.detail else ""
        )

    orchestrator = build_orchestrator(settings)
    try:
        report = await orchestrator.run(args.address, task_id=args.task_id, progress=progress)
    except OrchestratorError as exc:
        logger.error("audit failed: %s (%s)", exc, exc.error_code)
        await asyncio.to_thread(
            Path(args.output).write_text,
            json.dumps(
                {
                    "ok": False,
                    "task_id": args.task_id,
                    "address": args.address,
                    "error_code": exc.error_code,
                    "error": str(exc),
                    "stages": [s.model_dump(mode="json") for s in stages_written],
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        return 3

    await asyncio.to_thread(
        Path(args.output).write_text,
        report.model_dump_json(indent=2),
        encoding="utf-8",
    )
    s = report.summary
    logger.info(
        "audit complete: findings=%d (critical=%d high=%d) tools_failed=%s errors=%d",
        s.total_findings,
        s.by_severity.get("critical", 0),
        s.by_severity.get("high", 0),
        s.tools_failed or "none",
        len(report.errors),
    )
    print(f"report written to {args.output}")
    return 0


def main() -> None:
    args = parse_args()
    try:
        code = asyncio.run(run(args))
    except KeyboardInterrupt:
        code = 130
    sys.exit(code)


if __name__ == "__main__":
    main()
