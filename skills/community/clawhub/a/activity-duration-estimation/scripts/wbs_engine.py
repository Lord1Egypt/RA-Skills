"""
activity-duration-estimation WBS 引擎
工作分解结构：模板匹配、递归分解、100%规则验证、多格式输出
"""

import json
import math
from typing import Optional


# ═══════════════════════════════════════════════════
# 1. 数据结构
# ═══════════════════════════════════════════════════

class WBSNode:
    """WBS树节点"""
    def __init__(self, name: str = "", description: str = "",
                 level: int = 0, parent: Optional['WBSNode'] = None):
        self.name = name                     # 节点名称
        self.description = description       # 节点描述
        self.level = level                   # 层级（0=根节点）
        self.parent = parent                 # 父节点
        self.children: list['WBSNode'] = []  # 子节点
        self.code: str = ""                  # WBS编码 (如 "1.2.3")
        self.is_work_package: bool = False   # 是否为工作包（叶节点）
        self.deliverable: str = ""           # 交付物描述
        self.o: Optional[float] = None       # 乐观估算（天）
        self.m: Optional[float] = None       # 最可能估算（天）
        self.p: Optional[float] = None       # 悲观估算（天）

    def to_dict(self) -> dict:
        """递归转为字典"""
        d = {
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "level": self.level,
            "work_package": self.is_work_package,
            "deliverable": self.deliverable,
            "o": self.o, "m": self.m, "p": self.p,
        }
        if self.children:
            d["children"] = [c.to_dict() for c in self.children]
        return d

    def __repr__(self) -> str:
        return f"WBSNode({self.code or '?'}: {self.name})"


class WBSResult:
    """完整的WBS分解结果"""
    def __init__(self):
        self.project_name: str = ""
        self.method_name: str = ""               # 使用的分解方法
        self.root: Optional[WBSNode] = None       # WBS根节点
        self.work_packages: list[WBSNode] = []    # 所有工作包（叶节点）
        self.validation_issues: list[str] = []    # 验证问题列表
        self.is_valid: bool = False               # 是否通过验证
        self.max_depth: int = 0                   # 实际最大深度

    def collect_work_packages(self) -> list[WBSNode]:
        """收集所有叶节点（工作包）"""
        self.work_packages = []

        def _collect(node: WBSNode):
            if not node.children:
                self.work_packages.append(node)
            for c in node.children:
                _collect(c)

        if self.root:
            _collect(self.root)
        return self.work_packages

    def to_dict(self) -> dict:
        """转为完整字典"""
        self.collect_work_packages()
        return {
            "project": self.project_name,
            "method": self.method_name,
            "max_depth": self.max_depth,
            "valid": self.is_valid,
            "issues": self.validation_issues,
            "work_packages": [
                {"code": wp.code, "name": wp.name,
                 "deliverable": wp.deliverable,
                 "o": wp.o, "m": wp.m, "p": wp.p}
                for wp in self.work_packages
            ],
            "tree": self.root.to_dict() if self.root else None,
        }


# ═══════════════════════════════════════════════════
# 2. 参考模板骨架
# ═══════════════════════════════════════════════════

# 模板1: 交付成果式（最通用）
TEMPLATE_DELIVERABLE = {
    "name": "交付成果式",
    "description": "按项目最终交付物的组成部分分解。最推荐，适用于大多数项目。",
    "skeleton": {
        "需求工程": ["需求调研与分析", "需求文档编写", "需求评审确认"],
        "设计": ["架构设计", "详细设计"],
        "开发/实现": None,   # None = LLM自定义填充
        "测试": ["单元测试", "集成测试", "验收测试"],
        "部署发布": ["环境准备", "部署实施", "上线验证"],
        "项目管理": ["进度跟踪", "质量评审"],
    }
}

# 模板2: 生命周期式（流程类项目）
TEMPLATE_LIFECYCLE = {
    "name": "生命周期式",
    "description": "按项目自然阶段分解。适用于流程清晰、重复性高的项目。",
    "skeleton": {
        "可行性阶段": ["市场/需求调研", "可行性评估报告"],
        "规划阶段": ["详细设计", "资源计划", "风险识别"],
        "执行阶段": None,
        "监控阶段": ["进度检查", "质量审计"],
        "收尾阶段": ["验收交付", "文档归档", "总结复盘"],
    }
}

