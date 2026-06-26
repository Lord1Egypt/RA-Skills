from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Any, Iterable


def sanitize_filename(value: str) -> str:
    cleaned = "".join(char if char.isalnum() or char in ("-", "_") else "-" for char in value.strip())
    return cleaned.strip("-") or "report"


def ratio(value: int, total: int) -> str:
    if total <= 0:
        return "0.0%"
    return f"{(value / total) * 100:.1f}%"


def star_score(level: int) -> str:
    level = max(1, min(level, 5))
    return "⭐" * level


@dataclass
class RenderedReport:
    markdown_path: Path
    html_path: Path


class ReportRenderer:
    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir

    def render(self, report: dict[str, Any]) -> RenderedReport:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        slug = sanitize_filename(f"{report['brand']}-{report['category']}-{timestamp}")
        target_dir = self.output_dir / slug
        target_dir.mkdir(parents=True, exist_ok=True)

        markdown = self._build_markdown(report)
        html = self._build_html(report, markdown)

        markdown_path = target_dir / "report.md"
        html_path = target_dir / "report.html"
        markdown_path.write_text(markdown, encoding="utf-8")
        html_path.write_text(html, encoding="utf-8")
        return RenderedReport(markdown_path=markdown_path, html_path=html_path)

    def _build_markdown(self, report: dict[str, Any]) -> str:
        lines: list[str] = [
            f"# {report['title']}",
            "",
            f"报告人：{report['reporter']}",
            f"分析日期：{report['analysis_date']}",
            f"数据来源：{report['data_source']}",
            "",
            "## 执行摘要",
            report["executive_summary"],
            "",
            "### 关键发现",
            self._table_to_markdown(report["key_findings"]),
            "",
            "### 核心建议",
        ]
        lines.extend(f"- {item}" for item in report["core_suggestions"])

        lines.extend(
            [
                "",
                "## 第一部分：数据概览",
                "### 1.1 分析样本",
                self._table_to_markdown(report["sample_overview"]),
                "",
                "### 1.2 样本品牌销售排名",
                self._table_to_markdown(report["brand_ranking"]),
                "",
                "## 第二部分：品牌维度深度分析",
                "### 2.1 核心竞品品牌矩阵",
                self._table_to_markdown(report["brand_matrix"]),
                "",
                "### 2.2 品牌定位分类",
                self._table_to_markdown(report["brand_positioning"]),
                "",
                "### 2.3 各品牌价格带分布",
                self._table_to_markdown(report["price_distribution"]),
                "",
                "### 2.4 品牌打法总结",
                self._table_to_markdown(report["brand_strategy"]),
                "",
                "### 2.5 竞争空白点",
                self._table_to_markdown(report["whitespace"]),
                "",
                "## 第三部分：功能趋势分析",
                "### 3.1 竞品功能词频",
                self._table_to_markdown(report["feature_frequency"]),
                "",
                "### 3.2 洞察",
            ]
        )
        lines.extend(f"- {item}" for item in report["feature_insights"])

        lines.extend(
            [
                "",
                "## 第四部分：价格带分析",
                self._table_to_markdown(report["price_band_analysis"]),
                "",
                "## 第五部分：用户需求洞察",
                "### 5.1 用户需求排名",
                self._table_to_markdown(report["user_needs"]),
                "",
                "### 5.2 用户痛点",
                self._table_to_markdown(report["pain_points"]),
                "",
                "### 5.3 购买决策障碍",
                self._table_to_markdown(report["purchase_barriers"]),
                "",
                f"## 第六部分：{report['brand']}机会分析",
                "### 6.1 竞争优势",
                self._table_to_markdown(report["advantages"]),
                "",
                "### 6.2 差异化机会",
                self._table_to_markdown(report["differentiation"]),
                "",
                "### 6.3 产品机会",
                "产品定义建议：",
                report["product_definition"],
                "",
                "SKU建议：",
                self._table_to_markdown(report["sku_suggestions"]),
                "",
                "核心卖点：",
            ]
        )
        lines.extend(f"- {item}" for item in report["selling_points"])

        lines.extend(
            [
                "",
                "## 第七部分：行动计划",
                "### 7.1 产品开发",
                self._table_to_markdown(report["product_actions"]),
                "",
                "### 7.2 上市准备",
                self._table_to_markdown(report["go_to_market_actions"]),
                "",
                "### 7.3 预期目标",
                self._table_to_markdown(report["goals"]),
                "",
                "## 第八部分：风险与建议",
                "### 8.1 潜在风险",
                self._table_to_markdown(report["risks"]),
                "",
                "### 8.2 风险控制建议",
            ]
        )
        lines.extend(f"- {item}" for item in report["risk_controls"])

        lines.extend(
            [
                "",
                "## 附录",
                "### 分析方法",
            ]
        )
        lines.extend(f"- {item}" for item in report["methods"])
        lines.extend(["", "### 数据来源"])
        lines.extend(f"- {item}" for item in report["sources"])
        lines.extend(["", "报告完毕。"])
        return "\n".join(lines).strip() + "\n"

    def _build_html(self, report: dict[str, Any], markdown: str) -> str:
        sections = [
            "<!DOCTYPE html>",
            "<html lang='zh-CN'>",
            "<head>",
            "<meta charset='utf-8'>",
            f"<title>{escape(report['title'])}</title>",
            "<style>",
            "body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:1080px;margin:32px auto;padding:0 20px;color:#1f2328;line-height:1.7;}",
            "table{border-collapse:collapse;width:100%;margin:12px 0 24px;}",
            "th,td{border:1px solid #d0d7de;padding:8px 10px;text-align:left;vertical-align:top;}",
            "th{background:#f6f8fa;}",
            "h1,h2,h3{margin-top:24px;}",
            "ul{padding-left:20px;}",
            "code{background:#f6f8fa;padding:2px 4px;border-radius:4px;}",
            "</style>",
            "</head>",
            "<body>",
            f"<h1>{escape(report['title'])}</h1>",
            f"<p>报告人：{escape(report['reporter'])}<br>分析日期：{escape(report['analysis_date'])}<br>数据来源：{escape(report['data_source'])}</p>",
            self._section("执行摘要", escape(report["executive_summary"]).replace("\n", "<br>")),
            "<h3>关键发现</h3>",
            self._table_to_html(report["key_findings"]),
            "<h3>核心建议</h3>",
            self._list_to_html(report["core_suggestions"]),
            "<h2>第一部分：数据概览</h2>",
            "<h3>1.1 分析样本</h3>",
            self._table_to_html(report["sample_overview"]),
            "<h3>1.2 样本品牌销售排名</h3>",
            self._table_to_html(report["brand_ranking"]),
            "<h2>第二部分：品牌维度深度分析</h2>",
            "<h3>2.1 核心竞品品牌矩阵</h3>",
            self._table_to_html(report["brand_matrix"]),
            "<h3>2.2 品牌定位分类</h3>",
            self._table_to_html(report["brand_positioning"]),
            "<h3>2.3 各品牌价格带分布</h3>",
            self._table_to_html(report["price_distribution"]),
            "<h3>2.4 品牌打法总结</h3>",
            self._table_to_html(report["brand_strategy"]),
            "<h3>2.5 竞争空白点</h3>",
            self._table_to_html(report["whitespace"]),
            "<h2>第三部分：功能趋势分析</h2>",
            "<h3>3.1 竞品功能词频</h3>",
            self._table_to_html(report["feature_frequency"]),
            "<h3>3.2 洞察</h3>",
            self._list_to_html(report["feature_insights"]),
            "<h2>第四部分：价格带分析</h2>",
            self._table_to_html(report["price_band_analysis"]),
            "<h2>第五部分：用户需求洞察</h2>",
            "<h3>5.1 用户需求排名</h3>",
            self._table_to_html(report["user_needs"]),
            "<h3>5.2 用户痛点</h3>",
            self._table_to_html(report["pain_points"]),
            "<h3>5.3 购买决策障碍</h3>",
            self._table_to_html(report["purchase_barriers"]),
            f"<h2>第六部分：{escape(report['brand'])}机会分析</h2>",
            "<h3>6.1 竞争优势</h3>",
            self._table_to_html(report["advantages"]),
            "<h3>6.2 差异化机会</h3>",
            self._table_to_html(report["differentiation"]),
            "<h3>6.3 产品机会</h3>",
            f"<p><strong>产品定义建议：</strong>{escape(report['product_definition'])}</p>",
            "<p><strong>SKU建议：</strong></p>",
            self._table_to_html(report["sku_suggestions"]),
            "<p><strong>核心卖点：</strong></p>",
            self._list_to_html(report["selling_points"]),
            "<h2>第七部分：行动计划</h2>",
            "<h3>7.1 产品开发</h3>",
            self._table_to_html(report["product_actions"]),
            "<h3>7.2 上市准备</h3>",
            self._table_to_html(report["go_to_market_actions"]),
            "<h3>7.3 预期目标</h3>",
            self._table_to_html(report["goals"]),
            "<h2>第八部分：风险与建议</h2>",
            "<h3>8.1 潜在风险</h3>",
            self._table_to_html(report["risks"]),
            "<h3>8.2 风险控制建议</h3>",
            self._list_to_html(report["risk_controls"]),
            "<h2>附录</h2>",
            "<h3>分析方法</h3>",
            self._list_to_html(report["methods"]),
            "<h3>数据来源</h3>",
            self._list_to_html(report["sources"]),
            "<hr>",
            "<details><summary>Markdown 原文</summary>",
            f"<pre>{escape(markdown)}</pre>",
            "</details>",
            "</body></html>",
        ]
        return "\n".join(sections)

    def _section(self, title: str, body: str) -> str:
        return f"<h2>{escape(title)}</h2><p>{body}</p>"

    def _list_to_html(self, items: Iterable[str]) -> str:
        return "<ul>" + "".join(f"<li>{escape(item)}</li>" for item in items) + "</ul>"

    def _table_to_markdown(self, rows: list[dict[str, Any]]) -> str:
        if not rows:
            return "| 说明 |\n| --- |\n| 无数据 |\n"
        headers = list(rows[0].keys())
        lines = [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join("---" for _ in headers) + " |",
        ]
        for row in rows:
            lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
        return "\n".join(lines)

    def _table_to_html(self, rows: list[dict[str, Any]]) -> str:
        if not rows:
            return "<table><thead><tr><th>说明</th></tr></thead><tbody><tr><td>无数据</td></tr></tbody></table>"
        headers = list(rows[0].keys())
        head = "".join(f"<th>{escape(header)}</th>" for header in headers)
        body_rows = []
        for row in rows:
            cells = "".join(f"<td>{escape(str(row.get(header, '')))}</td>" for header in headers)
            body_rows.append(f"<tr>{cells}</tr>")
        return f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(body_rows)}</tbody></table>"
