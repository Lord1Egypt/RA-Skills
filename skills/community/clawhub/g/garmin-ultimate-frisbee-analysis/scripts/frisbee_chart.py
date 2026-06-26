#!/usr/bin/env python3
"""
Frisbee tournament dashboard - interactive HTML visualizations.
Uses Chart.js. Called by frisbee_tournament.py.
"""

import json
import sys
import webbrowser
import tempfile
from datetime import datetime
from pathlib import Path


# Color palette for games (up to 8 games)
GAME_COLORS = [
    ("rgba(99, 179, 237, 1)",  "rgba(99, 179, 237, 0.15)"),   # Blue
    ("rgba(252, 129, 74, 1)",  "rgba(252, 129, 74, 0.15)"),   # Orange
    ("rgba(104, 211, 145, 1)", "rgba(104, 211, 145, 0.15)"),  # Green
    ("rgba(246, 173, 85, 1)",  "rgba(246, 173, 85, 0.15)"),   # Yellow
    ("rgba(183, 148, 246, 1)", "rgba(183, 148, 246, 0.15)"),  # Purple
    ("rgba(252, 129, 129, 1)", "rgba(252, 129, 129, 0.15)"),  # Red
    ("rgba(96, 219, 219, 1)",  "rgba(96, 219, 219, 0.15)"),   # Cyan
    ("rgba(255, 192, 203, 1)", "rgba(255, 192, 203, 0.15)"),  # Pink
]


def _game_label(activity, index):
    name = (activity.get("activity_name") or "").strip()
    date = activity.get("date", "")
    return f"Game {index + 1}: {name}" if name and name.lower() != "activity" else f"Game {index + 1} ({date})"


def _build_summary_stats(data):
    activities = data.get("activities", [])
    recovery = data.get("recovery_nights", [])
    fatigue = data.get("fatigue_timeline", [])

    total_games = len(activities)
    total_minutes = sum((a.get("duration_seconds") or 0) for a in activities) // 60

    # Average pre-game Body Battery: highest value on each game day (morning peak)
    game_dates = set(a["date"] for a in activities if a.get("date"))
    pre_game_bb_values = [
        f["body_battery_highest"]
        for f in fatigue
        if f["date"] in game_dates and f.get("body_battery_highest") is not None
    ]
    avg_pre_bb = round(sum(pre_game_bb_values) / len(pre_game_bb_values)) if pre_game_bb_values else "—"

    sleep_scores = [r["sleep_score"] for r in recovery if r.get("sleep_score")]
    avg_sleep = round(sum(sleep_scores) / len(sleep_scores)) if sleep_scores else "—"

    return {
        "Total Games": str(total_games),
        "Total Play Time": f"{total_minutes} min",
        "Avg Pre-Game Battery": f"{avg_pre_bb}/100",
        "Avg Sleep Score": f"{avg_sleep}/100" if isinstance(avg_sleep, int) else "—",
    }


def _build_fatigue_chart(data):
    fatigue = data.get("fatigue_timeline", [])

    labels = []
    highest_vals = []
    lowest_vals = []
    point_styles = []

    for f in fatigue:
        label = f["date"] + (" (Pre)" if f.get("is_baseline") else "")
        labels.append(label)
        highest_vals.append(f.get("body_battery_highest"))
        lowest_vals.append(f.get("body_battery_lowest"))
        point_styles.append("rect" if f.get("is_baseline") else "circle")

    return {
        "title": "Body Battery — Fatigue Timeline",
        "chart": {
            "type": "line",
            "data": {
                "labels": labels,
                "datasets": [
                    {
                        "label": "Highest Body Battery",
                        "data": highest_vals,
                        "borderColor": "rgba(104, 211, 145, 1)",
                        "backgroundColor": "rgba(104, 211, 145, 0.1)",
                        "borderWidth": 3,
                        "tension": 0.3,
                        "fill": True,
                        "pointRadius": 6,
                        "pointHoverRadius": 8,
                    },
                    {
                        "label": "Lowest Body Battery",
                        "data": lowest_vals,
                        "borderColor": "rgba(252, 129, 74, 1)",
                        "backgroundColor": "rgba(252, 129, 74, 0.05)",
                        "borderWidth": 2,
                        "tension": 0.3,
                        "borderDash": [5, 5],
                        "pointRadius": 4,
                    }
                ]
            },
            "options": {
                "responsive": True,
                "scales": {
                    "y": {
                        "min": 0,
                        "max": 100,
                        "title": {"display": True, "text": "Body Battery (0–100)"}
                    }
                },
                "plugins": {
                    "legend": {"display": True},
                    "annotation": {}
                }
            }
        }
    }


