#!/usr/bin/env python3
import argparse
import html
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


VALID_STATUS = {"compliant", "partial", "violation", "not_assessed"}
VALID_RISK = {"low", "medium", "high", "critical"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def default_controls_path() -> Path:
    return Path(__file__).resolve().parent.parent / "references" / "compliance-controls-map.json"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
        f.write("\n")


def init_assessment(controls: List[Dict[str, object]], system_name: str) -> Dict[str, object]:
    checks = []
    for ctrl in controls:
        checks.append(
            {
                "check_id": ctrl["check_id"],
                "status": "not_assessed",
                "risk": ctrl.get("default_risk", "medium"),
                "observed_state": "",
                "evidence": "",
                "gap": "",
                "mitigation": "",
                "owner": "",
                "due_date": "",
            }
        )
    return {
        "metadata": {
            "system": system_name,
            "generated_at_utc": utc_now(),
            "frameworks": ["ISO/IEC 27001:2022", "NIST CSF"],
        },
        "checks": checks,
    }


def validate_assessment(assessment: Dict[str, object]) -> None:
    checks = assessment.get("checks", [])
    if not isinstance(checks, list):
        raise ValueError("Assessment must include 'checks' list.")
    for c in checks:
        status = c.get("status", "")
        risk = c.get("risk", "")
        if status not in VALID_STATUS:
            raise ValueError(f"Invalid status '{status}' for check {c.get('check_id')}")
        if risk not in VALID_RISK:
            raise ValueError(f"Invalid risk '{risk}' for check {c.get('check_id')}")


def merge_controls(controls: List[Dict[str, object]], assessment: Dict[str, object]) -> List[Dict[str, object]]:
    by_id = {c["check_id"]: c for c in assessment.get("checks", [])}
    merged = []
    for ctrl in controls:
        check = by_id.get(ctrl["check_id"], {})
        merged.append(
            {
                "check_id": ctrl["check_id"],
                "title": ctrl["title"],
                "iso27001": ctrl.get("iso27001", []),
                "nist": ctrl.get("nist", []),
                "expected_state": ctrl.get("expected_state", ""),
                "status": check.get("status", "not_assessed"),
                "risk": check.get("risk", ctrl.get("default_risk", "medium")),
                "observed_state": check.get("observed_state", ""),
                "evidence": check.get("evidence", ""),
                "gap": check.get("gap", ""),
                "mitigation": check.get("mitigation", ""),
                "owner": check.get("owner", ""),
                "due_date": check.get("due_date", ""),
            }
        )
    return merged


def summarize(merged: List[Dict[str, object]]) -> Dict[str, object]:
    status_counts = Counter(item["status"] for item in merged)
    risk_counts = Counter(item["risk"] for item in merged)
    violations = [m for m in merged if m["status"] in ("violation", "partial")]
    mitigations = [m for m in merged if m["mitigation"]]
    return {
        "status_counts": dict(status_counts),
        "risk_counts": dict(risk_counts),
        "violations": violations,
        "mitigations": mitigations,
    }


STATUS_ORDER = ["compliant", "partial", "violation", "not_assessed"]
STATUS_LABELS = {
    "compliant": "Compliant",
    "partial": "Partial",
    "violation": "Violation",
    "not_assessed": "Not assessed",
}
# Plural forms used where the dashboard counts controls per status.
STATUS_COUNT_LABELS = {
    "compliant": "Compliant",
    "partial": "Partial",
    "violation": "Violations",
    "not_assessed": "Not Assessed",
}
RISK_ORDER = ["critical", "high", "medium", "low"]
RISK_LEVELS = {"low": 1, "medium": 2, "high": 3, "critical": 4}
# Rows shown per page in each table; a table with more rows than this is paginated.
PAGE_SIZE = 10

# 16px stroke icons (viewBox 0 0 16 16). Inline so the page needs no network access.
ICONS = {
    "overview": '<rect x="2" y="2" width="5" height="5" rx="1"/><rect x="9" y="2" width="5" height="5" rx="1"/>'
    '<rect x="2" y="9" width="5" height="5" rx="1"/><rect x="9" y="9" width="5" height="5" rx="1"/>',
    "controls": '<path d="M8 1.8 13 3.6v4c0 3-2 5.4-5 6.6-3-1.2-5-3.600-5-6.600v-4z"/><path d="m5.800 8 1.600 1.600 2.900-3"/>',
    "findings": '<path d="M8 2.200 14.200 13H1.800z"/><path d="M8 6.500v3"/><path d="M8 11.300v.2"/>',
    "mitigations": '<path d="M5.500 4h8"/><path d="M5.500 8h8"/><path d="M5.500 12h8"/>'
    '<path d="m2 4 .8.800L4 3.500"/><path d="m2 8 .8.800L4 7.500"/><path d="m2 12 .8.800L4 11.500"/>',
    "file": '<path d="M4 1.800h5l3 3v9.400H4z"/><path d="M9 1.800v3h3"/>',
    "search": '<circle cx="7" cy="7" r="4.200"/><path d="m10.200 10.200 3.300 3.300"/>',
    "export": '<path d="M8 10.500V2.500"/><path d="m5 5.300 3-3 3 3"/><path d="M2.500 10.500v3h11v-3"/>',
    "compliant": '<circle cx="8" cy="8" r="6"/><path d="m5.400 8.200 1.800 1.800 3.400-3.700"/>',
    "partial": '<path d="M8 2.200 14.200 13H1.800z"/><path d="M8 6.500v3"/><path d="M8 11.300v.2"/>',
    "violation": '<circle cx="8" cy="8" r="6"/><path d="m5.800 5.800 4.400 4.400"/><path d="m10.200 5.800-4.400 4.400"/>',
    "not_assessed": '<circle cx="8" cy="8" r="6"/><path d="M5.500 8h5"/>',
}

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


def _asset(name: str) -> str:
    """Text of a dashboard asset. The page inlines it, so the report stays one file."""
    return (ASSETS_DIR / name).read_text(encoding="utf-8")


def render_html(
    system_name: str,
    merged: List[Dict[str, object]],
    summary: Dict[str, object],
    summary_href: Optional[str] = None,
) -> str:
    """Render the dashboard as one self-contained HTML page (no external assets).

    ``summary_href`` is a relative link to the JSON summary, shown in the sidebar
    when the summary is written next to the page.
    """

    def esc(val: object) -> str:
        return html.escape(str(val), quote=True)

    def icon(name: str) -> str:
        return f'<svg class="ico" viewBox="0 0 16 16" aria-hidden="true">{ICONS[name]}</svg>'

    def chips(items: List[str]) -> str:
        if not items:
            return "-"
        return '<div class="chips">' + "".join(f'<span class="chip">{esc(i)}</span>' for i in items) + "</div>"

    def status_badge(status: str) -> str:
        label = STATUS_LABELS.get(status, status)
        return f'<span class="badge st-{esc(status)}">{icon(status)}{esc(label)}</span>'

    def risk_mark(risk: str) -> str:
        level = RISK_LEVELS.get(risk, 0)
        bars = "".join(f'<i class="{"on" if n <= level else ""}"></i>' for n in range(1, 5))
        return f'<span class="risk"><span class="bars" aria-hidden="true">{bars}</span>{esc(risk.capitalize())}</span>'

    def control_cell(m: Dict[str, object]) -> str:
        return (
            f'<td><div class="control-title">{esc(m["title"])}</div>'
            f'<div class="control-id">{esc(m["check_id"])}</div></td>'
        )

    def row_attrs(m: Dict[str, object]) -> str:
        return f'data-status="{esc(m["status"])}" data-risk="{esc(m["risk"])}"'

    def table(view: str, label: str, empty_text: str, head: List[str], rows: List[str], hidden: bool) -> str:
        cells = "".join(f'<th class="num">{h}</th>' if h == "#" else f"<th>{h}</th>" for h in head)
        return (
            f'<section data-view="{view}" data-empty="{esc(empty_text)}" role="tabpanel" aria-label="{esc(label)}"'
            f'{" hidden" if hidden else ""}>\n'
            f'<div class="table-scroll"><table><thead><tr>{cells}</tr></thead>\n<tbody>\n'
            + "\n".join(rows)
            + "\n</tbody></table></div></section>"
        )

    violations: List[Dict[str, object]] = summary["violations"]  # type: ignore[assignment]
    mitigations: List[Dict[str, object]] = summary["mitigations"]  # type: ignore[assignment]
    status_counts: Dict[str, int] = summary["status_counts"]  # type: ignore[assignment]
    total = len(merged)
    compliant = status_counts.get("compliant", 0)
    percent = round(100 * compliant / total) if total else 0

    control_rows = [
        f'<tr {row_attrs(m)}><td class="num">{i}</td>{control_cell(m)}<td>{chips(m["iso27001"])}</td>'
        f'<td>{chips(m["nist"])}</td><td>{risk_mark(str(m["risk"]))}</td><td>{status_badge(str(m["status"]))}</td>'
        f'<td class="nowrap">{esc(m["owner"] or "-")}</td><td class="nowrap">{esc(m["due_date"] or "-")}</td></tr>'
        for i, m in enumerate(merged, 1)
    ]
    finding_rows = [
        f'<tr {row_attrs(m)}><td class="num">{i}</td>{control_cell(m)}<td>{status_badge(str(m["status"]))}</td>'
        f'<td>{risk_mark(str(m["risk"]))}</td><td class="wrap">{esc(m["gap"] or "-")}</td>'
        f'<td class="wrap">{esc(m["evidence"] or "-")}</td></tr>'
        for i, m in enumerate(violations, 1)
    ]
    mitigation_rows = [
        f'<tr {row_attrs(m)}><td class="num">{i}</td>{control_cell(m)}<td class="wrap">{esc(m["mitigation"])}</td>'
        f'<td class="nowrap">{esc(m["owner"] or "-")}</td><td class="nowrap">{esc(m["due_date"] or "-")}</td></tr>'
        for i, m in enumerate(mitigations, 1)
    ]

    # Compliance by risk level: one meter per level that has controls.
    meters = []
    for risk in RISK_ORDER:
        in_level = [m for m in merged if m["risk"] == risk]
        if not in_level:
            continue
        ok = sum(1 for m in in_level if m["status"] == "compliant")
        width = 100 * ok / len(in_level)
        tip = f"{risk.capitalize()} risk: {ok} of {len(in_level)} controls compliant"
        meters.append(
            f'<li class="meter" tabindex="0" data-tip="{esc(tip)}" aria-label="{esc(tip)}">{risk_mark(risk)}'
            f'<div class="meter-track"><div class="meter-fill" style="width:{width:.1f}%"></div></div>'
            f'<div class="meter-figure"><b>{ok}</b> of {len(in_level)} compliant</div></li>'
        )

    # Status ring: one arc per status, separated by a small gap in the surface colour.
    radius, circumference = 50.0, 2 * 3.141592653589793 * 50.0
    present = [(s, status_counts.get(s, 0)) for s in STATUS_ORDER if status_counts.get(s, 0)]
    gap = 1.6 if len(present) > 1 else 0.0
    arcs, offset = [], 0.0
    for status, count in present:
        length = circumference * count / total
        tip = f"{STATUS_COUNT_LABELS[status]}: {count} of {total} controls"
        arcs.append(
            f'<circle class="seg seg-{status}" cx="60" cy="60" r="{radius:g}" tabindex="0" data-tip="{esc(tip)}"'
            f' aria-label="{esc(tip)}" stroke-dasharray="{max(length - gap, 0.5):.2f} {circumference:.2f}"'
            f' stroke-dashoffset="{-(offset + gap / 2):.2f}"/>'
        )
        offset += length
    if not arcs:
        arcs.append(f'<circle class="donut-empty" cx="60" cy="60" r="{radius:g}"/>')
    legend = "".join(
        f'<li><span class="swatch sw-{s}"></span>{STATUS_COUNT_LABELS[s]}<b>{status_counts.get(s, 0)}</b></li>'
        for s in STATUS_ORDER
    )

    generated = datetime.now(timezone.utc)
    stamp = generated.strftime("%d %b %Y, %H:%M UTC").lstrip("0")
    status_options = "".join(f'<option value="{s}">{STATUS_LABELS[s]}</option>' for s in STATUS_ORDER)
    risk_options = "".join(f'<option value="{r}">{r.capitalize()}</option>' for r in RISK_ORDER)
    summary_link = (
        f'<div class="nav-group">Data</div>\n'
        f'      <a class="nav" href="{esc(summary_href)}">{icon("file")}Summary JSON</a>'
        if summary_href
        else ""
    )
    brand_mark = esc((system_name.strip() or "?")[0].upper())

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Compliance Dashboard - {esc(system_name)}</title>
  <style>{_asset("dashboard.css")}</style>
</head>
<body>
<div class="app">
  <aside class="side">
    <div class="brand"><span class="brand-mark" aria-hidden="true">{brand_mark}</span>{esc(system_name)}</div>
    <nav aria-label="Dashboard">
      <div class="nav-group">Compliance</div>
      <button class="nav is-active" type="button" data-target="overview">{icon("overview")}Overview</button>
      <button class="nav" type="button" data-target="controls">{icon("controls")}Controls<span class="count">{total}</span></button>
      <button class="nav" type="button" data-target="findings">{icon("findings")}Findings<span class="count">{len(violations)}</span></button>
      <button class="nav" type="button" data-target="mitigations">{icon("mitigations")}Mitigations<span class="count">{len(mitigations)}</span></button>
      {summary_link}
    </nav>
  </aside>

  <main>
    <header class="top">
      <h1>ISO 27001 / NIST Compliance Dashboard</h1>
      <span class="stamp">Generated <time datetime="{generated.isoformat().replace("+00:00", "Z")}">{stamp}</time></span>
    </header>

    <div class="content">
      <div class="cards" id="overview">
        <section class="card card-pad" aria-labelledby="risk-title">
          <h2 id="risk-title">Compliance by risk level</h2>
          <div class="hero">
            <span class="hero-figure">{percent}%</span>
            <span class="hero-label">{compliant} of {total} controls compliant</span>
          </div>
          <ul class="meters">
            {"".join(meters)}
          </ul>
        </section>

        <section class="card card-pad" aria-labelledby="status-title">
          <h2 id="status-title" class="quiet">Status</h2>
          <div class="donut-wrap">
            <div class="donut">
              <svg viewBox="0 0 120 120" role="img" aria-label="Controls by status">{"".join(arcs)}</svg>
              <div class="donut-center"><div class="donut-total">{total}</div><div class="donut-caption">Controls</div></div>
            </div>
            <ul class="legend">{legend}</ul>
          </div>
        </section>
      </div>

      <div class="card" id="records">
        <div class="tabs" role="tablist" aria-label="Views">
          <button class="tab" type="button" role="tab" data-tab="controls" aria-selected="true">Controls<span class="count">{total}</span></button>
          <button class="tab" type="button" role="tab" data-tab="findings" aria-selected="false" tabindex="-1">Findings<span class="count">{len(violations)}</span></button>
          <button class="tab" type="button" role="tab" data-tab="mitigations" aria-selected="false" tabindex="-1">Mitigations<span class="count">{len(mitigations)}</span></button>
        </div>
        <div class="toolbar">
          <select class="control" id="filter-status" aria-label="Status"><option value="">All statuses</option>{status_options}</select>
          <select class="control" id="filter-risk" aria-label="Risk"><option value="">All risk levels</option>{risk_options}</select>
          <span class="spacer"></span>
          <label class="search">{icon("search")}<input id="filter-query" type="search" placeholder="Search" aria-label="Search" /></label>
          <button class="control" id="export" type="button">{icon("export")}Export</button>
        </div>
        {table("controls", "Controls", "No controls defined.",
               ["#", "Control", "ISO 27001", "NIST", "Risk", "Status", "Owner", "Due Date"], control_rows, False)}
        {table("findings", "Findings", "No violations or partial findings.",
               ["#", "Control", "Status", "Risk", "Gap", "Evidence"], finding_rows, True)}
        {table("mitigations", "Mitigations", "No mitigation actions recorded.",
               ["#", "Control", "Mitigation", "Owner", "Due Date"], mitigation_rows, True)}
        <div class="empty" id="empty" hidden></div>
        <div class="pager" id="pager" hidden>
          <span id="pager-range"></span>
          <span class="spacer"></span>
          <span id="pager-page"></span>
          <button class="control" id="pager-prev" type="button">Previous</button>
          <button class="control" id="pager-next" type="button">Next</button>
        </div>
      </div>
    </div>
  </main>
</div>
<script>{_asset("dashboard.js").replace("__PAGE_SIZE__", str(PAGE_SIZE))}</script>
</body>
</html>
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ISO 27001/NIST dashboard scaffold for OpenClaw")
    parser.add_argument(
        "--controls-file",
        default=str(default_controls_path()),
        help="Controls map JSON file",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    init_cmd = sub.add_parser("init-assessment", help="Create scaffold assessment JSON")
    init_cmd.add_argument("--system", default="OpenClaw", help="System name")
    init_cmd.add_argument(
        "--output",
        default="cyber-security-engineer/assessments/openclaw-assessment.json",
        help="Output path for assessment scaffold",
    )

    render_cmd = sub.add_parser("render", help="Render dashboard from controls+assessment")
    render_cmd.add_argument(
        "--assessment-file",
        default="cyber-security-engineer/assessments/openclaw-assessment.json",
        help="Assessment input JSON path",
    )
    render_cmd.add_argument(
        "--output-html",
        default="cyber-security-engineer/assessments/compliance-dashboard.html",
        help="Output HTML dashboard path",
    )
    render_cmd.add_argument(
        "--output-summary",
        default="cyber-security-engineer/assessments/compliance-summary.json",
        help="Output summary JSON path",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    controls = load_json(Path(args.controls_file).expanduser())
    if not isinstance(controls, list):
        raise ValueError("Controls file must be a JSON array.")

    if args.command == "init-assessment":
        scaffold = init_assessment(controls, args.system)
        out = Path(args.output)
        write_json(out, scaffold)
        print(json.dumps({"status": "ok", "created": str(out), "checks": len(scaffold["checks"])}))
        return 0

    if args.command == "render":
        assessment_path = Path(args.assessment_file)
        assessment = load_json(assessment_path)
        validate_assessment(assessment)

        merged = merge_controls(controls, assessment)
        summary = summarize(merged)
        system_name = assessment.get("metadata", {}).get("system", "OpenClaw")

        out_html = Path(args.output_html)
        out_summary = Path(args.output_summary)
        # Link the summary from the page only when both files sit in the same folder.
        same_folder = out_html.resolve().parent == out_summary.resolve().parent
        page = render_html(system_name, merged, summary, summary_href=out_summary.name if same_folder else None)
        out_html.parent.mkdir(parents=True, exist_ok=True)
        out_html.write_text(page, encoding="utf-8")

        write_json(
            out_summary,
            {
                "generated_at_utc": utc_now(),
                "system": system_name,
                "summary": summary,
                "controls": merged,
            },
        )
        print(
            json.dumps(
                {
                    "status": "ok",
                    "output_html": str(out_html),
                    "output_summary": str(out_summary),
                    "violations_or_partial": len(summary["violations"]),
                }
            )
        )
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
