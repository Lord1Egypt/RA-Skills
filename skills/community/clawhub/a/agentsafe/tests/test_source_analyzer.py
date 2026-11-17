"""Phase 3 tests: verified-source analyzer (mock subprocess; no real tools run)."""

import json
from pathlib import Path

import pytest

from agentsafe.analyzers.proc import (
    AnalyzerError,
    ProcResult,
    ProcSpec,
    TempWorkspace,
    safe_relpath_str,
)
from agentsafe.analyzers.source import (
    SourceAnalyzer,
    _parse_aderyn,
    _parse_slither,
)
from agentsafe.explorer import SourceBundle, SourceFile
from agentsafe.schemas import Severity

ADDR = "0x" + "ab" * 20

SLITHER_OK = {
    "success": True,
    "error": None,
    "results": {
        "detectors": [
            {
                "check": "reentrancy-eth",
                "impact": "High",
                "confidence": "Medium",
                "description": "Reentrancy in Vault.withdraw() (contracts/Vault.sol#42-43)",
                "elements": [
                    {
                        "type": "function",
                        "name": "withdraw",
                        "source_mapping": {
                            "lines": [42, 43],
                            "filename": {"short": "contracts/Vault.sol"},
                        },
                    }
                ],
            },
            {
                "check": "solc-version",
                "impact": "Informational",
                "confidence": "High",
                "description": "Solc version pragma is old",
                "elements": [],
            },
        ]
    },
}

ADERYN_OK = {
    "files": ["contracts/Vault.sol"],
    "issues": {
        "high": [
            {
                "title": "centralized risk: setOwner",
                "instances": [{"contract": "Vault", "function": "setOwner", "line": 10}],
            }
        ],
        "low": [{"title": "missing zero-check", "instances": []}],
    },
    "summary": {"files_scanned": 1, "high": 1, "low": 1},
}


def _bundle(**overrides) -> SourceBundle:
    base = dict(
        is_verified=True,
        contract_name="Vault",
        compiler_version="v0.8.19+commit.7dd6d404",
        files=[
            SourceFile(path="contracts/Vault.sol", content="contract Vault {}"),
            SourceFile(path="contracts/lib/X.sol", content="library X {}"),
        ],
        settings={"optimizer": {"enabled": True, "runs": 200}},
    )
    base.update(overrides)
    return SourceBundle.model_validate(base)


class FakeRunner:
    """Records every ProcSpec; returns canned results per executable."""

    def __init__(self, handler):
        self.handler = handler
        self.specs: list[ProcSpec] = []

    async def run(self, spec: ProcSpec) -> ProcResult:
        self.specs.append(spec)
        return self.handler(spec)


def _handler(slither=None, aderyn=None, versions=True):
    """Build a handler; None means executable missing. slither/aderyn are
    (exit_code, payload_dict_or_None) tuples or ProcResult."""

    def handle(spec: ProcSpec) -> ProcResult:
        if spec.args[:1] == ["--version"]:
            if not versions:
                return ProcResult(1, b"", b"")
            v = b"0.10.4" if spec.executable == "slither" else b"0.3.2"
            return ProcResult(0, v, b"")
        if spec.executable == "solc-select":
            return ProcResult(0, b"installed\n", b"")
        if spec.executable == "slither":
            if slither is None:
                return ProcResult(None, b"", b"", missing=True, error="not found")
            if isinstance(slither, ProcResult):
                return slither
            code, payload = slither
            data = b"" if payload is None else json.dumps(payload).encode()
            return ProcResult(code, data, b"")
        if spec.executable == "aderyn":
            if aderyn is None:
                return ProcResult(None, b"", b"", missing=True, error="not found")
            if isinstance(aderyn, ProcResult):
                return aderyn
            code, payload = aderyn
            # aderyn v0.6.x writes its report to --output <file>, not stdout.
            if payload is not None:
                (spec.cwd / "report.json").write_text(json.dumps(payload), encoding="utf-8")
            return ProcResult(code, b"", b"")
        raise AssertionError(f"unexpected executable {spec.executable}")

    return handle


class TestWorkspaceSafety:
    def test_safe_relpath_accepts_nested(self):
        ws = TempWorkspace.create()
        try:
            p = ws.safe_relpath("contracts/lib/X.sol")
            assert p.is_absolute()
            assert ws.root.resolve() in p.parents
        finally:
            ws.cleanup()

    def test_safe_relpath_rejects_traversal(self):
        ws = TempWorkspace.create()
        try:
            for bad in (
                "../escape.sol",
                "a/../../escape.sol",
                "/abs.sol",
                "C:\\x\\y.sol",
                "C:/x.sol",
                "..\\..\\x",
                "",
                ".",
            ):
                with pytest.raises(AnalyzerError):
                    ws.safe_relpath(bad)
        finally:
            ws.cleanup()

    def test_cleanup_removes_dir(self):
        ws = TempWorkspace.create()
        (ws.root / "f.sol").write_text("x")
        ws.cleanup()
        assert not ws.root.exists()

    def test_safe_relpath_str(self):
        assert safe_relpath_str("a/b.sol") == "a/b.sol"
        assert safe_relpath_str(".\\a\\b.sol") == "a/b.sol"
        with pytest.raises(AnalyzerError):
            safe_relpath_str("../x")


