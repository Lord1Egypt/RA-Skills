#!/usr/bin/env python3
"""
测试报告生成器

生成可视化 HTML 测试报告，支持中英文切换，默认英文。
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TRANSLATIONS = {
    "en": {
        "title": "Android Project Generator Test Report",
        "subtitle": "Verification summary for the current test run",
        "summary": "Summary",
        "suites": "Suite Details",
        "total": "Total Tests",
        "passed": "Passed",
        "failed": "Failed",
        "skipped": "Skipped",
        "pass_rate": "Pass Rate",
        "runtime": "Runtime",
        "framework": "Framework",
        "empty": "No suite details available",
        "lang_en": "English",
        "lang_zh": "中文",
        "showing": "Showing up to 10 tests per suite",
        "verification": "Verification",
    },
    "zh": {
        "title": "Android Project Generator 测试报告",
        "subtitle": "当前测试运行的验证摘要",
        "summary": "概览",
        "suites": "测试套件详情",
        "total": "总测试数",
        "passed": "通过",
        "failed": "失败",
        "skipped": "跳过",
        "pass_rate": "通过率",
        "runtime": "耗时",
        "framework": "测试框架",
        "empty": "暂无测试套件详情",
        "lang_en": "English",
        "lang_zh": "中文",
        "showing": "每个套件最多展示 10 个测试",
        "verification": "验证",
    },
}


@dataclass
class TestResult:
    name: str
    status: str
    duration: float = 0.0
    error: str = ""


@dataclass
class TestSuite:
    name: str
    tests: List[TestResult]
    passed: int
    failed: int
    skipped: int


class TestReportGenerator:
    def __init__(self, output_path: str = "test-report.html"):
        self.output_path = Path(output_path)
        self.suites: List[TestSuite] = []
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.total_duration = 0.0
        self.default_language = "en"

    def add_suite(self, suite: TestSuite):
        self.suites.append(suite)

    def calculate_stats(self) -> Dict[str, Any]:
        total_tests = sum(s.passed + s.failed + s.skipped for s in self.suites)
        total_passed = sum(s.passed for s in self.suites)
        total_failed = sum(s.failed for s in self.suites)
        total_skipped = sum(s.skipped for s in self.suites)
        pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        return {
            "total": total_tests,
            "passed": total_passed,
            "failed": total_failed,
            "skipped": total_skipped,
            "pass_rate": pass_rate,
        }

    def generate_html(self) -> str:
        stats = self.calculate_stats()
        total = stats["total"]
        pass_rate_deg = (stats["passed"] / total * 360) if total > 0 else 0
        failed_deg = pass_rate_deg + (stats["failed"] / total * 360) if total > 0 else 0
        translations_json = json.dumps(TRANSLATIONS, ensure_ascii=False)
        suites_html = self._generate_suites_html()

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Android Project Generator - Test Report</title>
    <style>
        :root {{
            --m3-primary: #6750a4;
            --m3-on-primary: #ffffff;
            --m3-primary-container: #eaddff;
            --m3-on-primary-container: #21005d;
            --m3-secondary-container: #e8def8;
            --m3-on-secondary-container: #1d192b;
            --m3-surface: #fffbfe;
            --m3-surface-container: #f3edf7;
            --m3-surface-container-high: #ece6f0;
            --m3-outline: #79747e;
            --m3-outline-variant: #cac4d0;
            --m3-error: #b3261e;
            --m3-success: #2e7d32;
            --m3-text: #1c1b1f;
            --m3-text-secondary: #49454f;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: "Roboto", "Segoe UI", Arial, sans-serif;
            color: var(--m3-text);
            background:
                radial-gradient(circle at top left, rgba(255,255,255,0.7), transparent 26%),
                linear-gradient(135deg, #f8f3ff 0%, #eef2ff 42%, #fff8f7 100%);
            min-height: 100vh;
            padding: 24px;
        }}

        .container {{
            max-width: 1180px;
            margin: 0 auto;
            display: grid;
            gap: 24px;
        }}

        .m3-card {{
            display: block;
            --md-elevated-card-container-color: rgba(255, 251, 254, 0.92);
            --md-elevated-card-container-shape: 28px;
            box-shadow: 0 18px 48px rgba(103, 80, 164, 0.12);
            overflow: hidden;
        }}

        .header {{
            padding: 32px;
            display: flex;
            justify-content: space-between;
            gap: 24px;
            align-items: flex-start;
        }}

        .eyebrow {{
            display: inline-flex;
            padding: 7px 14px;
            border-radius: 999px;
            background: var(--m3-primary);
            color: var(--m3-on-primary);
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 14px;
        }}

        h1 {{
            font-size: 40px;
            line-height: 1.04;
            margin-bottom: 10px;
            color: var(--m3-text);
        }}

        .subtitle {{
            color: var(--m3-text-secondary);
            font-size: 16px;
            max-width: 720px;
        }}

        .timestamp {{
            margin-top: 14px;
            color: var(--m3-text-secondary);
            font-size: 14px;
        }}

        .lang-switch {{
            display: inline-flex;
            gap: 12px;
            padding: 10px;
            border-radius: 999px;
            background: rgba(103, 80, 164, 0.08);
            align-items: center;
        }}

        .lang-btn {{
            appearance: none;
            border: 0;
            border-radius: 999px;
            min-width: 108px;
            height: 42px;
            padding: 0 18px;
            font: 600 14px/1 "Roboto", "Segoe UI", Arial, sans-serif;
            cursor: pointer;
            color: var(--m3-on-secondary-container);
            background: var(--m3-secondary-container);
            box-shadow: 0 1px 2px rgba(31, 25, 43, 0.18);
            transition: background-color 160ms ease, color 160ms ease, box-shadow 160ms ease, transform 160ms ease;
        }}

        .lang-btn:hover {{
            background: #ddd0f1;
            box-shadow: 0 4px 12px rgba(103, 80, 164, 0.22);
            transform: translateY(-1px);
        }}

        .lang-btn:active {{
            background: #cfbdea;
            box-shadow: inset 0 1px 3px rgba(31, 25, 43, 0.18);
            transform: translateY(0);
        }}

        .lang-btn.active {{
            color: var(--m3-on-primary);
            background: var(--m3-primary);
            box-shadow: 0 6px 18px rgba(103, 80, 164, 0.28);
        }}

        .lang-btn.active:hover {{
            background: #5d469b;
        }}

        .lang-btn.active:active {{
            background: #533f8b;
        }}

        .section {{
            padding: 28px 30px;
        }}

        .section-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            margin-bottom: 16px;
        }}

        .section h2 {{
            font-size: 24px;
            color: var(--m3-text);
        }}

        md-divider {{
            --md-divider-color: var(--m3-outline-variant);
            margin: 4px 0 18px;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 18px;
        }}

        .stat-card {{
            display: block;
            padding: 22px;
            --md-elevated-card-container-color: var(--m3-surface);
            --md-elevated-card-container-shape: 22px;
            border-top: 4px solid var(--m3-primary);
        }}

        .stat-card.success {{ border-top-color: var(--m3-success); }}
        .stat-card.warning {{ border-top-color: #ef6c00; }}
        .stat-card.info {{ border-top-color: #1e88e5; }}

        .stat-value {{
            font-size: 44px;
            font-weight: 700;
            color: var(--m3-text);
            margin-bottom: 8px;
        }}

        .stat-label {{
            color: var(--m3-text-secondary);
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .progress-bar {{
            height: 8px;
            margin-top: 14px;
            border-radius: 999px;
            background: #e7e0ec;
            overflow: hidden;
        }}

        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #6750a4, #7d66c2);
            border-radius: 999px;
        }}

        .chart-shell {{
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 8px 0 4px;
        }}

        .donut-chart {{
            width: 300px;
            height: 300px;
            border-radius: 50%;
            background: conic-gradient(
                var(--m3-primary) 0deg {pass_rate_deg:.2f}deg,
                var(--m3-error) {pass_rate_deg:.2f}deg {failed_deg:.2f}deg,
                #d0c7d8 {failed_deg:.2f}deg 360deg
            );
            position: relative;
        }}

        .donut-chart::before {{
            content: "";
            position: absolute;
            inset: 58px;
            border-radius: 50%;
            background: var(--m3-surface);
        }}

        .donut-center {{
            position: absolute;
            inset: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            z-index: 1;
        }}

        .donut-center .percentage {{
            font-size: 48px;
            font-weight: 700;
            color: var(--m3-text);
        }}

        .legend {{
            display: flex;
            justify-content: center;
            gap: 28px;
            margin-top: 22px;
            flex-wrap: wrap;
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--m3-text-secondary);
            font-size: 14px;
        }}

        .legend-color {{
            width: 12px;
            height: 12px;
            border-radius: 999px;
        }}

        .suite-note {{
            color: var(--m3-text-secondary);
            font-size: 14px;
            margin-bottom: 16px;
        }}

        .test-suite {{
            display: block;
            margin-bottom: 16px;
            padding: 16px;
            --md-elevated-card-container-color: var(--m3-surface-container);
            --md-elevated-card-container-shape: 20px;
        }}

        .test-suite-header {{
            display: flex;
            justify-content: space-between;
            gap: 14px;
            align-items: center;
            margin-bottom: 12px;
        }}

        .test-suite-title {{
            font-size: 18px;
            font-weight: 600;
            color: var(--m3-text);
        }}

        .test-suite-badge {{
            padding: 6px 12px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 600;
            background: var(--m3-secondary-container);
            color: var(--m3-on-secondary-container);
        }}

        .badge-success {{
            background: #d6f5db;
            color: #1b5e20;
        }}

        .badge-warning {{
            background: #ffe0b2;
            color: #9a3412;
        }}

        .badge-danger {{
            background: #f9dedc;
            color: #8c1d18;
        }}

        .test-list {{
            list-style: none;
            display: grid;
            gap: 8px;
        }}

        .test-item {{
            display: flex;
            justify-content: space-between;
            gap: 12px;
            padding: 10px 12px;
            border-radius: 14px;
            background: rgba(255,255,255,0.92);
            border: 1px solid rgba(202, 196, 208, 0.7);
        }}

        .test-name {{
            color: var(--m3-text-secondary);
            font-family: "Roboto Mono", "Courier New", monospace;
            font-size: 13px;
        }}

        .test-status {{
            color: var(--m3-text-secondary);
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}

        .footer-note {{
            color: var(--m3-text-secondary);
            font-size: 14px;
            text-align: center;
        }}

        @media (max-width: 900px) {{
            .header {{
                flex-direction: column;
            }}
            .donut-chart {{
                width: 260px;
                height: 260px;
            }}
            .donut-chart::before {{
                inset: 48px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <md-elevated-card class="m3-card header">
            <div>
                <div class="eyebrow" data-i18n="verification">Verification</div>
                <h1 data-i18n="title">Android Project Generator Test Report</h1>
                <p class="subtitle" data-i18n="subtitle">Verification summary for the current test run</p>
                <p class="timestamp">{self.timestamp} | Python {self._get_python_version()} | pytest {self._get_pytest_version()}</p>
            </div>
            <div class="lang-switch" aria-label="Language Switcher">
                <button type="button" id="lang-en" class="lang-btn active" data-lang="en" data-i18n="lang_en">English</button>
                <button type="button" id="lang-zh" class="lang-btn" data-lang="zh" data-i18n="lang_zh">中文</button>
            </div>
        </md-elevated-card>

        <md-elevated-card class="m3-card section">
            <div class="section-header">
                <h2 data-i18n="summary">Summary</h2>
            </div>
            <md-divider></md-divider>
            <div class="stats-grid">
                <md-elevated-card class="stat-card info">
                    <div class="stat-value">{stats['total']}</div>
                    <div class="stat-label" data-i18n="total">Total Tests</div>
                </md-elevated-card>
                <md-elevated-card class="stat-card success">
                    <div class="stat-value">{stats['passed']}</div>
                    <div class="stat-label" data-i18n="passed">Passed</div>
                    <div class="progress-bar"><div class="progress-fill" style="width: {stats['pass_rate']:.1f}%"></div></div>
                </md-elevated-card>
                <md-elevated-card class="stat-card warning">
                    <div class="stat-value">{stats['failed']}</div>
                    <div class="stat-label" data-i18n="failed">Failed</div>
                </md-elevated-card>
                <md-elevated-card class="stat-card info">
                    <div class="stat-value">{stats['skipped']}</div>
                    <div class="stat-label" data-i18n="skipped">Skipped</div>
                </md-elevated-card>
            </div>
        </md-elevated-card>

        <md-elevated-card class="m3-card section">
            <div class="section-header">
                <h2 data-i18n="runtime">Runtime</h2>
            </div>
            <md-divider></md-divider>
            <div class="stats-grid" style="grid-template-columns: 1fr;">
                <md-elevated-card class="stat-card info">
                    <div class="stat-value">{self.total_duration:.2f}s</div>
                    <div class="stat-label" data-i18n="runtime">Runtime</div>
                </md-elevated-card>
            </div>
        </md-elevated-card>

        <md-elevated-card class="m3-card section">
            <div class="section-header">
                <h2 data-i18n="pass_rate">Pass Rate</h2>
            </div>
            <md-divider></md-divider>
            <div class="chart-shell">
                <div class="donut-chart">
                    <div class="donut-center">
                        <div class="percentage">{stats['pass_rate']:.1f}%</div>
                        <div data-i18n="pass_rate">Pass Rate</div>
                    </div>
                </div>
            </div>
            <div class="legend">
                <div class="legend-item"><span class="legend-color" style="background:var(--m3-primary)"></span><span><span data-i18n="passed">Passed</span> ({stats['passed']})</span></div>
                <div class="legend-item"><span class="legend-color" style="background:var(--m3-error)"></span><span><span data-i18n="failed">Failed</span> ({stats['failed']})</span></div>
                <div class="legend-item"><span class="legend-color" style="background:#d0c7d8"></span><span><span data-i18n="skipped">Skipped</span> ({stats['skipped']})</span></div>
            </div>
        </md-elevated-card>

        <md-elevated-card class="m3-card section">
            <div class="section-header">
                <h2 data-i18n="suites">Suite Details</h2>
            </div>
            <md-divider></md-divider>
            <p class="suite-note" data-i18n="showing">Showing up to 10 tests per suite</p>
            {suites_html if suites_html else '<p class="suite-note" data-i18n="empty">No suite details available</p>'}
        </md-elevated-card>

        <md-elevated-card class="m3-card section">
            <p class="footer-note"><span data-i18n="framework">Framework</span>: pytest {self._get_pytest_version()} | Python {self._get_python_version()}</p>
        </md-elevated-card>
    </div>
    <script type="module">
        import * as materialweb from 'https://esm.run/@material/web';
        window.materialweb = materialweb;
    </script>
    <script>
        const translations = {translations_json};
        function setLanguage(lang) {{
            document.documentElement.lang = lang;
            document.querySelectorAll("[data-i18n]").forEach((node) => {{
                const key = node.getAttribute("data-i18n");
                if (translations[lang] && translations[lang][key]) {{
                    node.textContent = translations[lang][key];
                }}
            }});
            document.getElementById("lang-en").classList.toggle("active", lang === "en");
            document.getElementById("lang-zh").classList.toggle("active", lang === "zh");
        }}
        window.addEventListener("DOMContentLoaded", () => {{
            document.querySelectorAll(".lang-btn").forEach((button) => {{
                button.addEventListener("click", () => setLanguage(button.dataset.lang));
            }});
            setLanguage("{self.default_language}");
        }});
    </script>
</body>
</html>"""

    def _generate_suites_html(self) -> str:
        cards = []
        for suite in self.suites:
            total = suite.passed + suite.failed + suite.skipped
            pass_rate = (suite.passed / total * 100) if total > 0 else 0
            badge_class = "badge-success" if pass_rate >= 80 else "badge-warning" if pass_rate >= 50 else "badge-danger"
            tests_html = []
            for test in suite.tests[:10]:
                tests_html.append(
                    f'<li class="test-item"><span class="test-name">{test.name}</span><span class="test-status">{test.status}</span></li>'
                )
            cards.append(
                f"""
                <md-elevated-card class="test-suite">
                    <div class="test-suite-header">
                        <span class="test-suite-title">{suite.name}</span>
                        <span class="test-suite-badge {badge_class}">{pass_rate:.1f}%</span>
                    </div>
                    <md-divider></md-divider>
                    <ul class="test-list">{''.join(tests_html)}</ul>
                </md-elevated-card>
                """
            )
        return "".join(cards)

    def _get_python_version(self) -> str:
        import sys
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    def _get_pytest_version(self) -> str:
        try:
            import pytest
            return pytest.__version__
        except Exception:
            return "unknown"

    def _display_path(self, path: Path) -> str:
        try:
            return str(Path(path).resolve().relative_to(PROJECT_ROOT)).replace("\\", "/")
        except Exception:
            return str(path).replace("\\", "/")

    def save(self):
        html = self.generate_html()
        self.output_path.write_text(html, encoding="utf-8")
        print(f"[OK] Test report generated: {self._display_path(self.output_path)}")


