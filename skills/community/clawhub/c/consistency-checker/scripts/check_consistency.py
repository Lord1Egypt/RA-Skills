#!/usr/bin/env python3
"""小说一致性检查器：检测角色、特征、时间线、地点的一致性"""

import argparse
import re
from pathlib import Path
from typing import Any

import yaml
from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()


class Character:
    """角色档案类"""

    def __init__(self, name: str, data: dict[str, Any]):
        self.name = name
        self.aliases = data.get("aliases", [])
        self.features = data.get("features", {})
        self.biography = data.get("biography", "")
        self.origin = data.get("origin", "")

    def get_all_names(self) -> list[str]:
        """获取角色所有可能的名称"""
        all_names = [self.name] + self.aliases
        return all_names


class Chapter:
    """章节数据类"""

    def __init__(self, filepath: Path, content: str):
        self.filepath = filepath
        self.content = content
        self.chapter_num = self._extract_chapter_num()

    def _extract_chapter_num(self) -> int:
        """提取章节号"""
        match = re.search(
            r"第\s*([0-9零一二三四五六七八九十百千年]+)\s*章", self.content
        )
        if match:
            num_str = match.group(1)
            return self._chinese_to_int(num_str)
        return 0

    @staticmethod
    def _chinese_to_int(chinese_num: str) -> int:
        """中文数字转阿拉伯数字"""
        chinese_digits = {
            "零": 0,
            "一": 1,
            "二": 2,
            "三": 3,
            "四": 4,
            "五": 5,
            "六": 6,
            "七": 7,
            "八": 8,
            "九": 9,
            "十": 10,
            "百": 100,
            "千": 1000,
            "万": 10000,
        }
        result = 0
        temp = 0
        for char in chinese_num:
            if char in chinese_digits:
                if chinese_digits[char] >= 10:
                    if temp == 0:
                        temp = 1
                    result += temp * chinese_digits[char]
                    temp = 0
                else:
                    temp = chinese_digits[char]
        result += temp
        return result if result > 0 else 0