# 模板3: 模块组件式（系统/软件/AI项目）
TEMPLATE_MODULAR = {
    "name": "模块组件式",
    "description": "按系统功能模块划分。适用于软件开发、AI系统等模块化项目。",
    "skeleton": {
        "基础设施": ["环境搭建", "技术选型"],
        "核心模块A": ["接口设计", "功能开发", "模块测试"],
        "核心模块B": ["接口设计", "功能开发", "模块测试"],
        "集成与联调": ["接口对接", "联调测试"],
        "测试验证": ["性能测试", "验收测试"],
        "发布上线": ["部署文档", "生产发布"],
    }
}

# 模板注册表（供LLM选择参考）
WBS_TEMPLATES = {
    "deliverable": TEMPLATE_DELIVERABLE,
    "lifecycle": TEMPLATE_LIFECYCLE,
    "modular": TEMPLATE_MODULAR,
}


def get_template_info() -> str:
    """返回模板注册信息供LLM参考"""
    lines = ["## 可用的WBS参考骨架模板\n"]
    for key, tmpl in WBS_TEMPLATES.items():
        lines.append(f"### {tmpl['name']} (`{key}`)")
        lines.append(f"{tmpl['description']}")
        lines.append(f"骨架：{list(tmpl['skeleton'].keys())}\n")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════
# 3. WBS树构建辅助函数
# ═══════════════════════════════════════════════════

def build_node_tree(
    children_data: dict,
    parent: WBSNode,
    name_key: str = "name",
    desc_key: str = "description"
) -> None:
    """
    从结构化数据构建WBS树（由LLM填充后的数据）
    children_data: {name: {description, children: {...或[str,...]}, ...}
    """
    if not children_data:
        return

    for idx, (child_name, child_info) in enumerate(children_data.items()):
        node = WBSNode(
            name=child_name,
            level=parent.level + 1,
            parent=parent
        )

        if isinstance(child_info, dict):
            node.description = child_info.get("description", "")
            node.deliverable = child_info.get("deliverable", "")
            node.o = child_info.get("o")
            node.m = child_info.get("m")
            node.p = child_info.get("p")

            # 递归构建子节点
            sub_children = child_info.get("children")
            if sub_children:
                if isinstance(sub_children, list):
                    for i, item in enumerate(sub_children):
                        if isinstance(item, str):
                            leaf = WBSNode(
                                name=item,
                                level=node.level + 1,
                                parent=node
                            )
                            leaf.is_work_package = True
                            node.children.append(leaf)
                        elif isinstance(item, dict):
                            sub_node = WBSNode(
                                name=item.get("name", f"子任务{i+1}"),
                                description=item.get("description", ""),
                                level=node.level + 1,
                                parent=node
                            )
                            sub_node.deliverable = item.get("deliverable", "")
                            sub_node.o = item.get("o")
                            sub_node.m = item.get("m")
                            sub_node.p = item.get("p")
                            sub_node.is_work_package = True
                            node.children.append(sub_node)
                elif isinstance(sub_children, dict):
                    build_node_tree(sub_children, node)
            else:
                node.is_work_package = True

        elif isinstance(child_info, list):
            # 简写：[子节点名称列表] → 全部为工作包
            for leaf_name in child_info:
                leaf = WBSNode(
                    name=leaf_name,
                    level=node.level + 1,
                    parent=node
                )
                leaf.is_work_package = True
                node.children.append(leaf)
        else:
            node.is_work_package = True

        parent.children.append(node)


def assign_wbs_codes(root: WBSNode, prefix: str = "") -> None:
    """递归分配WBS编码 (如 1.2.3)"""
    for idx, child in enumerate(root.children or []):
        child.code = f"{prefix}{idx + 1}" if not prefix else f"{prefix}.{idx + 1}"
        assign_wbs_codes(child, child.code)


def calc_max_depth(root: WBSNode) -> int:
    """计算树的最大深度"""
    if not root.children:
        return root.level

    max_d = 0
    for c in root.children:
        d = calc_max_depth(c)
        if d > max_d:
            max_d = d
    return max_d


def meets_termination_conditions(node: WBSNode) -> bool:
    """
    检查节点是否满足工作包终止条件（启发式标记，供LLM参考）

    条件：
    1. 可估算 — 有OMP值或可合理推断
    2. 可分配 — 单一责任人或角色
    3. 可验证 — 有交付物
    4. 可控制 — 不跨里程碑
    """
    has_deliverable = bool(node.deliverable)
    has_o = node.o is not None
    has_name = bool(node.name) and len(node.name) >= 2

    # 描述作为加分项但不是必要条件
    # 有交付物+名称即可视为满足终止条件
    return (has_deliverable or has_o) and has_name


