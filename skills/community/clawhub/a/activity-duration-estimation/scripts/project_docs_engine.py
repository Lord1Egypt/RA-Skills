"""
activity-duration-estimation :project-docs 引擎
双模式项目文档生成：手动模式（空模版） + 自动模式（逐节生成）
"""
import json
import os
from datetime import date
from typing import Optional

# R-12 审计锚点：数据目录字面量声明
DEFAULT_DATA_DIR_RAW = "skills/.standardization/activity-duration-estimation/data/"
_skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_data_dir_abs = os.path.normpath(os.path.join(_skill_dir, "..", DEFAULT_DATA_DIR_RAW))


# ═══════════════════════════════════════════════════
# 思维工具参考（手动模式时嵌入各章节的示例）
# ═══════════════════════════════════════════════════

TOOL_REFERENCES = {
    "background": {
        "name": "SWOT分析 + 5W2H",
        "purpose": "SWOT从内外部分析项目必要性；5W2H系统化覆盖七个维度，确保背景分析无遗漏",
        "example": (
            "> 💡 **参考：SWOT分析框架**\n"
            "> \n"
            "> | 维度 | 内容 |\n"
            "> |------|------|\n"
            "> | **S**trength（优势） | 内部有利因素，如：团队经验、技术积累 |\n"
            "> | **W**eakness（劣势） | 内部不利因素，如：资源不足、经验缺失 |\n"
            "> | **O**pportunity（机会） | 外部有利因素，如：政策支持、市场空白 |\n"
            "> | **T**hreat（威胁） | 外部不利因素，如：竞品、技术变更 |\n"
            "> \n"
            "> 亦可用 **5W2H** 检查覆盖度：What/Why/Who/Where/When/How/How much"
        ),
    },
    "objectives": {
        "name": "SMART原则",
        "purpose": "确保每个目标具体、可衡量、可达成、相关、有时限",
        "example": (
            "> 💡 **参考：SMART原则**\n"
            "> \n"
            "> | 维度 | 要求 | 示例 |\n"
            "> |------|------|------|\n"
            "> | **S**pecific（具体） | 明确做什么 | 开发电商后台管理系统 |\n"
            "> | **M**easurable（可衡量） | 有量化指标 | 日活>1000，加载<2s |\n"
            "> | **A**chievable（可实现） | 资源匹配 | 6人团队，4个月工期 |\n"
            "> | **R**elevant（相关） | 对齐业务目标 | 支撑电商战略 |\n"
            "> | **T**ime-bound（有时限） | 截止日期 | 2026年9月30日 |\n"
            "> \n"
            "> 每个目标逐项检查五维是否齐全。缺失任一维度即需补充。"
        ),
    },
    "scope": {
        "name": "MoSCoW + 思维导图",
        "purpose": "MoSCoW明确必须做/应该做/可以做/不做的边界；思维导图确保范围完整",
        "example": (
            "> 💡 **参考：MoSCoW优先级分类**\n"
            "> \n"
            "> | 分类 | 含义 | 示例 |\n"
            "> |------|------|------|\n"
            "> | **M**ust have | 必须实现，否则项目不达标 | 商品CRUD、订单流转 |\n"
            "> | **S**hould have | 应该实现，有替代方案可缓 | 数据看板、批量导入 |\n"
            "> | **C**ould have | 锦上添花，资源充裕时做 | 移动端适配、多语言 |\n"
            "> | **W**on't have | 本次明确不做（防蔓延） | 支付对接（二期） |\n"
            "> \n"
            "> 建议先用 **思维导图** 放射状罗列所有功能点，再归类到MoSCoW四象限。"
        ),
    },
    "wbs_overview": {
        "name": "思维导图 + Top-down & Bottom-up",
        "purpose": "自上而下出骨架，自下而上补充细节，双路径交叉验证确保100%覆盖",
        "example": (
            "> 💡 **参考：双路径分解法**\n"
            "> \n"
            "> 1. **Top-down**：从项目目标出发，逐层细化（L1→L2→L3→工作包）\n"
            "> 2. **Bottom-up**：收集所有具体任务，逐级归纳归类\n"
            "> 3. **交叉验证**：两条路径对比，查漏补缺\n"
            "> \n"
            "> 遵守 **100%规则**：子节点之和必须完整覆盖父节点，不多不少。\n"
            "> 工作包需满足：可估算（≤80h）+ 可分配 + 可验证 + 可控制。"
        ),
    },
    "risks": {
        "name": "Pareto（80/20法则）+ 概率-影响矩阵",
        "purpose": "聚焦关键风险的20%，用矩阵量化评估每条风险的等级",
        "example": (
            "> 💡 **参考：Pareto + 风险矩阵**\n"
            "> \n"
            "> 第一步：列出所有风险，**Pareto分析**找出影响最大的前20%\n"
            "> \n"
            "> 第二步：用**概率-影响矩阵**评估每条风险：\n"
            "> \n"
            "> | 概率\\影响 | 低 | 中 | 高 |\n"
            "> |-----------|----|----|----|\n"
            "> | 高 | 中 | 高 | 极高 |\n"
            "> | 中 | 低 | 中 | 高 |\n"
            "> | 低 | 低 | 低 | 中 |\n"
            "> \n"
            "> 优先级：极高→高（立即响应）> 中（制定计划）> 低（监控即可）"
        ),
    },
    "lessons_learned": {
        "name": "PDCA + 鱼骨图",
        "purpose": "PDCA按四阶段回顾执行过程；鱼骨图从六个维度追溯根因，避免表面归因",
        "example": (
            "> 💡 **参考：PDCA + 鱼骨图**\n"
            "> \n"
            "> **PDCA四阶段回顾**:\n"
            "> - **P**lan（计划）→ **D**o（执行）→ **C**heck（检查）→ **A**ct（处理）\n"
            "> \n"
            "> **鱼骨图六维度根因分析**:\n"
            "> | 维度 | 说明 |\n"
            "> |------|------|\n"
            "> | 人（Man） | 人员技能、配置、稳定性 |\n"
            "> | 机（Machine） | 工具、环境、设备 |\n"
            "> | 料（Material） | 数据、依赖、第三方服务 |\n"
            "> | 法（Method） | 流程、规范、方法 |\n"
            "> | 环（Environment） | 政策、市场、组织 |\n"
            "> | 测（Measurement） | 评估标准、数据采集 |\n"
            "> \n"
            "> 每条经验教训至少追问三次'为什么'直到找到根因。"
        ),
    },
    "stakeholders": {
        "name": "RACI矩阵",
        "purpose": "明确每个任务/决策的权责关系，避免推诿和决策真空",
        "example": (
            "> 💡 **参考：RACI权责矩阵**\n"
            "> \n"
            "> | 角色\\任务 | 需求确认 | 方案设计 | 开发实现 | 验收测试 | 审批 |\n"
            "> |-----------|---------|---------|---------|---------|------|\n"
            "> | 项目经理 | A | R | I | A | R |\n"
            "> | 业务方 | R | C | I | R | I |\n"
            "> | 开发团队 | C | A | R/A | I | - |\n"
            "> | 审批人 | I | I | - | I | A |\n"
            "> \n"
            "> R=执行人  A=最终责任人  C=咨询  I=告知\n"
            "> 每个任务必须有且仅有一个A，不可空缺也不可多人。"
        ),
    },
    "schedule": {
        "name": "关键路径法（CPM）",
        "purpose": "识别影响项目总工期的关键任务链，集中管理不允延误的任务",
        "example": (
            "> 💡 **参考：CPM关键路径**\n"
            "> \n"
            "> 总时差（TF）= LS - ES，TF=0的任务即为关键任务。\n"
            "> 关键路径决定了项目最短工期，路径上的任何延误都直接影响交付。\n"
            "> \n"
            "> 若已有CPM分析结果，关键路径和P50/P90数据可直接引用。"
        ),
    },
    "quality": {
        "name": "PDCA循环",
        "purpose": "按Plan-Do-Check-Act四阶段系统回顾质量管理的执行效果",
        "example": (
            "> 💡 **参考：PDCA循环**\n"
            "> \n"
            "> 1. **P**lan：计划了什么质量标准？目标值多少？\n"
            "> 2. **D**o：实际执行了什么质量活动？\n"
            "> 3. **C**heck：实际结果 vs 目标，偏差多少？\n"
            "> 4. **A**ct：哪些做法可标准化？哪些需要改进？\n"
            "> \n"
            "> 每个环节既有'计划'也要有'实际'的对比。"
        ),
    },
}


