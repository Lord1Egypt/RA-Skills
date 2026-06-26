#!/usr/bin/env python3
"""
Event Manager - 小说事件管理工具

创建、编辑、查询事件档案，支持因果链、时间线、多线叙事追踪。
AutoNovel Writer v5.0 项目 - Architect 代理在 Phase 2 使用。
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.table import Table
from rich.traceback import install
import yaml

install()
console = Console()


class EventManagerError(Exception):
    """事件管理器自定义异常"""

    pass


class EventProfile:
    """事件档案数据模型"""

    SUPPORTED_TYPES = {
        "转折点": "改变故事方向的重大事件",
        "冲突": "角色间的对抗事件",
        "揭示": "揭露秘密或真相",
        "成长": "角色能力提升或心理成长",
        "相遇": "重要角色首次见面",
        "离别": "角色分离或死亡",
    }

    def __init__(self, data: dict[str, Any]):
        self.data = data
        self.validate()

    def validate(self) -> None:
        """验证事件档案数据"""
        required_fields = ["title", "type", "chapter"]
        for field in required_fields:
            if field not in self.data:
                raise EventManagerError(f"缺少必填字段: {field}")

        if self.data["type"] not in self.SUPPORTED_TYPES:
            raise EventManagerError(
                f"不支持的事件类型: {self.data['type']}. "
                f"支持的类型: {', '.join(self.SUPPORTED_TYPES.keys())}"
            )

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return self.data.copy()

    def to_yaml(self) -> str:
        """转换为 YAML 字符串"""
        return yaml.dump(self.data, allow_unicode=True, default_flow_style=False)

    @classmethod
    def from_yaml(cls, yaml_str: str) -> "EventProfile":
        """从 YAML 字符串创建"""
        data = yaml.safe_load(yaml_str)
        return cls(data)

    @property
    def title(self) -> str:
        return self.data["title"]

    @property
    def event_type(self) -> str:
        return self.data["type"]

    @property
    def chapter(self) -> int:
        return self.data["chapter"]


class EventManager:
    """事件管理器主类"""

    def __init__(self, project_dir: Path | None = None):
        self.project_dir = project_dir or Path.cwd()
        self.events_dir = self.project_dir / "events"
        self.templates_dir = Path(__file__).parent.parent / "configs"

    def ensure_events_dir(self) -> None:
        """确保事件目录存在"""
        self.events_dir.mkdir(parents=True, exist_ok=True)

    def create_event(
        self,
        title: str,
        event_type: str,
        chapter: int,
        output: str | None = None,
        template: str | None = None,
    ) -> EventProfile:
        """创建新事件档案"""
        self.ensure_events_dir()

        data: dict[str, Any] = {
            "title": title,
            "type": event_type,
            "chapter": chapter,
            "description": "",
            "causality": {"causes": [], "effects": []},
            "characters": [],
            "foreshadowing": [],
            "emotion_arc": {"start": "平静", "middle": "平静", "end": "平静"},
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        if template:
            template_path = self.templates_dir / f"{template}.yml"
            if template_path.exists():
                with open(template_path) as f:
                    template_data = yaml.safe_load(f)
                    data.update(template_data)

        profile = EventProfile(data)

        if output:
            output_file = Path(output)
            if not output_file.is_absolute():
                output_file = self.events_dir / output_file.name
        else:
            output_file = self.events_dir / f"{title}.yml"
        # 确保输出目录存在
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w") as f:
            f.write(profile.to_yaml())

        console.print(f"[green]✓ 事件档案已创建: {output_file}[/green]")
        return profile

    def list_events(self) -> list[EventProfile]:
        """列出所有事件"""
        self.ensure_events_dir()

        yaml_files = list(self.events_dir.glob("*.yml")) + list(
            self.events_dir.glob("*.yaml")
        )

        if not yaml_files:
            console.print("[yellow]没有找到事件档案[/yellow]")
            return []

        profiles = []
        for yaml_file in yaml_files:
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
                profiles.append(EventProfile(data))

        profiles.sort(key=lambda p: (p.chapter, p.title))

        table = Table(title="事件列表")
        table.add_column("章节", style="cyan")
        table.add_column("标题", style="magenta")
        table.add_column("类型", style="green")
        table.add_column("创建时间", style="yellow")

        for profile in profiles:
            table.add_row(
                str(profile.chapter),
                profile.title,
                profile.event_type,
                profile.data.get("created_at", "N/A"),
            )

        console.print(table)
        return profiles

    def query_event(self, title: str, show_chain: bool = False) -> EventProfile | None:
        """查询事件信息"""
        self.ensure_events_dir()

        yaml_files = list(self.events_dir.glob("*.yml")) + list(
            self.events_dir.glob("*.yaml")
        )

        for yaml_file in yaml_files:
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
                if data.get("title") == title:
                    profile = EventProfile(data)

                    console.print(f"\n[bold cyan]事件: {profile.title}[/bold cyan]")
                    console.print(f"[bold]类型:[/bold] {profile.event_type}")
                    console.print(f"[bold]章节:[/bold] {profile.chapter}")

                    if profile.data.get("description"):
                        console.print(
                            f"\n[bold]描述:[/bold]\n{profile.data['description']}"
                        )

                    if show_chain and profile.data.get("causality"):
                        self._print_causality_chain(profile.data["causality"])

                    return profile

        console.print(f"[red]未找到事件: {title}[/red]")
        return None

    def _print_causality_chain(self, causality: dict[str, Any]) -> None:
        """打印因果链可视化"""
        console.print("\n[bold yellow]因果链:[/bold yellow]")

        if causality.get("causes"):
            console.print("[green]原因:[/green]")
            for cause in causality["causes"]:
                console.print(f"  → {cause}")

        if causality.get("effects"):
            console.print("[red]结果:[/red]")
            for effect in causality["effects"]:
                console.print(f"  → {effect}")

    def update_event(self, title: str, **updates) -> EventProfile | None:
        """更新事件档案"""
        self.ensure_events_dir()

        yaml_files = list(self.events_dir.glob("*.yml")) + list(
            self.events_dir.glob("*.yaml")
        )

        for yaml_file in yaml_files:
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
                if data.get("title") == title:
                    data.update(updates)
                    data["updated_at"] = datetime.now().isoformat()

                    with open(yaml_file, "w") as f:
                        f.write(
                            yaml.dump(
                                data, allow_unicode=True, default_flow_style=False
                            )
                        )

                    console.print(f"[green]✓ 事件档案已更新: {yaml_file}[/green]")
                    return EventProfile(data)

        console.print(f"[red]未找到事件: {title}[/red]")
        return None

    def delete_event(self, title: str) -> bool:
        """删除事件档案"""
        self.ensure_events_dir()

        yaml_files = list(self.events_dir.glob("*.yml")) + list(
            self.events_dir.glob("*.yaml")
        )

        for yaml_file in yaml_files:
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
                if data.get("title") == title:
                    if console.input(f"确认删除事件 '{title}'? (y/N): ").lower() == "y":
                        yaml_file.unlink()
                        console.print(f"[red]✓ 事件已删除: {yaml_file}[/red]")
                        return True
                    else:
                        console.print("[yellow]删除已取消[/yellow]")
                        return False

        console.print(f"[red]未找到事件: {title}[/red]")
        return False

    def export_timeline(self, output: str) -> None:
        """导出事件时间线为 Markdown"""
        profiles = self.list_events()

        if not profiles:
            return

        output_path = Path(output)
        if output_path.is_absolute():
            md_file = output_path
        else:
            md_file = self.project_dir / output_path

        md_content = "# 事件时间线\n\n"
        md_content += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        md_content += "---\n\n"

        for profile in profiles:
            md_content += f"## 第 {profile.chapter} 章 - {profile.title}\n\n"
            md_content += f"**类型**: {profile.event_type}\n\n"

            if profile.data.get("description"):
                md_content += f"**描述**: {profile.data['description']}\n\n"

            if profile.data.get("characters"):
                md_content += "**参与角色**:\n"
                for char in profile.data["characters"]:
                    md_content += f"- {char.get('name', '未知')} ({char.get('role', '未知')}): {char.get('action', '')}\n"
                md_content += "\n"

            if profile.data.get("causality"):
                md_content += "**因果链**:\n"
                if profile.data["causality"].get("causes"):
                    md_content += (
                        "  - 原因: "
                        + ", ".join(profile.data["causality"]["causes"])
                        + "\n"
                    )
                if profile.data["causality"].get("effects"):
                    md_content += (
                        "  - 结果: "
                        + ", ".join(profile.data["causality"]["effects"])
                        + "\n"
                    )
                md_content += "\n"

            md_content += "---\n\n"

        with open(md_file, "w") as f:
            f.write(md_content)

        console.print(f"[green]✓ 时间线已导出: {md_file}[/green]")


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        prog="manage_events",
        description="Event Manager - 小说事件管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # create 命令
    create_parser = subparsers.add_parser("create", help="创建新事件档案")
    create_parser.add_argument("--title", required=True, help="事件标题")
    create_parser.add_argument(
        "--type",
        required=True,
        choices=EventProfile.SUPPORTED_TYPES.keys(),
        help="事件类型",
    )
    create_parser.add_argument("--chapter", type=int, required=True, help="章节号")
    create_parser.add_argument("--output", help="输出文件路径")
    create_parser.add_argument("--template", help="使用的模板名称")

    # list 命令
    list_parser = subparsers.add_parser("list", help="列出所有事件")
    list_parser.add_argument("--project", default=".", help="项目目录")

    # query 命令
    query_parser = subparsers.add_parser("query", help="查询事件信息")
    query_parser.add_argument("--title", required=True, help="事件标题")
    query_parser.add_argument("--project", default=".", help="项目目录")
    query_parser.add_argument("--show-chain", action="store_true", help="显示因果链")

    # update 命令
    update_parser = subparsers.add_parser("update", help="更新事件档案")
    update_parser.add_argument("--title", required=True, help="事件标题")
    update_parser.add_argument("--project", default=".", help="项目目录")
    update_parser.add_argument("--title-new", help="新标题")
    update_parser.add_argument("--chapter", type=int, help="新章节号")
    update_parser.add_argument("--description", help="新描述")

    # delete 命令
    delete_parser = subparsers.add_parser("delete", help="删除事件档案")
    delete_parser.add_argument("--title", required=True, help="事件标题")
    delete_parser.add_argument("--project", default=".", help="项目目录")

    # export 命令
    export_parser = subparsers.add_parser("export", help="导出事件时间线")
    export_parser.add_argument("--project", default=".", help="项目目录")
    export_parser.add_argument("--output", required=True, help="输出文件路径")

    return parser


def main() -> int:
    """主函数"""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        manager = EventManager(Path(args.project) if hasattr(args, "project") else None)

        if args.command == "create":
            manager.create_event(
                title=args.title,
                event_type=args.type,
                chapter=args.chapter,
                output=args.output,
                template=args.template,
            )

        elif args.command == "list":
            manager.list_events()

        elif args.command == "query":
            manager.query_event(args.title, show_chain=args.show_chain)

        elif args.command == "update":
            updates = {}
            if args.title_new:
                updates["title"] = args.title_new
            if args.chapter:
                updates["chapter"] = args.chapter
            if args.description:
                updates["description"] = args.description

            if not updates:
                console.print("[yellow]没有提供更新内容[/yellow]")
                return 1

            manager.update_event(args.title, **updates)

        elif args.command == "delete":
            manager.delete_event(args.title)

        elif args.command == "export":
            manager.export_timeline(args.output)

        return 0

    except EventManagerError as e:
        console.print(f"[red]错误: {e}[/red]")
        return 1
    except KeyboardInterrupt:
        console.print("\n[yellow]操作已取消[/yellow]")
        return 130
    except Exception as e:
        console.print(f"[red]未预期的错误: {e}[/red]")
        console.print_exception()
        return 1


if __name__ == "__main__":
    sys.exit(main())