# ═══════════════════════════════════════════════════
# 4. 100%规则验证
# ═══════════════════════════════════════════════════

def validate_wbs(result: WBSResult, max_depth: int = 4) -> WBSResult:
    """
    100%规则启发式验证

    检查项：
    - 最小子节点数：每个非叶节点至少2个子节点
    - 无"其他"遗漏：子节点名称不含"其他/等等"
    - 深度合规：无超过max_depth的路径
    - 名称非空：所有节点有名称
    """
    issues = []

    if not result.root:
        issues.append("WBS根节点为空")
        result.is_valid = False
        result.validation_issues = issues
        return result

    def _check(node: WBSNode, path: str):
        if not node.name or len(node.name.strip()) < 2:
            issues.append(f"{path}: 节点名称为空或过短")

        if node.is_work_package:
            return

        if node.children:
            # 最小子节点数
            if len(node.children) < 2:
                issues.append(f"{path}「{node.name}」: 子节点少于2个，建议至少拆为2项")

            # 无"其他"遗漏
            for c in node.children:
                omit_words = ["其他", "等等", "其它", "其他工作", "杂项"]
                for w in omit_words:
                    if w in c.name:
                        issues.append(
                            f"{path}「{node.name}」→「{c.name}」: "
                            f"含「{w}」字样，可能是分解未尽"
                        )

            # 递归检查
            for i, c in enumerate(node.children):
                child_path = f"{path}.{i+1}" if path else f"{i+1}"
                _check(c, child_path)
        else:
            # 非工作包但没有子节点
            issues.append(f"{path}「{node.name}」: 非工作包但无子节点，请确认是否分解完成")

    _check(result.root, "")

    # 深度检查
    result.max_depth = calc_max_depth(result.root)
    if result.max_depth > max_depth:
        issues.append(f"最大深度 {result.max_depth} 超过限制 {max_depth}")

    # ── WBS粒度检查 ──
    if result.root and result.root.children:
        # 收集所有L2节点（根节点的直接子节点）
        l2_nodes = [c for c in result.root.children if c.level <= 2]
        for node in l2_nodes:
            name_lower = node.name.lower()
            # 识别核心技术类阶段（AI/ML/Skill/Engine等）
            core_keywords = ["ai", "智能体", "agent", "skill", "引擎", "engine",
                             "模型", "model", "learning", "算法", "algorithm"]
            is_core = any(k in name_lower for k in core_keywords)

            # 收集该阶段下的工作包（叶节点）
            def count_work_packages(n: WBSNode) -> int:
                if n.is_work_package:
                    return 1
                return sum(count_work_packages(c) for c in n.children)

            wp_count = count_work_packages(node)

            if is_core and wp_count < 5:
                issues.append(
                    f"「{node.name}」为核心技术阶段，仅{wp_count}个工作包，"
                    f"建议至少分解为5个以上子任务"
                )
            elif wp_count < 3:
                issues.append(
                    f"「{node.name}」仅{wp_count}个工作包，"
                    f"建议至少分解为3个以上子任务"
                )

        # 检查总工作包数是否与项目规模匹配
        total_wps = len(result.work_packages) if result.work_packages else 0
        total_l2 = len(l2_nodes)
        if total_l2 >= 5 and total_wps < total_l2 * 2:
            issues.append(
                f"项目共{total_l2}个阶段，仅{total_wps}个工作包，"
                f"平均每阶段{total_wps/total_l2:.1f}个，建议每阶段至少2-3个工作包"
            )

        # 检查交付物完整性
        for wp in (result.work_packages or []):
            if not wp.deliverable or len(wp.deliverable.strip()) < 2:
                issues.append(f"工作包「{wp.name}」缺少交付物描述")

    result.validation_issues = issues
    result.is_valid = len(issues) == 0
    return result


# ═══════════════════════════════════════════════════
# 5. WBS → Phase 0 估算参数转换
# ═══════════════════════════════════════════════════