class TestSourceAnalyzer:
    async def test_both_tools_success(self):
        analyzer = SourceAnalyzer(
            runner=FakeRunner(_handler(slither=(0, SLITHER_OK), aderyn=(0, ADERYN_OK)))
        )
        result = await analyzer.analyze(_bundle())
        assert not result.partial_failure
        assert len(result.runs) == 2
        slither_run = next(r for r in result.runs if r.tool == "slither")
        aderyn_run = next(r for r in result.runs if r.tool == "aderyn")
        assert slither_run.executed and slither_run.version == "0.10.4"
        assert aderyn_run.executed and aderyn_run.version == "0.3.2"
        # 2 slither + 2 aderyn (1 instance + 1 instance-less low issue)
        assert len(result.findings) == 4
        reent = next(f for f in result.findings if f.detector_id == "reentrancy-eth")
        assert reent.severity is Severity.HIGH
        assert reent.file_path == "contracts/Vault.sol"
        assert reent.line_start == 42 and reent.line_end == 43
        assert reent.status.value == "tool_detected"
        central = next(f for f in result.findings if "centralized" in f.detector_id)
        assert central.severity is Severity.HIGH
        assert central.line_start == 10

    async def test_files_materialized_with_paths_and_settings(self):
        runner = FakeRunner(_handler(slither=(0, SLITHER_OK), aderyn=(0, ADERYN_OK)))
        # The workspace is deleted in analyze()'s finally (spec: no residue),
        # so the spy must snapshot file layout DURING the tool call.
        captured: dict[str, dict] = {}
        handle = runner.handler

        def spy(spec: ProcSpec) -> ProcResult:
            if spec.cwd.name.startswith("agentSAFE-audit-"):
                std = spec.cwd / "standard_input.json"
                captured[spec.executable] = {
                    "vault_exists": (spec.cwd / "contracts" / "Vault.sol").exists(),
                    "lib_exists": (spec.cwd / "contracts" / "lib" / "X.sol").exists(),
                    "std_content": std.read_text(encoding="utf-8") if std.exists() else None,
                }
            return handle(spec)

        runner.handler = spy
        await SourceAnalyzer(runner=runner).analyze(_bundle())
        snap = captured["slither"]
        assert snap["vault_exists"]
        assert snap["lib_exists"]
        assert snap["std_content"] is not None
        data = json.loads(snap["std_content"])
        assert data["settings"] == {"optimizer": {"enabled": True, "runs": 200}}
        assert set(data["sources"]) == {"contracts/Vault.sol", "contracts/lib/X.sol"}

    async def test_workspace_cleaned_after_analysis(self):
        runner = FakeRunner(_handler(slither=(0, SLITHER_OK), aderyn=(0, ADERYN_OK)))
        roots: list[Path] = []
        orig = runner.handler

        def spy(spec: ProcSpec) -> ProcResult:
            # Only temp workspaces are the analyzer's responsibility;
            # --version probes run with cwd="." and must not be tracked.
            if spec.cwd.name.startswith("agentSAFE-audit-"):
                roots.append(spec.cwd)
            return orig(spec)

        runner.handler = spy
        await SourceAnalyzer(runner=runner).analyze(_bundle())
        assert roots and all(not r.exists() for r in roots)

    async def test_slither_missing_keeps_aderyn_results(self):
        result = await SourceAnalyzer(
            runner=FakeRunner(_handler(slither=None, aderyn=(0, ADERYN_OK)))
        ).analyze(_bundle())
        assert result.partial_failure
        slither_run = next(r for r in result.runs if r.tool == "slither")
        aderyn_run = next(r for r in result.runs if r.tool == "aderyn")
        assert not slither_run.executed
        assert "not installed" in (slither_run.error or "")
        assert aderyn_run.executed and len(aderyn_run.findings) == 2

    async def test_timeout_produces_error_not_silence(self):
        timeout_res = ProcResult(None, b"", b"", timed_out=True, error="timeout after 5s")
        result = await SourceAnalyzer(
            runner=FakeRunner(_handler(slither=timeout_res, aderyn=(0, ADERYN_OK)))
        ).analyze(_bundle())
        assert result.partial_failure
        slither_run = next(r for r in result.runs if r.tool == "slither")
        assert not slither_run.executed and "timed out" in (slither_run.error or "")

    async def test_invalid_json_is_recorded_not_faked(self):
        bad = ProcResult(0, b"<html>not json</html>", b"")

        def handle(spec: ProcSpec) -> ProcResult:
            if spec.args[:1] == ["--version"]:
                v = b"0.10.4" if spec.executable == "slither" else b"0.3.2"
                return ProcResult(0, v, b"")
            if spec.executable == "slither":
                return bad
            # aderyn contract: report lands in report.json, not stdout
            (spec.cwd / "report.json").write_text("<html>not json</html>", encoding="utf-8")
            return ProcResult(0, b"", b"")

        result = await SourceAnalyzer(runner=FakeRunner(handle)).analyze(_bundle())
        for r in result.runs:
            assert not r.executed
            assert "could not be parsed" in (r.error or "")
            assert r.findings == []

    async def test_slither_compilation_error_is_partial_failure(self):
        err_json = {
            "success": False,
            "error": "compilation failed: solc 0.8.19 not found",
            "results": {"detectors": []},
        }
        result = await SourceAnalyzer(
            runner=FakeRunner(_handler(slither=(255, err_json), aderyn=(0, ADERYN_OK)))
        ).analyze(_bundle())
        assert result.partial_failure
        slither_run = next(r for r in result.runs if r.tool == "slither")
        assert slither_run.executed  # tool ran and reported its own failure
        assert "compilation failed" in (slither_run.error or "")
        assert slither_run.findings == []

    async def test_nonzero_exit_without_json_not_executed(self):
        result = await SourceAnalyzer(
            runner=FakeRunner(_handler(slither=(2, None), aderyn=(2, None)))
        ).analyze(_bundle())
        for r in result.runs:
            assert not r.executed and "exited with 2" in (r.error or "")

    async def test_empty_bundle_rejected(self):
        analyzer = SourceAnalyzer(runner=FakeRunner(_handler()))
        with pytest.raises(AnalyzerError, match="no source files"):
            await analyzer.analyze(SourceBundle(is_verified=False))

    async def test_ensure_solc_provisions_etherscan_version_before_slither(self):
        runner = FakeRunner(_handler(slither=(0, SLITHER_OK), aderyn=(0, ADERYN_OK)))
        await SourceAnalyzer(runner=runner).analyze(
            _bundle(compiler_version="v0.4.19+commit.c4cbbb05")
        )
        solc_specs = [s for s in runner.specs if s.executable == "solc-select"]
        assert solc_specs and solc_specs[0].args == ["install", "0.4.19"]
        # provisioning must happen BEFORE the slither run
        first_slither = next(i for i, s in enumerate(runner.specs) if s.executable == "slither")
        assert runner.specs.index(solc_specs[0]) < first_slither

    async def test_slither_run_pins_recorded_solc_version(self):
        """Regression: crytic-compile uses solc-select's GLOBAL version and
        never picks a pragma-compatible one; slither exits 1 silently when
        the global solc cannot compile. The recorded version must be pinned
        per-process via SOLC_VERSION (verified in a container repro)."""
        runner = FakeRunner(_handler(slither=(0, SLITHER_OK), aderyn=(0, ADERYN_OK)))
        await SourceAnalyzer(runner=runner).analyze(
            _bundle(compiler_version="v0.4.19+commit.c4cbbb05")
        )
        slither_specs = [s for s in runner.specs if s.executable == "slither"]
        probe, run = slither_specs[0], slither_specs[1]
        assert probe.args[:1] == ["--version"] and probe.extra_env is None
        assert run.extra_env == {"SOLC_VERSION": "0.4.19"}

    async def test_solc_pin_skipped_when_provisioning_fails(self):
        def handle(spec: ProcSpec) -> ProcResult:
            if spec.executable == "solc-select":
                return ProcResult(1, b"", b"no such version")
            return _handler(slither=(0, SLITHER_OK), aderyn=(0, ADERYN_OK))(spec)

        runner = FakeRunner(handle)
        await SourceAnalyzer(runner=runner).analyze(
            _bundle(compiler_version="v0.4.19+commit.c4cbbb05")
        )
        run_specs = [
            s for s in runner.specs if s.executable == "slither" and s.args[:1] != ["--version"]
        ]
        assert run_specs[0].extra_env is None

    async def test_extra_env_rejects_invalid_keys(self):
        from agentsafe.analyzers.proc import DefaultSubprocessRunner

        runner = DefaultSubprocessRunner()
        res = await runner.run(
            ProcSpec(
                executable="python",
                args=["-c", "print('should never run')"],
                cwd=Path("."),
                extra_env={"bad-key; rm -rf /": "x"},
            )
        )
        assert res.error and "invalid extra_env" in res.error
        assert res.stdout == b""

    async def test_extra_env_actually_reaches_the_subprocess(self):
        """Regression: the runner built the merged env but passed a FRESH
        sanitized env to create_subprocess_exec, silently dropping
        extra_env (the SOLC_VERSION pin) - the third real audit failed
        because of this. A real subprocess must observe the variable."""
        import sys

        from agentsafe.analyzers.proc import DefaultSubprocessRunner

        runner = DefaultSubprocessRunner()
        res = await runner.run(
            ProcSpec(
                executable=sys.executable,
                args=["-c", "import os; print(os.environ.get('SOLC_VERSION'))"],
                cwd=Path("."),
                extra_env={"SOLC_VERSION": "0.4.19"},
            )
        )
        assert b"0.4.19" in res.stdout

    async def test_ensure_solc_failure_is_tolerated(self):
        def handle(spec: ProcSpec) -> ProcResult:
            if spec.executable == "solc-select":
                return ProcResult(1, b"", b"no such version")
            return _handler(slither=(0, SLITHER_OK), aderyn=(0, ADERYN_OK))(spec)

        result = await SourceAnalyzer(runner=FakeRunner(handle)).analyze(_bundle())
        assert not result.partial_failure  # provisioning failure alone is not a tool failure

    async def test_ensure_solc_skipped_when_no_recorded_version(self):
        runner = FakeRunner(_handler(slither=(0, SLITHER_OK), aderyn=(0, ADERYN_OK)))
        await SourceAnalyzer(runner=runner).analyze(_bundle(compiler_version=""))
        assert not [s for s in runner.specs if s.executable == "solc-select"]

    async def test_slither_failure_recorded_with_stderr_detail(self):
        # regression for the first WETH audit: exit 1, empty stdout, and the
        # report only said "produced no JSON output" with no diagnostic.
        bad = ProcResult(1, b"", b"Traceback ... solc 0.4.19 is not installed")
        result = await SourceAnalyzer(
            runner=FakeRunner(_handler(slither=bad, aderyn=(0, ADERYN_OK)))
        ).analyze(_bundle(compiler_version=""))
        slither_run = next(r for r in result.runs if r.tool == "slither")
        assert not slither_run.executed
        assert "exited with 1" in (slither_run.error or "")
        assert "solc 0.4.19 is not installed" in (slither_run.error or "")
        assert "stderr" in (slither_run.error or "")

    async def test_source_size_cap_enforced(self):
        big = [
            SourceFile(path="big.sol", content="x" * 3_000_000),
            SourceFile(path="big2.sol", content="y" * 3_000_000),
        ]
        analyzer = SourceAnalyzer(runner=FakeRunner(_handler()))
        with pytest.raises(AnalyzerError, match="exceeds"):
            await analyzer.analyze(_bundle(files=big))

    async def test_no_shell_and_fixed_argv(self):
        runner = FakeRunner(_handler(slither=(0, SLITHER_OK), aderyn=(0, ADERYN_OK)))
        await SourceAnalyzer(runner=runner).analyze(_bundle())
        for spec in runner.specs:
            if spec.args[:1] == ["--version"]:
                continue
            assert isinstance(spec.executable, str) and spec.executable
            assert all(isinstance(a, str) for a in spec.args)
            # target dir passed positionally, never via shell string
            assert not any("|" in a or ";" in a or "`" in a for a in spec.args)