def get_tool_reference(section_key: str) -> str:
    """获取指定章节的思维工具参考文本（含框架说明+示例）"""
    tool = TOOL_REFERENCES.get(section_key)
    if not tool:
        return ""
    return (
        f"> 🔧 **推荐工具**: {tool['name']}\n"
        f"> **目的**: {tool['purpose']}\n"
        ">\n"
        f"{tool['example']}\n"
    )


def inject_tool_references(markdown: str, customized: dict) -> str:
    """
    在生成的MD文档中，为各章节注入思维工具参考。
    在每个章节的结束分界线(---)之前插入工具参考。
    """
    lines = markdown.split("\n")
    result = []
    current_section_key = None

    for line in lines:
        # 检测章节标题
        if line.startswith("## "):
            # 从标题找对应的section key
            title = line[3:].strip()
            for sec in customized.get("sections", []):
                if sec.get("title") == title:
                    current_section_key = sec.get("key")
                    break
                # 也检查是否包含
                if title in sec.get("title", "") or sec.get("title") in title:
                    current_section_key = sec.get("key")
        elif line.strip() == "---" and current_section_key:
            # 在章节结束标记前注入工具参考
            tool_ref = get_tool_reference(current_section_key)
            if tool_ref:
                result.append("")
                result.extend(tool_ref.strip().split("\n"))
            current_section_key = None

        result.append(line)

    return "\n".join(result)


