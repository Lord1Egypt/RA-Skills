#!/usr/bin/env python3
"""伏笔追踪器 - Foreshadowing Tracker

用于识别、追踪和报告小说中的伏笔。
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich.table import Table
from rich.text import Text


console = Console()


class Foreshadowing:
    """伏笔类"""

    def __init__(
        self,
        text: str,
        chapter: int,
        location: int,
        hint_type: str,
        pattern_key: str,
        confidence: float = 1.0,
        is_recycled: bool = False,
        recycled_chapter: int | None = None,
        recycled_location: int | None = None,
        explanation: str = "",
    ):
        self.text = text
        self.chapter = chapter
        self.location = location
        self.hint_type = hint_type
        self.pattern_key = pattern_key
        self.confidence = confidence
        self.is_recycled = is_recycled
        self.recycled_chapter = recycled_chapter
        self.recycled_location = recycled_location
        self.explanation = explanation

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "chapter": self.chapter,
            "location": self.location,
            "hint_type": self.hint_type,
            "pattern_key": self.pattern_key,
            "confidence": round(self.confidence, 3),
            "is_recycled": self.is_recycled,
            "recycled_chapter": self.recycled_chapter,
            "recycled_location": self.recycled_location,
            "explanation": self.explanation,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Foreshadowing":
        return cls(
            text=data["text"],
            chapter=data["chapter"],
            location=data["location"],
            hint_type=data["hint_type"],
            pattern_key=data.get("pattern_key", "unknown"),
            confidence=data.get("confidence", 1.0),
            is_recycled=data.get("is_recycled", False),
            recycled_chapter=data.get("recycled_chapter"),
            recycled_location=data.get("recycled_location"),
            explanation=data.get("explanation", ""),
        )


class ForeshadowingTracker:
    """伏笔追踪器"""

    # 伏笔模式定义：模式名 -> (正则表达式, 描述)
    HINT_PATTERNS: dict[str, list[tuple[str, str]]] = {
        "suspense": [
            # 疑惑与不确定 (1-10)
            (r"似乎[只]?有[我他她它].*知道", "独自知晓的秘密"),
            (r"不知道[为什什么].*", "困惑与疑惑"),
            (r"总觉得.*要发生", "预感即将发生"),
            (r"隐约.*不祥", "不祥预感"),
            (r"似乎.*着什么", "隐约察觉"),
            (r"这.*绝不简单", "事有蹊跷"),
            (r"背后.*有.*原因", "背后隐情"),
            (r"[可是然而但是]，谁.*知道呢", "不确定的反问"),
            (r"心中.*疑惑", "内心疑惑"),
            (r"有些.*不对[劲经]", "直觉警觉"),
            # 隐藏信息 (11-20)
            (r"没有说.*真相", "隐瞒真相"),
            (r"隐瞒.*事实", "刻意隐瞒"),
            (r"隐瞒.*真相", "隐藏真相"),
            (r"眼中闪过.*异样", "神色异常"),
            (r"眼中闪过.*复杂", "复杂神情"),
            (r"欲言又止", "欲言又止"),
            (r"欲言.*止", "欲言又止"),
            (r"话到嘴边.*咽了回去", "话语中断"),
            (r"话中有话", "话中有深意"),
            (r"意有所指", "暗示意味"),
            # 异常迹象 (21-30)
            (r"奇怪的是", "异常情况"),
            (r"不寻常的", "不寻常之处"),
            (r"似乎.*故意", "刻意为之"),
            (r"故意.*隐瞒", "刻意隐瞒"),
            (r"有些.*古怪", "古怪之处"),
            (r"令人.*费解", "难以理解"),
            (r"匪夷所思", "不可思议"),
            (r"隐隐约约.*感觉", "模糊感觉"),
            (r"心中.*不安", "不安预感"),
            (r"不妙的感觉", "不祥预感"),
        ],
        "foreshadowing": [
            # 时间预告 (31-40)
            (r"此时.*还不.*知道", "时机未到"),
            (r"多年.*后才明白", "事后领悟"),
            (r"那时.*还年轻", "年轻无知"),
            (r"说.*时，.*不.*懂", "当时不懂"),
            (r"这.*后来.*关键", "关键伏笔"),
            (r"日后.*会.*明白", "日后领悟"),
            (r"等到.*的时候", "时机等待"),
            (r"当时.*没有.*意识到", "未曾察觉"),
            (r"后来.*才知道", "后知后觉"),
            (r"那时.*不懂得", "当时不懂"),
            # 命运暗示 (41-50)
            (r"命运的.*安排", "命运安排"),
            (r"命中注定", "命运注定"),
            (r"一切.*早已.*注定", "宿命暗示"),
            (r"似乎.*有.*安排", "暗中安排"),
            (r"不知道.*等待.*什么", "未知等待"),
            (r"那.*会成为.*转折点", "转折预示"),
            (r"日后.*证明", "日后证明"),
            (r"这将.*影响.*一生", "人生影响"),
            (r"埋下.*伏笔", "明确伏笔"),
            (r"埋下.*种子", "伏笔种子"),
        ],
        "callback": [
            # 回收验证 (51-60)
            (r"后来.*证实.*这.*原因", "事后证实"),
            (r"之前.*说过.*这", "前文呼应"),
            (r"终于明白.*当时.*为什么", "恍然大悟"),
            (r"这一切.*是因为.*之前", "因果揭示"),
            (r"原来.*那时", "原来如此"),
            (r"终于.*明白.*当年", "事后明白"),
            (r"终于.*明白.*那时", "事后明白"),
            (r"正是.*当年", "往事呼应"),
            (r"正是.*那时", "往事呼应"),
            (r"回想起.*当年", "回忆往昔"),
            # 线索串联 (61-70)
            (r"原来如此", "真相大白"),
            (r"真相.*大白", "真相揭示"),
            (r"恍然大悟", "顿悟时刻"),
            (r"一切都.*说.*通了", "线索贯通"),
            (r"终于.*揭开.*谜底", "谜底揭晓"),
            (r"原来.*就是", "身份揭示"),
            (r"一切.*真相.*揭开", "真相揭开"),
            (r"往事.*浮上心头", "往事回忆"),
            (r"那.*正是.*关键", "关键揭示"),
            (r"终于.*证实", "最终证实"),
        ],
        "symbolic": [
            # 象征物品 (71-78)
            (r"那[个只]物件.*一直.*保存", "重要物品"),
            (r"祖传.*之物", "传承之物"),
            (r"这是.*信物", "信物象征"),
            (r"那[个只]物品.*有.*故事", "物品故事"),
            (r"珍藏.*多年", "珍藏之物"),
            (r"从不离身", "重要物品"),
            (r"神秘.*礼物", "神秘礼物"),
            (r"奇怪.*标记", "神秘标记"),
        ],
        "prophecy": [
            # 预言暗示 (79-86)
            (r"预言.*说", "预言引用"),
            (r"据说.*将来", "传闻预言"),
            (r"老[人辈]说.*将来", "长辈预言"),
            (r"古人.*预言", "古老预言"),
            (r"传说.*会有", "传说预言"),
            (r"天命.*注定", "天命注定"),
            (r"星象.*显示", "星象预言"),
            (r"占卜.*结果", "占卜预言"),
        ],
        "mystery": [
            # 神秘悬念 (87-94)
            (r"神秘的.*人", "神秘人物"),
            (r"身份.*成谜", "身份谜团"),
            (r"来历不明", "来历不明"),
            (r"没有.*人.*知道", "无人知晓"),
            (r"一直是.*谜", "持续谜团"),
            (r"这.*是个谜", "谜团"),
            (r"谜一般的", "神秘莫测"),
            (r"不为人知的.*秘密", "隐藏秘密"),
        ],
        "contrast": [
            # 对比反衬 (95-100)
            (r"却.*不知道", "对比无知"),
            (r"殊不知", "殊不知"),
            (r"却不知.*已经", "未知变化"),
            (r"然而.*真相", "真相反转"),
            (r"表面上.*实际上", "表里不一"),
            (r"看似.*其实", "真相隐藏"),
        ],
    }

    # 置信度权重：模式键 -> 权重 (0.0-1.0)
    CONFIDENCE_WEIGHTS: dict[str, float] = {
        # 明确伏笔关键词，高置信度
        "埋下.*伏笔": 0.95,
        "埋下.*种子": 0.90,
        "这.*后来.*关键": 0.92,
        "那.*会成为.*转折点": 0.88,
        "日后.*证明": 0.85,
        "多年.*后才明白": 0.85,
        "后来.*才知道": 0.82,
        "终于明白.*当时.*为什么": 0.90,
        "原来.*那时": 0.85,
        # 预言类，高置信度
        "预言.*说": 0.88,
        "天命.*注定": 0.85,
        "命中注定": 0.82,
        # 回收验证类，高置信度
        "后来.*证实.*这.*原因": 0.95,
        "终于.*揭开.*谜底": 0.90,
        "原来.*就是": 0.88,
        "真相.*大白": 0.90,
        "恍然大悟": 0.85,
        # 象征物品类，中高置信度
        "祖传.*之物": 0.78,
        "这是.*信物": 0.80,
        "从不离身": 0.75,
        "珍藏.*多年": 0.72,
        # 神秘类，中等置信度
        "神秘的.*人": 0.70,
        "身份.*成谜": 0.72,
        "来历不明": 0.68,
        "一直是.*谜": 0.70,
        # 悬念类，中等置信度
        "似乎[只]?有[我他她它].*知道": 0.72,
        "背后.*有.*原因": 0.68,
        "这.*绝不简单": 0.65,
        "有些.*不对[劲经]": 0.60,
        "心中.*不安": 0.58,
        "隐约.*不祥": 0.62,
        # 时间预告类，中高置信度
        "此时.*还不.*知道": 0.80,
        "当时.*没有.*意识到": 0.75,
        "日后.*会.*明白": 0.78,
        "那时.*还年轻": 0.70,
        "说.*时，.*不.*懂": 0.72,
        # 命运暗示类，中高置信度
        "命运的.*安排": 0.75,
        "一切.*早已.*注定": 0.78,
        # 对比反衬类，中等置信度
        "却.*不知道": 0.65,
        "殊不知": 0.68,
        "看似.*其实": 0.62,
        "表面上.*实际上": 0.60,
        # 异常迹象类，中等置信度
        "奇怪的是": 0.55,
        "不寻常的": 0.58,
        "有些.*古怪": 0.52,
        "令人.*费解": 0.50,
        # 隐藏信息类，中等置信度
        "欲言又止": 0.60,
        "话中有话": 0.65,
        "意有所指": 0.62,
        "眼中闪过.*异样": 0.58,
        "隐瞒.*真相": 0.68,
        # 困惑类，较低置信度
        "不知道[为什什么].*": 0.45,
        "总觉得.*要发生": 0.48,
        "心中.*疑惑": 0.42,
        # 默认模式
        "default": 0.50,
    }

    def __init__(self):
        self.foreshadowings: list[Foreshadowing] = []
        self._seen_texts: dict[tuple[str, int], bool] = {}  # 用于去重

    def _get_confidence(self, pattern_key: str, text: str) -> float:
        """计算伏笔置信度

        基于模式权重和文本特征综合计算
        """
        # 基础权重
        base_weight = self.CONFIDENCE_WEIGHTS.get(
            pattern_key, self.CONFIDENCE_WEIGHTS["default"]
        )

        # 文本长度加成 (适中长度的伏笔更可靠)
        text_len = len(text)
        if 5 <= text_len <= 20:
            length_bonus = 0.05
        elif 20 < text_len <= 40:
            length_bonus = 0.02
        else:
            length_bonus = 0.0

        # 关键词加成
        keyword_bonus = 0.0
        strong_keywords = ["伏笔", "注定", "预言", "后来", "终于", "原来", "真相"]
        for keyword in strong_keywords:
            if keyword in text:
                keyword_bonus += 0.03

        # 计算最终置信度，确保在 0-1 范围内
        confidence = min(1.0, max(0.0, base_weight + length_bonus + keyword_bonus))

        return round(confidence, 3)

    def load_existing(self, file_path: Path) -> None:
        """加载已记录的伏笔"""
        if not file_path.exists():
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data.get("foreshadowings", []):
                    fs = Foreshadowing.from_dict(item)
                    self.foreshadowings.append(fs)
                    self._seen_texts[(fs.text, fs.chapter)] = True
        except (json.JSONDecodeError, KeyError) as e:
            console.print(
                f"[yellow]警告: 读取伏笔记录失败 {file_path}: {e}[/yellow]"
            )

    def extract_hints(self, text: str, chapter: int) -> list[Foreshadowing]:
        """从文本中提取伏笔线索"""
        foreshadowings = []

        lines = text.split("\n")
        for line_num, line in enumerate(lines):
            for hint_type, patterns in self.HINT_PATTERNS.items():
                for pattern, description in patterns:
                    try:
                        matches = re.finditer(pattern, line)
                        for match in matches:
                            pattern_key = pattern
                            confidence = self._get_confidence(
                                pattern_key, match.group(0)
                            )

                            foreshadowings.append(
                                Foreshadowing(
                                    text=match.group(0),
                                    chapter=chapter,
                                    location=line_num,
                                    hint_type=hint_type,
                                    pattern_key=pattern_key,
                                    confidence=confidence,
                                    is_recycled=False,
                                )
                            )
                    except re.error:
                        # 忽略无效的正则表达式
                        continue

        return foreshadowings

    def detect_recycling(self, text: str, chapter: int) -> dict[int, bool]:
        """检测已存在的伏笔是否被回收"""
        recycling_map = {}

        for idx, fs in enumerate(self.foreshadowings):
            if fs.is_recycled:
                continue

            if re.search(re.escape(fs.text), text):
                recycling_map[idx] = True
            elif self._match_context(fs.text, text):
                recycling_map[idx] = True

        return recycling_map

    def _match_context(self, hint_text: str, chapter_text: str) -> bool:
        """通过上下文匹配检测伏笔回收"""
        hint_lower = hint_text.lower()

        recycling_keywords = [
            "证实",
            "证明",
            "原来",
            "竟然是",
            "终于明白",
            "正是此时",
            "一切揭晓",
            "真相大白",
            "恍然大悟",
            "当年那个",
            "此刻",
            "多年后",
            "回忆起",
        ]

        for keyword in recycling_keywords:
            if keyword in chapter_text and hint_lower in chapter_text.lower():
                return True

        return False

    def process_chapter(
        self, chapter_path: Path, chapter_num: int
    ) -> list[Foreshadowing]:
        """处理单个章节"""
        console.print(f"[bold blue]处理章节: {chapter_path.name}[/bold blue]")

        foreshadowings = []

        try:
            with open(chapter_path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            console.print(f"[red]错误: 无法读取章节 {chapter_path}: {e}[/red]")
            return foreshadowings

        new_hints = self.extract_hints(text, chapter_num)
        foreshadowings.extend(new_hints)

        recycling_map = self.detect_recycling(text, chapter_num)

        for idx, is_recycled in recycling_map.items():
            if is_recycled and idx < len(self.foreshadowings):
                self.foreshadowings[idx].is_recycled = True
                self.foreshadowings[idx].recycled_chapter = chapter_num
                self.foreshadowings[idx].recycled_location = (
                    0  # 需要进一步分析确定具体位置
                )

        return foreshadowings

    def process_book(
        self, book_dir: Path, chapter_file: str | None = None
    ) -> list[Foreshadowing]:
        """处理整本书"""
        all_new_foreshadowings: list[Foreshadowing] = []

        if chapter_file:
            chapter_path = book_dir / chapter_file
            if chapter_path.exists():
                new_foreshadowings = self.process_chapter(chapter_path, 1)
                all_new_foreshadowings.extend(new_foreshadowings)
            else:
                console.print(
                    f"[yellow]警告: 指定章节文件不存在: {chapter_path}[/yellow]"
                )
        else:
            chapters = sorted(book_dir.glob("chapter_*.txt"))

            with Progress() as progress:
                task = progress.add_task(
                    f"[cyan]处理书籍 {book_dir.name}...", total=len(chapters)
                )

                for i, chapter_path in enumerate(chapters, 1):
                    new_foreshadowings = self.process_chapter(chapter_path, i)
                    all_new_foreshadowings.extend(new_foreshadowings)
                    progress.update(task, advance=1)

        return all_new_foreshadowings

    def generate_report(self, output_path: Path) -> None:
        """生成伏笔追踪报告"""
        console.print("\n[bold underline]生成伏笔追踪报告[/bold underline]")

        new_foreshadowings = [
            fs
            for fs in self.foreshadowings
            if not fs.is_recycled and (fs.text, fs.chapter) not in self._seen_texts
        ]

        pending_foreshadowings = [
            fs for fs in self.foreshadowings if not fs.is_recycled
        ]

        recycled_foreshadowings = [
            fs for fs in self.foreshadowings if fs.is_recycled
        ]

        # 按置信度排序 (高到低)
        new_foreshadowings.sort(key=lambda x: x.confidence, reverse=True)
        pending_foreshadowings.sort(key=lambda x: x.confidence, reverse=True)
        recycled_foreshadowings.sort(key=lambda x: x.confidence, reverse=True)

        report_data = {
            "summary": {
                "total_foreshadowings": len(self.foreshadowings),
                "new_count": len(new_foreshadowings),
                "pending_count": len(pending_foreshadowings),
                "recycled_count": len(recycled_foreshadowings),
                "avg_confidence": (
                    round(
                        sum(fs.confidence for fs in self.foreshadowings)
                        / len(self.foreshadowings),
                        3,
                    )
                    if self.foreshadowings
                    else 0.0
                ),
            },
            "new": [fs.to_dict() for fs in new_foreshadowings],
            "pending": [fs.to_dict() for fs in pending_foreshadowings],
            "recycled": [fs.to_dict() for fs in recycled_foreshadowings],
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)

        self._print_report_dashboard(report_data)

    def _print_report_dashboard(self, report_data: dict[str, Any]) -> None:
        """打印报告仪表盘"""
        summary = report_data["summary"]

        console.print("\n" + "=" * 70)
        console.print(
            Panel.fit(
                Text.from_markup(
                    "[bold green]伏笔追踪报告[/bold green]\n"
                    f"新增: [cyan]{summary['new_count']}[/cyan] | "
                    f"待回收: [yellow]{summary['pending_count']}[/yellow] | "
                    f"已回收: [green]{summary['recycled_count']}[/green] | "
                    f"总计: [blue]{summary['total_foreshadowings']}[/blue] | "
                    f"平均置信度: [magenta]{summary['avg_confidence']:.2%}[/magenta]"
                ),
                title="统计概览",
            )
        )
        console.print("=" * 70)

        if report_data["new"]:
            table = Table(
                title="[bold cyan]新增伏笔[/bold cyan]",
                show_header=True,
                header_style="bold magenta",
            )
            table.add_column("置信度", style="magenta", justify="right")
            table.add_column("章节", style="cyan")
            table.add_column("位置", style="cyan")
            table.add_column("类型", style="yellow")
            table.add_column("伏笔内容", style="white")

            for fs in report_data["new"]:
                table.add_row(
                    f"{fs['confidence']:.2f}",
                    str(fs["chapter"]),
                    str(fs["location"]),
                    fs["hint_type"],
                    fs["text"][:50] + "..." if len(fs["text"]) > 50 else fs["text"],
                )

            console.print("\n")
            console.print(table)

        if report_data["pending"]:
            table = Table(
                title="[bold yellow]待回收伏笔[/bold yellow]",
                show_header=True,
                header_style="bold yellow",
            )
            table.add_column("置信度", style="magenta", justify="right")
            table.add_column("章节", style="cyan")
            table.add_column("类型", style="yellow")
            table.add_column("伏笔内容", style="white")

            for fs in report_data["pending"]:
                table.add_row(
                    f"{fs['confidence']:.2f}",
                    str(fs["chapter"]),
                    fs["hint_type"],
                    fs["text"][:50] + "..." if len(fs["text"]) > 50 else fs["text"],
                )

            console.print("\n")
            console.print(table)

        if report_data["recycled"]:
            table = Table(
                title="[bold green]已回收伏笔[/bold green]",
                show_header=True,
                header_style="bold green",
            )
            table.add_column("置信度", style="magenta", justify="right")
            table.add_column("原章节", style="cyan")
            table.add_column("回收章节", style="green")
            table.add_column("类型", style="yellow")
            table.add_column("伏笔内容", style="white")

            for fs in report_data["recycled"]:
                table.add_row(
                    f"{fs['confidence']:.2f}",
                    str(fs["chapter"]),
                    str(fs.get("recycled_chapter", "N/A")),
                    fs["hint_type"],
                    fs["text"][:50] + "..." if len(fs["text"]) > 50 else fs["text"],
                )

            console.print("\n")
            console.print(table)


def main() -> int:
    """主函数"""
    parser = argparse.ArgumentParser(
        description="伏笔追踪器 - 识别、追踪和报告小说中的伏笔"
    )
    parser.add_argument(
        "--book-dir",
        type=str,
        required=True,
        help="书籍目录路径",
    )
    parser.add_argument(
        "--chapter",
        type=str,
        default=None,
        help="指定章节文件名（可选）",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="输出报告文件路径",
    )
    parser.add_argument(
        "--record",
        type=str,
        default="foreshadowings.json",
        help="伏笔记录文件路径",
    )

    args = parser.parse_args()

    book_dir = Path(args.book_dir)
    output_path = Path(args.output)
    record_path = Path(args.record)

    if not book_dir.exists():
        console.print(f"[red]错误: 书籍目录不存在: {book_dir}[/red]")
        return 1

    tracker = ForeshadowingTracker()
    tracker.load_existing(record_path)

    new_foreshadowings = tracker.process_book(book_dir, args.chapter)

    tracker.foreshadowings.extend(new_foreshadowings)

    tracker.generate_report(output_path)

    with open(record_path, "w", encoding="utf-8") as f:
        json.dump(
            {"foreshadowings": [fs.to_dict() for fs in tracker.foreshadowings]},
            f,
            ensure_ascii=False,
            indent=2,
        )

    console.print(f"\n[green]报告已保存: {output_path}[/green]")
    console.print(f"[green]伏笔记录已更新: {record_path}[/green]")

    return 0


if __name__ == "__main__":
    sys.exit(main())