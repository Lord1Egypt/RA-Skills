#!/usr/bin/env python3
"""Baby tracker CSV logger/query/chart helper.

Stores flexible baby events in a single append-only CSV plus JSON metadata.
No third-party dependencies required.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import html
import json
import math
import os
import re
import sys
import uuid
from pathlib import Path
from zoneinfo import ZoneInfo

DEFAULT_DATA_DIR = Path(os.environ.get("BABY_TRACKER_DIR", Path.home() / ".openclaw" / "workspace" / "data" / "baby-tracker"))
EVENT_HEADERS = [
    "event_id",
    "timestamp_local",
    "timestamp_utc",
    "timezone",
    "baby_id",
    "type",
    "subtype",
    "metric",
    "value",
    "unit",
    "details_json",
    "notes",
    "source_text",
    "created_at_utc",
]

PERCENTILE_HEADERS = ["sex", "age_days", "p3", "p15", "p50", "p85", "p97", "unit", "source"]

# Approximate WHO-style weight-for-age guide points. Visual aid only; replace with exact WHO data if needed.
# Values are kg at monthly ages 0-24. Interpolation is linear between points.
APPROX_WEIGHT_PCTS = {
    "female": [
        (0, 2.4, 2.8, 3.2, 3.7, 4.2), (30, 3.2, 3.6, 4.2, 4.8, 5.4),
        (61, 4.0, 4.5, 5.1, 5.8, 6.6), (91, 4.6, 5.2, 5.8, 6.6, 7.5),
        (122, 5.1, 5.7, 6.4, 7.3, 8.2), (152, 5.5, 6.1, 6.9, 7.8, 8.8),
        (183, 5.8, 6.5, 7.3, 8.2, 9.3), (213, 6.1, 6.8, 7.6, 8.6, 9.8),
        (244, 6.3, 7.0, 7.9, 9.0, 10.2), (274, 6.6, 7.3, 8.2, 9.3, 10.5),
        (304, 6.8, 7.5, 8.5, 9.6, 10.9), (335, 7.0, 7.7, 8.7, 9.9, 11.2),
        (365, 7.1, 7.9, 8.9, 10.1, 11.5), (396, 7.3, 8.1, 9.2, 10.4, 11.8),
        (426, 7.5, 8.3, 9.4, 10.6, 12.1), (457, 7.7, 8.5, 9.6, 10.9, 12.4),
        (487, 7.8, 8.7, 9.8, 11.1, 12.6), (518, 8.0, 8.8, 10.0, 11.4, 12.9),
        (548, 8.2, 9.0, 10.2, 11.6, 13.2), (578, 8.3, 9.2, 10.4, 11.8, 13.5),
        (609, 8.5, 9.4, 10.6, 12.1, 13.7), (639, 8.7, 9.6, 10.9, 12.3, 14.0),
        (670, 8.8, 9.8, 11.1, 12.5, 14.3), (700, 9.0, 9.9, 11.3, 12.8, 14.6),
        (730, 9.2, 10.1, 11.5, 13.0, 14.8),
    ],
    "male": [
        (0, 2.5, 2.9, 3.3, 3.9, 4.4), (30, 3.4, 3.9, 4.5, 5.1, 5.8),
        (61, 4.3, 4.9, 5.6, 6.3, 7.1), (91, 5.0, 5.7, 6.4, 7.2, 8.0),
        (122, 5.6, 6.2, 7.0, 7.8, 8.7), (152, 6.0, 6.7, 7.5, 8.4, 9.3),
        (183, 6.4, 7.1, 7.9, 8.8, 9.8), (213, 6.7, 7.4, 8.3, 9.2, 10.3),
        (244, 6.9, 7.7, 8.6, 9.6, 10.7), (274, 7.1, 7.9, 8.9, 9.9, 11.0),
        (304, 7.4, 8.2, 9.2, 10.2, 11.4), (335, 7.6, 8.4, 9.4, 10.5, 11.7),
        (365, 7.7, 8.6, 9.6, 10.8, 12.0), (396, 7.9, 8.8, 9.9, 11.0, 12.3),
        (426, 8.1, 9.0, 10.1, 11.3, 12.6), (457, 8.3, 9.2, 10.3, 11.5, 12.8),
        (487, 8.4, 9.4, 10.5, 11.7, 13.1), (518, 8.6, 9.6, 10.7, 12.0, 13.4),
        (548, 8.8, 9.8, 10.9, 12.2, 13.7), (578, 8.9, 10.0, 11.1, 12.5, 13.9),
        (609, 9.1, 10.1, 11.3, 12.7, 14.2), (639, 9.2, 10.3, 11.5, 12.9, 14.5),
        (670, 9.4, 10.5, 11.8, 13.2, 14.7), (700, 9.5, 10.7, 12.0, 13.4, 15.0),
        (730, 9.7, 10.8, 12.2, 13.6, 15.3),
    ],
}


def data_paths(data_dir: Path) -> dict[str, Path]:
    return {
        "dir": data_dir,
        "events": data_dir / "events.csv",
        "metadata": data_dir / "metadata.json",
        "percentiles": data_dir / "weight_percentiles_approx.csv",
        "charts": data_dir / "charts",
    }


def ensure_store(data_dir: Path) -> dict[str, Path]:
    paths = data_paths(data_dir)
    paths["dir"].mkdir(parents=True, exist_ok=True)
    paths["charts"].mkdir(parents=True, exist_ok=True)
    if not paths["events"].exists():
        with paths["events"].open("w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=EVENT_HEADERS).writeheader()
    if not paths["metadata"].exists():
        write_json(paths["metadata"], {
            "baby_id": "baby-1",
            "name": None,
            "date_of_birth": None,
            "sex": None,
            "timezone": "Europe/London",
            "notes": "Set name, date_of_birth, and sex for age-aware percentile charts.",
        })
    if not paths["percentiles"].exists():
        with paths["percentiles"].open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=PERCENTILE_HEADERS)
            writer.writeheader()
            for sex, rows in APPROX_WEIGHT_PCTS.items():
                for age_days, p3, p15, p50, p85, p97 in rows:
                    writer.writerow({
                        "sex": sex, "age_days": age_days, "p3": p3, "p15": p15,
                        "p50": p50, "p85": p85, "p97": p97, "unit": "kg",
                        "source": "Approximate guide points; replace with exact WHO LMS data for clinical use.",
                    })
    return paths


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")
    tmp.replace(path)


def parse_fields(items: list[str]) -> dict[str, str]:
    out = {}
    for item in items or []:
        if "=" not in item:
            raise SystemExit(f"--field must be key=value, got: {item}")
        k, v = item.split("=", 1)
        k = k.strip()
        if not k:
            raise SystemExit(f"field key cannot be empty: {item}")
        out[k] = v.strip()
    return out


def parse_timestamp(value: str | None, tz_name: str) -> tuple[str, str]:
    tz = ZoneInfo(tz_name)
    if not value or value.lower() == "now":
        local = dt.datetime.now(tz).replace(microsecond=0)
    else:
        raw = value.strip()
        if re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", raw):
            parsed = dt.datetime.strptime(raw, "%Y-%m-%d %H:%M")
            local = parsed.replace(tzinfo=tz)
        else:
            parsed = dt.datetime.fromisoformat(raw)
            local = parsed.replace(tzinfo=tz) if parsed.tzinfo is None else parsed.astimezone(tz)
    utc = local.astimezone(dt.timezone.utc)
    return local.isoformat(), utc.isoformat().replace("+00:00", "Z")


def parse_dateish(value: str | None, tz_name: str, end: bool = False) -> dt.datetime | None:
    if not value:
        return None
    tz = ZoneInfo(tz_name)
    v = value.strip().lower()
    now = dt.datetime.now(tz)
    if v == "today":
        base = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return base + dt.timedelta(days=1) if end else base
    if v == "yesterday":
        base = (now - dt.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        return base + dt.timedelta(days=1) if end else base
    if v.endswith("d") and v[:-1].isdigit():
        return now - dt.timedelta(days=int(v[:-1]))
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
        d = dt.date.fromisoformat(v)
        t = dt.time.max if end else dt.time.min
        return dt.datetime.combine(d, t, tzinfo=tz)
    parsed = dt.datetime.fromisoformat(value)
    return parsed.replace(tzinfo=tz) if parsed.tzinfo is None else parsed.astimezone(tz)


def load_events(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def cmd_meta(args: argparse.Namespace) -> int:
    paths = ensure_store(args.data_dir)
    meta = read_json(paths["metadata"])
    for key in ["baby_id", "name", "date_of_birth", "sex", "timezone", "notes"]:
        val = getattr(args, key, None)
        if val is not None:
            meta[key] = val
    extra = parse_fields(args.field)
    meta.update(extra)
    write_json(paths["metadata"], meta)
    print(json.dumps(meta, indent=2, ensure_ascii=False))
    return 0


def cmd_log(args: argparse.Namespace) -> int:
    paths = ensure_store(args.data_dir)
    meta = read_json(paths["metadata"])
    tz_name = args.timezone or meta.get("timezone") or "Europe/London"
    local_ts, utc_ts = parse_timestamp(args.at, tz_name)
    details = parse_fields(args.field)
    row = {
        "event_id": args.event_id or str(uuid.uuid4()),
        "timestamp_local": local_ts,
        "timestamp_utc": utc_ts,
        "timezone": tz_name,
        "baby_id": args.baby_id or meta.get("baby_id") or "baby-1",
        "type": args.type.lower().strip(),
        "subtype": (args.subtype or "").lower().strip(),
        "metric": (args.metric or "").lower().strip(),
        "value": "" if args.value is None else str(args.value),
        "unit": args.unit or "",
        "details_json": json.dumps(details, ensure_ascii=False, sort_keys=True),
        "notes": args.notes or "",
        "source_text": args.source_text or "",
        "created_at_utc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }
    with paths["events"].open("a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=EVENT_HEADERS).writerow(row)
    print(json.dumps(row, indent=2, ensure_ascii=False))
    return 0


def event_dt(row: dict) -> dt.datetime:
    return dt.datetime.fromisoformat(row["timestamp_local"])


def filter_events(events: list[dict], args: argparse.Namespace, tz_name: str) -> list[dict]:
    since = parse_dateish(args.since, tz_name, end=False)
    until = parse_dateish(args.until, tz_name, end=True)
    out = []
    for row in events:
        try:
            ts = event_dt(row)
        except Exception:
            continue
        if args.type and row.get("type") != args.type.lower():
            continue
        if args.metric and row.get("metric") != args.metric.lower():
            continue
        if args.subtype and row.get("subtype") != args.subtype.lower():
            continue
        if since and ts < since:
            continue
        if until and ts > until:
            continue
        out.append(row)
    out.sort(key=event_dt)
    if args.limit:
        out = out[-args.limit:]
    return out


def cmd_query(args: argparse.Namespace) -> int:
    paths = ensure_store(args.data_dir)
    meta = read_json(paths["metadata"])
    tz_name = meta.get("timezone") or "Europe/London"
    rows = filter_events(load_events(paths["events"]), args, tz_name)
    if args.format == "json":
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    elif args.format == "csv":
        writer = csv.DictWriter(sys.stdout, fieldnames=EVENT_HEADERS)
        writer.writeheader()
        writer.writerows(rows)
    else:
        print(summary(rows))
    return 0


def summary(rows: list[dict]) -> str:
    if not rows:
        return "No matching events."
    counts: dict[str, int] = {}
    lines = [f"{len(rows)} matching event(s)."]
    for r in rows:
        key = r.get("type") or "unknown"
        counts[key] = counts.get(key, 0) + 1
    lines.append("Counts: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    lines.append("Latest:")
    for r in rows[-10:]:
        bits = [r["timestamp_local"][:16].replace("T", " "), r.get("type", "")]
        for k in ["subtype", "metric", "value", "unit"]:
            if r.get(k):
                bits.append(r[k])
        if r.get("details_json") and r["details_json"] != "{}":
            bits.append(r["details_json"])
        if r.get("notes"):
            bits.append(r["notes"])
        lines.append("- " + " | ".join(bits))
    return "\n".join(lines)


def read_percentiles(path: Path, sex: str) -> list[dict]:
    if not path.exists() or not sex:
        return []
    sex = sex.lower()
    with path.open("r", newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r.get("sex", "").lower() == sex]
    return sorted(rows, key=lambda r: float(r["age_days"]))


def baby_age_days(meta: dict, timestamp: dt.datetime) -> float | None:
    dob = meta.get("date_of_birth")
    if not dob:
        return None
    birth = dt.date.fromisoformat(dob)
    return (timestamp.date() - birth).days + (timestamp.hour / 24) + (timestamp.minute / 1440)


def metric_points(events: list[dict], meta: dict, metric: str, unit: str | None) -> list[tuple[float, float, str]]:
    pts = []
    for r in events:
        if r.get("metric") != metric:
            continue
        if unit and r.get("unit") and r.get("unit") != unit:
            continue
        try:
            value = float(r.get("value") or "")
            ts = event_dt(r)
            age = baby_age_days(meta, ts)
            if age is None:
                continue
            pts.append((age, value, ts.strftime("%Y-%m-%d %H:%M")))
        except Exception:
            continue
    return sorted(pts)


def polyline(points: list[tuple[float, float]], xmap, ymap) -> str:
    return " ".join(f"{xmap(x):.1f},{ymap(y):.1f}" for x, y in points if math.isfinite(x) and math.isfinite(y))


def cmd_chart(args: argparse.Namespace) -> int:
    paths = ensure_store(args.data_dir)
    meta = read_json(paths["metadata"])
    events = load_events(paths["events"])
    metric = args.metric.lower()
    unit = args.unit or ("kg" if metric == "weight" else None)
    pts = metric_points(events, meta, metric, unit)
    if not pts:
        raise SystemExit(f"No chartable {metric} points found. Need metadata.date_of_birth and logged numeric values.")

    pcts = read_percentiles(paths["percentiles"], meta.get("sex", "")) if metric == "weight" else []
    pct_lines = []
    for p in ["p3", "p15", "p50", "p85", "p97"]:
        line = []
        for r in pcts:
            try:
                line.append((float(r["age_days"]), float(r[p])))
            except Exception:
                pass
        pct_lines.append((p, line))

    x_values = [p[0] for p in pts]
    y_values = [p[1] for p in pts]
    for _, line in pct_lines:
        for x, y in line:
            if min(x_values) - 30 <= x <= max(x_values) + 180:
                x_values.append(x); y_values.append(y)
    xmin, xmax = max(0, min(x_values) - 7), max(x_values) + 30
    ymin, ymax = max(0, min(y_values) - 0.5), max(y_values) + 0.8
    if xmax == xmin: xmax += 1
    if ymax == ymin: ymax += 1

    W, H = 960, 620
    ml, mr, mt, mb = 70, 30, 45, 80
    plot_w, plot_h = W - ml - mr, H - mt - mb
    xmap = lambda x: ml + ((x - xmin) / (xmax - xmin)) * plot_w
    ymap = lambda y: mt + plot_h - ((y - ymin) / (ymax - ymin)) * plot_h

    grid = []
    for i in range(6):
        y = ymin + (ymax - ymin) * i / 5
        yy = ymap(y)
        grid.append(f'<line x1="{ml}" x2="{W-mr}" y1="{yy:.1f}" y2="{yy:.1f}" class="grid"/><text x="{ml-10}" y="{yy+4:.1f}" text-anchor="end" class="axis-label">{y:.1f}</text>')
    for i in range(6):
        x = xmin + (xmax - xmin) * i / 5
        xx = xmap(x)
        grid.append(f'<line y1="{mt}" y2="{H-mb}" x1="{xx:.1f}" x2="{xx:.1f}" class="grid"/><text x="{xx:.1f}" y="{H-mb+26}" text-anchor="middle" class="axis-label">{int(round(x))}d</text>')

    pct_svg = []
    colors = {"p3":"#c7d2fe", "p15":"#93c5fd", "p50":"#64748b", "p85":"#f9a8d4", "p97":"#f0abfc"}
    for name, line in pct_lines:
        visible = [(x, y) for x, y in line if xmin <= x <= xmax]
        if len(visible) >= 2:
            pts_attr = polyline(visible, xmap, ymap)
            pct_svg.append(f'<polyline points="{pts_attr}" fill="none" stroke="{colors[name]}" stroke-width="2" stroke-dasharray="5 5"/>')
            lx, ly = visible[-1]
            pct_svg.append(f'<text x="{xmap(lx)-4:.1f}" y="{ymap(ly)-5:.1f}" text-anchor="end" class="pct-label">{name.upper()}</text>')

    baby_line = polyline([(x, y) for x, y, _ in pts], xmap, ymap)
    dots = []
    for age, value, label in pts:
        dots.append(f'<circle cx="{xmap(age):.1f}" cy="{ymap(value):.1f}" r="5" class="dot"><title>{html.escape(label)} — {value:g} {html.escape(unit or "")}</title></circle>')

    title = args.title or f"{meta.get('name') or 'Baby'} {metric} over time"
    subtitle = f"DOB: {meta.get('date_of_birth') or 'not set'} · Sex: {meta.get('sex') or 'not set'} · Generated {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}"
    warning = "Percentile lines are approximate guide points, not medical advice. Replace CSV with exact WHO data for clinical precision." if pcts else "No percentile data shown: set baby sex or add percentile CSV."

    svg = f'''<svg viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(title)}">
    <rect width="{W}" height="{H}" fill="#fff" rx="18"/>
    <text x="{ml}" y="30" class="title">{html.escape(title)}</text>
    <text x="{ml}" y="54" class="subtitle">{html.escape(subtitle)}</text>
    {''.join(grid)}
    <line x1="{ml}" y1="{H-mb}" x2="{W-mr}" y2="{H-mb}" class="axis"/>
    <line x1="{ml}" y1="{mt}" x2="{ml}" y2="{H-mb}" class="axis"/>
    <text x="{W/2}" y="{H-18}" text-anchor="middle" class="axis-title">Age in days</text>
    <text transform="translate(20 {H/2}) rotate(-90)" text-anchor="middle" class="axis-title">{html.escape(metric)} ({html.escape(unit or '')})</text>
    {''.join(pct_svg)}
    <polyline points="{baby_line}" fill="none" class="baby-line"/>
    {''.join(dots)}
    </svg>'''

    html_doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{html.escape(title)}</title>
<style>
  body {{ margin: 0; background: #f8fafc; font-family: Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif; color:#0f172a; }}
  main {{ max-width: 1040px; margin: 24px auto; padding: 20px; }}
  .card {{ background:white; border:1px solid #e2e8f0; border-radius:24px; box-shadow:0 18px 50px rgba(15,23,42,.08); padding:18px; }}
  .title {{ font-size:24px; font-weight:800; fill:#0f172a; }}
  .subtitle {{ font-size:13px; fill:#475569; }}
  .axis {{ stroke:#334155; stroke-width:1.5; }}
  .grid {{ stroke:#e2e8f0; stroke-width:1; }}
  .axis-label, .pct-label {{ font-size:12px; fill:#64748b; }}
  .axis-title {{ font-size:14px; fill:#334155; font-weight:650; }}
  .baby-line {{ stroke:#0f766e; stroke-width:4; stroke-linecap:round; stroke-linejoin:round; }}
  .dot {{ fill:#14b8a6; stroke:#0f766e; stroke-width:2; }}
  .note {{ margin: 14px 8px 2px; color:#64748b; font-size:13px; }}
</style>
</head>
<body><main><div class="card">{svg}<p class="note">{html.escape(warning)}</p></div></main></body></html>'''

    out = Path(args.output) if args.output else paths["charts"] / f"{metric}-{dt.datetime.now().strftime('%Y%m%d-%H%M%S')}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_doc, encoding="utf-8")
    print(out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Baby tracker CSV logger/query/chart helper")
    p.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    sub = p.add_subparsers(dest="cmd", required=True)

    meta = sub.add_parser("meta", help="create/update/show baby metadata")
    meta.add_argument("--baby-id")
    meta.add_argument("--name")
    meta.add_argument("--date-of-birth")
    meta.add_argument("--sex", choices=["female", "male", "unknown"])
    meta.add_argument("--timezone")
    meta.add_argument("--notes")
    meta.add_argument("--field", action="append", default=[], help="extra metadata key=value")
    meta.set_defaults(func=cmd_meta)

    log = sub.add_parser("log", help="append one event")
    log.add_argument("--type", required=True, help="diaper, feed, sleep, growth, temperature, medication, custom...")
    log.add_argument("--subtype", help="wet, dirty, both, bottle, breast, weight...")
    log.add_argument("--metric", help="weight, height, temperature, volume...")
    log.add_argument("--value", type=float)
    log.add_argument("--unit")
    log.add_argument("--field", action="append", default=[], help="structured detail key=value, repeatable")
    log.add_argument("--notes")
    log.add_argument("--source-text")
    log.add_argument("--at", help="local ISO time, 'YYYY-MM-DD HH:MM', or now")
    log.add_argument("--timezone")
    log.add_argument("--baby-id")
    log.add_argument("--event-id")
    log.set_defaults(func=cmd_log)

    q = sub.add_parser("query", help="filter events")
    q.add_argument("--type")
    q.add_argument("--subtype")
    q.add_argument("--metric")
    q.add_argument("--since", help="today, yesterday, 7d, YYYY-MM-DD, ISO datetime")
    q.add_argument("--until", help="YYYY-MM-DD or ISO datetime")
    q.add_argument("--limit", type=int)
    q.add_argument("--format", choices=["summary", "json", "csv"], default="summary")
    q.set_defaults(func=cmd_query)

    c = sub.add_parser("chart", help="make self-contained HTML chart")
    c.add_argument("--metric", required=True, help="weight currently has percentile guide support")
    c.add_argument("--unit")
    c.add_argument("--output")
    c.add_argument("--title")
    c.set_defaults(func=cmd_chart)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