# ═══════════════════════════════════════════════════
# 1. 数据结构
# ═══════════════════════════════════════════════════

TEMPLATES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "references", "templates"
)


class ProjectData:
    """项目资料数据，由WBS/估算/CPM等子技能的产出物填充"""
    def __init__(self):
        self.project_name: str = ""
        self.project_description: str = ""
        self.project_type: str = ""           # 软件/建筑/制造/科研/农业/活动/通用
        self.wbs_tree_text: str = ""           # WBS文本树
        self.wbs_json: str = ""                # WBS字典JSON字符串
        self.wbs_work_packages: list[dict] = []  # 工作包列表
        self.estimation_result: str = ""       # 估算结果摘要
        self.cpm_result: str = ""              # CPM关键路径结果
        self.p50: Optional[float] = None       # P50工期
        self.p90: Optional[float] = None       # P90工期
        self.project_duration: Optional[float] = None
        self.critical_path: list[str] = []     # 关键路径任务名列表
        self.gantt_svg: str = ""               # 甘特图SVG
        self.semantic_analysis: str = ""       # 语义分析结果
        self.custom_notes: dict = {}           # 用户自定义备注

    @staticmethod
    def from_wbs_result(wbs_dict: dict) -> 'ProjectData':
        """从WBS字典构建项目资料"""
        pd = ProjectData()
        pd.project_name = wbs_dict.get("project", "")
        pd.wbs_json = json.dumps(wbs_dict, ensure_ascii=False, indent=2)
        wps = wbs_dict.get("work_packages", [])
        pd.wbs_work_packages = wps

        # 构建文本树描述
        tree = wbs_dict.get("tree", {})
        if tree and "children" in tree:
            lines = [f"WBS: {pd.project_name}"]
            for c in tree["children"]:
                pd._build_text_tree(c, lines, "")
            pd.wbs_tree_text = "\n".join(lines)

        return pd

    def _build_text_tree(self, node: dict, lines: list, prefix: str):
        """递归构建WBS文本树"""
        icon = "📄" if node.get("work_package") else "📁"
        name = node.get("name", "?")
        code = node.get("code", "")
        code_str = f" ({code})" if code else ""
        lines.append(f"{prefix}{icon} {name}{code_str}")

        for i, child in enumerate(node.get("children", [])):
            is_last = i == len(node["children"]) - 1
            child_prefix = prefix + ("    " if is_last else "│   ")
            self._build_text_tree(child, lines, child_prefix)

    def summary(self) -> str:
        """输出资料摘要用于LLM上下文"""
        lines = [
            f"项目名称: {self.project_name}",
            f"项目类型: {self.project_type or '未分类'}",
            f"描述: {self.project_description or '无'}",
        ]
        if self.p50 is not None:
            lines.append(f"估算工期: P50={self.p50}, P90={self.p90}")
        if self.project_duration:
            lines.append(f"CPM总工期: {self.project_duration}")
        if self.critical_path:
            lines.append(f"关键路径: {'→'.join(self.critical_path)}")
        lines.append(f"工作包数: {len(self.wbs_work_packages)}")
        return "\n".join(lines)


# ═══════════════════════════════════════════════════
# 2. 模板加载
# ═══════════════════════════════════════════════════

