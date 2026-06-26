#!/usr/bin/env python3
"""
raw_data_check.py — enforce Phase 3.5 (data-source snapshot) of the
cn-client-investigation skill.

Rule: every CN banker deliverable must include a `raw-data/` subdirectory
containing the JSON responses captured from the 3 CN MCP tools
(aigroup-market-mcp / PrimeMatrixData / Tianyancha) during the Phase 3
data-gathering step. Without those snapshots, there is no audit trail
showing the hard numbers in analysis.md actually came from an installed
tool call — exactly the failure mode that let 2026-04-20 MiniMax-host
decks ship Wind-fabricated citations.

Bifurcated expectations:

    Listed company (ts_code matches {NNNNNN.SH,NNNNNN.SZ,NNNNNN.BJ,NNNN.HK})
      - ≥ 3 aigroup-market-mcp files; among them at least
        basic_info / company_performance / stock_data
      - ≥ 1 corporate-risk overlay: PrimeMatrixData (primary)
        OR Tianyancha (accepted if registered)

    Non-listed company (no ts_code — only 统一社会信用代码 available)
      - ≥ 1 corporate-risk overlay: PrimeMatrixData (primary)
        OR Tianyancha (accepted if registered)
      - aigroup-market-mcp files optional (usually not applicable)

Tianyancha posture (2026-04+): the 智谱 MCP broker account is currently
suspended due to balance exhaustion, so PrimeMatrixData is the only
actively-reachable CN risk overlay. The gate accepts Tianyancha snapshots
when present (for when the account is topped up or replaced) but does
NOT require them.

The detection is heuristic: we look at raw-data/ filenames for
ts_code-shaped tokens. If none are found we fall back to non-listed mode.

Provenance cross-check: every `raw-data/*.json` filename stem must appear
in data-provenance.md somewhere, so the analysis tracks which tool fed
which number. Missing references are FAILures (not warnings) because an
un-referenced raw file is dead weight, and a referenced-but-missing tool
call is a fabrication risk.

Usage:
    python3 raw_data_check.py <deliverable_dir>
    python3 raw_data_check.py --strict-mcp <deliverable_dir>

    # exit 0 → raw-data/ present and complete for the detected company type
    # exit 1 → missing tool snapshots or missing provenance references
    # exit 0 with WARN → raw-data/ absent and --strict-mcp NOT passed
    # exit 1 → raw-data/ absent and --strict-mcp IS passed
"""
from __future__ import annotations
import argparse
import json
import pathlib
import re
import sys

TS_CODE = re.compile(r"\b\d{4,6}\.(SH|SZ|BJ|HK|SS)\b")
REQUIRED_MARKET_TOOLS = ("basic_info", "company_performance", "stock_data")
# PM basic_info MUST contain at least ONE of these identity fields. If none are
# present, the query hit an unregistered name (e.g. calling "北京字节跳动科技有限公司"
# instead of the actual legal name "抖音有限公司") and returned {}. That empty
# result will quietly propagate into analysis.md with "N/A" fields — exactly
# the failure mode found 2026-04-20 non-listed smoke-test.
PM_BASIC_IDENTITY_KEYS = (
    "统一社会信用代码", "企业名称全称", "企业名称", "法定代表人或负责人或执行事务合伙人姓名",
)


def classify_file(name: str) -> str | None:
    """Return 'market' | 'primematrix' | 'tianyancha' | None for a filename stem."""
    low = name.lower()
    if "market-mcp" in low or "aigroup-market" in low or "tushare" in low:
        return "market"
    if "primematrix" in low or "prime-matrix" in low or "prime_matrix" in low:
        return "primematrix"
    if "tianyancha" in low or "tyc" in low:
        return "tianyancha"
    return None


def detect_listed(raw_dir: pathlib.Path) -> bool:
    for f in raw_dir.glob("*.json"):
        if TS_CODE.search(f.name):
            return True
    return False


def covered_market_tools(raw_dir: pathlib.Path) -> set[str]:
    """Which of REQUIRED_MARKET_TOOLS have at least one matching raw file?"""
    covered: set[str] = set()
    for f in raw_dir.glob("*.json"):
        if classify_file(f.name) != "market":
            continue
        name = f.name.lower()
        for tool in REQUIRED_MARKET_TOOLS:
            if tool in name:
                covered.add(tool)
    return covered


