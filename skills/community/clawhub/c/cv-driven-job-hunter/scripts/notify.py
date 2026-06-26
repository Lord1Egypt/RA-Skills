#!/usr/bin/env python3
"""
notify.py — Arma un digest formateado con:
  - Top matches nuevos del último scan
  - Follow-ups pendientes
  - Estado del pipeline de postulaciones

El agente toma este output y lo presenta en el chat (canal `claude_chat`)
o lo enruta al canal configurado. No envía mensajes — solo formatea.

Uso:
    python3 notify.py --config config.json [--matches matches.json] [--format md|json]
"""

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


ACTIVE_STATUSES = {"drafted", "submitted", "viewed", "screening", "interview"}


def _data_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "data"


def _load_apps() -> list[dict]:
    p = _data_dir() / "applications.json"
    if not p.exists():
        return []
    try:
        return json.loads(p.read_text(encoding="utf-8")).get("applications", [])
    except json.JSONDecodeError:
        return []


def _load_matches(path: Path | None) -> list[dict]:
    if not path or not path.exists():
        # Fallback: leer data/recent_matches.json si existe
        fallback = _data_dir() / "recent_matches.json"
        path = fallback if fallback.exists() else None
    if not path:
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else data.get("matches", [])
    except json.JSONDecodeError:
        return []


def _pending_followups(apps: list[dict], follow_up_days: list[int]) -> list[dict]:
    now = datetime.now(timezone.utc)
    pending = []
    for app in apps:
        if app.get("status") not in ACTIVE_STATUSES:
            continue
        ref = app.get("submitted_at") or app.get("updated_at") or app.get("created_at")
        if not ref:
            continue
        try:
            ref_dt = datetime.fromisoformat(ref.replace("Z", "+00:00"))
        except ValueError:
            continue
        days = (now - ref_dt).days
        triggers = [d for d in follow_up_days if days >= d]
        if triggers:
            pending.append({**app, "_days_since": days, "_milestone": max(triggers)})
    pending.sort(key=lambda a: -a["_days_since"])
    return pending


def format_md(matches: list[dict], pending: list[dict], apps: list[dict], cfg: dict) -> str:
    lines = []
    lines.append(f"# Job-hunter digest — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")

    # Top matches
    threshold = cfg.get("notifications", {}).get("alert_threshold_score", 85)
    high = [m for m in matches if (m.get("score") or 0) >= threshold]
    medium = [m for m in matches if 70 <= (m.get("score") or 0) < threshold]
    if high:
        lines.append(f"## Matches calientes ({len(high)})")
        for m in high[:5]:
            lines.append(_format_match_card(m, prefix="⭐"))
        lines.append("")
    if medium:
        lines.append(f"## Matches a considerar ({len(medium)})")
        for m in medium[:5]:
            lines.append(_format_match_card(m, prefix="·"))
        lines.append("")
    if not high and not medium:
        lines.append("## Matches")
        lines.append("Sin matches nuevos sobre el threshold. Considerá:")
        lines.append("- Bajar `min_match_score` en config si querés ver más")
        lines.append("- Ampliar `preferred_titles` o `markets`")
        lines.append("- Esperar 24-48h y volver a escanear")
        lines.append("")

    # Pipeline state
    counts = Counter(a.get("status", "unknown") for a in apps)
    if apps:
        lines.append(f"## Pipeline ({len(apps)} postulaciones totales)")
        for status in ["drafted", "submitted", "viewed", "screening", "interview", "offer"]:
            n = counts.get(status, 0)
            if n:
                lines.append(f"- **{status}**: {n}")
        rejected = counts.get("rejected", 0) + counts.get("ghosted", 0)
        if rejected:
            lines.append(f"- _cerradas_: {rejected}")
        lines.append("")

    # Follow-ups
    if pending:
        lines.append(f"## Follow-ups pendientes ({len(pending)})")
        for p in pending[:10]:
            milestone_label = {3: "día 3", 7: "día 7", 14: "día 14"}.get(p["_milestone"], f"{p['_milestone']}d+")
            lines.append(
                f"- **{p.get('company')}** — {p.get('title')} ({p.get('status')}, {p['_days_since']}d) "
                f"→ trigger {milestone_label}"
            )
        lines.append("")
        lines.append("Acciones sugeridas: corré `track_applications.py pending-followups` para detalle.")
        lines.append("")

    if not high and not medium and not pending:
        lines.append("Nada urgente hoy. Buen momento para mejorar el CV — "
                    "abrí `analyze_profile.py` y revisá los gaps top.")
    return "\n".join(lines).strip() + "\n"


def _format_match_card(m: dict, prefix: str = "·") -> str:
    score = m.get("score", "?")
    title = m.get("title", "(sin título)")
    company = m.get("company", "(sin empresa)")
    flags = m.get("flags") or []
    flag_str = f"  ⚠ {', '.join(flags)}" if flags else ""
    rationale = m.get("rationale") or []
    why = "; ".join(rationale[:2]) if rationale else ""
    url = m.get("url") or m.get("job_id", "")
    return (
        f"{prefix} **{score}/100** — {title} @ {company}{flag_str}\n"
        f"  {why}\n"
        f"  {url}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--matches", type=Path, help="JSON con matches recientes")
    parser.add_argument("--format", choices=["md", "json"], default="md")
    args = parser.parse_args()

    cfg = json.loads(args.config.read_text(encoding="utf-8"))
    follow_up_days = cfg.get("tracking", {}).get("follow_up_days", [3, 7, 14])

    apps = _load_apps()
    matches = _load_matches(args.matches)
    pending = _pending_followups(apps, follow_up_days)

    if args.format == "json":
        print(json.dumps({
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "matches": matches,
            "pending_followups": pending,
            "pipeline_summary": dict(Counter(a.get("status") for a in apps)),
        }, indent=2, ensure_ascii=False))
    else:
        print(format_md(matches, pending, apps, cfg))
    return 0


if __name__ == "__main__":
    sys.exit(main())