def wbs_to_phases(result: WBSResult) -> list[dict]:
    """
    将WBS工作包转换为估算阶段参数列表

    返回: [{name, o, m, p, deliverable}, ...]
    紧前关系按WBS层级自动推演（同级从左到右FS串联）
    """
    result.collect_work_packages()

    phases = []
    for wp in result.work_packages:
        phase = {
            "name": wp.name,
            "o": wp.o or 0,
            "m": wp.m or 0,
            "p": wp.p or 0,
            "deliverable": wp.deliverable,
        }
        phases.append(phase)

    return phases


def wbs_to_dependencies(result: WBSResult) -> dict[int, list[tuple[int, str]]]:
    """
    根据WBS层级结构自动推演紧前关系

    规则：
    - 同一父节点的子节点（同组）：按 WBS 编码顺序 FS 串联
    - 跨父节点边界：本组第一个任务依赖上一组中 M 值最大的任务（FS）
    """
    result.collect_work_packages()
    wps = result.work_packages

    # 按code排序确保顺序
    sorted_wps = sorted(enumerate(wps), key=lambda x: x[1].code)

    deps: dict[int, list[tuple[int, str]]] = {}

    # 按父节点分组
    groups: list[list[tuple[int, 'WBSNode']]] = []
    current_group: list[tuple[int, 'WBSNode']] = []

    for item in sorted_wps:
        if not current_group:
            current_group.append(item)
        else:
            _, prev_wp = current_group[-1]
            _, wp = item
            if wp.parent and prev_wp.parent and wp.parent == prev_wp.parent:
                current_group.append(item)
            else:
                groups.append(current_group)
                current_group = [item]
    if current_group:
        groups.append(current_group)

    for g_idx, group in enumerate(groups):
        for i, item in enumerate(group):
            idx, wp = item
            if g_idx == 0 and i == 0:
                # 第一组第一个任务：无前置
                deps[idx] = []
            elif g_idx > 0 and i == 0:
                # 跨组边界：本组第一个依赖上一组 max-M 任务
                prev_group = groups[g_idx - 1]
                prev_constraint = max(prev_group, key=lambda x: x[1].m or 0)
                deps[idx] = [(prev_constraint[0], "FS")]
            elif i > 0:
                # 组内串联：前一个 → 当前，用 infer_dep_type
                prev_idx, prev_wp = group[i - 1]
                dep_type = "FS"
                try:
                    from analysis_engine import infer_dep_type
                    dep_type = infer_dep_type(
                        prev_wp.name or "",
                        wp.name or ""
                    )
                except ImportError:
                    pass
                deps[idx] = [(prev_idx, dep_type)]
            else:
                deps[idx] = []

    return deps


# ═══════════════════════════════════════════════════
# 6. 输出格式化
# ═══════════════════════════════════════════════════

def format_text_tree(result: WBSResult, use_emoji: bool = False) -> str:
    """格式A: 缩进文本树（控制台快速展示）
    use_emoji: True 时使用 📁📄 图标（仅限 UTF-8 终端）
               False 时使用 [P] [T] [W] ASCII 安全标记
    """
    if not result.root:
        return "[空WBS]"

    lines = []
    project_icon = "📁" if use_emoji else "[P]"
    wp_icon = "📄" if use_emoji else "[W]"
    task_icon = "📁" if use_emoji else "[T]"

    def _walk(node: WBSNode, prefix: str, is_last: bool):
        connector = "└── " if is_last else "├── "
        icon = wp_icon if node.is_work_package else task_icon

        name_part = f"{icon} {node.name}"
        if node.code:
            name_part = f"{name_part} ({node.code})"
        if node.is_work_package and node.deliverable:
            name_part += f" → {node.deliverable}"
        if node.is_work_package and node.o is not None:
            name_part += f" [{node.o}/{node.m}/{node.p}]"

        lines.append(f"{prefix}{connector}{name_part}")

        child_prefix = prefix + ("    " if is_last else "│   ")
        for i, child in enumerate(node.children):
            _walk(child, child_prefix, i == len(node.children) - 1)

    # 根节点
    lines.append(f"{project_icon} {result.project_name}")
    for i, child in enumerate(result.root.children or []):
        _walk(child, "", i == len(result.root.children) - 1)

    return "\n".join(lines)


