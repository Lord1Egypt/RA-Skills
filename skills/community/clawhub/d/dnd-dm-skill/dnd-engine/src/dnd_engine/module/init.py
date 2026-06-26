"""
模组通用初始化：在模组选择/章节过渡时自动生成所有数据文件
不依赖特定模组的内容——适用于任意 D&D 5e 模组
"""
import os
import json
import re
import sys

sys.path.insert(0, os.path.dirname(__file__) or '.')
from dnd_engine.module.scanner import scan_modules, get_module_level_range, _identify_module


# ---------- 模组文件命名规则 ----------

def get_chapter_filename(module_name, chapter_label):
    """
    根据模组命名约定，构建章节文件名
    
    支持的文件名格式（自动尝试）：
    - {module_name} - {chapter_label}.md
    - {module_name} - Ch.{chapter_label}.md
    - {module_name}_ Ch.{chapter_label}.md
    - {module_name}_{chapter_label}.md
    
    参数:
        module_name: str - 模组名（如"失落的矿坑"）
        chapter_label: str - 章节标签（如"Ch.1"或"第1章"）
    
    返回:
        str: 完整的文件名，如未找到返回 None
    """
    from dnd_engine.module.scanner import MODULES_DIR
    
    candidates = [
        # 下划线分隔
        f"{module_name}_{chapter_label}.md",
        f"{module_name}_{chapter_label.replace(' ', '_')}.md",
        # 空格分隔
        f"{module_name} - {chapter_label}.md",
        f"{module_name} - {chapter_label.replace(' ', '_')}.md",
    ]
    
    for c in candidates:
        full = os.path.join(MODULES_DIR, c)
        if os.path.exists(full):
            return full
    
    return None


def resolve_chapter_filepath(module_name, chapter_label):
    """
    通过 scan_modules() 查找指定模组指定章节的文件路径
    不依赖文件名约定——从实际文件列表中匹配

    参数:
        module_name: str
        chapter_label: str - 如 "Ch.1", "Chapter 2", "第一章"

    返回:
        str: 完整文件路径，或 None
    """
    modules = scan_modules()
    for mod in modules:
        if mod['name'] == module_name:
            # Try matching chapter_label in file basename
            for fp in mod.get('files', []):
                basename = os.path.basename(fp)
                # Extract chapter number from label
                ch_match = re.search(r'(\d+)', chapter_label)
                if ch_match:
                    ch_num = ch_match.group(1)
                    if re.search(rf'(?:Ch\.?\s*)?{re.escape(ch_num)}(?:\s|\.|$|-)', basename, re.IGNORECASE):
                        return fp
            # Fallback: first file
            if mod['files']:
                return mod['files'][0]
    return None


# ---------- MODULE_INDEX.md 模板生成 ----------

def generate_module_index(module_name, module_files, chapter_count):
    """
    生成通用 MODULE_INDEX.md 初始模板

    参数:
        module_name: str
        module_files: list[str]
        chapter_count: int

    返回:
        str: Markdown 内容
    """
    lines = [
        f"# 📖 {module_name} — 模组索引",
        f"",
        f"> 目标：运行模组时快速定位所需信息，减少上下文浪费。",
        f"> 由 `code/module/init.py:generate_module_index()` 自动生成，每次章节过渡时重建。",
        f"",
        f"---",
        f"",
        f"## 一、模组文件结构",
        f"",
        f"| 文件 | 用途 |",
        f"|------|------|",
    ]
    for fp in sorted(module_files):
        fname = os.path.basename(fp)
        lines.append(f"| `{fname}` | 待扫描 |")

    lines += [
        f"",
        f"---",
        f"",
        f"## 二、当前场景参考（动态加载）",
        f"",
        f"> 详细数据通过场景索引按需加载，不在此处全文保留。",
        f"> 当前场景数据见 `srd/scenes_index.json`。",
        f"",
        f"### 场景索引",
        f"```",
        f"srd/scenes_index.json — 场景级行号索引（由 build_scene_index() 生成）",
        f"  每个场景包含：标题、起止行号、子节列表、关键词标签",
        f"",
        f"加载规则：",
        f"  → 每次只加载 `_current_scene` 对应的场景原文行",
        f"  → 场景切换时调用 `scene_index.set_current_scene()` 更新",
        f"  → 同一章节内的场景切换不触发章节过渡协议",
        f"```",
        f"",
        f"## 三、章节过渡条件",
        f"",
        f"| 当前 | 目标 | 条件（由存档中的 completedNodes 驱动） |",
        f"|------|------|--------------------------------------|",
    ]
    for i in range(1, chapter_count):
        lines.append(f"| Ch.{i} | Ch.{i+1} | 完成 Ch.{i} 关键节点 → 调用 `build_scene_index()` |")

    lines += [
        f"",
        f"> 章节过渡时 `code/module/builder.py:build_chapter_content()` 自动处理索引构建和内容替换。",
        f"> 过渡后首次进入新场景时 `code/module/scene_index.py:build_scene_index()` 扫描新章节文件生成场景索引。",
        f"",
        f"## 四、玩家技能速查（从 live_party.json 动态生成，此处不重复保存）",
        f"",
        f"以上内容由 `world_state.json` + `live_party.json` 在每次对话时动态摘要。",
    ]
    return '\n'.join(lines)


