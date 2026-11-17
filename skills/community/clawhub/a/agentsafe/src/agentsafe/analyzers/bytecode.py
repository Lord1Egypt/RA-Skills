"""Closed-source bytecode analysis: classification, Heimdall, Mythril.

CLI contract (mythril flags verified against the pinned 0.24.3 sdist source,
heimdall flags against the 0.9.3 tag source; the CI smoke test must still
exercise both on the runner):

  myth analyze --code 0x... --bin-runtime -o json --execution-timeout <secs>
      -> stdout JSON {"success": bool, "error": null, "issues": [
           {"address": int, "title": str, "description": str,
            "severity": "High|Medium|Low", "swc-id": str|null}]}
           (--bin-runtime: eth_getCode returns RUNTIME bytecode)
  heimdall decompile <0x-target> --include-sol --output <dir>
      -> writes pseudo-Solidity files into the dir
         (target is a POSITIONAL arg: file, bytecode, address, or ENS)

Decompiler output is PSEUDO-SOURCE: an approximate representation that must
never be presented as the original Solidity or as proof of a vulnerability.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path

from agentsafe.schemas import Finding, FindingStatus, Severity

from .proc import (
    DefaultSubprocessRunner,
    ProcResult,
    ProcSpec,
    SubprocessRunner,
    TempWorkspace,
)

logger = logging.getLogger("agentSAFE.bytecode")


class BytecodeClass(StrEnum):
    EMPTY = "empty"
    MINIMAL_PROXY_EIP1167 = "minimal_proxy_eip1167"
    PROXY_EIP1967 = "proxy_eip1967"
    BEACON_PROXY_EIP1967 = "beacon_proxy_eip1967"
    UPGRADEABLE_PROXY_UUPS = "upgradeable_proxy_uups"
    NORMAL = "normal"
    UNKNOWN_SPECIAL = "unknown_special"


# EIP-1967 slots (published constants; classification is heuristic).
_EIP1967_IMPL_SLOT = "360894a13ba1a3210667c828492db98dca3e207c2492db32e19c33d1f2c9c8a3f"[:64]
_EIP1967_BEACON_SLOT = "a3f0ad74e5423aebfd80d3ef4346578335a9a72aeaee59ff6cb3582b35133d50"
_EIP1167_PREFIX = "363d3d373d3d3d363d73"
_EIP1167_SUFFIX = "5af43d82803e903d91602b57fd5bf3"


@dataclass
class BytecodeClassification:
    bytecode_class: BytecodeClass
    code_size: int
    proxy_target: str | None = None
    notes: list[str] = field(default_factory=list)


def classify_bytecode(code: str) -> BytecodeClassification:
    """Heuristic classifier. Records what it CAN determine, nothing more."""
    size = (len(code) - 2) // 2 if code and code.startswith("0x") else 0
    if size == 0:
        return BytecodeClassification(BytecodeClass.EMPTY, 0)

    low = code.lower()
    notes: list[str] = []

    if low.startswith("0x" + _EIP1167_PREFIX) and low.endswith(_EIP1167_SUFFIX):
        target = "0x" + low[2 + len(_EIP1167_PREFIX) : 2 + len(_EIP1167_PREFIX) + 40]
        notes.append("EIP-1167 minimal proxy; delegatecalls to embedded target")
        return BytecodeClassification(
            BytecodeClass.MINIMAL_PROXY_EIP1167, size, proxy_target=target, notes=notes
        )

    if _EIP1967_IMPL_SLOT in low:
        notes.append("EIP-1967 implementation slot constant present")
        return BytecodeClassification(BytecodeClass.PROXY_EIP1967, size, notes=notes)
    if _EIP1967_BEACON_SLOT in low:
        notes.append("EIP-1967 beacon slot constant present")
        return BytecodeClassification(BytecodeClass.BEACON_PROXY_EIP1967, size, notes=notes)
    if "5f50" in low[:4000] and size < 600 and "363d3d373d3d3d363d" in low:
        notes.append("small proxy-like selector pattern; UUPS candidates need review")
        return BytecodeClassification(BytecodeClass.UPGRADEABLE_PROXY_UUPS, size, notes=notes)
    if size < 64:
        notes.append("very small contract; classification uncertain")
        return BytecodeClassification(BytecodeClass.UNKNOWN_SPECIAL, size, notes=notes)

    return BytecodeClassification(BytecodeClass.NORMAL, size, notes=notes)


_MYTHRIL_SEVERITY = {"high": Severity.HIGH, "medium": Severity.MEDIUM, "low": Severity.LOW}


@dataclass
class BytecodeToolRun:
    tool: str
    executed: bool
    findings: list[Finding] = field(default_factory=list)
    error: str | None = None
    version: str | None = None
    pseudo_sources: dict[str, str] = field(default_factory=dict)  # label -> content


@dataclass
class BytecodeAnalysis:
    classification: BytecodeClassification
    runs: list[BytecodeToolRun] = field(default_factory=list)

    @property
    def findings(self) -> list[Finding]:
        out: list[Finding] = []
        for r in self.runs:
            out.extend(r.findings)
        return out

    @property
    def partial_failure(self) -> bool:
        return any((not r.executed) or r.error for r in self.runs)

    def pseudo_source_segments(self) -> dict[str, str]:
        segs: dict[str, str] = {}
        for r in self.runs:
            segs.update(r.pseudo_sources)
        return segs


class BytecodeAnalyzer:
    """Runs Mythril + Heimdall on runtime bytecode obtained from the RPC."""

    def __init__(
        self,
        *,
        mythril_bin: str = "myth",
        heimdall_bin: str = "heimdall",
        runner: SubprocessRunner | None = None,
        tool_timeout_seconds: float = 300.0,
        max_output_bytes: int = 2_000_000,
        max_pseudo_source_bytes: int = 400_000,
    ) -> None:
        self._mythril = mythril_bin
        self._heimdall = heimdall_bin
        self._runner: SubprocessRunner = runner or DefaultSubprocessRunner()
        self._timeout = tool_timeout_seconds
        self._max_output = max_output_bytes
        self._max_pseudo = max_pseudo_source_bytes

    async def analyze(self, bytecode: str) -> BytecodeAnalysis:
        """Analyze runtime bytecode. Empty bytecode raises before any tool runs."""
        if not bytecode or not bytecode.startswith("0x") or len(bytecode) <= 2:
            raise ValueError("empty or invalid bytecode")
        classification = classify_bytecode(bytecode)
        analysis = BytecodeAnalysis(classification=classification)

        myth_run = await self._run_mythril(bytecode)
        analysis.runs.append(myth_run)

        decomp_run = await self._run_heimdall(bytecode)
        analysis.runs.append(decomp_run)

        return analysis

    async def _version(self, executable: str, flag: str) -> str | None:
        res = await self._runner.run(
            ProcSpec(
                executable=executable,
                args=[flag],
                cwd=Path("."),
                timeout_seconds=30.0,
                max_output_bytes=4096,
            )
        )
        if res.missing or res.timed_out or res.error:
            return None
        text = (res.stdout or res.stderr or b"").decode("utf-8", "replace")
        m = re.search(r"(\d+\.\d+(?:\.\d+)?)", text)
        return m.group(1) if m else (text.strip()[:40] or None)

    async def _run_mythril(self, bytecode: str) -> BytecodeToolRun:
        run = BytecodeToolRun(tool="mythril", executed=False)
        run.version = await self._version(self._mythril, "version")
        # Verified against the pinned mythril 0.24.3 sdist (interfaces/cli.py):
        # --code accepts 0x-prefixed hex; --bin-runtime marks the input as
        # runtime bytecode (what eth_getCode returns); -o json emits
        # {"success", "error", "issues": [...]}.
        res = await self._runner.run(
            ProcSpec(
                executable=self._mythril,
                args=[
                    "analyze",
                    "--code",
                    bytecode,
                    "--bin-runtime",
                    "-o",
                    "json",
                    "--execution-timeout",
                    str(int(self._timeout)),
                ],
                cwd=Path("."),
                timeout_seconds=self._timeout + 30.0,  # hard outer timeout
                max_output_bytes=self._max_output,
            )
        )
        if res.missing:
            run.error = f"mythril not installed: {res.error}"
            return run
        if res.timed_out:
            run.error = "mythril timed out (hard outer limit)"
            return run
        if res.error:
            run.error = f"mythril spawn error: {res.error}"
            return run

        try:
            findings, tool_err = _parse_mythril(res)
        except Exception as exc:
            run.error = f"mythril output could not be parsed: {exc}"
            return run
        run.findings = findings
        run.executed = True
        if tool_err:
            run.error = tool_err
        if res.exit_code not in (0, None) and not findings and not tool_err:
            run.error = f"mythril exited with {res.exit_code} without JSON"
            run.executed = False
        return run

    async def _run_heimdall(self, bytecode: str) -> BytecodeToolRun:
        """Heimdall decompiles to pseudo-source for LLM analysis.

        Output dir is a temp workspace, always cleaned. Bytecode length is
        capped to keep command lines sane on every OS.
        """
        run = BytecodeToolRun(tool="heimdall", executed=False)
        run.version = await self._version(self._heimdall, "--version")
        if len(bytecode) > 24_000:  # 12KB runtime cap
            run.error = "bytecode exceeds 12KB; decompile skipped (size policy)"
            return run

        ws = TempWorkspace.create(prefix="agentSAFE-decompile-")
        try:
            # Verified against heimdall 0.9.3 (crates/decompile/src/interfaces/args.rs):
            # decompile takes a POSITIONAL target (file, bytecode, address, ENS);
            # there is no --byte-code flag. --include-sol emits the pseudo-Solidity
            # files this analysis consumes.
            res = await self._runner.run(
                ProcSpec(
                    executable=self._heimdall,
                    args=["decompile", bytecode, "--include-sol", "--output", str(ws.root)],
                    cwd=Path("."),
                    timeout_seconds=self._timeout,
                    max_output_bytes=self._max_output,
                )
            )
            if res.missing:
                run.error = f"heimdall not installed: {res.error}"
                return run
            if res.timed_out:
                run.error = "heimdall timed out"
                return run
            if res.error:
                run.error = f"heimdall spawn error: {res.error}"
                return run

            pseudo: dict[str, str] = {}
            total = 0
            for f in sorted(ws.root.rglob("*.sol")):
                content = f.read_text(encoding="utf-8", errors="replace")
                total += len(content.encode("utf-8", "replace"))
                if total > self._max_pseudo:
                    run.error = "pseudo-source exceeded size policy; truncated set kept"
                    break
                pseudo[f.name] = content
            run.pseudo_sources = pseudo
            run.executed = True
            if not pseudo:
                # Tool ran but produced nothing usable: that is a tool-level
                # failure, NOT "bytecode is clean".
                run.error = "heimdall produced no pseudo-source files"
        finally:
            ws.cleanup()
        return run


def _parse_mythril(res: ProcResult) -> tuple[list[Finding], str | None]:
    data = json.loads((res.stdout or b"").decode("utf-8", "replace"))
    if not isinstance(data, dict):
        raise ValueError("mythril JSON root is not an object")
    tool_err: str | None = None
    if data.get("error"):
        tool_err = str(data["error"])[:500]
    issues = data.get("issues") or []
    findings: list[Finding] = []
    for issue in issues:
        if not isinstance(issue, dict):
            continue
        title = str(issue.get("title") or "unknown-issue")
        sev_raw = str(issue.get("severity") or "Medium").lower()
        severity = _MYTHRIL_SEVERITY.get(sev_raw, Severity.MEDIUM)
        swc = issue.get("swc-id") or issue.get("swc_id")
        detector_id = f"SWC-{swc}" if swc else f"mythril-{_slug(title)}"
        description = str(issue.get("description") or title)
        addr = issue.get("address")
        code = issue.get("code") or ""
        evidence = f"bytecode offset {addr}: {code}" if addr is not None else (code or description)
        findings.append(
            Finding(
                title=f"[mythril] {title}",
                severity=severity,
                status=FindingStatus.TOOL_DETECTED,
                source=["mythril"],
                detector_id=detector_id,
                description=description,
                evidence=evidence[:2000],
                recommendation=(
                    "Review the Mythril report entry and verify against runtime "
                    "behavior; bytecode findings need manual confirmation of "
                    "reachability."
                ),
                line_start=None,
                metadata={
                    "swc_id": swc,
                    "bytecode_offset": addr,
                    "analyzed_from": "runtime_bytecode",
                },
            )
        )
    return findings, tool_err


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "issue"