def format_markdown_tree(result: WBSResult) -> str:
    """格式B: Markdown结构化树"""
    if not result.root:
        return "# 空WBS\n\n*无数据*"

    lines = [f"# WBS: {result.project_name}", f"**分解方法**: {result.method_name}", ""]

    def _walk(node: WBSNode):
        level = node.level
        heading = "#" * min(level + 2, 6)

        if node.is_work_package:
            code_part = f"### {node.code} " if node.code else ""
            lines.append(f"{code_part}{node.name}")
            lines.append(f"- **交付物**: {node.deliverable or '待确认'}")
            if node.o is not None:
                lines.append(f"- **估算**: O={node.o} / M={node.m} / P={node.p} (天)")
            lines.append("")
        else:
            code_part = f"{node.code} " if node.code else ""
            lines.append(f"{heading} {code_part}{node.name}")
            lines.append("")

        for child in node.children:
            _walk(child)

    for child in result.root.children:
        _walk(child)

    return "\n".join(lines)


def format_json(result: WBSResult, indent: int = 2) -> str:
    """格式C: WBS字典JSON"""
    return json.dumps(result.to_dict(), ensure_ascii=False, indent=indent)


def format_svg_tree(result: WBSResult, width: int = 800) -> str:
    """格式D: SVG树形图"""
    if not result.root or not result.root.children:
        return (f'<svg width="{width}" height="200" xmlns="http://www.w3.org/2000/svg">'
                f'<text x="{width//2}" y="100" text-anchor="middle" fill="#999">暂无数据</text></svg>')

    all_nodes: list[WBSNode] = []
    def _flatten(node: WBSNode):
        all_nodes.append(node)
        for c in node.children:
            _flatten(c)

    _flatten(result.root)

    # 布局参数
    v_gap = 50       # 垂直间距
    h_gap = 20       # 水平间距
    node_h = 36      # 节点高度
    level_widths: dict[int, int] = {}  # 每层节点数
    for n in all_nodes:
        level_widths[n.level] = level_widths.get(n.level, 0) + 1

    max_level = max(n.level for n in all_nodes) if all_nodes else 0
    max_width = max(level_widths.values()) if level_widths else 3

    # 动态计算画布尺寸
    svg_w = max(width, max_width * 180)
    svg_h = (max_level + 1) * v_gap + 100

    # 按层分配节点位置（居中）
    level_positions: dict[int, list[tuple[WBSNode, int]]] = {}  # level -> [(node, x), ...]
    for n in all_nodes:
        level_positions.setdefault(n.level, [])

    # 先计算每层的x位置
    lvl_nodes = level_positions.get(0, [])
    if result.root not in [n for n, _ in lvl_nodes]:
        root_x = svg_w // 2
        level_positions[0] = [(result.root, root_x)]

    def _layout(node: WBSNode):
        if not node.children:
            return
        children = node.children
        ch_count = len(children)
        parent_x = 0
        for n, x in level_positions.get(node.level, []):
            if n == node:
                parent_x = x
                break

        total_w = ch_count * 180
        start_x = parent_x - total_w // 2 + 80

        for i, child in enumerate(children):
            cx = start_x + i * 180
            level_positions.setdefault(child.level, []).append((child, cx))
            _layout(child)

    _layout(result.root)

    # 构建SVG
    colors = ['#667eea', '#764ba2', '#4facfe', '#43e97b', '#f093fb', '#ff9671', '#ffc75f', '#845ec2']
    svg = [
        f'<svg width="{svg_w}" height="{svg_h}" xmlns="http://www.w3.org/2000/svg">',
        f'<rect width="{svg_w}" height="{svg_h}" fill="#fafbff"/>',
        f'<text x="{svg_w//2}" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#333">WBS: {result.project_name}</text>',
        f'<text x="{svg_w//2}" y="50" text-anchor="middle" font-size="12" fill="#888">分解方法: {result.method_name}</text>',
    ]

    # 绘制连线
    for node in all_nodes:
        if not node.children:
            continue
        parent_y = 70 + node.level * v_gap + node_h
        parent_x = 0
        for n, x in level_positions.get(node.level, []):
            if n == node:
                parent_x = x
                break

        for child in node.children:
            child_y = 70 + child.level * v_gap
            child_x = 0
            for n, x in level_positions.get(child.level, []):
                if n == child:
                    child_x = x
                    break

            if parent_x and child_x:
                # 竖直线
                mid_y = (parent_y + child_y) / 2
                svg.append(
                    f'<path d="M{parent_x},{parent_y} L{parent_x},{mid_y} '
                    f'L{child_x},{mid_y} L{child_x},{child_y}" '
                    f'fill="none" stroke="#ccc" stroke-width="1.5"/>'
                )

    # 绘制节点
    for level in sorted(level_positions.keys()):
        for node, x in level_positions[level]:
            y = 70 + level * v_gap
            color = colors[level % len(colors)]
            radius = 6

            if node.is_work_package:
                # 工作包：矩形
                svg.append(
                    f'<rect x="{x-80}" y="{y}" width="160" height="{node_h}" '
                    f'rx="{radius}" ry="{radius}" fill="{color}" opacity="0.15" '
                    f'stroke="{color}" stroke-width="1.5"/>'
                )
            else:
                # 父节点：圆角矩形
                svg.append(
                    f'<rect x="{x-80}" y="{y}" width="160" height="{node_h}" '
                    f'rx="{radius}" ry="{radius}" fill="{color}" opacity="0.1" '
                    f'stroke="{color}" stroke-width="1.5" stroke-dasharray="4,2"/>'
                )

            # 节点名称
            display_name = node.name if len(node.name) <= 10 else node.name[:9] + "…"
            svg.append(
                f'<text x="{x}" y="{y + node_h//2 + 5}" text-anchor="middle" '
                f'font-size="12" fill="#333">{display_name}</text>'
            )

            # 编码
            if node.code:
                svg.append(
                    f'<text x="{x}" y="{y - 5}" text-anchor="middle" '
                    f'font-size="9" fill="#999">{node.code}</text>'
                )

    # 图例
    ly = svg_h - 30
    svg.append(f'<rect x="20" y="{ly}" width="14" height="14" rx="3" fill="#667eea" opacity="0.15" stroke="#667eea" stroke-width="1.5" stroke-dasharray="4,2"/>')
    svg.append(f'<text x="40" y="{ly+11}" font-size="11" fill="#666">父节点</text>')
    svg.append(f'<rect x="120" y="{ly}" width="14" height="14" rx="3" fill="#4facfe" opacity="0.15" stroke="#4facfe" stroke-width="1.5"/>')
    svg.append(f'<text x="140" y="{ly+11}" font-size="11" fill="#666">工作包</text>')

    # 工作包统计
    wp_count = len(result.work_packages)
    svg.append(f'<text x="{svg_w - 20}" y="{ly+11}" text-anchor="end" font-size="11" fill="#888">共 {wp_count} 个工作包</text>')

    svg.append('</svg>')
    return '\n'.join(svg)


