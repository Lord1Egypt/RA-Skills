#!/usr/bin/env python3
"""
Frisbee multi-activity comparison and season trend analysis.

Modes:
  training   — compare training sessions over time
  tournament — compare multiple tournaments by date range
  cross      — training vs tournament intensity comparison
  season     — full season overview with HRV + load trends

Usage:
    python3 scripts/frisbee_compare.py --mode training --days 90
    python3 scripts/frisbee_compare.py --mode cross --days 60
    python3 scripts/frisbee_compare.py --mode season --days 180
    python3 scripts/frisbee_compare.py --mode training --days 90 --output ~/Desktop/compare.html
"""

import sys
import json
import argparse
import tempfile
import webbrowser
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from garmin_auth import get_client
from garmin_data import fetch_hrv, fetch_heart_rate, fetch_body_battery


# Intensity label heuristics based on avg HR % of estimated max
def _intensity_label(avg_hr, max_hr_estimate=185):
    if not avg_hr:
        return "Unknown"
    pct = avg_hr / max_hr_estimate * 100
    if pct >= 80:
        return "High"
    if pct >= 65:
        return "Moderate"
    return "Low"


def load_activities_summary(client, days=90, start=None, end=None):
    """
    Fetch all activities in range with key metrics.
    Returns list of activity summary dicts.
    """
    if start and end:
        start_date, end_date = start, end
    else:
        end_dt = datetime.now()
        start_dt = end_dt - timedelta(days=days)
        start_date = start_dt.strftime("%Y-%m-%d")
        end_date = end_dt.strftime("%Y-%m-%d")

    try:
        raw = client.get_activities_by_date(start_date, end_date, activitytype="")
    except Exception as e:
        print(f"⚠️  Error fetching activities: {e}", file=sys.stderr)
        return []

    result = []
    for a in raw:
        start_local = a.get("startTimeLocal", "")
        date = start_local.split(" ")[0] if start_local else ""
        duration_s = a.get("duration") or 0
        distance_m = a.get("distance") or 0
        top_speed_ms = a.get("maxSpeed")
        avg_hr = a.get("averageHR")
        max_hr = a.get("maxHR")
        name = a.get("activityName") or "Activity"
        atype = (a.get("activityType") or {}).get("typeKey", "other")
        calories = a.get("calories") or 0

        result.append({
            "activity_id": a.get("activityId"),
            "date": date,
            "name": name,
            "type": atype,
            "duration_min": round(duration_s / 60, 1),
            "distance_km": round(distance_m / 1000, 2),
            "top_speed_kmh": round(top_speed_ms * 3.6, 1) if top_speed_ms else None,
            "avg_hr": avg_hr,
            "max_hr": max_hr,
            "calories": calories,
            "intensity": _intensity_label(avg_hr),
        })

    return sorted(result, key=lambda x: x["date"])


def classify_activity(activity, training_keywords=None, game_keywords=None):
    """
    Classify an activity as 'game', 'training', or 'other'.
    Uses name keywords heuristically, falls back to 'other'.
    """
    if training_keywords is None:
        training_keywords = ["practice", "training", "train", "drill", "练", "训", "scrimmage"]
    if game_keywords is None:
        game_keywords = ["game", "match", "tournament", "比赛", "finals", "semifinal", "vs", "vs."]

    name_lower = (activity.get("name") or "").lower()
    for kw in game_keywords:
        if kw in name_lower:
            return "game"
    for kw in training_keywords:
        if kw in name_lower:
            return "training"
    return "other"


def build_comparison_data(activities, hrv_by_date, rhr_by_date):
    """Attach recovery metrics to each activity."""
    enriched = []
    for a in activities:
        d = a["date"]
        hrv = hrv_by_date.get(d, {}).get("last_night_avg")
        rhr = rhr_by_date.get(d, {}).get("resting_hr")
        enriched.append({**a, "hrv": hrv, "resting_hr": rhr})
    return enriched