def check_provenance_refs(
    raw_dir: pathlib.Path, provenance_text: str
) -> list[pathlib.Path]:
    """Return raw-data files whose filename stem is NOT mentioned in data-provenance.md."""
    missing: list[pathlib.Path] = []
    for f in sorted(raw_dir.glob("*.json")):
        stem = f.stem
        if stem not in provenance_text:
            missing.append(f)
    return missing


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    ap.add_argument("deliverable_dir", type=pathlib.Path)
    ap.add_argument(
        "--strict-mcp",
        action="store_true",
        help="missing raw-data/ is a FAIL (otherwise a warning for 0.8.x back-compat)",
    )
    args = ap.parse_args(argv[1:])

    d = args.deliverable_dir.resolve()
    if not d.is_dir():
        print(f"ERR: {d} is not a directory", file=sys.stderr)
        return 2

    raw_dir = d / "raw-data"
    provenance = d / "data-provenance.md"

    if not raw_dir.is_dir():
        msg = (
            f"raw-data/ not present in {d}. Phase 3.5 of cn-client-investigation "
            f"requires snapshots of every MCP tool call that produced hard numbers."
        )
        if args.strict_mcp:
            print(f"FAIL: {msg}", file=sys.stderr)
            return 1
        print(f"WARN (backward-compat): {msg}", file=sys.stderr)
        print("OK: raw_data_check skipped (raw-data/ absent; legacy deliverable).")
        return 0

    json_files = sorted(raw_dir.glob("*.json"))
    if not json_files:
        print(f"FAIL: raw-data/ exists but contains no *.json files in {raw_dir}",
              file=sys.stderr)
        return 1

    listed = detect_listed(raw_dir)
    mode = "listed" if listed else "non-listed"

    failures: list[str] = []

    # Market-tool coverage — only required for listed companies.
    if listed:
        covered_market = covered_market_tools(raw_dir)
        missing_market = set(REQUIRED_MARKET_TOOLS) - covered_market
        if missing_market:
            failures.append(
                "Listed company: missing aigroup-market-mcp tool snapshots for "
                + ", ".join(sorted(missing_market))
                + f". Expected files like 002594.SZ-aigroup-market-mcp-{sorted(missing_market)[0]}.json"
            )

    # Corporate-risk overlay coverage. PrimeMatrix is the primary source
    # (Tianyancha 智谱 broker is currently paused — see docstring).
    has_pm = any(classify_file(f.name) == "primematrix" for f in json_files)
    has_tyc = any(classify_file(f.name) == "tianyancha" for f in json_files)
    if not (has_pm or has_tyc):
        kind = "Listed" if listed else "Non-listed"
        failures.append(
            f"{kind} company: corporate-risk overlay required "
            f"(PrimeMatrixData primary; Tianyancha accepted when registered). "
            f"Found neither."
        )

    # PM content sanity: if a PM basic_info file exists but is empty or missing
    # identity keys, the query used a non-registered name and the JSON is a
    # quiet false-negative. Fail early with a specific hint.
    warnings: list[str] = []
    for f in json_files:
        if classify_file(f.name) != "primematrix":
            continue
        if "basic_info" not in f.name.lower():
            continue
        try:
            payload = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            failures.append(f"PM basic_info file is not valid JSON: {f.name}")
            continue
        if not payload or not any(k in payload for k in PM_BASIC_IDENTITY_KEYS):
            failures.append(
                f"PM basic_info is empty or missing identity fields in {f.name}. "
                f"Likely cause: called basic_info with a non-registered 公众名. "
                f"Fix: run PrimeMatrixData__company_name(blur_name=...) first to "
                f"resolve the legal registered name, then re-call basic_info."
            )
        # risk_info sanity: empty-except-name payload is suspicious but not fatal
        if "risk_info" in f.name.lower():
            meaningful_keys = [k for k in payload.keys() if k != "公司名称"]
            if not meaningful_keys:
                warnings.append(
                    f"PM risk_info has only '公司名称' field in {f.name} — "
                    f"not proof the company is risk-free; verify manually."
                )

    # Provenance cross-reference.
    if provenance.exists():
        prov_text = provenance.read_text(encoding="utf-8", errors="replace")
        unreferenced = check_provenance_refs(raw_dir, prov_text)
        if unreferenced:
            failures.append(
                f"{len(unreferenced)} raw-data file(s) not referenced in "
                f"data-provenance.md: "
                + ", ".join(f.name for f in unreferenced[:5])
                + (f" (+{len(unreferenced) - 5} more)" if len(unreferenced) > 5 else "")
            )
    else:
        failures.append(
            "data-provenance.md missing — cannot cross-reference raw-data files."
        )

    for w in warnings:
        print(f"WARN: {w}", file=sys.stderr)

    if failures:
        print(
            f"FAIL [{mode}]: raw_data_check found {len(failures)} issue(s) in {d}:",
            file=sys.stderr,
        )
        for msg in failures:
            print(f"  - {msg}", file=sys.stderr)
        return 1

    print(
        f"OK: raw_data_check [{mode}] clean on {d} "
        f"({len(json_files)} raw JSON files; listed={listed}; "
        f"PM={has_pm}, TYC={has_tyc})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
