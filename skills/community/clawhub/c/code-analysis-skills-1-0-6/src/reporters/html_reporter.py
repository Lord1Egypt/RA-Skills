"""
HTML Reporter - Generates comprehensive analysis reports in HTML format.

Uses Jinja2 templates for rich, styled HTML output with:
  - Developer evaluations (score, grade, strengths, weaknesses, suggestions)
  - Slacking index visualization
  - Score bar charts
  - Comparison tables and leaderboards
"""

from typing import Dict

from jinja2 import Template

from src.reporters.base_reporter import BaseReporter

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Analysis Report</title>
    <style>
        :root {
            --primary: #4f46e5;
            --primary-light: #818cf8;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text: #1e293b;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --success: #22c55e;
            --warning: #f59e0b;
            --danger: #ef4444;
            --info: #3b82f6;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            padding: 2rem;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 {
            font-size: 2rem;
            color: var(--primary);
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid var(--primary);
        }
        h2 {
            font-size: 1.5rem;
            margin: 2rem 0 1rem;
            padding: 0.5rem 1rem;
            background: var(--primary);
            color: white;
            border-radius: 8px;
        }
        h3 {
            font-size: 1.2rem;
            color: var(--primary);
            margin: 1.5rem 0 0.5rem;
        }
        h4 {
            font-size: 1rem;
            color: var(--text-muted);
            margin: 1rem 0 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 0.5rem 0 1rem;
        }
        th, td {
            padding: 0.6rem 1rem;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }
        th {
            background: var(--bg);
            font-weight: 600;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
        }
        tr:hover { background: #f1f5f9; }
        .metric-value { font-weight: 600; color: var(--primary); }
        .comparison-table th { background: var(--primary); color: white; }
        .comparison-table tr:nth-child(even) { background: #f8fafc; }
        .badge {
            display: inline-block;
            padding: 0.15rem 0.5rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .badge-good { background: #dcfce7; color: #166534; }
        .badge-warn { background: #fef3c7; color: #92400e; }
        .badge-bad { background: #fee2e2; color: #991b1b; }
        .badge-info { background: #dbeafe; color: #1e40af; }

        /* Evaluation styles */
        .eval-header {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1rem;
            flex-wrap: wrap;
        }
        .score-circle {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            font-weight: 700;
            color: white;
            flex-shrink: 0;
        }
        .score-s { background: linear-gradient(135deg, #f59e0b, #ef4444); }
        .score-a { background: linear-gradient(135deg, #22c55e, #16a34a); }
        .score-b { background: linear-gradient(135deg, #3b82f6, #2563eb); }
        .score-c { background: linear-gradient(135deg, #f59e0b, #d97706); }
        .score-d { background: linear-gradient(135deg, #f97316, #ea580c); }
        .score-e { background: linear-gradient(135deg, #ef4444, #dc2626); }
        .score-f { background: linear-gradient(135deg, #991b1b, #7f1d1d); }
        .grade-label {
            font-size: 2rem;
            font-weight: 800;
            margin-left: 0.5rem;
        }
        .verdict {
            font-style: italic;
            color: var(--text-muted);
            margin: 0.5rem 0 1rem;
            padding: 0.5rem 1rem;
            border-left: 4px solid var(--primary);
            background: #f1f5f9;
            border-radius: 0 8px 8px 0;
        }
        .score-bar-container {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .score-bar {
            height: 12px;
            border-radius: 6px;
            background: #e2e8f0;
            flex: 1;
            max-width: 200px;
            overflow: hidden;
        }
        .score-bar-fill {
            height: 100%;
            border-radius: 6px;
            transition: width 0.3s ease;
        }
        .fill-high { background: linear-gradient(90deg, #22c55e, #16a34a); }
        .fill-mid { background: linear-gradient(90deg, #f59e0b, #d97706); }
        .fill-low { background: linear-gradient(90deg, #ef4444, #dc2626); }

        .strength-item { color: #166534; margin: 0.3rem 0; }
        .weakness-item { color: #991b1b; margin: 0.3rem 0; }
        .suggestion-item { color: #1e40af; margin: 0.3rem 0; }

        .strength-item::before { content: "✅ "; }
        .weakness-item::before { content: "❌ "; }
        .suggestion-item::before { content: "💡 "; }

        /* Slacking Index */
        .slacking-meter {
            width: 100%;
            height: 30px;
            background: linear-gradient(90deg, #22c55e, #f59e0b, #ef4444);
            border-radius: 15px;
            position: relative;
            margin: 1rem 0;
        }
        .slacking-indicator {
            position: absolute;
            top: -5px;
            width: 20px;
            height: 40px;
            background: white;
            border: 3px solid #1e293b;
            border-radius: 4px;
            transform: translateX(-50%);
        }
        .slacking-label {
            font-size: 1.2rem;
            font-weight: 700;
            margin: 0.5rem 0;
        }

        /* Leaderboard */
        .leaderboard-rank {
            font-size: 1.2rem;
            font-weight: 700;
        }
        .rank-1 { color: #f59e0b; }
        .rank-2 { color: #94a3b8; }
        .rank-3 { color: #b45309; }

        footer {
            text-align: center;
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border);
            color: var(--text-muted);
            font-size: 0.875rem;
        }

        @media print {
            body { padding: 0.5rem; }
            .card { break-inside: avoid; }
            h2 { break-before: page; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Code Analysis Report</h1>

        {% for repo_name, repo_metrics in metrics.items() %}
        <h2>📁 {{ repo_name }}</h2>

        {% set all_authors = [] %}
        {% for key, analyzer_data in repo_metrics.items() %}
            {% if key != 'evaluations' and analyzer_data is mapping %}
                {% for author in analyzer_data.keys() %}
                    {% if author not in all_authors %}
                        {% if all_authors.append(author) %}{% endif %}
                    {% endif %}
                {% endfor %}
            {% endif %}
        {% endfor %}

        {% for author in all_authors | sort %}
        <div class="card">
            <h3>👤 {{ author }}</h3>

            {# ── Developer Evaluation ── #}
            {% set ev = repo_metrics.get('evaluations', {}).get(author, {}) %}
            {% if ev %}
            <h4>🏆 Developer Evaluation</h4>
            <div class="eval-header">
                <div class="score-circle score-{{ ev.grade | lower }}">
                    {{ ev.overall_score }}
                </div>
                <div>
                    <span class="grade-label">{{ ev.grade }}</span>
                    <div class="verdict">{{ ev.verdict }}</div>
                </div>
            </div>

            {# Dimension score bars #}
            <table>
                <tr><th>Dimension</th><th>Score</th><th>Bar</th></tr>
                {% set dim_names = {
                    'commit_discipline': '📝 Commit Discipline',
                    'work_consistency': '⏰ Work Consistency',
                    'efficiency': '🚀 Efficiency',
                    'code_quality': '🔍 Code Quality',
                    'code_style': '🎨 Code Style',
                    'engagement': '💪 Engagement'
                } %}
                {% for dim, score in ev.get('dimension_scores', {}).items() %}
                <tr>
                    <td>{{ dim_names.get(dim, dim) }}</td>
                    <td class="metric-value">{{ "%.0f" | format(score) }}/100</td>
                    <td>
                        <div class="score-bar-container">
                            <div class="score-bar">
                                <div class="score-bar-fill {% if score >= 70 %}fill-high{% elif score >= 40 %}fill-mid{% else %}fill-low{% endif %}"
                                     style="width: {{ score }}%"></div>
                            </div>
                        </div>
                    </td>
                </tr>
                {% endfor %}
            </table>

            {# Strengths #}
            {% if ev.strengths %}
            <h4 style="color: #166534">Strengths</h4>
            {% for s in ev.strengths %}
            <div class="strength-item">{{ s }}</div>
            {% endfor %}
            {% endif %}

            {# Weaknesses #}
            {% if ev.weaknesses %}
            <h4 style="color: #991b1b; margin-top: 1rem">Weaknesses</h4>
            {% for w in ev.weaknesses %}
            <div class="weakness-item">{{ w }}</div>
            {% endfor %}
            {% endif %}

            {# Suggestions #}
            {% if ev.suggestions %}
            <h4 style="color: #1e40af; margin-top: 1rem">Suggestions</h4>
            {% for sg in ev.suggestions %}
            <div class="suggestion-item">{{ sg }}</div>
            {% endfor %}
            {% endif %}
            {% endif %}

            {# ── Slacking Index ── #}
            {% set sl = repo_metrics.get('slacking', {}).get(author, {}) %}
            {% if sl %}
            <h4>🐟 Slacking Index (摸鱼指数)</h4>
            <div class="slacking-label">
                {{ sl.slacking_index }}/100 — {{ sl.slacking_level_cn }} ({{ sl.slacking_level }})
            </div>
            <div class="slacking-meter">
                <div class="slacking-indicator" style="left: {{ sl.slacking_index }}%"></div>
            </div>
            <table>
                <tr><th>Signal</th><th>Value</th></tr>
                <tr><td>Activity Ratio</td><td>{{ "%.1f%%" | format(sl.activity_ratio * 100) }}</td></tr>
                <tr><td>Trivial Commit Ratio</td><td>{{ "%.1f%%" | format(sl.trivial_commit_ratio * 100) }}</td></tr>
                <tr><td>Large Gap Ratio</td><td>{{ "%.1f%%" | format(sl.large_gap_ratio * 100) }}</td></tr>
                <tr><td>Lines/Active Day</td><td>{{ sl.lines_per_active_day }}</td></tr>
                <tr><td>Non-code Commit Ratio</td><td>{{ "%.1f%%" | format(sl.non_code_commit_ratio * 100) }}</td></tr>
            </table>
            {% endif %}

            {# ── Commit Patterns ── #}
            {% set cd = repo_metrics.get('commit_patterns', {}).get(author, {}) %}
            {% if cd %}
            <h4>📝 Commit Patterns</h4>
            <table>
                <tr><th>Metric</th><th>Value</th></tr>
                <tr><td>Total Commits</td><td class="metric-value">{{ cd.total_commits }}</td></tr>
                <tr><td>Merge Ratio</td><td>{{ "%.1f%%" | format(cd.merge_ratio * 100) }}</td></tr>
                <tr><td>Active Span</td><td>{{ cd.active_span_days }} days</td></tr>
                <tr><td>Avg Commits/Day</td><td class="metric-value">{{ cd.avg_commits_per_active_day }}</td></tr>
                <tr><td>Avg Lines Added</td><td>{{ cd.avg_lines_added }}</td></tr>
                <tr><td>Avg Lines Deleted</td><td>{{ cd.avg_lines_deleted }}</td></tr>
                <tr><td>Total Lines Added</td><td>{{ "{:,}".format(cd.total_lines_added) }}</td></tr>
                <tr><td>Total Lines Deleted</td><td>{{ "{:,}".format(cd.total_lines_deleted) }}</td></tr>
            </table>
            {% endif %}

            {# ── Work Habits ── #}
            {% set hd = repo_metrics.get('work_habits', {}).get(author, {}) %}
            {% if hd %}
            <h4>⏰ Work Habits</h4>
            <table>
                <tr><th>Metric</th><th>Value</th></tr>
                <tr><td>Peak Hour</td><td class="metric-value">{{ hd.peak_hour }}:00</td></tr>
                <tr><td>Weekend Ratio</td><td>{{ "%.1f%%" | format(hd.weekend_ratio * 100) }}</td></tr>
                <tr><td>Late Night Ratio</td><td>
                    {{ "%.1f%%" | format(hd.late_night_ratio * 100) }}
                    {% if hd.late_night_ratio > 0.3 %}
                        <span class="badge badge-warn">High</span>
                    {% endif %}
                </td></tr>
                <tr><td>Longest Streak</td><td>{{ hd.longest_streak_days }} days</td></tr>
                <tr><td>Avg Gap</td><td>{{ hd.avg_gap_between_commits_hours }} hrs</td></tr>
            </table>
            {% endif %}

            {# ── Efficiency ── #}
            {% set ed = repo_metrics.get('efficiency', {}).get(author, {}) %}
            {% if ed %}
            <h4>🚀 Efficiency</h4>
            <table>
                <tr><th>Metric</th><th>Value</th></tr>
                <tr><td>Churn Rate</td><td>{{ "%.1f%%" | format(ed.churn_rate * 100) }}</td></tr>
                <tr><td>Rework Ratio</td><td>
                    {{ "%.1f%%" | format(ed.rework_ratio * 100) }}
                    {% if ed.rework_ratio > 0.3 %}
                        <span class="badge badge-warn">High Rework</span>
                    {% endif %}
                </td></tr>
                <tr><td>Lines/Commit</td><td>{{ ed.lines_per_commit }}</td></tr>
                <tr><td>Files Touched</td><td>{{ ed.unique_files_touched }}</td></tr>
                <tr><td>Ownership Ratio</td><td>{{ "%.1f%%" | format(ed.ownership_ratio * 100) }}</td></tr>
                <tr><td>Bus Factor</td><td>{{ ed.repo_avg_bus_factor }}</td></tr>
            </table>
            {% endif %}

            {# ── Code Style ── #}
            {% set sd = repo_metrics.get('code_style', {}).get(author, {}) %}
            {% if sd %}
            <h4>🎨 Code Style</h4>
            <table>
                <tr><th>Metric</th><th>Value</th></tr>
                <tr><td>Conventional Commit Ratio</td><td>{{ "%.1f%%" | format(sd.conventional_commit_ratio * 100) }}</td></tr>
                <tr><td>Issue Reference Ratio</td><td>{{ "%.1f%%" | format(sd.issue_reference_ratio * 100) }}</td></tr>
                <tr><td>Avg Change Size</td><td>{{ sd.avg_change_size_lines }} lines</td></tr>
            </table>
            {% endif %}

            {# ── Code Quality ── #}
            {% set qd = repo_metrics.get('code_quality', {}).get(author, {}) %}
            {% if qd %}
            <h4>🔍 Code Quality</h4>
            <table>
                <tr><th>Metric</th><th>Value</th></tr>
                <tr><td>Bug Fix Ratio</td><td>
                    {{ "%.1f%%" | format(qd.bug_fix_ratio * 100) }}
                    {% if qd.bug_fix_ratio > 0.5 %}
                        <span class="badge badge-bad">High</span>
                    {% elif qd.bug_fix_ratio > 0.3 %}
                        <span class="badge badge-warn">Moderate</span>
                    {% else %}
                        <span class="badge badge-good">Low</span>
                    {% endif %}
                </td></tr>
                <tr><td>Revert Ratio</td><td>{{ "%.1f%%" | format(qd.revert_ratio * 100) }}</td></tr>
                <tr><td>Large Commit Ratio</td><td>{{ "%.1f%%" | format(qd.large_commit_ratio * 100) }}</td></tr>
                <tr><td>Test Modification Ratio</td><td>{{ "%.1f%%" | format(qd.test_modification_ratio * 100) }}</td></tr>
                <tr><td>Avg Commit Size</td><td>{{ qd.avg_commit_size }} lines</td></tr>
                {% if qd.avg_python_complexity > 0 %}
                <tr><td>Avg Python Complexity</td><td>{{ qd.avg_python_complexity }}</td></tr>
                {% endif %}
            </table>
            {% endif %}
        </div>
        {% endfor %}
        {% endfor %}

        {# ── Leaderboard ── #}
        {% set has_evals = false %}
        {% for repo_name, repo_metrics in metrics.items() %}
            {% if repo_metrics.get('evaluations') %}
                {% set has_evals = true %}
            {% endif %}
        {% endfor %}

        {% for repo_name, repo_metrics in metrics.items() %}
        {% if repo_metrics.get('evaluations') %}
        <h2>🏆 Developer Leaderboard</h2>
        <div class="card">
            <table class="comparison-table">
                <tr><th>Rank</th><th>Developer</th><th>Score</th><th>Grade</th><th>Verdict</th></tr>
                {% for author, ev in repo_metrics.get('evaluations', {}).items() | sort(attribute='1.overall_score', reverse=true) %}
                <tr>
                    <td class="leaderboard-rank {% if loop.index <= 3 %}rank-{{ loop.index }}{% endif %}">
                        {% if loop.index == 1 %}🥇{% elif loop.index == 2 %}🥈{% elif loop.index == 3 %}🥉{% else %}{{ loop.index }}{% endif %}
                    </td>
                    <td><strong>{{ author }}</strong></td>
                    <td class="metric-value">{{ ev.overall_score }}</td>
                    <td><span class="badge badge-info">{{ ev.grade }}</span></td>
                    <td>{{ ev.verdict }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
        {% endif %}

        {# ── Slacking Leaderboard ── #}
        {% if repo_metrics.get('slacking') %}
        <h2>🐟 Slacking Index Leaderboard (摸鱼排行榜)</h2>
        <div class="card">
            <table class="comparison-table">
                <tr><th>Rank</th><th>Developer</th><th>Index</th><th>Level</th><th>Lines/Day</th></tr>
                {% for author, sl in repo_metrics.get('slacking', {}).items() | sort(attribute='1.slacking_index', reverse=true) %}
                <tr>
                    <td>{{ loop.index }}</td>
                    <td><strong>{{ author }}</strong></td>
                    <td class="metric-value">{{ sl.slacking_index }}/100</td>
                    <td>{{ sl.slacking_level_cn }}</td>
                    <td>{{ sl.lines_per_active_day }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
        {% endif %}
        {% endfor %}

        <footer>
            Generated by <strong>Code Analysis Skills</strong> | Powered by ClawHub
        </footer>
    </div>
</body>
</html>
"""


class HtmlReporter(BaseReporter):
    """Generates styled HTML reports from analysis metrics."""

    def generate(self, metrics: Dict) -> str:
        """Generate an HTML report using Jinja2 template."""
        template = Template(HTML_TEMPLATE)
        return template.render(metrics=metrics)