def parse_pytest_json_report(json_file: str) -> TestReportGenerator:
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    generator = TestReportGenerator()
    generator.total_duration = data.get("summary", {}).get("duration", 0)

    tests_by_file = {}
    for test in data.get("tests", []):
        file = test.get("file", "unknown")
        tests_by_file.setdefault(file, []).append(
            TestResult(
                name=test.get("name", "unknown"),
                status=test.get("outcome", "unknown"),
                duration=test.get("duration", 0),
                error=test.get("call", {}).get("crash", {}).get("message", ""),
            )
        )

    for file, tests in tests_by_file.items():
        generator.add_suite(
            TestSuite(
                name=Path(file).stem,
                tests=tests,
                passed=sum(1 for t in tests if t.status == "passed"),
                failed=sum(1 for t in tests if t.status == "failed"),
                skipped=sum(1 for t in tests if t.status == "skipped"),
            )
        )

    return generator


def parse_summary_report(json_file: str) -> TestReportGenerator:
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    generator = TestReportGenerator()
    summary = data.get("summary", {})
    generator.total_duration = summary.get("duration", 0)

    for suite_data in data.get("suite_details", []):
        tests = [
            TestResult(
                name=test.get("name", "unknown"),
                status=test.get("status", "unknown"),
            )
            for test in suite_data.get("tests", [])
        ]
        generator.add_suite(
            TestSuite(
                name=suite_data.get("name", "unknown"),
                tests=tests,
                passed=suite_data.get("passed", 0),
                failed=suite_data.get("failed", 0),
                skipped=suite_data.get("skipped", 0),
            )
        )

    return generator


if __name__ == "__main__":
    generator = TestReportGenerator(output_path="test-report.html")
    generator.add_suite(
        TestSuite(
            name="Config Generation",
            tests=[
                TestResult("test_agp_87_requires_gradle_89", "passed"),
                TestResult("test_agp_91_requires_gradle_93", "passed"),
            ],
            passed=2,
            failed=0,
            skipped=0,
        )
    )
    generator.total_duration = 0.05
    generator.save()
