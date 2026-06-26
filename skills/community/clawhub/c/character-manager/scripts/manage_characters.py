#!/usr/bin/env python3
"""
Character Manager - 小说角色管理工具

创建、编辑、查询角色档案，支持角色关系网络、情感弧光、动机追踪。
专为 AutoNovel Writer v5.0 设计。

Usage:
    python3 manage_characters.py create --name "林风" --role "主角" --output characters/linfeng.yml
    python3 manage_characters.py list --project ./my-novel
    python3 manage_characters.py query --name "林风" --relation "盟友"
    python3 manage_characters.py update --name "林风" --output characters/linfeng.yml
    python3 manage_characters.py delete --name "林风" --output characters/linfeng.yml
    python3 manage_characters.py export --project ./my-novel --output characters_export.md
    python3 manage_characters.py validate --project ./my-novel
"""

import sys
import argparse
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
    from rich import box

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

try:
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False


@dataclass
class Appearance:
    """外貌特征"""

    height: Optional[int] = None
    build: Optional[str] = None
    features: List[str] = field(default_factory=list)
    clothing_style: Optional[str] = None


@dataclass
class Personality:
    """性格特征"""

    traits: List[str] = field(default_factory=list)
    flaws: List[str] = field(default_factory=list)
    mbti: Optional[str] = None


@dataclass
class BackgroundEvent:
    """背景事件"""

    chapter: int
    event: str


@dataclass
class Background:
    """背景故事"""

    origin: Optional[str] = None
    family: Optional[str] = None
    key_events: List[BackgroundEvent] = field(default_factory=list)


@dataclass
class Ability:
    """能力体系"""

    cultivation_realm: Optional[str] = None
    max_realm: Optional[str] = None
    skills: List[str] = field(default_factory=list)


@dataclass
class SpecialAbility:
    """特殊能力"""

    special_abilities: List[str] = field(default_factory=list)


@dataclass
class Relationship:
    """人际关系"""

    name: str
    type: str
    status: str
    description: Optional[str] = None


@dataclass
class EmotionalArc:
    """情感弧光"""

    start: Optional[str] = None
    midpoint: Optional[str] = None
    end: Optional[str] = None


@dataclass
class Motivation:
    """动机追踪"""

    surface_goal: Optional[str] = None
    deep_goal: Optional[str] = None
    internal_conflict: Optional[str] = None