def generate_comparison_html(activities, mode, days):
    """Generate comparison HTML dashboard."""
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")
    mode_labels = {
        "training": "Training Sessions",
        "tournament": "Tournament Games",
        "cross": "Training vs Game Comparison",
        "season": "Season Overview",
    }
    title = f"🥏 {mode_labels.get(mode, 'Comparison')} — Last {days} days"

    # Split into game vs training for cross mode
    games = [a for a in activities if a.get("category") == "game"]
    trainings = [a for a in activities if a.get("category") == "training"]
    others = [a for a in activities if a.get("category") == "other"]

    def dates(lst): return [a["date"] for a in lst]
    def metric(lst, key): return [a.get(key) for a in lst]

    # ── Chart 1: Top Speed over time ──
    speed_datasets = []
    if mode == "cross":
        if trainings:
            speed_datasets.append({
                "label": "Training Top Speed (km/h)",
                "data": [{"x": a["date"], "y": a.get("top_speed_kmh")} for a in trainings if a.get("top_speed_kmh")],
                "borderColor": "rgba(99, 179, 237, 1)",
                "backgroundColor": "rgba(99, 179, 237, 0.15)",
                "borderWidth": 2, "tension": 0.3, "fill": False, "pointRadius": 5,
            })
        if games:
            speed_datasets.append({
                "label": "Game Top Speed (km/h)",
                "data": [{"x": a["date"], "y": a.get("top_speed_kmh")} for a in games if a.get("top_speed_kmh")],
                "borderColor": "rgba(252, 129, 74, 1)",
                "backgroundColor": "rgba(252, 129, 74, 0.15)",
                "borderWidth": 2, "tension": 0.3, "fill": False, "pointRadius": 5,
            })
    else:
        relevant = games if mode == "tournament" else trainings if mode == "training" else activities
        speed_datasets.append({
            "label": "Top Speed (km/h)",
            "data": [{"x": a["date"], "y": a.get("top_speed_kmh")} for a in relevant if a.get("top_speed_kmh")],
            "borderColor": "rgba(99, 179, 237, 1)",
            "backgroundColor": "rgba(99, 179, 237, 0.1)",
            "borderWidth": 2, "tension": 0.3, "fill": False, "pointRadius": 5,
        })

    chart_speed = {
        "title": "Top Speed Trend",
        "chart": {
            "type": "line",
            "data": {"datasets": speed_datasets},
            "options": {
                "responsive": True, "parsing": False,
                "scales": {
                    "x": {"type": "category", "title": {"display": True, "text": "Date"}},
                    "y": {"title": {"display": True, "text": "Top Speed (km/h)"}, "min": 14}
                },
                "plugins": {"legend": {"display": True}}
            }
        }
    }

    # ── Chart 2: Avg HR comparison (training vs game or solo) ──
    relevant_for_hr = activities if mode == "season" else (
        games if mode == "tournament" else trainings if mode == "training" else activities
    )
    hr_colors = [
        "rgba(252, 129, 74, 0.7)" if a.get("intensity") == "High"
        else "rgba(246, 173, 85, 0.7)" if a.get("intensity") == "Moderate"
        else "rgba(99, 179, 237, 0.6)"
        for a in relevant_for_hr
    ]
    chart_hr = {
        "title": "Avg Heart Rate per Activity  (color=intensity)",
        "chart": {
            "type": "bar",
            "data": {
                "labels": [f"{a['date'][:5]} {a['name'][:12]}" for a in relevant_for_hr],
                "datasets": [{
                    "label": "Avg HR (bpm)",
                    "data": metric(relevant_for_hr, "avg_hr"),
                    "backgroundColor": hr_colors,
                    "borderWidth": 0,
                }]
            },
            "options": {
                "responsive": True,
                "scales": {
                    "y": {"title": {"display": True, "text": "Avg HR (bpm)"}, "min": 80}
                },
                "plugins": {"legend": {"display": False}}
            }
        }
    }

    # ── Chart 3: HRV trend ──
    hrv_data = [a for a in activities if a.get("hrv")]
    chart_hrv = None
    if hrv_data:
        chart_hrv = {
            "title": "Morning HRV Trend (day of activity)",
            "chart": {
                "type": "line",
                "data": {
                    "labels": [a["date"] for a in hrv_data],
                    "datasets": [{
                        "label": "HRV (ms)",
                        "data": [a["hrv"] for a in hrv_data],
                        "borderColor": "rgba(104, 211, 145, 1)",
                        "backgroundColor": "rgba(104, 211, 145, 0.1)",
                        "borderWidth": 2.5, "tension": 0.4, "fill": True, "pointRadius": 5,
                    }]
                },
                "options": {
                    "responsive": True,
                    "scales": {"y": {"title": {"display": True, "text": "HRV (ms)"}}},
                    "plugins": {"legend": {"display": False}}
                }
            }
        }

    # ── Chart 4: Duration / distance trend ──
    chart_volume = {
        "title": "Activity Volume (Duration & Distance)",
        "chart": {
            "type": "bar",
            "data": {
                "labels": [a["date"] for a in activities],
                "datasets": [
                    {
                        "label": "Duration (min)",
                        "data": metric(activities, "duration_min"),
                        "backgroundColor": "rgba(183, 148, 246, 0.6)",
                        "borderWidth": 0, "yAxisID": "y",
                    },
                    {
                        "label": "Distance (km)",
                        "data": metric(activities, "distance_km"),
                        "type": "line",
                        "borderColor": "rgba(255,255,255,0.5)",
                        "borderWidth": 2, "tension": 0.3, "pointRadius": 3, "yAxisID": "y1",
                    }
                ]
            },
            "options": {
                "responsive": True,
                "scales": {
                    "y": {"title": {"display": True, "text": "Duration (min)"}, "min": 0},
                    "y1": {
                        "type": "linear", "position": "right",
                        "title": {"display": True, "text": "Distance (km)"},
                        "grid": {"drawOnChartArea": False}, "min": 0
                    }
                },
                "plugins": {"legend": {"display": True}}
            }
        }
    }

    # ── Chart 5: Max HR vs Avg HR with zone reference lines ──
    # Shows whether activities actually reached high-intensity zones
    zone4_threshold = 148  # ~80% of 185 bpm estimated max
    zone5_threshold = 167  # ~90% of 185 bpm estimated max
    chart_intensity = {
        "title": "Intensity Ceiling — Did You Hit High Zones?  (dashed = Zone 4/5 thresholds)",
        "chart": {
            "type": "bar",
            "data": {
                "labels": [f"{a['date'][:5]} {a['name'][:10]}" for a in relevant_for_hr],
                "datasets": [
                    {
                        "label": "Avg HR (bpm)",
                        "data": [a.get("avg_hr") for a in relevant_for_hr],
                        "backgroundColor": "rgba(99, 179, 237, 0.65)",
                        "borderWidth": 0,
                    },
                    {
                        "label": "Max HR (bpm)",
                        "data": [a.get("max_hr") for a in relevant_for_hr],
                        "backgroundColor": "rgba(252, 129, 74, 0.65)",
                        "borderWidth": 0,
                    },
                ]
            },
            "options": {
                "responsive": True,
                "scales": {
                    "y": {
                        "title": {"display": True, "text": "Heart Rate (bpm)"},
                        "min": 80,
                        "suggestedMax": 200,
                    }
                },
                "plugins": {
                    "legend": {"display": True},
                    "annotation": {
                        "annotations": {
                            "zone4line": {
                                "type": "line",
                                "yMin": zone4_threshold, "yMax": zone4_threshold,
                                "borderColor": "rgba(246, 173, 85, 0.7)",
                                "borderWidth": 1.5,
                                "borderDash": [6, 4],
                                "label": {
                                    "content": f"Zone 4 ({zone4_threshold} bpm)",
                                    "display": True, "position": "end",
                                    "color": "rgba(246, 173, 85, 0.9)",
                                    "backgroundColor": "rgba(0,0,0,0)",
                                    "font": {"size": 11},
                                }
                            },
                            "zone5line": {
                                "type": "line",
                                "yMin": zone5_threshold, "yMax": zone5_threshold,
                                "borderColor": "rgba(252, 129, 74, 0.7)",
                                "borderWidth": 1.5,
                                "borderDash": [6, 4],
                                "label": {
                                    "content": f"Zone 5 ({zone5_threshold} bpm)",
                                    "display": True, "position": "end",
                                    "color": "rgba(252, 129, 74, 0.9)",
                                    "backgroundColor": "rgba(0,0,0,0)",
                                    "font": {"size": 11},
                                }
                            },
                        }
                    }
                }
            }
        }
    }

    charts = [c for c in [chart_speed, chart_hr, chart_intensity, chart_hrv, chart_volume] if c]

    # Summary stats
    all_relevant = activities
    stats = {
        "Activities": str(len(all_relevant)),
        "Avg Top Speed": f"{round(sum(a['top_speed_kmh'] for a in all_relevant if a.get('top_speed_kmh')) / max(1, sum(1 for a in all_relevant if a.get('top_speed_kmh'))), 1)} km/h"
            if any(a.get("top_speed_kmh") for a in all_relevant) else "—",
        "Avg Avg HR": f"{round(sum(a['avg_hr'] for a in all_relevant if a.get('avg_hr')) / max(1, sum(1 for a in all_relevant if a.get('avg_hr'))))} bpm"
            if any(a.get("avg_hr") for a in all_relevant) else "—",
        "Total Distance": f"{round(sum(a['distance_km'] for a in all_relevant if a.get('distance_km')), 1)} km",
    }

    # Activity table
    table_rows = ""
    for a in all_relevant:
        table_rows += f"""<tr>
            <td>{a['date']}</td>
            <td>{a['name'][:20]}</td>
            <td>{a.get('category','—')}</td>
            <td>{a['duration_min']} min</td>
            <td>{a['distance_km']} km</td>
            <td>{a.get('top_speed_kmh','—')}</td>
            <td>{a.get('avg_hr','—')}</td>
            <td>{a.get('hrv','—')}</td>
            <td>{a.get('intensity','—')}</td>
        </tr>"""

    payload_json = json.dumps({"stats": stats, "charts": charts})

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation@3.0.1/dist/chartjs-plugin-annotation.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
            color: #e8f4f8; padding: 24px; min-height: 100vh;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        h1 {{ text-align: center; font-size: 1.8rem; margin-bottom: 6px; font-weight: 700; }}
        .subtitle {{ text-align: center; opacity: 0.5; font-size: 0.82rem; margin-bottom: 32px; }}
        .stats-grid {{
            display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 14px; margin-bottom: 32px;
        }}
        .stat-card {{
            background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.12);
            border-radius: 12px; padding: 18px; text-align: center;
        }}
        .stat-value {{ font-size: 1.8rem; font-weight: 800; margin: 6px 0 3px; }}
        .stat-label {{ font-size: 0.75rem; opacity: 0.6; text-transform: uppercase; letter-spacing: 1px; }}
        .charts-grid {{
            display: grid; grid-template-columns: repeat(auto-fit, minmax(540px, 1fr));
            gap: 24px; margin-bottom: 32px;
        }}
        .chart-container {{
            background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
            border-radius: 14px; padding: 26px;
        }}
        .chart-title {{ font-size: 1rem; font-weight: 600; margin-bottom: 16px; text-align: center; opacity: 0.9; }}
        canvas {{ max-height: 360px; }}
        .table-section {{
            background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
            border-radius: 14px; padding: 24px; margin-bottom: 28px;
        }}
        .section-title {{ font-size: 0.95rem; font-weight: 600; margin-bottom: 16px; opacity: 0.9; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 0.84rem; }}
        th, td {{ padding: 9px 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.06); }}
        th {{ opacity: 0.5; font-weight: 600; text-transform: uppercase; font-size: 0.72rem; letter-spacing: 0.8px; }}
        tr:hover td {{ background: rgba(255,255,255,0.03); }}
        .footer {{ text-align: center; opacity: 0.3; font-size: 0.78rem; margin-top: 20px; }}
    </style>
