#!/usr/bin/env python3
"""章节大纲生成器 - 基于15节拍系统生成小说章节大纲"""

from pathlib import Path
from typing import Any
import argparse
import yaml
import re
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn


console = Console()


class ChapterOutliner:
    """章节大纲生成器核心类"""
    
    def __init__(self, book_dir: Path) -> None:
        """初始化出纲器
        
        Args:
            book_dir: 小说项目目录路径
        """
        self.book_dir = book_dir
        self.outline: dict[str, Any] | None = None
        self.style: dict[str, Any] | None = None
        self.characters: list[dict[str, Any]] = []
        self._load_project_files()
    
    def _load_project_files(self) -> None:
        """加载项目文件：outline.md, style.yml, characters/"""
        console.print("[bold blue]正在加载项目文件...[/bold blue]")
        
        outline_path = self.book_dir / "outline.md"
        if outline_path.exists():
            self.outline = self._parse_outline(outline_path)
            console.print(f"✓ 已加载大纲文件: [green]{outline_path}[/green]")
        else:
            console.print(f"⚠ 大纲文件不存在: [yellow]{outline_path}[/yellow]")
        
        style_path = self.book_dir / "style.yml"
        if style_path.exists():
            with open(style_path, "r", encoding="utf-8") as f:
                self.style = yaml.safe_load(f)
            console.print(f"✓ 已加载风格文件: [green]{style_path}[/green]")
        else:
            console.print(f"⚠ 风格文件不存在: [yellow]{style_path}[/yellow]")
        
        chars_dir = self.book_dir / "characters"
        if chars_dir.exists():
            self._load_characters(chars_dir)
        else:
            console.print(f"ℹ 角色目录不存在: [dim]{chars_dir}[/dim]")
    
    def _parse_outline(self, path: Path) -> dict[str, Any]:
        """解析 outline.md 文件
        
        期待格式:
        # 小说标题
        
        ## 章节
        ### 第1章
        - 章节概述
        
        ### 第2章
        - 章节概述
        """
        content = path.read_text(encoding="utf-8")
        
        chapters = re.findall(r"### 第(\d+)章\s*\n(.*?)(?=### 第\d+章|$)", content, re.DOTALL)
        
        return {
            "chapters": [
                {"number": int(ch_num), "summary": summary.strip()}
                for ch_num, summary in chapters
            ],
            "raw": content
        }
    
    def _load_characters(self, chars_dir: Path) -> None:
        """加载角色文件"""
        for char_file in chars_dir.glob("*.yml"):
            try:
                with open(char_file, "r", encoding="utf-8") as f:
                    char_data = yaml.safe_load(f)
                    char_data["file"] = char_file.name
                    self.characters.append(char_data)
            except Exception as e:
                console.print(f"⚠ 角色文件加载失败 {char_file.name}: [yellow]{e}[/yellow]")
        
        if self.characters:
            console.print(f"✓ 已加载 [cyan]{len(self.characters)}[/cyan] 个角色")
    
    def generate_chapter_outline(
        self,
        chapter_num: int,
        word_count: int = 3000
    ) -> dict[str, Any]:
        """生成指定章节的15节拍大纲
        
        Args:
            chapter_num: 章节编号
            word_count: 目标字数
            
        Returns:
            包含15节拍的大纲字典
        """
        console.print(f"\n[bold blue]正在生成第 [cyan]{chapter_num}[/cyan] 章大纲...[/bold blue]")
        
        chapter_info = None
        if self.outline and "chapters" in self.outline:
            for ch in self.outline["chapters"]:
                if ch["number"] == chapter_num:
                    chapter_info = ch
                    break
        
        if not chapter_info:
            chapter_info = {
                "number": chapter_num,
                "summary": f"第 {chapter_num} 章 - 待填充"
            }
        
        beats = self._create_beat_template(chapter_num, word_count, chapter_info)
        
        return {
            "chapter_num": chapter_num,
            "word_count": word_count,
            "base_summary": chapter_info.get("summary", ""),
            "beats": beats,
            "style_notes": self.style or {},
            "characters": self.characters
        }
    
    def _create_beat_template(
        self,
        chapter_num: int,
        word_count: int,
        chapter_info: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """创建15节拍模板
        
        15节拍系统:
        1-3: 铺垫阶段
        4-7: 转折阶段
        8-11: 高潮阶段
        12-15: 结局阶段
        """
        beats = []
        
        total_beat_count = 15
        
        for i in range(1, total_beat_count + 1):
            beat = self._create_single_beat(i, chapter_num, word_count, chapter_info)
            beats.append(beat)
        
        return beats
    
    def _create_single_beat(
        self,
        beat_num: int,
        chapter_num: int,
        word_count: int,
        chapter_info: dict[str, Any]
    ) -> dict[str, Any]:
        """创建单个节拍"""
        
        beat_info = self._get_beat_info(beat_num, chapter_num)
        
        word_allocation = self._allocate_words_for_beat(
            beat_num, word_count, beat_info["phase"]
        )
        
        return {
            "beat_number": beat_num,
            "beat_name": beat_info["name"],
            "phase": beat_info["phase"],
            "description": f"第{beat_num}节拍 - 待填充",
            "target_words": word_allocation,
            "purpose": beat_info["purpose"],
            "key_elements": [],
            "characters_involved": [],
            "plot_threads": [],
            "notes": ""
        }
    
    def _get_beat_info(self, beat_num: int, chapter_num: int) -> dict[str, str]:
        """获取节拍信息"""
        
        phases = {
            "铺垫": ["钩子", "设定", "context"],
            "转折": ["/inciting", "发展", "turning"],
            "高潮": ["对抗", "发展", "高潮", "转折"],
            "结局": ["解决", "收尾", "余韵"]
        }
        
        if beat_num <= 3:
            phase = "铺垫"
            name = phases["铺垫"][beat_num - 1] if beat_num - 1 < len(phases["铺垫"]) else f"铺垫-{beat_num}"
            purpose = "建立场景和基础信息"
        elif beat_num <= 7:
            phase = "转折"
            idx = beat_num - 4
            name = phases["转折"][idx] if idx < len(phases["转折"]) else f"转折-{beat_num}"
            purpose = "引入冲突和变化"
        elif beat_num <= 11:
            phase = "高潮"
            idx = beat_num - 8
            name = phases["高潮"][idx] if idx < len(phases["高潮"]) else f"高潮-{beat_num}"
            purpose = "升级冲突和紧张"
        else:
            phase = "结局"
            idx = beat_num - 12
            name = phases["结局"][idx] if idx < len(phases["结局"]) else f"结局-{beat_num}"
            purpose = "解决和收尾"
        
        return {
            "name": name,
            "phase": phase,
            "purpose": purpose
        }
    
    def _allocate_words_for_beat(
        self,
        beat_num: int,
        total_words: int,
        phase: str
    ) -> int:
        """为节拍分配字数"""
        
        phase_weights = {
            "铺垫": 0.15,
            "转折": 0.20,
            "高潮": 0.45,
            "结局": 0.20
        }
        
        phase_weight = phase_weights.get(phase, 0.20)
        base_words = int(total_words * phase_weight)
        
        beat_weights = {
            "铺垫": [0.3, 0.35, 0.35],
            "转折": [0.25, 0.25, 0.25, 0.25],
            "高潮": [0.20, 0.20, 0.20, 0.20, 0.20],
            "结局": [0.30, 0.35, 0.35]
        }
        
        beat_idx_map = {
            "铺垫": beat_num - 1,
            "转折": beat_num - 4,
            "高潮": beat_num - 8,
            "结局": beat_num - 12
        }
        
        beat_idx = beat_idx_map.get(phase, 0)
        beat_weights_list = beat_weights.get(phase, [1.0])
        
        if beat_idx < len(beat_weights_list):
            return int(base_words * beat_weights_list[beat_idx])
        else:
            return base_words // len(beat_weights_list)
    
    def format_output_markdown(self, outline_data: dict[str, Any]) -> str:
        """格式化输出为 Markdown"""
        
        lines = []
        
        lines.append(f"# 第 {outline_data['chapter_num']} 章 大纲")
        lines.append("")
        lines.append(f"**字数目标**: {outline_data['word_count']} 字")
        lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        if outline_data.get("base_summary"):
            lines.append("## 章节概述")
            lines.append(outline_data["base_summary"])
            lines.append("")
        
        lines.append("## 15节拍大纲")
        lines.append("")
        
        for beat in outline_data["beats"]:
            lines.append(f"### {beat['beat_number']}. {beat['beat_name']} ({beat['phase']})")
            lines.append("")
            lines.append(f"**目标字数**: {beat['target_words']} 字")
            lines.append(f"**目的**: {beat['purpose']}")
            lines.append("")
            lines.append(f"{beat['description']}")
            lines.append("")
            
            if beat['key_elements']:
                lines.append("**关键元素**:")
                for elem in beat['key_elements']:
                    lines.append(f"- {elem}")
                lines.append("")
            
            if beat['characters_involved']:
                lines.append("**涉及角色**:")
                for char in beat['characters_involved']:
                    lines.append(f"- {char}")
                lines.append("")
            
            if beat['plot_threads']:
                lines.append("**情节线索**:")
                for thread in beat['plot_threads']:
                    lines.append(f"- {thread}")
                lines.append("")
            
            if beat['notes']:
                lines.append("**备注**: ")
                lines.append(beat['notes'])
                lines.append("")
        
        if outline_data.get("characters"):
            lines.append("## 角色参考")
            lines.append("")
            for char in outline_data['characters']:
                name = char.get('name', '未知角色')
                description = char.get('description', '')[:100]
                lines.append(f"### {name}")
                lines.append(f"{description}...")
                lines.append("")
        
        return "\n".join(lines)
    
    def display_outline(self, outline_data: dict[str, Any]) -> None:
        """使用 Rich 美化显示大纲"""
        
        console.print(Panel(
            f"[bold cyan]第 {outline_data['chapter_num']} 章[/bold cyan]\n"
            f"字数目标: [bold]{outline_data['word_count']}[/bold] 字\n"
            f"节拍数量: [bold]15[/bold] 个",
            title="章节大纲生成完成",
            border_style="green"
        ))
        
        table = Table(title="15节拍概览")
        table.add_column("节拍", style="cyan")
        table.add_column("名称", style="magenta")
        table.add_column("阶段", style=" green")
        table.add_column("目标字数", style="yellow")
        
        for beat in outline_data["beats"]:
            table.add_row(
                str(beat["beat_number"]),
                beat["beat_name"],
                beat["phase"],
                str(beat["target_words"])
            )
        
        console.print(table)
        
        if outline_data.get("characters"):
            console.print(f"\n[bold blue]角色参考 ([cyan]{len(outline_data['characters'])}[/cyan] 位):[/bold blue]")
            for char in outline_data["characters"][:5]:
                name = char.get("name", "未知")
                console.print(f"  • [cyan]{name}[/cyan]")
            if len(outline_data["characters"]) > 5:
                console.print(f"  ... 还有 [cyan]{len(outline_data['characters']) - 5}[/cyan] 个角色")


def create_arg_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    
    parser = argparse.ArgumentParser(
        description="章节大纲生成器 - 基于15节拍系统生成小说章节大纲",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python generate_outline.py --book-dir ./my-novel --chapter 1 --word-count 5000
  python generate_outline.py -d ./project -c 5 -w 3000 -o output.md
        """
    )
    
    parser.add_argument(
        "--book-dir", "-d",
        type=str,
        required=True,
        help="小说项目目录路径"
    )
    
    parser.add_argument(
        "--chapter", "-c",
        type=int,
        required=True,
        help="章节编号"
    )
    
    parser.add_argument(
        "--word-count", "-w",
        type=int,
        default=3000,
        help="目标字数 (默认: 3000)"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="输出文件路径 (缺省则只显示不保存)"
    )
    
    return parser


def main() -> None:
    """主函数"""
    
    parser = create_arg_parser()
    args = parser.parse_args()
    
    book_dir = Path(args.book_dir)
    
    if not book_dir.exists():
        console.print(f"[bold red]错误: 项目目录不存在[/bold red]: [yellow]{book_dir}[/yellow]")
        return
    
    if not book_dir.is_dir():
        console.print(f"[bold red]错误: 路径不是目录[/bold red]: [yellow]{book_dir}[/yellow]")
        return
    
    try:
        with Progress(
            SpinnerColumn(),
            BarColumn(),
            "[progress.description]{task.description}",
            transient=True
        ) as progress:
            progress.add_task("初始化出纲器...", total=None)
            outliner = ChapterOutliner(book_dir)
        
        outline_data = outliner.generate_chapter_outline(
            chapter_num=args.chapter,
            word_count=args.word_count
        )
        
        outliner.display_outline(outline_data)
        
        markdown_output = outliner.format_output_markdown(outline_data)
        
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(markdown_output, encoding="utf-8")
            console.print(f"\n[bold green]大纲已保存至:[/bold green] [cyan]{output_path}[/cyan]")
        else:
            console.print("\n" + "=" * 60)
            console.print("[bold]Markdown 输出:[/bold]")
            console.print("-" * 60)
            console.print(markdown_output)
            console.print("-" * 60)
            console.print("\n[bold yellow]提示: 使用 --output 参数保存到文件[/bold yellow]")
    
    except KeyboardInterrupt:
        console.print("\n[bold yellow]操作已取消[/bold yellow]")
    except Exception as e:
        console.print(f"[bold red]发生错误:[/bold red] [yellow]{e}[/yellow]")
        raise


if __name__ == "__main__":
    main()