@dataclass
class Character:
    """角色档案"""

    name: str
    role: str
    age: Optional[int] = None
    gender: Optional[str] = None
    appearance: Appearance = field(default_factory=Appearance)
    personality: Personality = field(default_factory=Personality)
    background: Background = field(default_factory=Background)
    abilities: Ability = field(default_factory=Ability)
    special_abilities: SpecialAbility = field(default_factory=SpecialAbility)
    relationships: List[Relationship] = field(default_factory=list)
    emotional_arc: EmotionalArc = field(default_factory=EmotionalArc)
    motivation: Motivation = field(default_factory=Motivation)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {
            "name": self.name,
            "role": self.role,
            "age": self.age,
            "gender": self.gender,
            "appearance": self._clean_dict(asdict(self.appearance)),
            "personality": self._clean_dict(asdict(self.personality)),
            "background": self._clean_dict(asdict(self.background)),
            "abilities": self._clean_dict(asdict(self.abilities)),
            "special_abilities": self._clean_dict(asdict(self.special_abilities)),
            "relationships": [asdict(r) for r in self.relationships],
            "emotional_arc": self._clean_dict(asdict(self.emotional_arc)),
            "motivation": self._clean_dict(asdict(self.motivation)),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        return {k: v for k, v in result.items() if v not in [None, [], {}]}

    def _clean_dict(self, d: Dict) -> Dict:
        """清理字典中的空值"""
        return {k: v for k, v in d.items() if v not in [None, [], {}]}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Character":
        """从字典创建实例"""
        appearance = Appearance(**(data.get("appearance") or {}))
        personality = Personality(**(data.get("personality") or {}))
        background = Background(**(data.get("background") or {}))
        abilities = Ability(**(data.get("abilities") or {}))
        special_abilities = SpecialAbility(**(data.get("special_abilities") or {}))

        relationships = [
            Relationship(**rel) for rel in (data.get("relationships") or [])
        ]
        emotional_arc = EmotionalArc(**(data.get("emotional_arc") or {}))
        motivation = Motivation(**(data.get("motivation") or {}))

        return cls(
            name=data["name"],
            role=data["role"],
            age=data.get("age"),
            gender=data.get("gender"),
            appearance=appearance,
            personality=personality,
            background=background,
            abilities=abilities,
            special_abilities=special_abilities,
            relationships=relationships,
            emotional_arc=emotional_arc,
            motivation=motivation,
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
        )


class CharacterManager:
    """角色管理器"""

    VALID_ROLES = ["主角", "女主角", "重要配角", "配角", "反派", "中立"]
    VALID_RELATIONSHIP_TYPES = [
        "盟友",
        "敌人",
        "竞争对手",
        "师徒",
        "亲人",
        "暧昧",
        "恋人",
    ]

    def __init__(self, console: Optional["Console"] = None):
        self.template_dir = Path(__file__).parent.parent / "configs"
        self.templates: Dict[str, Any] = {}

    # 内置模板配置
    TEMPLATE_CONFIGS = {
        "xuanhuan": {
            "name": "玄幻主角",
            "role": "主角",
            "age": 18,
            "appearance": {
                "height": 180,
                "build": "结实",
                "features": ["眼神凌厉", "气度不凡"],
            },
            "personality": {
                "traits": ["坚韧不拔", "聪慧过人", "杀伐果断"],
                "flaws": ["过于自信", "偶尔冲动"],
            },
            "abilities": {"cultivation_realm": "练气期", "max_realm": "大罗金仙"},
            "special_abilities": {"special_abilities": ["金手指", "系统"]},
            "motivation": {
                "surface_goal": "变强复仇",
                "deep_goal": "守护所爱",
                "internal_conflict": "力量与仁慈的抉择",
            },
        },
        "dushi": {
            "name": "都市主角",
            "role": "主角",
            "age": 25,
            "appearance": {
                "height": 178,
                "build": "匀称",
                "features": ["阳光帅气", "气质儒雅"],
            },
            "personality": {
                "traits": ["正直善良", "机智幽默", "重情重义"],
                "flaws": ["太讲原则", "偶尔优柔寡断"],
            },
            "abilities": {"skills": ["商业头脑", "格斗技巧"]},
            "motivation": {
                "surface_goal": "事业成功",
                "deep_goal": "实现自我价值",
                "internal_conflict": "财富与初心的平衡",
            },
        },
        "kehuan": {
            "name": "科幻主角",
            "role": "角色",
            "age": 28,
            "appearance": {
                "height": 182,
                "build": "精壮",
                "features": ["冷静理性", "科技感"],
            },
            "personality": {
                "traits": ["逻辑性强", "探索精神", "责任心强"],
                "flaws": ["过于理性", "社交笨拙"],
            },
            "abilities": {"skills": ["科技研发", "战略规划"]},
            "special_abilities": {"special_abilities": ["未来科技", "特殊能力"]},
            "motivation": {
                "surface_goal": "探索宇宙",
                "deep_goal": "保护人类文明",
                "internal_conflict": "科技伦理的抉择",
            },
        },
        "lishi": {
            "name": "历史主角",
            "role": "主角",
            "age": 30,
            "appearance": {
                "height": 185,
                "build": "魁梧",
                "features": ["气度恢弘", "不怒自威"],
            },
            "personality": {
                "traits": ["雄才大略", "知人善任", "深谋远虑"],
                "flaws": ["猜疑心重", "手段狠辣"],
            },
            "abilities": {"skills": ["权谋术", "军事指挥"]},
            "motivation": {
                "surface_goal": "争霸天下",
                "deep_goal": "开创盛世",
                "internal_conflict": "仁政与铁腕的平衡",
            },
        },
    }

    def _print_progress(self, message: str, total: int = 100) -> Optional[Progress]:
        """打印进度条"""
        if not RICH_AVAILABLE:
            print(message)
            return None

        progress = Progress(
            SpinnerColumn(),
            TextColumn("{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )
        progress.add_task(message, total=total)
        return progress

        self.templates: Dict[str, Any] = {}

    def load_templates(self) -> None:
        """加载角色模板"""
        template_file = self.template_dir / "character_templates.yml"
        if template_file.exists():
            with open(template_file, "r", encoding="utf-8") as f:
                self.templates = yaml.safe_load(f)

    def create_character(
        self,
        name: str,
        role: str,
        output_path: str,
        template: Optional[str] = None,
        **kwargs,
    ) -> bool:
        """创建新角色"""
        if role not in self.VALID_ROLES:
            self.console.print(
                f"[red]错误：角色类型必须是 {self.VALID_ROLES} 之一[/red]"
            )
            return False

        character = Character(name=name, role=role)

        if template:
            self._apply_template(character, template)

        for key, value in kwargs.items():
            if hasattr(character, key):
                setattr(character, key, value)

        character.updated_at = datetime.now().isoformat()

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with open(output, "w", encoding="utf-8") as f:
            yaml.dump(
                character.to_dict(),
                f,
                allow_unicode=True,
                sort_keys=False,
                default_flow_style=False,
            )

        self.console.print(f"[green]✓ 角色 '{name}' 创建成功[/green]")
        self.console.print(f"  文件: {output.resolve()}")
        return True

    def _apply_template(self, character: Character, template_name: str) -> bool:
        """应用角色模板"""
        if not self.templates:
            self.load_templates()

        templates = self.templates.get("templates", {})

        if template_name in templates:
            template = templates[template_name]
            if "role" in template:
                character.role = template["role"]
            return True
        elif template_name in self.TEMPLATE_CONFIGS:
            default_config = self.TEMPLATE_CONFIGS[template_name]
            character.role = default_config.get("role", character.role)
            self.console.print(
                f"[yellow]使用内置模板: {default_config['name']}[/yellow]"
            )
            return True
        else:
            self.console.print(f"[yellow]警告：模板 '{template_name}' 不存在[/yellow]")
            return False

    def list_characters(self, project_path: str) -> None:
        """列出项目中的所有角色"""
        project = Path(project_path)

        if not project.exists():
            self.console.print(f"[red]错误：项目目录 '{project_path}' 不存在[/red]")
            return

        character_files = list(project.rglob("*.yml")) + list(project.rglob("*.yaml"))

        if not character_files:
            self.console.print("[yellow]未找到任何角色文件[/yellow]")
            return

        table = Table(
            title="角色列表", box=box.ROUNDED, show_lines=True, title_style="bold cyan"
        )

        table.add_column("名称", style="cyan")
        table.add_column("角色", style="magenta")
        table.add_column("文件", style="green")
        table.add_column("更新时间", style="yellow")

        for filepath in sorted(character_files):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)

                if data and "name" in data and "role" in data:
                    table.add_row(
                        data["name"],
                        data["role"],
                        str(filepath.relative_to(project)),
                        data.get("updated_at", "未知"),
                    )
            except Exception as e:
                self.console.print(f"[yellow]警告：无法读取 {filepath}: {e}[/yellow]")

        self.console.print(table)

    def query_character(
        self,
        name: str,
        project_path: Optional[str] = None,
        relation: Optional[str] = None,
    ) -> Optional[Character]:
        """查询角色信息（支持模糊搜索）"""
        if project_path:
            project = Path(project_path)
            character_files = list(project.rglob("*.yml")) + list(
                project.rglob("*.yaml")
            )

            matched_characters = []

            for filepath in character_files:
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)

                    if data and "name" in data:
                        char_name = data.get("name", "")
                        if (
                            name.lower() in char_name.lower()
                            or char_name.lower() in name.lower()
                        ):
                            character = Character.from_dict(data)
                            matched_characters.append((char_name, character))
                except Exception as e:
                    self.console.print(
                        f"[yellow]警告：无法读取 {filepath}: {e}[/yellow]"
                    )

            if not matched_characters:
                self.console.print(f"[red]错误：未找到角色 '{name}'[/red]")
                return None

            if len(matched_characters) == 1:
                _, character = matched_characters[0]
                self._display_character(character, relation)
                return character
            else:
                self.console.print(
                    f"[yellow]找到 {len(matched_characters)} 个匹配的角色:[/yellow]"
                )
                for i, (char_name, character) in enumerate(matched_characters, 1):
                    self.console.print(f"  [bold]{i}. {char_name}[/bold]")
                    self._display_character(character, relation)
                    if i < len(matched_characters):
                        self.console.print("")
                return matched_characters[0][1]
        else:
            self.console.print("[yellow]提示：需要指定项目路径进行查询[/yellow]")
            return None

    def _display_character(
        self, character: Character, relation_filter: Optional[str] = None
    ) -> None:
        """显示角色详情"""
        panel = Panel(
            f"[bold cyan]{character.name}[/bold cyan]\n"
            f"[magenta]角色类型:[/magenta] {character.role}\n"
            f"[yellow]年龄:[/yellow] {character.age or '未知'} | "
            f"[yellow]性别:[/yellow] {character.gender or '未知'}",
            title="角色档案",
            box=box.ROUNDED,
            title_align="left",
        )
        self.console.print(panel)

        if character.appearance.features or character.appearance.clothing_style:
            self.console.print("\n[yellow]外貌特征[/yellow]")
            if character.appearance.features:
                for feature in character.appearance.features:
                    self.console.print(f"  • {feature}")
            if character.appearance.clothing_style:
                self.console.print(f"  衣着风格: {character.appearance.clothing_style}")

        if character.personality.traits or character.personality.flaws:
            self.console.print("\n[yellow]性格特征[/yellow]")
            if character.personality.traits:
                self.console.print(f"  优点: {', '.join(character.personality.traits)}")
            if character.personality.flaws:
                self.console.print(f"  缺点: {', '.join(character.personality.flaws)}")
            if character.personality.mbti:
                self.console.print(f"  MBTI: {character.personality.mbti}")

        if character.motivation.surface_goal:
            self.console.print("\n[yellow]动机追踪[/yellow]")
            self.console.print(f"  表面目标: {character.motivation.surface_goal}")
            if character.motivation.deep_goal:
                self.console.print(f"  深层目标: {character.motivation.deep_goal}")
            if character.motivation.internal_conflict:
                self.console.print(
                    f"  内心冲突: {character.motivation.internal_conflict}"
                )

        if character.background.origin:
            self.console.print("\n[yellow]背景故事[/yellow]")
            self.console.print(f"  出身: {character.background.origin}")
            if character.background.family:
                self.console.print(f"  家庭: {character.background.family}")

        if character.relationships:
            self.console.print("\n[yellow]人际关系[/yellow]")
            for rel in character.relationships:
                if relation_filter and rel.type != relation_filter:
                    continue
                self.console.print(
                    f"  • [cyan]{rel.name}[/cyan] ({rel.type}) - {rel.status}"
                )
                if rel.description:
                    self.console.print(f"    {rel.description}")

    def update_character(self, name: str, output_path: str, **kwargs) -> bool:
        """更新角色档案"""
        filepath = Path(output_path)

        if not filepath.exists():
            self.console.print(f"[red]错误：文件 '{output_path}' 不存在[/red]")
            return False

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if not data or data.get("name") != name:
                self.console.print("[red]错误：文件中角色名称不匹配[/red]")
                return False

            character = Character.from_dict(data)

            for key, value in kwargs.items():
                if hasattr(character, key) and value is not None:
                    setattr(character, key, value)

            character.updated_at = datetime.now().isoformat()

            with open(filepath, "w", encoding="utf-8") as f:
                yaml.dump(
                    character.to_dict(),
                    f,
                    allow_unicode=True,
                    sort_keys=False,
                    default_flow_style=False,
                )

            self.console.print(f"[green]✓ 角色 '{name}' 更新成功[/green]")
            return True

        except Exception as e:
            self.console.print(f"[red]错误：更新失败 - {e}[/red]")
            return False

    def delete_character(
        self, name: str, output_path: str, force: bool = False
    ) -> bool:
        """删除角色档案"""
        filepath = Path(output_path)

        if not filepath.exists():
            self.console.print(f"[red]错误：文件 '{output_path}' 不存在[/red]")
            return False

        if not force:
            confirm = self.console.input(
                f"[yellow]确定要删除角色 '{name}' 吗？(y/N): [/yellow]"
            )
            if confirm.lower() != "y":
                self.console.print("[red]已取消[/red]")
                return False

        try:
            filepath.unlink()
            self.console.print(f"[green]✓ 角色 '{name}' 已删除[/green]")
            return True
        except Exception as e:
            self.console.print(f"[red]错误：删除失败 - {e}[/red]")
            return False

    def export_to_markdown(
        self, project_path: str, output_path: str, format: str = "detailed"
    ) -> bool:
        """导出角色档案为 Markdown"""
        project = Path(project_path)

        if not project.exists():
            self.console.print(f"[red]错误：项目目录 '{project_path}' 不存在[/red]")
            return False

        character_files = list(project.rglob("*.yml")) + list(project.rglob("*.yaml"))

        if not character_files:
            self.console.print("[yellow]未找到任何角色文件[/yellow]")
            return False

        md_content = f"""# 角色档案导出

导出时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

"""

        for filepath in sorted(character_files):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)

                if not data or "name" not in data:
                    continue

                md_content += f"""## {data.get("name", "未知角色")}

**角色类型**: {data.get("role", "未知")}

"""

                if data.get("age"):
                    md_content += f"**年龄**: {data['age']}\n\n"
                if data.get("gender"):
                    md_content += f"**性别**: {data['gender']}\n\n"

                if data.get("appearance"):
                    md_content += "### 外貌特征\n\n"
                    if data["appearance"].get("features"):
                        for feature in data["appearance"]["features"]:
                            md_content += f"- {feature}\n"
                    if data["appearance"].get("clothing_style"):
                        md_content += (
                            f"\n**衣着风格**: {data['appearance']['clothing_style']}\n"
                        )
                    md_content += "\n"

                if data.get("personality"):
                    md_content += "### 性格特征\n\n"
                    if data["personality"].get("traits"):
                        md_content += (
                            f"**优点**: {', '.join(data['personality']['traits'])}\n\n"
                        )
                    if data["personality"].get("flaws"):
                        md_content += (
                            f"**缺点**: {', '.join(data['personality']['flaws'])}\n\n"
                        )
                    if data["personality"].get("mbti"):
                        md_content += f"**MBTI**: {data['personality']['mbti']}\n\n"

                if data.get("motivation"):
                    md_content += "### 动机追踪\n\n"
                    if data["motivation"].get("surface_goal"):
                        md_content += (
                            f"**表面目标**: {data['motivation']['surface_goal']}\n\n"
                        )
                    if data["motivation"].get("deep_goal"):
                        md_content += (
                            f"**深层目标**: {data['motivation']['deep_goal']}\n\n"
                        )
                    if data["motivation"].get("internal_conflict"):
                        md_content += f"**内心冲突**: {data['motivation']['internal_conflict']}\n\n"

                if data.get("background"):
                    md_content += "### 背景故事\n\n"
                    if data["background"].get("origin"):
                        md_content += f"**出身**: {data['background']['origin']}\n\n"
                    if data["background"].get("family"):
                        md_content += f"**家庭**: {data['background']['family']}\n\n"

                if data.get("relationships"):
                    md_content += "### 人际关系\n\n"
                    for rel in data["relationships"]:
                        md_content += f"- **{rel.get('name')}** ({rel.get('type')}) - {rel.get('status')}\n"
                        if rel.get("description"):
                            md_content += f"  - {rel['description']}\n"
                    md_content += "\n"

                md_content += "---\n\n"

            except Exception as e:
                self.console.print(f"[yellow]警告：无法处理 {filepath}: {e}[/yellow]")

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with open(output, "w", encoding="utf-8") as f:
            f.write(md_content)

        self.console.print(
            f"[green]✓ 已导出 {len(character_files)} 个角色到 '{output.resolve()}'[/green]"
        )
        return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        prog="manage_characters",
        description="小说角色管理工具 - 创建、编辑、查询角色档案",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 manage_characters.py create --name "林风" --role "主角" --output characters/linfeng.yml
  python3 manage_characters.py list --project ./my-novel
  python3 manage_characters.py query --name "林风" --project ./my-novel
  python3 manage_characters.py update --name "林风" --output characters/linfeng.yml
  python3 manage_characters.py delete --name "林风" --output characters/linfeng.yml
  python3 manage_characters.py export --project ./my-novel --output characters_export.md
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="命令")

    # create 命令
    create_parser = subparsers.add_parser("create", help="创建新角色档案")
    create_parser.add_argument("--name", required=True, help="角色名称")
    create_parser.add_argument("--role", required=True, help="角色类型")
    create_parser.add_argument("--output", required=True, help="输出文件路径")
    create_parser.add_argument("--template", help="使用的模板")
    create_parser.add_argument("--age", type=int, help="年龄")
    create_parser.add_argument("--gender", help="性别")

    # list 命令
    list_parser = subparsers.add_parser("list", help="列出所有角色")
    list_parser.add_argument("--project", required=True, help="项目目录路径")

    # query 命令
    query_parser = subparsers.add_parser("query", help="查询角色信息")
    query_parser.add_argument("--name", required=True, help="角色名称")
    query_parser.add_argument("--project", help="项目目录路径")
    query_parser.add_argument("--relation", help="筛选关系类型")

    # update 命令
    update_parser = subparsers.add_parser("update", help="更新角色档案")
    update_parser.add_argument("--name", required=True, help="角色名称")
    update_parser.add_argument("--output", required=True, help="输出文件路径")

    # delete 命令
    delete_parser = subparsers.add_parser("delete", help="删除角色档案")
    delete_parser.add_argument("--name", required=True, help="角色名称")
    delete_parser.add_argument("--output", required=True, help="输出文件路径")
    delete_parser.add_argument(
        "--force", action="store_true", help="强制删除，无需确认"
    )

    # export 命令
    export_parser = subparsers.add_parser("export", help="导出角色档案")
    export_parser.add_argument("--project", required=True, help="项目目录路径")
    export_parser.add_argument("--output", required=True, help="输出文件路径")
    export_parser.add_argument(
        "--format",
        choices=["markdown", "json", "yaml"],
        default="markdown",
        help="导出格式",
    )

    # validate 命令
    validate_parser = subparsers.add_parser("validate", help="验证角色档案完整性")
    validate_parser.add_argument("--project", required=True, help="项目目录路径")
    validate_parser.add_argument("--fix", action="store_true", help="自动修复")

    # visualize 命令
    visualize_parser = subparsers.add_parser(
        "visualize-relations", help="可视化角色关系网络"
    )
    visualize_parser.add_argument("--project", required=True, help="项目目录路径")
    visualize_parser.add_argument("--output", help="输出文件路径")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    manager = CharacterManager()

    if RICH_AVAILABLE:
        console = Console()
    else:
        console = None
        print("注意: rich 库未安装，将使用基础输出")

    manager.console = console or Console()

    if args.command == "create":
        success = manager.create_character(
            name=args.name,
            role=args.role,
            output_path=args.output,
            template=args.template,
            age=args.age,
            gender=args.gender,
        )
        sys.exit(0 if success else 1)

    elif args.command == "list":
        manager.list_characters(project_path=args.project)
        sys.exit(0)

    elif args.command == "query":
        character = manager.query_character(
            name=args.name, project_path=args.project, relation=args.relation
        )
        sys.exit(0 if character else 1)

    elif args.command == "update":
        success = manager.update_character(name=args.name, output_path=args.output)
        sys.exit(0 if success else 1)

    elif args.command == "delete":
        success = manager.delete_character(
            name=args.name, output_path=args.output, force=args.force
        )
        sys.exit(0 if success else 1)

    elif args.command == "export":
        success = manager.export_to_markdown(
            project_path=args.project, output_path=args.output, format=args.format
        )
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