def _build_game_hr_chart(data):
    activities = data.get("activities", [])

    labels = [_game_label(a, i) for i, a in enumerate(activities)]
    avg_hrs = [a.get("avg_hr") for a in activities]
    max_hrs = [a.get("max_hr") for a in activities]

    return {
        "title": "Per-Game Heart Rate Intensity",
        "chart": {
            "type": "bar",
            "data": {
                "labels": labels,
                "datasets": [
                    {
                        "label": "Avg HR (bpm)",
                        "data": avg_hrs,
                        "backgroundColor": "rgba(99, 179, 237, 0.7)",
                        "borderColor": "rgba(99, 179, 237, 1)",
                        "borderWidth": 2,
                        "yAxisID": "y",
                    },
                    {
                        "label": "Max HR (bpm)",
                        "data": max_hrs,
                        "backgroundColor": "rgba(252, 129, 74, 0.7)",
                        "borderColor": "rgba(252, 129, 74, 1)",
                        "borderWidth": 2,
                        "yAxisID": "y",
                    }
                ]
            },
            "options": {
                "responsive": True,
                "scales": {
                    "y": {
                        "title": {"display": True, "text": "Heart Rate (bpm)"},
                        "min": 60
                    }
                },
                "plugins": {"legend": {"display": True}}
            }
        }
    }


def _build_hrr_chart(data):
    activities = data.get("activities", [])

    datasets = []
    has_data = False
    for i, activity in enumerate(activities):
        hrr = activity.get("hrr", [])
        if not hrr:
            continue
        has_data = True
        color_border, color_bg = GAME_COLORS[i % len(GAME_COLORS)]
        # Compute HRR-1 and HRR-2 for the legend label
        hr_at_0 = hrr[0]["hr"] if hrr else None
        hr_at_1 = next((p["hr"] for p in hrr if p["minutes"] >= 1), None)
        hr_at_2 = next((p["hr"] for p in hrr if p["minutes"] >= 2), None)
        hrr1 = (hr_at_0 - hr_at_1) if (hr_at_0 and hr_at_1) else None
        hrr2 = (hr_at_0 - hr_at_2) if (hr_at_0 and hr_at_2) else None
        suffix = ""
        if hrr1 is not None:
            suffix += f" ▼{hrr1}@1min"
        if hrr2 is not None:
            suffix += f" ▼{hrr2}@2min"
        label = _game_label(activity, i) + suffix
        datasets.append({
            "label": label,
            "data": [{"x": p["minutes"], "y": p["hr"]} for p in hrr],
            "borderColor": color_border,
            "backgroundColor": color_bg,
            "borderWidth": 2,
            "tension": 0.3,
            "fill": False,
            "pointRadius": 2,
        })

    if not has_data:
        return None

    return {
        "title": "Heart Rate Recovery (30 min post-game)",
        "chart": {
            "type": "line",
            "data": {"datasets": datasets},
            "options": {
                "responsive": True,
                "parsing": False,
                "scales": {
                    "x": {
                        "type": "linear",
                        "title": {"display": True, "text": "Minutes After Game End"},
                        "min": 0,
                        "max": 30,
                    },
                    "y": {
                        "title": {"display": True, "text": "Heart Rate (bpm)"},
                    }
                },
                "plugins": {
                    "legend": {"display": True},
                    "tooltip": {
                        "callbacks": {}
                    }
                }
            }
        }
    }