def list_templates() -> dict[str, str]:
    """列出所有可用的模板"""
    templates = {}
    if not os.path.isdir(TEMPLATES_DIR):
        return templates

    for fname in sorted(os.listdir(TEMPLATES_DIR)):
        if fname.endswith(".json"):
            name = fname.replace(".json", "")
            # 读取description
            fpath = os.path.join(TEMPLATES_DIR, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                templates[name] = data.get("description", "")
            except Exception:
                templates[name] = ""

    return templates


def load_template(template_name: str) -> dict:
    """加载指定模板的JSON定义"""
    fpath = os.path.join(TEMPLATES_DIR, f"{template_name}.json")
    if not os.path.isfile(fpath):
        available = list(list_templates().keys())
        raise FileNotFoundError(
            f"模板 '{template_name}' 不存在。可用模板: {available}"
        )
    with open(fpath, "r", encoding="utf-8") as f:
        return json.load(f)


# ═══════════════════════════════════════════════════
# 3. 模板特化（根据项目资料定制模板）
# ═══════════════════════════════════════════════════

def customize_template(template: dict, project: ProjectData) -> dict:
    """
    根据项目资料特化模板：
    - 标题插入项目名称
    - 标记有引用资料的章节
    - 填充hint中的占位符
    """
    customized = json.loads(json.dumps(template))  # 深拷贝

    for section in customized.get("sections", []):
        refs = section.get("reference_sources", [])

        # 标记资料状态
        has_refs = []
        for ref in refs:
            if ref == "wbs_tree" and project.wbs_tree_text:
                has_refs.append("✅ WBS分解")
            elif ref == "wbs_json" and project.wbs_json:
                has_refs.append("✅ WBS字典")
            elif ref == "wbs_work_packages" and project.wbs_work_packages:
                has_refs.append(f"✅ 共{len(project.wbs_work_packages)}个工作包")
            elif ref == "wbs_scope" and project.wbs_tree_text:
                has_refs.append("✅ WBS范围")
            elif ref == "cpm_result" and project.cpm_result:
                has_refs.append("✅ CPM分析")
            elif ref == "estimation_result" and project.estimation_result:
                has_refs.append("✅ 历时估算")
            elif ref == "estimation_report":
                parts = []
                if project.p50 is not None:
                    parts.append(f"P50={project.p50}")
                if project.p90 is not None:
                    parts.append(f"P90={project.p90}")
                if parts:
                    has_refs.append(f"✅ 估算({', '.join(parts)})")
            elif ref == "project_description" and project.project_description:
                has_refs.append("✅ 项目描述")
            elif ref == "semantic_analysis" and project.semantic_analysis:
                has_refs.append("✅ 语义分析")
            elif ref == "risk_register":
                has_refs.append("(见风险登记册)")
            elif ref == "stakeholder_register":
                has_refs.append("(见相关方登记册)")

        section["_has_references"] = has_refs

    return customized


# ═══════════════════════════════════════════════════
# 4. 手动模式：输出空模板 Markdown
# ═══════════════════════════════════════════════════

def output_manual(template: dict, project: ProjectData) -> str:
    """
    手动模式：输出项目特化的空模板Markdown
    每节包含：标题、描述、填充提示、已有资料引用
    不生成任何正文内容
    """
    customized = customize_template(template, project)
    lines = []

    # 标题
    doc_name = template.get("name", "项目文档")
    project_name = project.project_name or "（项目名称）"
    lines.append(f"# {doc_name}")
    lines.append(f"**项目**: {project_name}")
    lines.append(f"**生成日期**: {date.today().isoformat()}")
    lines.append(f"**模式**: 手动填充（空模板）")
    lines.append("")

    # 项目资料摘要
    if project.wbs_tree_text or project.p50 is not None:
        lines.append("> **已有资料摘要**")
        if project.wbs_tree_text:
            lines.append("> - ✅ WBS工作分解已完成")
        if project.p50 is not None:
            lines.append(f"> - ✅ 历时估算: P50={project.p50}, P90={project.p90}")
        if project.critical_path:
            lines.append(f"> - ✅ CPM关键路径: {' → '.join(project.critical_path)}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # 各章节
    for section in customized.get("sections", []):
        sec_type = section.get("type", "rich_text")
        title = section.get("title", "未命名章节")
        desc = section.get("description", "")
        hint = section.get("hint", "")
        refs = section.get("_has_references", [])

        lines.append(f"## {title}")
        lines.append(f"> {desc}")
        lines.append("")

        # 已有资料引用
        if refs:
            lines.append("**可参考的已有资料**:")
            for r in refs:
                lines.append(f"- {r}")
            lines.append("")
        else:
            lines.append("**可参考的已有资料**:（暂无）")
            lines.append("")

        # 根据类型输出占位结构
        if sec_type == "fields":
            fields = section.get("fields", [])
            lines.append("| 字段 | 填写内容 |")
            lines.append("|------|---------|")
            for f in fields:
                label = f.get("label", f.get("key", "?"))
                hint_text = f.get("hint", "")
                lines.append(f"| **{label}** | {hint_text} |")
            lines.append("")

        elif sec_type == "table":
            cols = section.get("columns", [])
            rows = section.get("rows", 0)
            # 表头
            lines.append("| " + " | ".join(cols) + " |")
            lines.append("|" + "|".join(["---"] * len(cols)) + "|")
            # 空行
            row_count = rows if rows > 0 else 3
            for _ in range(row_count):
                lines.append("| " + " | ".join([""] * len(cols)) + " |")
            lines.append("")

        elif sec_type == "wbs_attachment":
            lines.append("```text")
            lines.append(project.wbs_tree_text or "（WBS分解结构，待填充）")
            lines.append("```")
            lines.append("")

        else:  # rich_text
            lines.append("")
            lines.append("---")
            lines.append("*（在此处填写内容）*")
            lines.append("")

        # 填充提示
        if hint:
            lines.append("> **填充提示**: " + hint)
            lines.append("")

        lines.append("---")
        lines.append("")

    # 附录
    appendix = template.get("appendix", [])
    if appendix:
        lines.append("## 附录")
        for a in appendix:
            lines.append(f"- {a.get('title', '未命名附件')}")
        lines.append("")

    raw = "\n".join(lines)
    return inject_tool_references(raw, customized)


# ═══════════════════════════════════════════════════
# 5. 自动模式：逐节生成
# ═══════════════════════════════════════════════════

class SectionGenState:
    """自动模式逐节生成的状态跟踪"""
    def __init__(self, template: dict, project: ProjectData):
        self.template = template
        self.project = project
        self.sections = template.get("sections", [])
        self.current_index: int = 0
        self.completed: list[dict] = []      # 已完成的节 {key, title, content}
        self.pending: list[dict] = []        # 待生成的节
        self.total = len(self.sections)

    @property
    def current_section(self) -> Optional[dict]:
        if self.current_index < self.total:
            return self.sections[self.current_index]
        return None

    @property
    def progress_text(self) -> str:
        return f"第 {self.current_index + 1}/{self.total} 节"

    def mark_done(self, content: str):
        """标记当前节已完成"""
        sec = self.current_section
        if sec:
            self.completed.append({
                "key": sec["key"],
                "title": sec["title"],
                "content": content
            })
        self.current_index += 1

    def get_context_for_llm(self) -> str:
        """为LLM生成当前节的上下文（只带之前节的摘要，不带全文）"""
        lines = [f"项目: {self.project.project_name}"]
        lines.append(f"文档类型: {self.template.get('name', '')}")
        lines.append(f"当前进度: {self.progress_text}")
        lines.append("")

        # 已有资料摘要
        summary = self.project.summary()
        if summary:
            lines.append("=== 项目资料 ===")
            lines.append(summary)
            lines.append("")

        # 已完成章节的摘要（仅标题+前100字）
        if self.completed:
            lines.append("=== 已完成章节摘要 ===")
            for c in self.completed:
                preview = c["content"][:100].replace("\n", " ") if c["content"] else "（空）"
                lines.append(f"- {c['title']}: {preview}...")
            lines.append("")

        # 当前节详情
        sec = self.current_section
        if sec:
            lines.append("=== 当前待生成章节 ===")
            lines.append(f"标题: {sec.get('title', '')}")
            lines.append(f"描述: {sec.get('description', '')}")
            lines.append(f"类型: {sec.get('type', 'rich_text')}")
            if sec.get("hint"):
                lines.append(f"填充提示: {sec['hint']}")

            refs = sec.get("reference_sources", [])
            if refs:
                lines.append("可参考的资料:")
                if "wbs_tree" in refs and self.project.wbs_tree_text:
                    lines.append(f"  WBS树:\n{self.project.wbs_tree_text[:500]}")
                if "cpm_result" in refs and self.project.cpm_result:
                    lines.append(f"  CPM:\n{self.project.cpm_result[:300]}")
                if "estimation_result" in refs and self.project.estimation_result:
                    lines.append(f"  估算:\n{self.project.estimation_result[:300]}")

            # table类型需特殊处理
            if sec.get("type") == "table":
                cols = sec.get("columns", [])
                rows = sec.get("rows", 3)
                lines.append(f"  [表格] 列: {cols}, 建议行数: {rows}")
            elif sec.get("type") == "fields":
                fields = sec.get("fields", [])
                lines.append(f"  [字段表] 字段: {[f.get('label') for f in fields]}")
            elif sec.get("type") == "wbs_attachment":
                lines.append("  [WBS附件] 输出WBS文本树")

        return "\n".join(lines)

    def full_context(self) -> str:
        """生成全部已完成内容的上下文（文档组装用）"""
        lines = [f"# {self.template.get('name', '')}"]
        lines.append(f"**项目**: {self.project.project_name}")
        lines.append(f"**生成日期**: {date.today().isoformat()}")
        lines.append("")

        for c in self.completed:
            lines.append(f"## {c['title']}")
            lines.append("")
            lines.append(c["content"])
            lines.append("")

        # 添加未完成的节为占位
        for i in range(self.current_index, self.total):
            sec = self.sections[i]
            lines.append(f"## {sec.get('title', '')}")
            lines.append("")
            if sec.get("type") == "wbs_attachment" and self.project.wbs_tree_text:
                lines.append("```text")
                lines.append(self.project.wbs_tree_text)
                lines.append("```")
            else:
                lines.append("_（待填充）_")
            lines.append("")

        # 附录
        appendix = self.template.get("appendix", [])
        if appendix:
            lines.append("## 附录")
            for a in appendix:
                lines.append(f"- {a.get('title', '')}")

        return "\n".join(lines)


# ═══════════════════════════════════════════════════
# 6. 文档组装
# ═══════════════════════════════════════════════════

def assemble_document(state: SectionGenState) -> str:
    """拼接完整文档"""
    return state.full_context()


def assemble_mixed_document(
    template: dict,
    project: ProjectData,
    filled_sections: dict[str, str]
) -> str:
    """
    按章节模式组装混合文档。
    
    filled_sections: {section_key: rendered_content}
    - auto模式: LLM生成的完整内容
    - outline模式: LLM生成的概要内容
    - manual模式: 不在filled_sections中，自动生成空占位
    - wbs_attachment类型: 自动填入WBS树，忽略mode和filled_sections
    
    返回完整Markdown文档。
    """
    customized = customize_template(template, project)
    lines = []

    doc_name = template.get("name", "项目文档")
    project_name = project.project_name or "（项目名称）"
    lines.append(f"# {doc_name}")
    lines.append(f"**项目**: {project_name}")
    lines.append(f"**生成日期**: {date.today().isoformat()}")

    # 模式摘要
    modes = set()
    for sec in customized.get("sections", []):
        m = sec.get("mode", "auto")
        modes.add(m)
    mode_labels = {"auto": "自动生成", "manual": "手动填充", "outline": "概要思路"}
    mode_desc = " + ".join(mode_labels[m] for m in sorted(modes, key=lambda x: ["auto","manual","outline"].index(x)))
    lines.append(f"**模式**: {mode_desc}")
    lines.append("")

    # 项目资料摘要
    if project.wbs_tree_text or project.p50 is not None:
        lines.append("> **已有资料摘要**")
        if project.wbs_tree_text:
            lines.append("> - ✅ WBS工作分解已完成")
        if project.p50 is not None:
            lines.append(f"> - ✅ 历时估算: P50={project.p50}, P90={project.p90}")
        if project.critical_path:
            lines.append(f"> - ✅ CPM关键路径: {' → '.join(project.critical_path)}")
        lines.append("")

    lines.append("---")
    lines.append("")

    for section in customized.get("sections", []):
        sec_key = section.get("key", "")
        sec_title = section.get("title", "未命名章节")
        sec_type = section.get("type", "rich_text")
        sec_mode = section.get("mode", "auto")
        desc = section.get("description", "")
        hint = section.get("hint", "")

        lines.append(f"## {sec_title}")

        # 模式标记行
        mode_tag = {"auto": "[自动生成]", "manual": "[手动填写]", "outline": "[概要思路]"}.get(sec_mode, "")
        lines.append(f"> {desc}　{mode_tag}")
        lines.append("")

        # WBS附件：始终显示WBS树
        if sec_type == "wbs_attachment":
            lines.append("```text")
            lines.append(project.wbs_tree_text or "（WBS分解结构，待填充）")
            lines.append("```")
            lines.append("")
            continue

        # 已有内容（auto / outline 模式）
        if sec_key in filled_sections and filled_sections[sec_key].strip():
            lines.append(filled_sections[sec_key].strip())
            lines.append("")
            continue

        # manual 模式：空占位
        if sec_mode == "manual":
            if sec_type == "fields":
                fields = section.get("fields", [])
                lines.append("| 字段 | 填写内容 |")
                lines.append("|------|---------|")
                for f in fields:
                    label = f.get("label", f.get("key", "?"))
                    ht = f.get("hint", "")
                    lines.append(f"| **{label}** | {ht} |")
                lines.append("")
            elif sec_type == "table":
                cols = section.get("columns", [])
                rows = section.get("rows", 3)
                lines.append("| " + " | ".join(cols) + " |")
                lines.append("|" + "|".join(["---"] * len(cols)) + "|")
                for _ in range(rows if rows > 0 else 3):
                    lines.append("| " + " | ".join([""] * len(cols)) + " |")
                lines.append("")
            else:
                lines.append("")
                lines.append("---")
                lines.append("*（在此处填写内容）*")
                lines.append("")

        # 填充提示
        if hint:
            lines.append("> **填充提示**: " + hint)
            lines.append("")

        lines.append("---")
        lines.append("")

    # 附录
    appendix = template.get("appendix", [])
    if appendix:
        lines.append("## 附录")
        for a in appendix:
            lines.append(f"- {a.get('title', '未命名附件')}")
        lines.append("")

    raw = "\n".join(lines)
    return inject_tool_references(raw, customized)


def save_document(content: str, template: dict, project: ProjectData) -> str:
    """保存文档到文件（数据目录下），返回文件路径"""
    filename = template.get("output_filename", "{project_name}_文档.md")
    filename = filename.replace("{project_name}", project.project_name or "未命名项目")

    # 保存到数据目录下的 docs/，不污染安装目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)
    data_dir = os.path.normpath(os.path.join(
        skill_dir, "..", ".standardization",
        os.path.basename(skill_dir), "data", "docs"
    ))
    os.makedirs(data_dir, exist_ok=True)

    fpath = os.path.join(data_dir, filename)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

    return fpath


# ═══════════════════════════════════════════════════
# 7. 模板管理
# ═══════════════════════════════════════════════════

def get_template_info(template_name: str) -> str:
    """获取模板的详细信息（供LLM参考）"""
    try:
        tpl = load_template(template_name)
    except FileNotFoundError as e:
        return str(e)

    lines = [
        f"# 模板: {tpl.get('name', template_name)}",
        f"{tpl.get('description', '')}",
        "",
        "## 章节结构",
    ]

    for i, sec in enumerate(tpl.get("sections", []), 1):
        title = sec.get("title", "?")
        sec_type = sec.get("type", "rich_text")
        desc = sec.get("description", "")[:60]
        lines.append(f"{i}. [{sec_type}] {title} — {desc}")

    appendix = tpl.get("appendix", [])
    if appendix:
        lines.append("")
        lines.append("## 附录")
        for a in appendix:
            lines.append(f"- {a.get('title', '')}")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════
# 8. 模板定制（增/删/改/排序 + 另存为新模板）
# ═══════════════════════════════════════════════════

def _resolve_section(template: dict, target: str) -> tuple[int, dict] | tuple[None, None]:
    """根据key或title查找章节，返回(index, section)"""
    sections = template.get("sections", [])
    # 先精确匹配 key
    for i, sec in enumerate(sections):
        if sec.get("key") == target:
            return i, sec
    # 再匹配 title（不含"章节"等后缀）
    for i, sec in enumerate(sections):
        sec_title = sec.get("title", "")
        if sec_title == target:
            return i, sec
    # 模糊匹配：target是否包含在title中，或title是否包含在target中
    for i, sec in enumerate(sections):
        sec_title = sec.get("title", "")
        if target in sec_title or sec_title in target:
            return i, sec
    # 匹配 key 前缀
    for i, sec in enumerate(sections):
        if sec.get("key", "").startswith(target):
            return i, sec
    return None, None


def add_section(
    template: dict,
    new_section: dict,
    after_key: str = None,
    before_key: str = None
) -> dict:
    """
    在模板中插入一个新章节。
    new_section: 章节定义（与sections[]中的格式一致）
    after_key/before_key: 按key或title定位插入位置（二选一）
    都不指定时追加到末尾。
    """
    sections = template.get("sections", [])
    section_to_add = dict(new_section)
    # 自动补充必填字段
    section_to_add.setdefault("type", "rich_text")
    section_to_add.setdefault("description", "")
    section_to_add.setdefault("hint", "")
    section_to_add.setdefault("reference_sources", [])

    if before_key:
        idx, _ = _resolve_section(template, before_key)
        if idx is not None:
            sections.insert(idx, section_to_add)
            return template
    if after_key:
        idx, _ = _resolve_section(template, after_key)
        if idx is not None:
            sections.insert(idx + 1, section_to_add)
            return template

    # 默认追加
    sections.append(section_to_add)
    return template


def remove_section(template: dict, target: str) -> dict:
    """删除指定章节（按key或title）"""
    idx, _ = _resolve_section(template, target)
    if idx is not None:
        template["sections"].pop(idx)
    return template


def reorder_sections(template: dict, ordered_keys: list[str]) -> dict:
    """
    按指定keys顺序重排章节。
    ordered_keys: 按key或title排列的目标顺序。
    未匹配到的章节追加到末尾。
    """
    old_sections = list(template.get("sections", []))
    new_sections: list[dict] = []

    matched_indices = set()
    for target in ordered_keys:
        # 在 old_sections（未修改的副本）中查找
        idx, sec = _resolve_section({"sections": old_sections}, target)
        if idx is not None and idx not in matched_indices:
            new_sections.append(dict(old_sections[idx]))
            matched_indices.add(idx)

    # 未匹配到的追加到末尾
    for i, sec in enumerate(old_sections):
        if i not in matched_indices:
            new_sections.append(dict(sec))

    template["sections"] = new_sections
    return template


def rename_section(template: dict, target: str, new_title: str = None, new_key: str = None) -> dict:
    """重命名章节标题或key"""
    idx, sec = _resolve_section(template, target)
    if idx is not None and sec:
        if new_title:
            sec["title"] = new_title
        if new_key:
            sec["key"] = new_key
    return template


def set_section_mode(template: dict, target: str, mode: str) -> dict:
    """
    设置章节生成模式，模式固化在模板中，下次直接生效。
    
    mode: "auto"   → 自动生成完整内容
          "manual" → 输出空模板占位，用户手动填
          "outline" → 生成概要思路（短，适合用户在此基础上扩展）
    """
    if mode not in ("auto", "manual", "outline"):
        raise ValueError(f"无效模式: {mode}，可选: auto/manual/outline")

    idx, sec = _resolve_section(template, target)
    if idx is not None and sec:
        sec["mode"] = mode
    return template


def list_sections_by_mode(template: dict) -> dict[str, list[dict]]:
    """
    按模式分组列出所有章节。
    返回: {"auto": [...], "manual": [...], "outline": [...]}
    """
    groups = {"auto": [], "manual": [], "outline": []}
    for sec in template.get("sections", []):
        mode = sec.get("mode", "auto")
        groups.setdefault(mode, []).append(sec)
    return groups


def customize_sections(template: dict, operations: list[dict]) -> dict:
    """
    批量定制模板章节。

    支持的operation格式：
    {"action": "remove", "target": "预算估算"}
    {"action": "add", "after": "范围与交付物", "section": {...}}
    {"action": "add", "before": "审批意见", "section": {...}}
    {"action": "reorder", "order": ["key1", "key2", ...]}
    {"action": "rename", "target": "旧标题", "new_title": "新标题"}
    {"action": "set_mode", "target": "项目背景", "mode": "auto|manual|outline"}
    """
    for op in operations:
        action = op.get("action", "")
        if action == "remove":
            remove_section(template, op["target"])
        elif action == "add":
            add_section(
                template, op.get("section", {}),
                after_key=op.get("after"),
                before_key=op.get("before"),
            )
        elif action == "reorder":
            reorder_sections(template, op.get("order", []))
        elif action == "rename":
            rename_section(
                template, op.get("target", ""),
                new_title=op.get("new_title"),
                new_key=op.get("new_key"),
            )
        elif action == "set_mode":
            set_section_mode(template, op["target"], op["mode"])
    return template


# ═══════════════════════════════════════════════════
# 9. 模板另存为
# ═══════════════════════════════════════════════════

def save_template(template_data: dict, new_name: str, overwrite: bool = False) -> str:
    """
    将当前模板保存为新模板（JSON文件）。
    new_name: 模板名称，同时也是文件名（不包含.json）
    overwrite: 是否覆盖已存在的模板
    返回: 保存路径

    调用方负责在保存前确保：
    - 每个section有唯一的key
    - 模板名不为空
    """
    if not new_name:
        raise ValueError("模板名称不能为空")

    fpath = os.path.join(TEMPLATES_DIR, f"{new_name}.json")

    if os.path.isfile(fpath) and not overwrite:
        raise FileExistsError(
            f"模板 '{new_name}' 已存在。如需覆盖请设置 overwrite=True"
        )

    # 深拷贝，避免修改原数据
    save_data = json.loads(json.dumps(template_data))
    save_data["name"] = new_name
    save_data["version"] = "1.0"
    # 清理内部字段
    for sec in save_data.get("sections", []):
        sec.pop("_has_references", None)

    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2)

    return fpath


def delete_template(template_name: str) -> bool:
    """删除已保存的自定义模板"""
    fpath = os.path.join(TEMPLATES_DIR, f"{template_name}.json")
    if os.path.isfile(fpath):
        os.remove(fpath)
        return True
    return False


def get_template_structure_summary(template_name: str) -> str:
    """以易读格式输出模板章节结构，供用户预览和定制参考"""
    try:
        tpl = load_template(template_name)
    except FileNotFoundError as e:
        return str(e)

    lines = [
        f"📋 模板: {tpl.get('name', template_name)}",
        f"📝 说明: {tpl.get('description', '')}",
        f"📄 共 {len(tpl.get('sections', []))} 个章节, "
        f"{len(tpl.get('appendix', []))} 个附件",
        "",
        "章节列表:",
    ]

    for i, sec in enumerate(tpl.get("sections", []), 1):
        title = sec.get("title", "?")
        sec_type = sec.get("type", "rich_text")
        sec_mode = sec.get("mode", "auto")
        key = sec.get("key", "")
        mode_icon = {"auto": "🔄自动", "manual": "✏️手动", "outline": "📝概要"}.get(sec_mode, "")
        markers = []
        if mode_icon:
            markers.append(mode_icon)
        if sec.get("wbs_ref"):
            markers.append("WBS引用")
        refs = sec.get("reference_sources", [])
        if refs:
            markers.append(f"参考: {', '.join(refs[:3])}")
        marker_str = f" ({'; '.join(markers)})" if markers else ""
        lines.append(f"  {i}. [{sec_type}] {title} [key={key}]{marker_str}")

    appendix = tpl.get("appendix", [])
    if appendix:
        lines.append("")
        lines.append("附录:")
        for a in appendix:
            lines.append(f"  - {a.get('title', '')}")

    lines.append("")
    lines.append("💡 定制操作示例:")
    lines.append('  - 去掉某节: {"action": "remove", "target": "预算估算"}')
    lines.append('  - 新增一节: {"action": "add", "after": "范围与交付物", "section": {"key": "xxx", "title": "...", "type": "rich_text", "description": "..."}}')
    lines.append('  - 重排顺序: {"action": "reorder", "order": ["key1", "key2", ...]}')
    lines.append('  - 重命名:   {"action": "rename", "target": "旧标题", "new_title": "新标题"}')
    lines.append('  - 设章节模式: {"action": "set_mode", "target": "项目背景", "mode": "auto|manual|outline"}')
    lines.append('  - 另存为新模板: save_template(template, "我的模板名")')

    return "\n".join(lines)


def get_template_mode_summary(template_name: str) -> str:
    """输出模板的章节模式分配摘要（缩短版，聚焦模式）"""
    try:
        tpl = load_template(template_name)
    except FileNotFoundError as e:
        return str(e)

    groups = list_sections_by_mode(tpl)
    lines = [
        f"📋 模板: {tpl.get('name', template_name)}",
        f"共 {len(tpl.get('sections', []))} 章节",
        "",
    ]

    for mode, label in [("auto", "🔄 自动生成"), ("manual", "✏️ 手动填写"), ("outline", "📝 概要思路")]:
        secs = groups.get(mode, [])
        if secs:
            lines.append(f"{label} ({len(secs)}节):")
            for s in secs:
                lines.append(f"  - {s.get('title', '?')} [key={s.get('key', '')}]")
            lines.append("")

    lines.append("💡 可用 set_section_mode(tpl, key, mode) 调整模式")
    return "\n".join(lines)
