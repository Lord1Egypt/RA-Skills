"""
dnd_engine.context.loader — DM 上下文加载器

统一加载 D&D DM 所需的完整上下文，包括规则、人格、模板等引用文件。
不依赖任何特定运行时环境——输出纯文本/Markdown，可被任何 LLM 消费。
"""

import os
import re
from dataclasses import dataclass, field
from typing import Optional


# ── 核心引用文件清单 ──────────────────────────────────────
CORE_REFERENCES = [
    "DM_RULES.md",
    "DM_TEMPLATES.md",
    "DM_MAP_SYS.md",
    "DM_DEV_GUIDE.md",
    "SOUL.md",
    "IDENTITY.md",
    "AGENTS.md",
    "TOOLS.md",
    "MODULE_ARC.md",
    "MODULE_INDEX.md",
    "ECHO_ARC.md",
    "CHAR_CREATION.md",
]

OPTIONAL_REFERENCES = [
    "USER.md",
    "MEMORY.md",
    "HEARTBEAT.md",
    "SKILL.md",
]


@dataclass
class ContextBundle:
    """加载后的上下文包"""
    references: dict = field(default_factory=dict)  # filename → content
    missing: list = field(default_factory=list)      # 缺失的文件列表
    root_path: str = ""
    total_chars: int = 0

    def to_prompt_block(self, heading_level: int = 3) -> str:
        """将上下文渲染为 LLM system prompt 块"""
        parts = []
        for filename, content in self.references.items():
            if not content.strip():
                continue
            heading = "#" * heading_level
            parts.append(f"{heading} {filename}\n\n{content.strip()}\n\n---\n")
        return "\n".join(parts)

    def summary(self) -> str:
        """返回上下文加载摘要"""
        loaded = len(self.references)
        missing = len(self.missing)
        total_kb = self.total_chars / 1024
        return f"已加载 {loaded} 个引用文件 ({total_kb:.1f} KB)，缺失 {missing} 个"


def _find_reference_dir(base_path: str) -> Optional[str]:
    """在多个可能位置查找 references 目录"""
    candidates = [
        os.path.join(base_path, "references"),
        base_path,  # 根目录兜底
        os.path.join(base_path, "dnd-engine", "references"),
    ]
    for c in candidates:
        if os.path.isdir(c):
            return c
    return None


def _read_file_safe(filepath: str) -> Optional[str]:
    """安全读取文件，忽略编码错误"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(filepath, "r", encoding="gbk") as f:
                return f.read()
        except Exception:
            return None
    except Exception:
        return None


def list_available_references(base_path: str = None) -> dict:
    """列出所有可用的引用文件及其位置"""
    if base_path is None:
        base_path = os.getcwd()

    ref_dir = _find_reference_dir(base_path)
    if ref_dir is None:
        return {"reference_dir": None, "available": [], "all_files": []}

    available = []
    for fname in CORE_REFERENCES + OPTIONAL_REFERENCES:
        fpath = os.path.join(ref_dir, fname)
        if os.path.exists(fpath):
            available.append(fname)

    all_files = []
    try:
        all_files = sorted(os.listdir(ref_dir))
    except Exception:
        pass

    return {
        "reference_dir": ref_dir,
        "available": available,
        "all_files": all_files,
    }


def load_context(
    base_path: str = None,
    include_optional: bool = False,
    max_chars_per_file: int = 8000,
) -> ContextBundle:
    """
    加载 DM 上下文。

    Args:
        base_path: 工作目录根路径（默认 os.getcwd()）
        include_optional: 是否包含可选引用文件（USER.md, MEMORY.md 等）
        max_chars_per_file: 单个文件最大字符数（超出截断）

    Returns:
        ContextBundle 对象
    """
    if base_path is None:
        base_path = os.getcwd()

    ref_dir = _find_reference_dir(base_path)
    bundle = ContextBundle(root_path=base_path)
    total_chars = 0

    files_to_load = list(CORE_REFERENCES)
    if include_optional:
        files_to_load += OPTIONAL_REFERENCES

    if ref_dir is None:
        bundle.missing = files_to_load
        return bundle

    for fname in files_to_load:
        fpath = os.path.join(ref_dir, fname)

        if not os.path.exists(fpath):
            # 根目录兜底
            fpath = os.path.join(base_path, fname)

        if not os.path.exists(fpath):
            bundle.missing.append(fname)
            continue

        content = _read_file_safe(fpath)
        if content is None:
            bundle.missing.append(fname)
            continue

        # 截断超长内容
        if len(content) > max_chars_per_file:
            content = content[:max_chars_per_file] + f"\n\n... [已截断，原文件 {len(content)} 字符]"

        bundle.references[fname] = content
        total_chars += len(content)

    bundle.total_chars = total_chars
    return bundle


def build_system_prompt(
    base_path: str = None,
    runtime_name: str = "Unknown",
    extra_context: str = None,
) -> str:
    """
    构建完整的 DM system prompt。

    用于非 OpenClaw 运行时（终端交互、MCP server 等），
    生成可供 LLM 使用的完整 system prompt。
    """
    bundle = load_context(base_path=base_path, include_optional=True)

    parts = []

    # 身份标识
    parts.append("# D&D 地下城主 (AI Dungeon Master)\n")
    parts.append(f"运行环境: {runtime_name}\n")
    parts.append("你是一个 D&D 5e (2024版) 的地下城主。你拥有以下规则和参考资料。\n")

    # 核心规则
    for fname in ["DM_RULES.md", "DM_TEMPLATES.md", "DM_MAP_SYS.md", "DM_DEV_GUIDE.md"]:
        if fname in bundle.references:
            content = bundle.references[fname]
            if content.strip():
                parts.append(f"## {fname}\n\n{content}\n\n---\n")

    # 角色人格
    for fname in ["SOUL.md", "IDENTITY.md", "AGENTS.md"]:
        if fname in bundle.references:
            content = bundle.references[fname]
            if content.strip():
                parts.append(f"## {fname}\n\n{content}\n\n---\n")

    # 可选上下文
    if extra_context:
        parts.append(f"## 额外上下文\n\n{extra_context}\n\n---\n")

    # 工具说明
    parts.append("## 可用能力\n\n")
    parts.append("你可以通过以下方式与游戏引擎交互：\n")
    parts.append("- 掷骰: roll_dice(expr)\n")
    parts.append("- 命中判定: check_hit(attack_roll, bonus, ac)\n")
    parts.append("- 伤害计算: calc_damage(dice_count, dice_sides, bonus)\n")
    parts.append("- 技能检定: resolve_skill_check(d20_result, components, dc)\n")
    parts.append("- 战斗状态: combat_new/advance/end/apply_damage\n")
    parts.append("- 搜索 SRD 规则: srd_search(query)\n")
    parts.append("- 存档管理: save_game/load_game/list_saves\n\n")

    # 缺失文件提示
    if bundle.missing:
        parts.append("## 提示\n\n")
        parts.append(f"以下引用文件未找到: {', '.join(bundle.missing)}\n")
        parts.append("部分功能可能受限。\n\n")

    return "\n".join(parts)