def _build_recovery_chart(data):
    recovery = data.get("recovery_nights", [])

    dates = [r["date"] for r in recovery]
    sleep_hours = [round(r["sleep_hours"], 1) if r.get("sleep_hours") else None for r in recovery]
    hrv_vals = [r.get("hrv") for r in recovery]

    return {
        "title": "Overnight Recovery (Sleep + HRV)",
        "chart": {
            "type": "bar",
            "data": {
                "labels": dates,
                "datasets": [
                    {
                        "label": "Sleep Hours",
                        "data": sleep_hours,
                        "backgroundColor": "rgba(183, 148, 246, 0.6)",
                        "borderColor": "rgba(183, 148, 246, 1)",
                        "borderWidth": 2,
                        "yAxisID": "y",
                    },
                    {
                        "label": "HRV (ms)",
                        "data": hrv_vals,
                        "type": "line",
                        "borderColor": "rgba(104, 211, 145, 1)",
                        "backgroundColor": "rgba(104, 211, 145, 0.1)",
                        "borderWidth": 3,
                        "tension": 0.3,
                        "yAxisID": "y1",
                        "pointRadius": 6,
                    }
                ]
            },
            "options": {
                "responsive": True,
                "interaction": {"mode": "index", "intersect": False},
                "scales": {
                    "y": {
                        "type": "linear",
                        "position": "left",
                        "title": {"display": True, "text": "Sleep (hours)"},
                        "min": 0,
                        "max": 12,
                    },
                    "y1": {
                        "type": "linear",
                        "position": "right",
                        "title": {"display": True, "text": "HRV (ms)"},
                        "grid": {"drawOnChartArea": False},
                    }
                },
                "plugins": {"legend": {"display": True}}
            }
        }
    }