# ═══════════════════════════════════════════════════
# 7. WBS输出管理器
# ═══════════════════════════════════════════════════

class WBSOutput:
    """WBS输出管理器（LLM根据用户选择调用）"""
    _outputs: dict[str, str] = {}

    @staticmethod
    def build(result: WBSResult, output_formats: list[str] = None) -> dict[str, str]:
        """
        构建指定格式的输出

        output_formats: ['text', 'markdown', 'json', 'svg']
        默认: ['text']
        """
        if output_formats is None:
            output_formats = ['text']

        result.collect_work_packages()

        outputs = {}
        if 'text' in output_formats:
            outputs['text'] = format_text_tree(result)
        if 'markdown' in output_formats:
            outputs['markdown'] = format_markdown_tree(result)
        if 'json' in output_formats:
            outputs['json'] = format_json(result)
        if 'svg' in output_formats:
            outputs['svg'] = format_svg_tree(result)

        WBSOutput._outputs = outputs
        return outputs

    @staticmethod
    def get(format_name: str) -> str:
        return WBSOutput._outputs.get(format_name, "")


# ═══════════════════════════════════════════════════
# 8. 全流程状态标记
# ═══════════════════════════════════════════════════

class WBSFlowState:
    """WBS全流程状态（供LLM追踪执行进度）"""
    def __init__(self):
        self.step: int = 0
        self.description: str = ""          # 用户原始描述
        self.template: str = ""              # 选中的模板key
        self.result: Optional[WBSResult] = None
        self.phases: list[dict] = []         # 转换后的阶段参数
        self.dependencies: dict = {}         # 紧前关系

    def summary(self) -> str:
        """输出当前状态摘要"""
        lines = [f"WBS全流程状态 (步骤 {self.step})"]
        if self.result:
            wp_count = len(self.result.work_packages)
            lines.append(f"  WBS: {self.result.project_name}")
            lines.append(f"  方法: {self.result.method_name}")
            lines.append(f"  工作包: {wp_count} 个")
            lines.append(f"  验证: {'✅通过' if self.result.is_valid else '❌有' + str(len(self.result.validation_issues)) + '个问题'}")
        return "\n".join(lines)
