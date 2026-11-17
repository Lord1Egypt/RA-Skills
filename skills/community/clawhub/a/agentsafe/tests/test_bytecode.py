"""Bytecode analyzer acceptance: classifier + tool runs (mock subprocess)."""

import json
from pathlib import Path

import pytest

from agentsafe.analyzers.bytecode import (
    BytecodeAnalyzer,
    BytecodeClass,
    classify_bytecode,
)
from agentsafe.analyzers.proc import ProcResult, ProcSpec


class FakeRunner:
    def __init__(self, handler):
        self.handler = handler

    async def run(self, spec: ProcSpec) -> ProcResult:
        return self.handler(spec)


def _handler(mythril=None, heimdall=None, heimdall_files=None):
    def handle(spec: ProcSpec) -> ProcResult:
        if spec.args[:1] in (["version"], ["--version"]):
            return (
                ProcResult(0, b"mythril 0.24.3", b"")
                if spec.executable == "myth"
                else ProcResult(0, b"heimdall 0.8.4", b"")
            )
        if spec.executable == "myth":
            if mythril is None:
                return ProcResult(None, b"", b"", missing=True, error="not found")
            if isinstance(mythril, ProcResult):
                return mythril
            code, payload = mythril
            return ProcResult(code, b"" if payload is None else json.dumps(payload).encode(), b"")
        if spec.executable == "heimdall":
            if heimdall is None:
                return ProcResult(None, b"", b"", missing=True, error="not found")
            if isinstance(heimdall, ProcResult):
                return heimdall
            if heimdall_files is not None:
                # side-effect: write pseudo sources into --output dir
                out = Path(spec.args[spec.args.index("--output") + 1])
                for name, content in heimdall_files.items():
                    (out / name).write_text(content)
            code, payload = heimdall
            return ProcResult(code, b"" if payload is None else json.dumps(payload).encode(), b"")
        raise AssertionError(spec.executable)

    return handle


MYTHRIL_OK = {
    "success": True,
    "error": None,
    "issues": [
        {
            "address": 1234,
            "title": "Unchecked Call Return Value",
            "description": "The return value of a call is not checked",
            "severity": "Low",
            "swc-id": "104",
            "code": "CALL",
        },
        {
            "address": 5678,
            "title": "Integer Overflow",
            "description": "Potential overflow",
            "severity": "High",
            "swc-id": "101",
            "code": "ADD",
        },
    ],
}


class TestClassifier:
    def test_empty(self):
        c = classify_bytecode("0x")
        assert c.bytecode_class is BytecodeClass.EMPTY

    def test_eip1167_minimal_proxy_target_extracted(self):
        target = "ab" * 20
        code = "0x363d3d373d3d3d363d73" + target + "5af43d82803e903d91602b57fd5bf3"
        c = classify_bytecode(code)
        assert c.bytecode_class is BytecodeClass.MINIMAL_PROXY_EIP1167
        assert c.proxy_target == "0x" + target

    def test_eip1967_proxy_detected(self):
        code = (
            "0x6080"
            + "60" * 20
            + "7f360894a13ba1a3210667c828492db98dca3e207c2492db32e19c33d1f2c9c8a3f"
            + "ff" * 30
        )
        c = classify_bytecode(code)
        assert c.bytecode_class is BytecodeClass.PROXY_EIP1967

    def test_normal_contract(self):
        code = "0x6080604052" + "aa" * 200
        c = classify_bytecode(code)
        assert c.bytecode_class is BytecodeClass.NORMAL


class TestBytecodeAnalyzer:
    async def test_both_tools_success(self):
        analyzer = BytecodeAnalyzer(
            runner=FakeRunner(
                _handler(
                    mythril=(0, MYTHRIL_OK),
                    heimdall=(0, {}),
                    heimdall_files={"decompiled.sol": "contract Pseudo {}"},
                )
            )
        )
        result = await analyzer.analyze("0x6080604052" + "bb" * 300)
        assert len(result.runs) == 2
        myth = next(r for r in result.runs if r.tool == "mythril")
        assert myth.executed and len(myth.findings) == 2
        swc = next(f for f in myth.findings if f.detector_id == "SWC-104")
        assert swc.severity.value == "low"
        assert swc.status.value == "tool_detected"
        assert swc.metadata["analyzed_from"] == "runtime_bytecode"
        heim = next(r for r in result.runs if r.tool == "heimdall")
        assert heim.executed and "decompiled.sol" in heim.pseudo_sources
        assert not result.partial_failure

    async def test_missing_tools_are_errors_not_clean(self):
        result = await BytecodeAnalyzer(runner=FakeRunner(_handler())).analyze(
            "0x6080604052" + "bb" * 300
        )
        assert result.partial_failure
        for r in result.runs:
            assert not r.executed and "not installed" in (r.error or "")

    async def test_mythril_timeout(self):
        result = await BytecodeAnalyzer(
            runner=FakeRunner(_handler(mythril=ProcResult(None, b"", b"", timed_out=True)))
        ).analyze("0x6080604052" + "bb" * 300)
        myth = next(r for r in result.runs if r.tool == "mythril")
        assert "timed out" in (myth.error or "")

    async def test_mythril_invalid_json(self):
        result = await BytecodeAnalyzer(
            runner=FakeRunner(_handler(mythril=ProcResult(0, b"<html>", b"")))
        ).analyze("0x6080604052" + "bb" * 300)
        myth = next(r for r in result.runs if r.tool == "mythril")
        assert not myth.executed and "could not be parsed" in (myth.error or "")

    async def test_heimdall_no_files_is_tool_failure(self):
        result = await BytecodeAnalyzer(
            runner=FakeRunner(_handler(mythril=(0, MYTHRIL_OK), heimdall=(0, {})))
        ).analyze("0x6080604052" + "bb" * 300)
        heim = next(r for r in result.runs if r.tool == "heimdall")
        assert "no pseudo-source" in (heim.error or "")

    async def test_empty_bytecode_rejected(self):
        with pytest.raises(ValueError):
            await BytecodeAnalyzer(runner=FakeRunner(_handler())).analyze("0x")

    async def test_oversized_bytecode_skips_decompile(self):
        result = await BytecodeAnalyzer(
            runner=FakeRunner(
                _handler(mythril=(0, MYTHRIL_OK), heimdall=(0, {}), heimdall_files={"x.sol": "y"})
            )
        ).analyze("0x" + "cc" * 13_000)
        heim = next(r for r in result.runs if r.tool == "heimdall")
        assert "size policy" in (heim.error or "")