def _build_activity_table_html(activities):
    if not activities:
        return "<p style='text-align:center;opacity:0.6'>No activities found in this date range.</p>"

    rows = ""
    for i, a in enumerate(activities, 1):
        dur = int((a.get("duration_seconds") or 0) // 60)
        hrr_count = len(a.get("hrr", []))
        hrr_note = f"✓ {hrr_count} pts" if hrr_count else "—"
        rows += f"""
        <tr>
            <td>Game {i}</td>
            <td>{a.get('date', '—')}</td>
            <td>{a.get('activity_name', '—')}</td>
            <td>{a.get('activity_type', '—')}</td>
            <td>{dur} min</td>
            <td>{a.get('avg_hr') or '—'}</td>
            <td>{a.get('max_hr') or '—'}</td>
            <td>{a.get('calories') or '—'}</td>
            <td>{hrr_note}</td>
        </tr>"""

    return f"""
    <table class="activity-table">
        <thead>
            <tr>
                <th>#</th><th>Date</th><th>Name</th><th>Type</th>
                <th>Duration</th><th>Avg HR</th><th>Max HR</th><th>Calories</th><th>HRR Data</th>
            </tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>"""


def generate_tournament_html(data):
    name = data.get("name", "Tournament")
    start = data.get("start_date", "")
    end = data.get("end_date", "")
    title = f"{name}  |  {start} → {end}"
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")

    stats = _build_summary_stats(data)
    fatigue_chart = _build_fatigue_chart(data)
    game_hr_chart = _build_game_hr_chart(data)
    hrr_chart = _build_hrr_chart(data)
    recovery_chart = _build_recovery_chart(data)
    activity_table = _build_activity_table_html(data.get("activities", []))

    charts = [fatigue_chart, game_hr_chart, recovery_chart]
    if hrr_chart:
        charts.insert(2, hrr_chart)

    charts_json = json.dumps({"stats": stats, "charts": charts})

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
            color: #e8f4f8;
            padding: 24px;
            min-height: 100vh;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        h1 {{
            text-align: center;
            font-size: 2rem;
            margin-bottom: 6px;
            font-weight: 700;
            letter-spacing: -0.5px;
        }}
        .subtitle {{
            text-align: center;
            opacity: 0.55;
            font-size: 0.85rem;
            margin-bottom: 36px;
        }}
        /* Summary cards */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
            margin-bottom: 36px;
        }}
        .stat-card {{
            background: rgba(255,255,255,0.07);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 14px;
            padding: 20px;
            text-align: center;
        }}
        .stat-value {{ font-size: 2.2rem; font-weight: 800; margin: 8px 0 4px; }}
        .stat-label {{ font-size: 0.78rem; opacity: 0.65; text-transform: uppercase; letter-spacing: 1px; }}
        /* Charts */
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(560px, 1fr));
            gap: 28px;
            margin-bottom: 36px;
        }}
        .chart-container {{
            background: rgba(255,255,255,0.04);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 28px;
        }}
        .chart-title {{
            font-size: 1.05rem;
            font-weight: 600;
            margin-bottom: 18px;
            text-align: center;
            opacity: 0.9;
        }}
        canvas {{ max-height: 380px; }}
        /* Activity table */
        .table-section {{
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 28px;
            margin-bottom: 36px;
        }}
        .section-title {{
            font-size: 1.05rem;
            font-weight: 600;
            margin-bottom: 18px;
            opacity: 0.9;
        }}
        .activity-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.88rem;
        }}
        .activity-table th, .activity-table td {{
            padding: 10px 14px;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.07);
        }}
        .activity-table th {{
            opacity: 0.55;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.8px;
        }}
        .activity-table tr:hover td {{ background: rgba(255,255,255,0.04); }}
        .footer {{
            text-align: center;
            opacity: 0.35;
            font-size: 0.8rem;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
<div class="container">
    <h1>🥏 {name}</h1>
    <div class="subtitle">{start} → {end} &nbsp;·&nbsp; Generated {generated}</div>

    <div class="stats-grid" id="stats"></div>
    <div class="charts-grid" id="charts"></div>

    <div class="table-section">
        <div class="section-title">Activities in Tournament</div>
        {activity_table}
    </div>

    <div class="footer">Garmin Frisbee Analysis · Data from Garmin Connect (unofficial API)</div>
</div>

<script>
Chart.defaults.color = 'rgba(232, 244, 248, 0.75)';
Chart.defaults.borderColor = 'rgba(255,255,255,0.08)';

const payload = {charts_json};

// Render summary stats
const statsEl = document.getElementById('stats');
for (const [label, value] of Object.entries(payload.stats)) {{
    const card = document.createElement('div');
    card.className = 'stat-card';
    card.innerHTML = `<div class="stat-label">${{label}}</div><div class="stat-value">${{value}}</div>`;
    statsEl.appendChild(card);
}}

// Render charts
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


def create_tournament_dashboard(data, output=None):
    html = generate_tournament_html(data)
    name = data.get("name", "tournament").lower().replace(" ", "_")

    if output:
        out_path = Path(output).expanduser()
        out_path.write_text(html, encoding="utf-8")
        print(f"✅ Dashboard saved to: {out_path}", file=sys.stderr)
        webbrowser.open(f"file://{out_path.resolve()}")
    else:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=f"_{name}.html", delete=False, encoding="utf-8"
        ) as f:
            f.write(html)
            tmp = f.name
        print(f"✅ Opening dashboard in browser... ({tmp})", file=sys.stderr)
        webbrowser.open(f"file://{tmp}")


# ──────────────────────────────────────────────
# Activity Dashboard (single game/training session)
# ──────────────────────────────────────────────

def _activity_stats_cards(analysis):
    s = analysis.get("summary", {})
    dur = int((s.get("duration_seconds") or 0) // 60)
    dist = s.get("total_distance_m")
    hi_dist = s.get("high_intensity_distance_m")
    top_spd = s.get("top_speed_kmh")
    fi = analysis.get("sprint_fatigue_index")
    if fi is not None:
        if fi >= 0.95:
            fi_label = f"{fi:.2f} Stable"
        elif fi >= 0.85:
            fi_label = f"{fi:.2f} Mild↓"
        else:
            fi_label = f"{fi:.2f} Fatigued"
    else:
        fi_label = "—"
    gct = s.get("avg_ground_contact_ms")
    gct_trend = s.get("gct_trend_ratio")
    if gct:
        if gct_trend is not None:
            gct_label = f"{gct} ms ({'↑ Fatigue' if gct_trend > 1.05 else '→ Stable'})"
        else:
            gct_label = f"{gct} ms"
    else:
        gct_label = "—"

    return {
        "Duration": f"{dur} min",
        "Total Distance": f"{round(dist/1000,2)} km" if dist else "—",
        "Sprint Count": str(analysis.get("sprint_count", 0)),
        "Top Speed": f"{top_spd} km/h" if top_spd else "—",
        "Sprint Fatigue": fi_label,
        "Hi-Intensity Dist": f"{round(hi_dist)} m" if hi_dist else "—",
        "Avg Ground Contact": gct_label,
    }


def _activity_speed_chart(analysis):
    timeline = analysis.get("speed_timeline", [])
    sprint_events = analysis.get("sprint_events", [])

    x = [p["minutes"] for p in timeline]
    speed = [p["speed_kmh"] for p in timeline]
    hr = [p.get("hr") for p in timeline]

    # Sprint highlight bands as Chart.js annotation boxes (via chartjs-plugin-annotation)
    # We'll inject them as vertical rectangle data via a separate bar dataset trick
    # Using a simple approach: shade via extra dataset with fill between threshold
    annotations = []
    for ev in sprint_events:
        annotations.append({
            "type": "box",
            "xMin": ev["start_min"],
            "xMax": round(ev["start_min"] + ev["duration_min"], 3),
            "backgroundColor": "rgba(252, 129, 74, 0.15)",
            "borderWidth": 0,
        })

    datasets = [
        {
            "label": "Speed (km/h)",
            "data": [{"x": xi, "y": yi} for xi, yi in zip(x, speed)],
            "borderColor": "rgba(99, 179, 237, 1)",
            "backgroundColor": "rgba(99, 179, 237, 0.05)",
            "borderWidth": 2,
            "tension": 0.2,
            "fill": True,
            "pointRadius": 0,
            "yAxisID": "y",
        }
    ]
    if any(v is not None for v in hr):
        datasets.append({
            "label": "Heart Rate (bpm)",
            "data": [{"x": xi, "y": yi} for xi, yi in zip(x, hr) if yi is not None],
            "borderColor": "rgba(252, 129, 74, 0.8)",
            "borderWidth": 1.5,
            "tension": 0.2,
            "fill": False,
            "pointRadius": 0,
            "yAxisID": "y1",
        })

    return {
        "title": "Speed Timeline  (orange bands = sprints)",
        "annotations": annotations,
        "chart": {
            "type": "line",
            "data": {"datasets": datasets},
            "options": {
                "responsive": True,
                "parsing": False,
                "animation": False,
                "scales": {
                    "x": {
                        "type": "linear",
                        "title": {"display": True, "text": "Time (min)"},
                    },
                    "y": {
                        "title": {"display": True, "text": "Speed (km/h)"},
                        "min": 0,
                    },
                    "y1": {
                        "type": "linear",
                        "position": "right",
                        "title": {"display": True, "text": "HR (bpm)"},
                        "grid": {"drawOnChartArea": False},
                        "min": 60,
                    }
                },
                "plugins": {"legend": {"display": True}}
            }
        }
    }


def _activity_sprint_fatigue_chart(analysis):
    sprints = analysis.get("sprints", [])
    if not sprints:
        return None

    labels = [f"#{s['index']}" for s in sprints]
    peaks = [s.get("peak_speed_kmh") for s in sprints]
    durations = [s.get("duration_s") for s in sprints]

    # Color: first 3 green, last 3 red, rest blue
    colors = []
    n = len(sprints)
    for i in range(n):
        if i < 3:
            colors.append("rgba(104, 211, 145, 0.8)")
        elif i >= n - 3:
            colors.append("rgba(252, 129, 74, 0.8)")
        else:
            colors.append("rgba(99, 179, 237, 0.7)")

    return {
        "title": "Sprint Peak Speed  (green=first, orange=last)",
        "chart": {
            "type": "bar",
            "data": {
                "labels": labels,
                "datasets": [
                    {
                        "label": "Peak Speed (km/h)",
                        "data": peaks,
                        "backgroundColor": colors,
                        "borderWidth": 0,
                        "yAxisID": "y",
                    },
                    {
                        "label": "Duration (s)",
                        "data": durations,
                        "type": "line",
                        "borderColor": "rgba(183, 148, 246, 0.8)",
                        "borderWidth": 2,
                        "pointRadius": 3,
                        "tension": 0.3,
                        "yAxisID": "y1",
                    }
                ]
            },
            "options": {
                "responsive": True,
                "scales": {
                    "y": {
                        "title": {"display": True, "text": "Peak Speed (km/h)"},
                        "min": 14,
                    },
                    "y1": {
                        "type": "linear",
                        "position": "right",
                        "title": {"display": True, "text": "Duration (s)"},
                        "grid": {"drawOnChartArea": False},
                        "min": 0,
                    }
                },
                "plugins": {"legend": {"display": True}}
            }
        }
    }


def _activity_hr_zones_chart(analysis):
    zones = analysis.get("hr_zones", [])
    if not zones:
        return None

    labels = [f"{z['name']} ({z['label']})" for z in zones]
    percents = [z["percent"] for z in zones]
    minutes = [round(z["seconds"] / 60, 1) for z in zones]
    colors = [z["color"] for z in zones]

    return {
        "title": "Heart Rate Zone Distribution",
        "chart": {
            "type": "bar",
            "data": {
                "labels": labels,
                "datasets": [
                    {
                        "label": "Time (%)",
                        "data": percents,
                        "backgroundColor": colors,
                        "borderWidth": 0,
                        "yAxisID": "y",
                    },
                    {
                        "label": "Time (min)",
                        "data": minutes,
                        "type": "line",
                        "borderColor": "rgba(255,255,255,0.5)",
                        "borderWidth": 2,
                        "pointRadius": 4,
                        "yAxisID": "y1",
                    }
                ]
            },
            "options": {
                "responsive": True,
                "scales": {
                    "y": {
                        "title": {"display": True, "text": "Percentage (%)"},
                        "min": 0,
                        "max": 100,
                    },
                    "y1": {
                        "type": "linear",
                        "position": "right",
                        "title": {"display": True, "text": "Minutes"},
                        "grid": {"drawOnChartArea": False},
                        "min": 0,
                    }
                },
                "plugins": {"legend": {"display": True}}
            }
        }
    }


def _activity_gct_chart(analysis):
    timeline = analysis.get("gct_timeline", [])
    if not timeline:
        return None
    s = analysis.get("summary", {})
    trend = s.get("gct_trend_ratio")
    trend_note = ""
    if trend is not None:
        trend_note = f"  — 2nd half / 1st half: {trend:.2f} ({'↑ fatigue signal' if trend > 1.05 else '→ stable'})"

    return {
        "title": f"Ground Contact Time over Activity{trend_note}",
        "chart": {
            "type": "line",
            "data": {
                "datasets": [{
                    "label": "Ground Contact Time (ms)",
                    "data": [{"x": p["minutes"], "y": p["gct_ms"]} for p in timeline],
                    "borderColor": "rgba(183, 148, 246, 0.9)",
                    "backgroundColor": "rgba(183, 148, 246, 0.08)",
                    "borderWidth": 1.5,
                    "tension": 0.2,
                    "fill": True,
                    "pointRadius": 0,
                }]
            },
            "options": {
                "responsive": True,
                "parsing": False,
                "animation": False,
                "scales": {
                    "x": {"type": "linear", "title": {"display": True, "text": "Time (min)"}},
                    "y": {"title": {"display": True, "text": "GCT (ms)"}, "min": 0},
                },
                "plugins": {"legend": {"display": False}}
            }
        }
    }


def generate_activity_html(analysis):
    activity_id = analysis.get("activity_id", "")
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")
    title = f"Activity {activity_id} — Frisbee Analysis"

    stats = _activity_stats_cards(analysis)
    speed_cfg = _activity_speed_chart(analysis)
    sprint_cfg = _activity_sprint_fatigue_chart(analysis)
    zone_cfg = _activity_hr_zones_chart(analysis)
    gct_cfg = _activity_gct_chart(analysis)

    # Annotations for speed chart (sprint highlight bands)
    annotations = speed_cfg.pop("annotations", [])
    annotations_json = json.dumps(annotations)

    charts = [c for c in [speed_cfg, sprint_cfg, zone_cfg, gct_cfg] if c]
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
            color: #e8f4f8;
            padding: 24px;
            min-height: 100vh;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        h1 {{ text-align: center; font-size: 1.8rem; margin-bottom: 6px; font-weight: 700; }}
        .subtitle {{ text-align: center; opacity: 0.5; font-size: 0.82rem; margin-bottom: 32px; }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 14px; margin-bottom: 32px;
        }}
        .stat-card {{
            background: rgba(255,255,255,0.07);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 12px; padding: 18px; text-align: center;
        }}
        .stat-value {{ font-size: 1.9rem; font-weight: 800; margin: 6px 0 3px; }}
        .stat-label {{ font-size: 0.75rem; opacity: 0.6; text-transform: uppercase; letter-spacing: 1px; }}
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(540px, 1fr));
            gap: 24px;
        }}
        .chart-container {{
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 14px; padding: 26px;
        }}
        .chart-title {{ font-size: 1rem; font-weight: 600; margin-bottom: 16px; text-align: center; opacity: 0.9; }}
        canvas {{ max-height: 360px; }}
        .footer {{ text-align: center; opacity: 0.3; font-size: 0.78rem; margin-top: 28px; }}
    </style>