class TimelineAnalyzer:
    """时间线分析器：识别时间表达式、季节、年龄变化"""

    def __init__(self):
        self.time_expressions = {
            "duration": [
                (r"([0-9零一二三四五六七八九十百千年]+)\s*天", "day"),
                (r"([0-9零一二三四五六七八九十百千年]+)\s*小时", "hour"),
                (r"([0-9零一二三四五六七八九十百千年]+)\s*月", "month"),
                (r"([0-9零一二三四五六七八九十百千年]+)\s*年", "year"),
                (r"次\s*日", "day"),
                (r"三\s*天\s*后", "day"),
                (r"两\s*天\s*后", "day"),
                (r"当\s*日", "day"),
                (r"翌\s*日", "day"),
                (r"隔\s*日", "day"),
            ],
            "time_of_day": [
                (r"清晨|早上|早晨", "morning"),
                (r"上午|中午", "noon"),
                (r"下午|午后", "afternoon"),
                (r"傍晚|黄昏", "evening"),
                (r"晚上|夜晚|入夜", "night"),
                (r"子\s*时", "midnight"),
                (r"午\s*时", "noon"),
            ],
            "seasons": [
                (r"春\s*天|春季|春天", "spring"),
                (r"夏\s*天|夏季|夏天", "summer"),
                (r"秋\s*天|秋季|秋天|金秋", "autumn"),
                (r"冬天|冬季|寒冬", "winter"),
            ],
        }

        self.season_months = {
            "spring": [3, 4, 5],
            "summer": [6, 7, 8],
            "autumn": [9, 10, 11],
            "winter": [12, 1, 2],
        }

        self.time_weights = {
            "morning": 1,
            "noon": 2,
            "afternoon": 3,
            "evening": 4,
            "night": 5,
            "midnight": 6,
        }

    def _chinese_num_to_int(self, chinese_num: str) -> int:
        """中文数字转阿拉伯数字"""
        chinese_digits = {
            "零": 0,
            "一": 1,
            "二": 2,
            "三": 3,
            "四": 4,
            "五": 5,
            "六": 6,
            "七": 7,
            "八": 8,
            "九": 9,
            "十": 10,
            "百": 100,
            "千": 1000,
            "万": 10000,
        }
        result = 0
        temp = 0
        for char in chinese_num:
            if char in chinese_digits:
                if chinese_digits[char] >= 10:
                    if temp == 0:
                        temp = 1
                    result += temp * chinese_digits[char]
                    temp = 0
                else:
                    temp = chinese_digits[char]
        result += temp
        return result if result > 0 else 0

    def extract_time_expressions(self, text: str) -> list[dict[str, Any]]:
        """提取时间表达式"""
        results = []

        for expr_type, patterns in self.time_expressions.items():
            for pattern, time_type in patterns:
                matches = re.finditer(pattern, text)
                for match in matches:
                    if expr_type == "duration":
                        num_str = match.group(1)
                        if num_str:
                            num = self._chinese_num_to_int(num_str)
                        else:
                            num = 1
                        results.append(
                            {
                                "type": expr_type,
                                "subtype": time_type,
                                "value": num,
                                "text": match.group(0),
                                "position": match.start(),
                            }
                        )
                    else:
                        results.append(
                            {
                                "type": expr_type,
                                "subtype": time_type,
                                "value": 1,
                                "text": match.group(0),
                                "position": match.start(),
                            }
                        )

        results.sort(key=lambda x: x["position"])
        return results

    def detect_season(self, text: str) -> list[str]:
        """检测文本中的季节"""
        found_seasons = []
        for season_pattern, season in self.time_expressions["seasons"]:
            if re.search(season_pattern, text):
                found_seasons.append(season)
        return found_seasons

    def detect_season_from_date(self, month: int) -> str | None:
        """根据月份检测季节"""
        for season, months in self.season_months.items():
            if month in months:
                return season
        return None

    def extract_age_info(
        self, text: str, character_name: str, aliases: list[str]
    ) -> list[dict[str, Any]]:
        """提取角色年龄信息"""
        results = []
        all_names = [character_name] + aliases

        for name in all_names:
            patterns = [
                rf"{re.escape(name)}\s*(今年|岁数|年龄|年|有)\s*([0-9零一二三四五六七八九十百千年]+)\s*(岁|春秋|年)",
                rf"([0-9零一二三四五六七八九十百千年]+)\s*(岁|春秋|年)\s*的\s*{re.escape(name)}",
                rf"{re.escape(name)}\s*([0-9零一二三四五六七八九十百千年]+)\s*(岁|春秋|年)",
            ]

            for pattern in patterns:
                matches = re.finditer(pattern, text)
                for match in matches:
                    age_match = re.search(
                        r"([0-9零一二三四五六七八九十百千年]+)", match.group(0)
                    )
                    if age_match:
                        age = self._chinese_num_to_int(age_match.group(1))
                        results.append(
                            {
                                "character": character_name,
                                "age": age,
                                "text": match.group(0),
                                "position": match.start(),
                            }
                        )

        return results

    def check_season_contradiction(self, chapter1: Chapter, chapter2: Chapter) -> bool:
        """检查两章之间是否存在季节矛盾"""
        seasons1 = []
        seasons2 = []

        for chapter, seasons in [(chapter1, seasons1), (chapter2, seasons2)]:
            for pattern, season in self.time_expressions["seasons"]:
                if re.search(pattern, chapter.content):
                    seasons.append(season)

        if seasons1 and seasons2:
            if seasons1[0] != seasons2[0]:
                return True
        return False

    def check_age_consistency(
        self, ages: list[dict[str, Any]], chapter_num: int
    ) -> list[dict[str, Any]]:
        """检查年龄变化是否合理"""
        issues = []

        if len(ages) < 2:
            return issues

        for i in range(len(ages) - 1):
            current = ages[i]
            next_age = ages[i + 1]

            if current["character"] != next_age["character"]:
                continue

            age_diff = next_age["age"] - current["age"]

            if age_diff < 0:
                issues.append(
                    {
                        "type": "age_regression",
                        "chapter": chapter_num,
                        "character": current["character"],
                        "old_age": current["age"],
                        "new_age": next_age["age"],
                        "context": f"年龄从 {current['age']} 岁减少到 {next_age['age']} 岁",
                    }
                )
            elif age_diff > 100:
                issues.append(
                    {
                        "type": "age_inconsistency",
                        "chapter": chapter_num,
                        "character": current["character"],
                        "old_age": current["age"],
                        "new_age": next_age["age"],
                        "context": f"年龄增加 {age_diff} 岁，变化过大",
                    }
                )

        return issues


