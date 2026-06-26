#!/usr/bin/env python3
"""
智能摘要和归档模块
自动将 daily logs 提炼为 MEMORY.md 的高价值内容
"""
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple
import json


class MemoryDigest:
    """
    记忆摘要器

    功能：
    1. 自动从 daily logs 提取高价值内容
    2. 智能去重和合并
    3. 按主题分类到 MEMORY.md 的对应章节
    4. 生成摘要报告
    """

    def __init__(self, workspace: str = "."):
        self.workspace = Path(workspace)
        self.memory_md = self.workspace / "MEMORY.md"
        self.memory_dir = self.workspace / "memory"
        self.digest_log = self.workspace / ".memory-digest.log"

    def digest(self, days: int = 7, dry_run: bool = False) -> Dict:
        """
        执行摘要和归档

        Args:
            days: 处理最近 N 天的日志
            dry_run: 仅预览，不实际写入

        Returns:
            摘要报告
        """
        today = datetime.now()
        digested_items = {
            "preferences": [],
            "decisions": [],
            "lessons": [],
            "projects": []
        }

        # 1. 从 daily logs 提取内容
        for i in range(days):
            date = today - timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            daily_file = self.memory_dir / f"{date_str}.md"

            if daily_file.exists():
                items = self._extract_from_daily(daily_file, date)
                for category, items_list in items.items():
                    digested_items[category].extend(items_list)

        # 2. 智能去重
        for category in digested_items:
            digested_items[category] = self._deduplicate(digested_items[category])

        # 3. 排序（按重要性）
        for category in digested_items:
            digested_items[category] = sorted(
                digested_items[category],
                key=lambda x: x.get("importance", 0),
                reverse=True
            )

        # 4. 生成报告
        report = self._generate_report(digested_items, days)

        if not dry_run:
            # 5. 写入 MEMORY.md
            self._update_memory_md(digested_items)
            self._log_digest(digested_items)
            report["status"] = "applied"
        else:
            report["status"] = "dry_run"

        return report

    def _extract_from_daily(self, daily_file: Path, date: datetime) -> Dict:
        """从单个 daily 文件提取内容"""
        content = daily_file.read_text()
        items = {
            "preferences": [],
            "decisions": [],
            "lessons": [],
            "projects": []
        }

        # 提取决策
        decisions_match = re.search(r"## Decisions Made\s*\n([\s\S]*?)(?=##|$)", content)
        if decisions_match:
            for line in decisions_match.group(1).split("\n"):
                line = line.strip("- ")
                if line and len(line) > 10:
                    importance = self._estimate_importance(line, "decision")
                    items["decisions"].append({
                        "content": line,
                        "date": date.strftime("%Y-%m-%d"),
                        "importance": importance
                    })

        # 提取教训
        lessons_match = re.search(r"## Lessons Learned\s*\n([\s\S]*?)(?=##|$)", content)
        if lessons_match:
            for line in lessons_match.group(1).split("\n"):
                line = line.strip("- ")
                if line and len(line) > 10:
                    importance = self._estimate_importance(line, "lesson")
                    items["lessons"].append({
                        "content": line,
                        "date": date.strftime("%Y-%m-%d"),
                        "importance": importance
                    })

        # 提取偏好（从 Tasks Completed 中推断）
        tasks_match = re.search(r"## Tasks Completed\s*\n([\s\S]*?)(?=##|$)", content)
        if tasks_match:
            for line in tasks_match.group(1).split("\n"):
                line = line.strip("- ")
                # 检测包含偏好的任务描述
                if any(kw in line.lower() for kw in ["prefer", "like", "want", "use"]):
                    importance = self._estimate_importance(line, "preference")
                    items["preferences"].append({
                        "content": line,
                        "date": date.strftime("%Y-%m-%d"),
                        "importance": importance
                    })

        return items

    def _estimate_importance(self, content: str, category: str) -> float:
        """
        估算内容重要性
        """
        score = 0.5

        # 关键词加成
        critical_keywords = ["critical", "important", "must", "never", "always"]
        if any(kw in content.lower() for kw in critical_keywords):
            score += 0.3

        # 包含原因加成
        if "because" in content.lower() or "因为" in content:
            score += 0.2

        # 长度加成
        if len(content) > 50:
            score += 0.1

        # 类别加成
        if category == "decision":
            score += 0.2
        elif category == "lesson":
            score += 0.15

        return min(score, 1.0)

    def _deduplicate(self, items: List[Dict]) -> List[Dict]:
        """
        智能去重
        基于内容相似度和语义匹配
        """
        if not items:
            return []

        unique_items = [items[0]]

        for item in items[1:]:
            is_duplicate = False

            for existing in unique_items:
                similarity = self._calculate_similarity(
                    item["content"],
                    existing["content"]
                )

                # 如果相似度 > 0.8，认为是重复
                if similarity > 0.8:
                    # 保留更重要的那个
                    if item["importance"] > existing["importance"]:
                        unique_items.remove(existing)
                        unique_items.append(item)
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique_items.append(item)

        return unique_items

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        计算文本相似度（Jaccard + 关键词匹配）
        """
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        # Jaccard 相似度
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        jaccard = intersection / union if union > 0 else 0

        # 关键词匹配
        important_words = {"prefer", "use", "decision", "decided", "must", "should"}
        important1 = words1 & important_words
        important2 = words2 & important_words
        keyword_match = len(important1 & important2) / max(len(important1 | important2), 1)

        # 综合相似度
        similarity = jaccard * 0.6 + keyword_match * 0.4

        return similarity

    def _generate_report(self, digested_items: Dict, days: int) -> Dict:
        """生成摘要报告"""
        report = {
            "summary": {
                "total_days": days,
                "preferences": len(digested_items["preferences"]),
                "decisions": len(digested_items["decisions"]),
                "lessons": len(digested_items["lessons"]),
                "projects": len(digested_items["projects"])
            },
            "details": {}
        }

        for category, items in digested_items.items():
            if items:
                report["details"][category] = [
                    {
                        "content": item["content"],
                        "date": item["date"],
                        "importance": item["importance"]
                    }
                    for item in items[:5]  # 只显示 Top 5
                ]

        return report

    def _update_memory_md(self, digested_items: Dict):
        """
        更新 MEMORY.md
        将摘要内容追加到对应章节
        """
        if not self.memory_md.exists():
            return

        content = self.memory_md.read_text()

        # 追加偏好
        if digested_items["preferences"]:
            pref_section = self._get_section(content, "Preferences")
            for item in digested_items["preferences"]:
                if item["importance"] > 0.7:  # 只添加高重要性的
                    pref_section += f"- {item['content']}\n"
            content = self._replace_section(content, "Preferences", pref_section)

        # 追加决策
        if digested_items["decisions"]:
            decisions_section = self._get_section(content, "Decisions Log")
            for item in digested_items["decisions"]:
                if item["importance"] > 0.7:
                    decisions_section += f"- {item['content']} ({item['date']})\n"
            content = self._replace_section(content, "Decisions Log", decisions_section)

        # 追加教训
        if digested_items["lessons"]:
            lessons_section = self._get_section(content, "Lessons Learned")
            for item in digested_items["lessons"]:
                if item["importance"] > 0.7:
                    lessons_section += f"- {item['content']}\n"
            content = self._replace_section(content, "Lessons Learned", lessons_section)

        # 写回文件
        self.memory_md.write_text(content)

    def _get_section(self, content: str, section_name: str) -> str:
        """获取章节内容"""
        pattern = rf"## {section_name}\s*\n([\s\S]*?)(?=##|$)"
        match = re.search(pattern, content)
        if match:
            return match.group(1)
        return ""

    def _replace_section(self, content: str, section_name: str, new_content: str) -> str:
        """替换章节内容"""
        pattern = rf"(## {section_name}\s*\n)([\s\S]*?)(?=##|$)"
        match = re.search(pattern, content)
        if match:
            return content.replace(match.group(0), match.group(1) + new_content)
        return content

    def _log_digest(self, digested_items: Dict):
        """记录摘要日志"""
        timestamp = datetime.now().isoformat()
        total_items = sum(len(items) for items in digested_items.values())

        log_entry = f"{timestamp} | Digested {total_items} items\n"

        try:
            with open(self.digest_log, "a") as f:
                f.write(log_entry)
        except:
            pass


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description="智能记忆摘要和归档")
    parser.add_argument("--days", type=int, default=7,
                       help="处理最近 N 天的日志")
    parser.add_argument("--dry-run", action="store_true",
                       help="预览模式，不实际写入")
    parser.add_argument("--workspace", default=".", help="工作目录")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")

    args = parser.parse_args()

    digester = MemoryDigest(args.workspace)
    report = digester.digest(args.days, args.dry_run)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"🧠 记忆摘要报告 ({args.days} 天)")
        print("-" * 50)
        print(f"状态: {report['status']}")
        print(f"偏好: {report['summary']['preferences']} 项")
        print(f"决策: {report['summary']['decisions']} 项")
        print(f"教训: {report['summary']['lessons']} 项")

        if report['details']:
            print("\n📋 Top 内容预览:")
            for category, items in report['details'].items():
                if items:
                    print(f"\n{category.upper()}:")
                    for item in items:
                        print(f"  • {item['content']}")
                        print(f"    重要性: {item['importance']:.2f} | 日期: {item['date']}")


if __name__ == "__main__":
    main()