</head>
<body>
<div class="container">
    <h1>🥏 Activity Analysis</h1>
    <div class="subtitle">ID: {activity_id} &nbsp;·&nbsp; Generated {generated}</div>
    <div class="stats-grid" id="stats"></div>
    <div class="charts-grid" id="charts"></div>
    <div class="footer">Garmin Frisbee Analysis · Data from Garmin Connect (unofficial API)</div>
</div>
<script>
Chart.defaults.color = 'rgba(232,244,248,0.75)';
Chart.defaults.borderColor = 'rgba(255,255,255,0.08)';

const payload = {payload_json};
const annotations = {annotations_json};

// Stats
const statsEl = document.getElementById('stats');
for (const [label, value] of Object.entries(payload.stats)) {{
    const card = document.createElement('div');
    card.className = 'stat-card';
    card.innerHTML = `<div class="stat-label">${{label}}</div><div class="stat-value">${{value}}</div>`;
    statsEl.appendChild(card);
}}

// Charts
const chartsEl = document.getElementById('charts');
payload.charts.forEach((cfg, i) => {{
    const wrap = document.createElement('div');
    wrap.className = 'chart-container';
    const titleEl = document.createElement('div');
    titleEl.className = 'chart-title';
    titleEl.textContent = cfg.title;
    wrap.appendChild(titleEl);
    const canvas = document.createElement('canvas');
    wrap.appendChild(canvas);
    chartsEl.appendChild(wrap);

    // Inject sprint highlight annotations into first chart (speed timeline)
    if (i === 0 && annotations.length > 0) {{
        cfg.chart.options.plugins = cfg.chart.options.plugins || {{}};
        cfg.chart.options.plugins.annotation = {{ annotations }};
    }}

    new Chart(canvas, cfg.chart);
}});
</script>
</body>
</html>"""


def create_activity_dashboard(analysis, output=None):
    html = generate_activity_html(analysis)
    suffix = f"_activity_{analysis.get('activity_id', 'unknown')}.html"

    if output:
        out_path = Path(output).expanduser()
        out_path.write_text(html, encoding="utf-8")
        print(f"✅ Dashboard saved to: {out_path}", file=sys.stderr)
        webbrowser.open(f"file://{out_path.resolve()}")
    else:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=suffix, delete=False, encoding="utf-8"
        ) as f:
            f.write(html)
            tmp = f.name
        print(f"✅ Opening in browser... ({tmp})", file=sys.stderr)
        webbrowser.open(f"file://{tmp}")