class TestParsersDirect:
    def test_parse_slither_unknown_impact_maps_info(self):
        payload = {
            "results": {
                "detectors": [
                    {"check": "weird", "impact": "Exotic", "description": "d", "elements": []}
                ]
            }
        }
        findings, err = _parse_slither(ProcResult(0, json.dumps(payload).encode(), b""))
        assert findings[0].severity is Severity.INFO
        assert err is None

    def test_parse_slither_tolerates_junk_entries(self):
        payload = {
            "results": {
                "detectors": ["junk", {"check": "c1", "impact": "Low", "description": "x"}, None]
            }
        }
        findings, _ = _parse_slither(ProcResult(0, json.dumps(payload).encode(), b""))
        assert len(findings) == 1

    def test_parse_aderyn_multiple_instances(self):
        payload = {
            "issues": {
                "high": [
                    {
                        "title": "T",
                        "instances": [{"contract": "A", "line": 1}, {"contract": "B", "line": 2}],
                    }
                ]
            }
        }
        findings, _ = _parse_aderyn(json.dumps(payload).encode())
        assert len(findings) == 2
        assert {f.line_start for f in findings} == {1, 2}

    def test_parse_slither_empty_results(self):
        findings, err = _parse_slither(ProcResult(0, b'{"results": {"detectors": []}}', b""))
        assert findings == [] and err is None