class ConsistencyChecker:
    """一致性检查器主类"""

    def __init__(self, book_dir: Path):
        self.book_dir = Path(book_dir)
        self.characters: dict[str, Character] = {}
        self.chapters: list[Chapter] = []
        self.issues: list[dict[str, Any]] = []
        self.timeline_analyzer = TimelineAnalyzer()

        self._load_characters()
        self._load_chapters()

    def _load_characters(self) -> None:
        """加载角色档案"""
        characters_dir = self.book_dir / "characters"
        if not characters_dir.exists():
            return

        for yml_file in characters_dir.glob("*.yml"):
            try:
                with open(yml_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    if data:
                        name = data.get("name", yml_file.stem)
                        self.characters[name] = Character(name, data)
            except Exception as e:
                console.print(
                    f"[yellow]警告: 加载角色文件 {yml_file} 失败: {e}[/yellow]"
                )

    def _load_chapters(self) -> None:
        """加载章节正文"""
        chapters_dir = self.book_dir / "chapters"
        if not chapters_dir.exists():
            return

        for txt_file in sorted(chapters_dir.glob("*.txt")):
            try:
                with open(txt_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    self.chapters.append(Chapter(txt_file, content))
            except Exception as e:
                console.print(
                    f"[yellow]警告: 加载章节文件 {txt_file} 失败: {e}[/yellow]"
                )

    def check_name_consistency(self) -> None:
        """检查角色名称一致性"""
        for chapter in self.chapters:
            for char_name, character in self.characters.items():
                for alias in character.get_all_names():
                    if alias != char_name:
                        pattern = re.compile(rf"\b{re.escape(alias)}\b")
                        if pattern.search(chapter.content):
                            self.issues.append(
                                {
                                    "type": "name_inconsistency",
                                    "chapter": chapter.chapter_num,
                                    "chapter_file": chapter.filepath.name,
                                    "character": char_name,
                                    "detected": alias,
                                    "actual": char_name,
                                    "context": self._get_context(
                                        chapter.content, alias
                                    ),
                                }
                            )

    def check_feature_contradictions(self) -> None:
        """检查角色特征矛盾"""
        for char_name, character in self.characters.items():
            features = character.features

            for chapter in self.chapters:
                content = chapter.content
                for feature_name, expected_value in features.items():
                    if expected_value:
                        pattern = re.compile(
                            rf"\b{re.escape(expected_value)}\b", re.IGNORECASE
                        )
                        if not pattern.search(content):
                            continue

                        for other_feature, other_value in features.items():
                            if other_feature != feature_name and other_value:
                                if re.compile(
                                    rf"\b{re.escape(other_value)}\b", re.IGNORECASE
                                ).search(content):
                                    self.issues.append(
                                        {
                                            "type": "feature_contradiction",
                                            "chapter": chapter.chapter_num,
                                            "chapter_file": chapter.filepath.name,
                                            "character": char_name,
                                            "feature1": feature_name,
                                            "value1": expected_value,
                                            "feature2": other_feature,
                                            "value2": other_value,
                                            "context": self._get_context(
                                                content, expected_value
                                            ),
                                        }
                                    )

    def check_timeline_conflicts(self) -> None:
        """检查时间线混乱"""
        if len(self.chapters) < 2:
            return

        for i in range(len(self.chapters) - 1):
            current = self.chapters[i]
            next_ch = self.chapters[i + 1]

            if current.chapter_num > next_ch.chapter_num:
                self.issues.append(
                    {
                        "type": "timeline_conflict",
                        "chapter": current.chapter_num,
                        "chapter_file": current.filepath.name,
                        "next_chapter": next_ch.chapter_num,
                        "next_chapter_file": next_ch.filepath.name,
                        "issue": "章节顺序与章节号不匹配",
                    }
                )

    def check_location_conflicts(self) -> None:
        """检查地点矛盾"""
        location_keywords = {
            "室内": ["室内", "房间里", "屋内", "堂屋", "卧室", "书房"],
            "室外": ["室外", "野外", "街道", "集市"],
        }

        for chapter in self.chapters:
            for loc_type, keywords in location_keywords.items():
                found = []
                for keyword in keywords:
                    if keyword in chapter.content:
                        found.append(keyword)

                if len(found) > 1:
                    self.issues.append(
                        {
                            "type": "location_conflict",
                            "chapter": chapter.chapter_num,
                            "chapter_file": chapter.filepath.name,
                            "location_type": loc_type,
                            "keywords": found,
                            "context": self._get_context(chapter.content, found[0]),
                        }
                    )

    def check_time_expressions(self) -> None:
        """检查时间表达式一致性"""
        for chapter in self.chapters:
            time_exprs = self.timeline_analyzer.extract_time_expressions(
                chapter.content
            )

            for expr in time_exprs:
                if expr["type"] == "duration":
                    self.issues.append(
                        {
                            "type": "time_expression",
                            "chapter": chapter.chapter_num,
                            "chapter_file": chapter.filepath.name,
                            "time_type": "duration",
                            "expression": expr["text"],
                            "value": expr["value"],
                            "context": self._get_context(chapter.content, expr["text"]),
                        }
                    )
                elif expr["type"] == "time_of_day":
                    self.issues.append(
                        {
                            "type": "time_expression",
                            "chapter": chapter.chapter_num,
                            "chapter_file": chapter.filepath.name,
                            "time_type": "time_of_day",
                            "expression": expr["text"],
                            "value": expr["subtype"],
                            "context": self._get_context(chapter.content, expr["text"]),
                        }
                    )

    def check_season_contradictions(self) -> None:
        """检查季节矛盾"""
        if len(self.chapters) < 2:
            return

        for i in range(len(self.chapters) - 1):
            current = self.chapters[i]
            next_ch = self.chapters[i + 1]

            if self.timeline_analyzer.check_season_contradiction(current, next_ch):
                self.issues.append(
                    {
                        "type": "season_contradiction",
                        "chapter": current.chapter_num,
                        "chapter_file": current.filepath.name,
                        "next_chapter": next_ch.chapter_num,
                        "next_chapter_file": next_ch.filepath.name,
                        "context": "连续两章存在季节矛盾",
                    }
                )

    def check_age_changes(self) -> None:
        """检查角色年龄变化"""
        for char_name, character in self.characters.items():
            ages = []

            for chapter in self.chapters:
                chapter_ages = self.timeline_analyzer.extract_age_info(
                    chapter.content, char_name, character.get_all_names()
                )
                ages.extend(chapter_ages)

            if len(ages) >= 2:
                age_issues = self.timeline_analyzer.check_age_consistency(
                    ages, ages[0].get("position", 0)
                )
                for issue in age_issues:
                    issue["chapter"] = ages[0].get("position", 0)
                    issue["chapter_file"] = "N/A"
                    self.issues.append(issue)

    def _get_context(self, text: str, keyword: str, context_len: int = 30) -> str:
        """获取关键词上下文"""
        pos = text.find(keyword)
        if pos == -1:
            return ""

        start = max(0, pos - context_len)
        end = min(len(text), pos + len(keyword) + context_len)
        context = text[start:end].replace("\n", " ")
        return context[:100] + "..." if len(context) > 100 else context

    def check(self) -> list[dict[str, Any]]:
        """执行所有一致性检查"""
        self.check_name_consistency()
        self.check_feature_contradictions()
        self.check_timeline_conflicts()
        self.check_location_conflicts()
        self.check_time_expressions()
        self.check_season_contradictions()
        self.check_age_changes()
        return self.issues

    def generate_report(self, output_path: Path | None = None) -> str:
        """生成一致性报告"""
        self.check()

        table = Table(title="一致性检查报告", show_lines=True)
        table.add_column("类型", style="cyan")
        table.add_column("章节", style="magenta")
        table.add_column("角色/问题", style="yellow")
        table.add_column("详情", style="white")

        for issue in self.issues:
            issue_type = issue["type"]
            chapter_info = (
                f"第{issue['chapter']}章 ({issue.get('chapter_file', 'N/A')})"
            )

            if issue_type == "name_inconsistency":
                detail = f"别名 '{issue['detected']}' 应为 '{issue['actual']}'"
                character = issue["character"]
            elif issue_type == "feature_contradiction":
                detail = f"{issue['feature1']}: {issue['value1']} vs {issue['feature2']}: {issue['value2']}"
                character = issue["character"]
            elif issue_type == "timeline_conflict":
                detail = issue["issue"]
                character = f"{issue['chapter']} → {issue['next_chapter']}"
            elif issue_type == "location_conflict":
                detail = f"地点关键词冲突: {', '.join(issue['keywords'])}"
                character = "地点"
            elif issue_type == "time_expression":
                detail = f"时间表达式: {issue['expression']} ({issue['time_type']}:{issue['value']})"
                character = "时间"
            elif issue_type == "season_contradiction":
                detail = "季节矛盾: 连续两章季节不一致"
                character = f"{issue['chapter']} → {issue['next_chapter']}"
            elif issue_type == "age_regression":
                detail = f"年龄倒退: {issue['old_age']} → {issue['new_age']} 岁"
                character = issue["character"]
            elif issue_type == "age_inconsistency":
                detail = f"年龄异常: {issue['old_age']} → {issue['new_age']} 岁"
                character = issue["character"]
            else:
                detail = "未知问题"
                character = "N/A"

            table.add_row(issue_type, chapter_info, character, detail)

        report_text = Text()
        report_text.append("\n检查结果: ", style="bold")
        if self.issues:
            report_text.append(f"发现 {len(self.issues)} 个问题\n", style="red bold")
        else:
            report_text.append("一致✅\n", style="green bold")

        console.print(table)
        console.print(report_text)

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("一致性检查报告\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"发现问题总数: {len(self.issues)}\n\n")
                for issue in self.issues:
                    f.write(f"- 类型: {issue['type']}\n")
                    f.write(
                        f"  章节: 第{issue['chapter']}章 ({issue.get('chapter_file', 'N/A')})\n"
                    )
                    if "character" in issue:
                        f.write(f"  角色: {issue['character']}\n")
                    f.write(f"  详情: {issue.get('context', 'N/A')}\n\n")

        return report_text.plain


def main() -> None:
    """主函数"""
    parser = argparse.ArgumentParser(
        description="小说一致性检查器 - 检测角色、特征、时间线、地点、季节、年龄的一致性"
    )
    parser.add_argument(
        "--book-dir",
        type=str,
        required=True,
        help="小说目录路径（包含 characters/ 和 chapters/ 子目录）",
    )
    parser.add_argument(
        "--chapter", type=int, default=None, help="只检查指定章节（可选）"
    )
    parser.add_argument(
        "--output", type=str, default=None, help="输出报告文件路径（可选）"
    )

    args = parser.parse_args()

    book_dir = Path(args.book_dir)
    if not book_dir.exists():
        console.print(f"[red]错误: 小说目录不存在: {book_dir}[/red]")
        return
    if not book_dir.is_dir():
        console.print(f"[red]错误: 路径不是目录: {book_dir}[/red]")
        return

    checker = ConsistencyChecker(book_dir)

    if args.chapter is not None:
        original_count = len(checker.chapters)
        checker.chapters = [
            c for c in checker.chapters if c.chapter_num == args.chapter
        ]
        if original_count > 0 and len(checker.chapters) == 0:
            console.print(f"[yellow]警告: 未找到第 {args.chapter} 章[/yellow]")

    output_path = Path(args.output) if args.output else None
    if output_path and not output_path.parent.exists():
        console.print(f"[red]错误: 输出目录不存在: {output_path.parent}[/red]")
        return

    checker.generate_report(output_path)


if __name__ == "__main__":
    main()