</head>
<body>
<div class="container">
    <h1>{title}</h1>
    <div class="subtitle">Generated {generated}</div>
    <div class="stats-grid" id="stats"></div>
    <div class="charts-grid" id="charts"></div>
    <div class="table-section">
        <div class="section-title">All Activities</div>
        <table>
            <thead><tr>
                <th>Date</th><th>Name</th><th>Category</th><th>Duration</th>
                <th>Distance</th><th>Top Speed</th><th>Avg HR</th><th>HRV</th><th>Intensity</th>
            </tr></thead>
            <tbody>{table_rows}</tbody>
        </table>
    </div>
    <div class="footer">Garmin Frisbee Analysis · Data from Garmin Connect (unofficial API)</div>
</div>
<script>
Chart.defaults.color = 'rgba(232,244,248,0.75)';
Chart.defaults.borderColor = 'rgba(255,255,255,0.08)';
const payload = {payload_json};
const statsEl = document.getElementById('stats');
for (const [label, value] of Object.entries(payload.stats)) {{
    const card = document.createElement('div');
    card.className = 'stat-card';
    card.innerHTML = `<div class="stat-label">${{label}}</div><div class="stat-value">${{value}}</div>`;
    statsEl.appendChild(card);
}}
const chartsEl = document.getElementById('charts');
for (const cfg of payload.charts) {{
    const wrap = document.createElement('div');
    wrap.className = 'chart-container';
    const titleEl = document.createElement('div');
    titleEl.className = 'chart-title';
    titleEl.textContent = cfg.title;
    wrap.appendChild(titleEl);
    const canvas = document.createElement('canvas');
    wrap.appendChild(canvas);
    chartsEl.appendChild(wrap);
    new Chart(canvas, cfg.chart);
}}
</script>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Compare frisbee activities over time")
    parser.add_argument("--mode", choices=["training", "tournament", "cross", "season"],
                        default="season", help="Comparison mode")
    parser.add_argument("--days", type=int, default=90, help="Look-back period in days")
    parser.add_argument("--output", help="Output HTML file (default: opens in browser)")
    parser.add_argument("--json", action="store_true", help="Output JSON summary")

    args = parser.parse_args()

    client = get_client()
    if not client:
        print("❌ Not authenticated. Run: python3 scripts/garmin_auth.py login", file=sys.stderr)
        sys.exit(1)

    print(f"\n⚡ Frisbee Comparison — mode: {args.mode}, last {args.days} days", file=sys.stderr)

    print("  [1/3] Loading activities...", file=sys.stderr)
    activities = load_activities_summary(client, days=args.days)
    print(f"        Found {len(activities)} activities", file=sys.stderr)

    # Classify each activity
    for a in activities:
        a["category"] = classify_activity(a)

    # Filter by mode
    if args.mode == "training":
        activities = [a for a in activities if a["category"] == "training"]
    elif args.mode == "tournament":
        activities = [a for a in activities if a["category"] == "game"]
    # cross and season: keep all

    if not activities:
        print("⚠️  No matching activities found. Check activity names or expand --days.",
              file=sys.stderr)
        print("    Tip: Activities are classified by name keywords.", file=sys.stderr)
        print("    Game keywords: game, match, tournament, vs, finals", file=sys.stderr)
        print("    Training keywords: practice, training, train, drill, scrimmage", file=sys.stderr)
        sys.exit(0)

    print(f"  [2/3] Loading HRV & heart rate data...", file=sys.stderr)
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")
    hrv_result = fetch_hrv(client, start=start_date, end=end_date)
    hrv_by_date = {h["date"]: h for h in hrv_result.get("hrv", [])}
    hr_result = fetch_heart_rate(client, start=start_date, end=end_date)
    rhr_by_date = {h["date"]: h for h in hr_result.get("heart_rate", [])}

    activities = build_comparison_data(activities, hrv_by_date, rhr_by_date)

    print(f"  [3/3] Generating dashboard...", file=sys.stderr)

    if args.json:
        print(json.dumps(activities, indent=2, default=str))
        return

    html = generate_comparison_html(activities, args.mode, args.days)

    if args.output:
        out_path = Path(args.output).expanduser()
        out_path.write_text(html, encoding="utf-8")
        print(f"✅ Saved to: {out_path}", file=sys.stderr)
        webbrowser.open(f"file://{out_path.resolve()}")
    else:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=f"_compare_{args.mode}.html", delete=False, encoding="utf-8"
        ) as f:
            f.write(html)
            tmp = f.name
        print(f"✅ Opening in browser... ({tmp})", file=sys.stderr)
        webbrowser.open(f"file://{tmp}")


if __name__ == "__main__":
    main()
