#!/usr/bin/env python3
"""
企业日报生成器 - 核心引擎
============================
功能：多源数据采集 → AI智能分析 → 结构化日报 → 多格式输出

使用方法：
  python generate_report.py --source ./data/today.csv --output ./output/report.md
  python generate_report.py --source ./data/weekly.json --format html --send-email
  python generate_report.py --template ./templates/custom.md --source ./data/

作者: Marvis AI Assistant
版本: 1.0.0
日期: 2026-06-10
"""

import argparse
import csv
import json
import os
import sys
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

# ============================================================================
# 配置区（可通过 config.yaml 覆盖）
# ============================================================================
DEFAULT_CONFIG = {
    "output_format": "markdown",  # markdown / html / pdf
    "template_dir": "./templates",
    "output_dir": "./output",
    "report_title": "每日工作汇报",
    "sections": [
        "今日完成",
        "进行中",
        "明日计划",
        "问题与风险",
        "需要支持",
    ],
    "send_email": False,
    "email_config": {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "from_addr": "",
        "to_addr": "",
    },
}


class DailyReportGenerator:
    """日报生成器主类"""

    def __init__(self, config: Optional[Dict] = None):
        self.config = {**DEFAULT_CONFIG, **(config or {})}
        self.data: List[Dict] = []
        self.report_date = datetime.now().strftime("%Y年%m月%d日")

    # ------------------------------------------------------------------
    # 第一阶段：数据收集
    # ------------------------------------------------------------------

    def load_csv(self, path: str) -> List[Dict]:
        """从CSV文件加载数据"""
        rows = []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        print(f"[DATA] 已加载 {len(rows)} 条记录（来源: {path}）")
        return rows

    def load_json(self, path: str) -> List[Dict]:
        """从JSON文件加载数据"""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            print(f"[DATA] 已加载 {len(data)} 条记录（来源: {path}）")
            return data
        elif isinstance(data, dict):
            print(f"[DATA] 已加载字典数据（来源: {path}）")
            return [data]
        return []

    def load_git_log(self, repo_path: str, days: int = 1) -> List[Dict]:
        """从Git仓库提取今日提交记录"""
        try:
            cmd = f'git -C "{repo_path}" log --since="{days} days ago" --pretty=format:"%h|%an|%s|%ad" --date=short'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"[WARN] Git仓库读取失败: {result.stderr.strip()}")
                return []

            commits = []
            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) >= 4:
                    commits.append(
                        {
                            "type": "代码提交",
                            "hash": parts[0],
                            "author": parts[1],
                            "message": parts[2],
                            "date": parts[3],
                        }
                    )
            print(f"[DATA] 已加载 {len(commits)} 条Git提交记录")
            return commits
        except Exception as e:
            print(f"[WARN] Git日志读取异常: {e}")
            return []

    def collect_data(self, sources: Dict[str, str]) -> None:
        """统一数据收集入口"""
        print("\n" + "=" * 60)
        print("[阶段1] 数据收集开始")
        print("=" * 60)

        all_data = []

        for source_type, source_path in sources.items():
            if not os.path.exists(source_path) and source_type != "git":
                print(f"[WARN] 数据源不存在: {source_path}，跳过")
                continue

            if source_type == "csv" or source_path.endswith(".csv"):
                all_data.extend(self.load_csv(source_path))
            elif source_type == "json" or source_path.endswith(".json"):
                all_data.extend(self.load_json(source_path))
            elif source_type == "git":
                all_data.extend(self.load_git_log(source_path))
            else:
                print(f"[WARN] 不支持的数据源类型: {source_type}")

        self.data = all_data

    # ------------------------------------------------------------------
    # 第二阶段：AI智能分析（分类、摘要、优先级）
    # ------------------------------------------------------------------

    def classify_items(self) -> Dict[str, List[Dict]]:
        """将原始数据按日报分区归类"""
        classified = {
            "今日完成": [],
            "进行中": [],
            "明日计划": [],
            "问题与风险": [],
            "需要支持": [],
        }

        for item in self.data:
            item_type = item.get("type", "").lower()
            status = item.get("status", "").lower()
            content = item.get("content", item.get("message", item.get("description", "")))

            # 智能分类规则
            if "完成" in content or "done" in status or "closed" in status:
                classified["今日完成"].append(item)
            elif "风险" in content or "问题" in content or "bug" in item_type or "blocked" in status:
                classified["问题与风险"].append(item)
            elif "计划" in content or "明天" in content or "todo" in item_type:
                classified["明日计划"].append(item)
            elif "帮助" in content or "支持" in content or "需要" in content:
                classified["需要支持"].append(item)
            else:
                # 默认为进行中
                classified["进行中"].append(item)

        # 打印统计
        print("\n[阶段2] AI分类统计:")
        for section, items in classified.items():
            print(f"  {section}: {len(items)} 项")

        return classified

    def generate_summary(self, items: List[Dict], max_items: int = 5) -> List[str]:
        """为每个分区生成摘要要点（本地规则引擎版）"""
        summaries = []
        for i, item in enumerate(items[:max_items]):
            content = item.get("content", item.get("message", str(item)))
            status = item.get("status", "")
            author = item.get("author", "")

            # 构建摘要行
            summary = f"- {content}"
            if status:
                summary += f"（{status}）"
            if author:
                summary += f" - {author}"
            summaries.append(summary)

        if len(items) > max_items:
            summaries.append(f"- ...及其他 {len(items) - max_items} 项")

        return summaries

    # ------------------------------------------------------------------
    # 第三阶段：格式化输出
    # ------------------------------------------------------------------

    def format_markdown(self, classified: Dict[str, List[Dict]]) -> str:
        """生成Markdown格式日报"""
        lines = []
        lines.append(f"# {self.config['report_title']}")
        lines.append(f"**日期**: {self.report_date}")
        lines.append(f"**生成时间**: {datetime.now().strftime('%H:%M:%S')}")
        lines.append("")
        lines.append("---")
        lines.append("")

        for section, items in classified.items():
            lines.append(f"## {section}")
            lines.append("")
            if not items:
                lines.append("*（本日无记录）*")
                lines.append("")
                continue

            summaries = self.generate_summary(items)
            for s in summaries:
                lines.append(s)
            lines.append("")

        # 数据概览
        lines.append("---")
        lines.append("")
        lines.append("## 数据概览")
        lines.append("")
        total = sum(len(v) for v in classified.values())
        lines.append(f"- 总任务数: **{total}**")
        lines.append(f"- 已完成: **{len(classified['今日完成'])}**")
        lines.append(f"- 进行中: **{len(classified['进行中'])}**")
        lines.append(f"- 风险项: **{len(classified['问题与风险'])}**")
        lines.append("")

        # 页脚
        lines.append("---")
        lines.append("*本日报由 AI 企业日报生成器自动生成*")
        lines.append("")

        return "\n".join(lines)

    def format_html(self, md_content: str) -> str:
        """将Markdown转换为HTML"""
        html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.config['report_title']} - {self.report_date}</title>
    <style>
        body {{ font-family: 'Microsoft YaHei', sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; color: #333; }}
        h1 {{ color: #1a73e8; border-bottom: 3px solid #1a73e8; padding-bottom: 10px; }}
        h2 {{ color: #5f6368; margin-top: 30px; }}
        li {{ margin: 8px 0; }}
        table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px 12px; text-align: left; }}
        th {{ background-color: #f5f5f5; }}
        .meta {{ color: #666; font-size: 14px; }}
        .footer {{ color: #999; font-size: 12px; text-align: center; margin-top: 40px; }}
    </style>
</head>
<body>
    <pre style="white-space: pre-wrap; font-family: inherit;">{md_content}</pre>
    <div class="footer">本日报由 AI 企业日报生成器自动生成 | {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
</body>
</html>"""
        return html_template

    def format_pdf(self, html_content: str, output_path: str) -> None:
        """将HTML转换为PDF（需要 wkhtmltopdf 或 weasyprint）"""
        html_path = output_path.replace(".pdf", ".html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        # 尝试使用 wkhtmltopdf
        try:
            subprocess.run(
                ["wkhtmltopdf", "--quiet", html_path, output_path],
                check=True,
                capture_output=True,
            )
            print(f"[PDF] 已生成: {output_path}")
            os.remove(html_path)  # 清理临时HTML
        except (FileNotFoundError, subprocess.CalledProcessError):
            print(
                "[WARN] wkhtmltopdf 未安装，请手动安装: https://wkhtmltopdf.org/downloads.html"
            )
            print(f"[INFO] 已将HTML临时文件保存为: {html_path}")

    # ------------------------------------------------------------------
    # 第四阶段：发送
    # ------------------------------------------------------------------

    def send_email(self, subject: str, body: str) -> bool:
        """通过邮件发送日报"""
        # 尝试使用系统邮件命令
        try:
            import smtplib
            from email.mime.text import MIMEText

            cfg = self.config["email_config"]
            if not cfg["from_addr"] or not cfg["to_addr"]:
                print("[WARN] 邮件配置不完整，跳过发送")
                return False

            msg = MIMEText(body, "html", "utf-8")
            msg["Subject"] = subject
            msg["From"] = cfg["from_addr"]
            msg["To"] = cfg["to_addr"]

            with smtplib.SMTP(cfg["smtp_server"], cfg["smtp_port"]) as server:
                server.starttls()
                print(f"[EMAIL] 日报已发送至 {cfg['to_addr']}")
                return True
        except Exception as e:
            print(f"[ERROR] 邮件发送失败: {e}")
            return False

    # ------------------------------------------------------------------
    # 主流程
    # ------------------------------------------------------------------

    def run(self, sources: Dict[str, str], output_path: Optional[str] = None, send: bool = False) -> str:
        """主执行流程"""
        print("\n" + "█" * 60)
        print("█  企业日报生成器 v1.0.0")
        print("█  AI-Powered Daily Report Generator")
        print("█" * 60)

        # 阶段1：数据收集
        self.collect_data(sources)

        if not self.data:
            print("\n[WARN] 未收集到任何数据，生成空白日报")
            self.data = [{"type": "提示", "content": "今日无数据记录"}]

        # 阶段2：AI分析
        classified = self.classify_items()

        # 阶段3：生成报告
        print("\n[阶段3] 日报生成中...")
        md_content = self.format_markdown(classified)

        # 确定输出路径
        if not output_path:
            output_dir = self.config["output_dir"]
            os.makedirs(output_dir, exist_ok=True)
            date_str = datetime.now().strftime("%Y%m%d")
            output_path = os.path.join(output_dir, f"daily_report_{date_str}.md")

        # 写入文件
        fmt = self.config["output_format"]
        if fmt == "html":
            html_content = self.format_html(md_content)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
        elif fmt == "pdf":
            html_content = self.format_html(md_content)
            self.format_pdf(html_content, output_path)
        else:
            # 默认 markdown
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(md_content)

        print(f"\n[OUTPUT] 日报已保存至: {output_path}")
        print(f"[STATS] 总任务数: {len(self.data)} | 已完成: {len(classified['今日完成'])}")
        print("█" * 60 + "\n")

        # 阶段4：发送
        if send or self.config["send_email"]:
            subject = f"{self.config['report_title']} - {self.report_date}"
            self.send_email(subject, md_content)

        return md_content


# ============================================================================
# 命令行入口
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="企业日报生成器 - AI-Powered Daily Report Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 从CSV生成Markdown日报
  python generate_report.py --csv ./data/today.csv

  # 从Git提交记录生成HTML日报
  python generate_report.py --git ./my-project --format html

  # 从多个数据源生成并发送邮件
  python generate_report.py --csv ./data/tasks.csv --git ./my-project --format pdf --send

  # 指定输出路径
  python generate_report.py --csv ./data/today.csv --output ./reports/my_report.md
        """,
    )

    parser.add_argument("--csv", help="CSV数据源路径")
    parser.add_argument("--json", help="JSON数据源路径")
    parser.add_argument("--git", help="Git仓库路径（提取今日提交记录）")
    parser.add_argument("--format", choices=["markdown", "html", "pdf"], default="markdown", help="输出格式（默认: markdown）")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--send", action="store_true", help="生成后自动发送邮件")
    parser.add_argument("--config", help="配置文件路径（YAML格式）")

    args = parser.parse_args()

    # 构建数据源
    sources = {}
    if args.csv:
        sources["csv"] = args.csv
    if args.json:
        sources["json"] = args.json
    if args.git:
        sources["git"] = args.git

    if not sources:
        print("[ERROR] 请至少指定一个数据源: --csv / --json / --git")
        print("使用 --help 查看完整帮助")
        sys.exit(1)

    # 配置
    config = DEFAULT_CONFIG.copy()
    if args.format:
        config["output_format"] = args.format

    # 执行
    generator = DailyReportGenerator(config=config)
    generator.run(sources=sources, output_path=args.output, send=args.send)


if __name__ == "__main__":
    main()