# ---------- MODULE_ARC.md 模板生成 ----------

def generate_module_arc(module_name):
    """
    生成通用 MODULE_ARC.md 初始模板

    参数:
        module_name: str

    返回:
        str: Markdown 内容
    """
    return f"""# 《{module_name}》模组运行结构

> 本文件由 `code/module/init.py` 自动生成。
> 换模组时重建此文件即可，`DM_RULES.md` 不需修改。

---

## 章节加载序列

（章节结构将在每次章节过渡时由 `builder.py:build_chapter_content()` 自动追加）

### 章节命名约定

模组文件放置于 `modules/` 目录下，命名格式：
- `{{模组名}} - Ch.{{章节号}} {{标题}}.md`
- 或 `{{模组名}}_{{章节号}} {{标题}}.md`
- 或 `{{模组名}} {{章节号}} {{标题}}.md`

### 通用规则

- **等级范围**：由文件内容中的 `等级范围` 标注自动识别
- **章节过渡**：完成所有关键节点后触发，由 Rule 8.7 控制流程
- **关键节点**：每个 `##` 场景标题为一个关键节点区域"""


# ---------- world_state.json 模板生成 ----------

def generate_world_state():
    """
    生成通用 world_state.json 初始模板
    不含任何特定模组的 NPC/派系/任务名

    返回:
        dict
    """
    return {
        "faction_relations": {},
        "discovered_locations": [],
        "quest_progress": {
            "完成": [],
            "进行中": [],
            "待触发": []
        },
        "key_npc_status": {},
        "current_chapter": 1,
        "current_scene": "起始",
        "day_in_game": 1,
        "_说明": "由 code/state/world.py 管理。派系/任务/NPC 由规则0a（模组选择后）开始填充。"
    }


# ---------- 完整初始化流程 ----------

def init_module(module_name):
    """
    初始化一个模组的所有动态数据文件

    参数:
        module_name: str - 模组名

    返回:
        dict: 初始化结果 {index_file, arc_file, world_file, scene_count}
    """
    root = os.path.join(os.path.dirname(__file__), '..', '..')
    modules = scan_modules()

    mod = None
    for m in modules:
        if m['name'] == module_name:
            mod = m
            break

    if not mod:
        return {'error': f'Module not found: {module_name}'}

    # 1. 生成 MODULE_INDEX.md
    index_content = generate_module_index(
        module_name, mod['files'], mod['chapter_count']
    )
    index_path = os.path.join(root, 'MODULE_INDEX.md')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)

    # 2. 生成 MODULE_ARC.md
    arc_content = generate_module_arc(module_name)
    arc_path = os.path.join(root, 'MODULE_ARC.md')
    with open(arc_path, 'w', encoding='utf-8') as f:
        f.write(arc_content)

    # 3. 生成 world_state.json
    ws = generate_world_state()
    ws_path = os.path.join(root, 'world_state.json')
    with open(ws_path, 'w', encoding='utf-8') as f:
        json.dump(ws, f, ensure_ascii=False, indent=2)

    # 4. Initialize scene index
    try:
        from dnd_engine.module.scene_index import build_scene_index, save_scene_index, set_current_scene
        srd_dir = os.path.join(root, 'srd')
        os.makedirs(srd_dir, exist_ok=True)

        total_scenes = 0
        for fp in mod['files'][:1]:  # Only first chapter initially
            idx = build_scene_index(fp)
            save_scene_index(module_name, idx, output_dir=srd_dir)
            total_scenes += len(idx.get('scenes', []))

            # Set first non-intro scene as current
            for s in idx.get('scenes', []):
                if 'intro' not in s.get('tags', []):
                    filename = os.path.basename(fp)
                    set_current_scene(
                        f'{module_name}:{filename}',
                        s['title'],
                        scene_index_path=os.path.join(srd_dir, 'scenes_index.json')
                    )
                    break
    except ImportError:
        pass
    except Exception as e:
        print(f"[WARN] scene_index init: {e}")

    return {
        'index_file': index_path,
        'arc_file': arc_path,
        'world_file': ws_path,
        'chapter_count': mod['chapter_count'],
    }
