"""
activity-duration-estimation 全流程编排层

Python 驱动三子技能的完整执行流程。LLM 只需调用 run_full() 主入口，
所有阶段顺序、验证、数据流转由代码硬编码保障，不依赖 LLM 自觉执行。

用法（LLM调用）：
    from scripts.runner import run_full, run_pipeline, PipelineState

    # 一键全流程（推荐）
    state = run_full("帮我规划并估算一个电商后台管理系统")

    # output: state.wbs_text_tree / state.estimate_summary / state.doc_content
    # blocked: state.errors / state.status()

    # 传统入口（保持兼容）
    state = run_pipeline("电商后台", mode="full")

    # 分步交互
    state = PipelineState("电商后台")
    state.run_wbs(template="deliverable", custom_data={...})
    state.prepare_estimation()
    state.run_estimate()
    state.generate_docs("立项申请书", mode="manual")
    state._generate_html_report()

读取当前全局设置：
    state.settings  → dict  # 5项设置值
    state.settings_manager  → settings_manager 模块引用
"""

import os
import sys
import json
import traceback
import re
from datetime import datetime
from typing import Optional

# R-12 审计锚点：数据目录字面量声明
DEFAULT_DATA_DIR_RAW = "skills/.standardization/activity-duration-estimation/data/"

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPTS_DIR)

# 确保 scripts/ 和 skill 根目录都在 sys.path 中
sys.path.insert(0, SCRIPTS_DIR)
sys.path.insert(0, SKILL_DIR)
from wbs_engine import (
    WBSNode, WBSResult, build_node_tree, assign_wbs_codes,
    calc_max_depth, validate_wbs, meets_termination_conditions,
    format_text_tree, format_markdown_tree, format_json, format_svg_tree,
    wbs_to_phases, wbs_to_dependencies,
    WBSOutput, WBSFlowState, get_template_info as wbs_get_templates,
    WBS_TEMPLATES
)
from analysis_engine import (
    calc_cpm, auto_plan_dependencies, parse_dependency_string,
    monte_carlo_multi, calc_overlap,
    generate_gantt_svg, generate_mc_svg,
    validate_cpm_input, validate_cpm_result,
    validate_mc_input, validate_mc_result,
    validate_overlap_tasks, validate_all,
    CPMResult, ValidationResult
)
from project_docs_engine import (
    ProjectData, load_template, list_templates,
    output_manual, customize_sections, add_section, remove_section,
    reorder_sections, rename_section, set_section_mode,
    list_sections_by_mode, customize_template,
    assemble_mixed_document, save_template, delete_template,
    get_template_structure_summary, get_template_mode_summary,
    SectionGenState, TEMPLATES_DIR
)
from risk_dimensions import select_dimensions, build_dimension_prompt, build_minimal_fallback
from settings_manager import load as load_settings


# ═══════════════════════════════════════════════════
# LLM交互点 — 需要LLM推理时抛出此异常
# ═══════════════════════════════════════════════════

class LLMInteractionRequired(Exception):
    """
    需要LLM进行推理/决策时抛出。
    LLM捕获此异常后，应按 prompt 要求提供数据，然后重试。
    """
    def __init__(self, phase: str, prompt: str, schema: dict = None, context: str = None):
        self.phase = phase
        self.prompt = prompt
        self.schema = schema or {}
        self.context = context or ""
        super().__init__(f"[LLM交互] 阶段={phase}: {prompt}")


# ═══════════════════════════════════════════════════
# 阶段枚举
# ═══════════════════════════════════════════════════

PHASE_WBS = "wbs"
PHASE_ESTIMATE = "estimate"
PHASE_DOCS = "docs"
PHASE_FULL = "full"

# 全流程阶段列表（强制顺序）
FULL_PHASE_SEQUENCE = [
    ("wbs", "WBS分解"),
    ("estimation_prep", "估算参数准备"),
    ("dependencies", "紧前关系规划"),
    ("estimation", "估算计算"),
    ("report", "报告生成"),
]


# ═══════════════════════════════════════════════════
# PipelineState — 全流程状态管理（增强版）
# ═══════════════════════════════════════════════════

class PipelineState:
    """
    全流程状态对象。所有阶段的数据、中间结果、错误信息都存储在此。
    LLM 读取 state 的各字段来获取当前进度和结果。
    """

    def __init__(self, description: str = ""):
        # 输入
        self.description: str = description
        self.project_name: str = ""

        # WBS阶段产出
        self.wbs_result: Optional[WBSResult] = None
        self.wbs_text_tree: str = ""
        self.wbs_json_str: str = ""
        self.wbs_svg: str = ""
        self.wbs_valid: bool = False
        self.wbs_issues: list[str] = []

        # 估算阶段产出
        self.phases: list[dict] = []           # [{name, o, m, p, deliverable}]
        self.dependencies: dict = {}            # {idx: [(pred_idx, type)]}
        self.cpm_result: Optional[CPMResult] = None
        self.mc_results: dict = {}
        self.overlap_results: dict = {}
        self.risk_analysis: str = ""  # LLM可设自定义风险分析（防模板套话）
        self.estimate_summary: str = ""
        self.html_report_path: str = ""

        # 文档阶段产出
        self.doc_content: str = ""
        self.doc_path: str = ""

        # 运行时
        self.current_phase: str = ""
        self.errors: list[str] = []
        self.last_error: str = ""
        self.completed_phases: list[str] = []

        # 审计
        self.audit_report: str = ""              # 文本审计报告
        self.audit_results: list[dict] = []       # 结构化审计条目 [{check, passed, issues}]

        # 全局设置（读取 skills/.standardization/.../data/settings.json）
        self.settings: dict = load_settings()
        self.settings_manager = __import__("settings_manager", fromlist=[""])

    # ── 查询 ──

    @property
    def has_wbs(self) -> bool:
        return self.wbs_result is not None

    @property
    def has_estimate(self) -> bool:
        return self.cpm_result is not None

    @property
    def has_doc(self) -> bool:
        return bool(self.doc_content)

    def status(self) -> str:
        """输出当前状态摘要（供LLM读取）"""
        lines = [f"项目: {self.project_name or '未设置'}"]
        lines.append(f"描述: {self.description[:80]}...")
        lines.append(f"已完成阶段: {', '.join(self.completed_phases) or '无'}")
        if self.has_wbs:
            lines.append(f"  WBS: 工作包{len(self.wbs_result.work_packages)}个, 验证{'通过' if self.wbs_valid else '有'+str(len(self.wbs_issues))+'个问题'}")
        if self.has_estimate:
            lines.append(f"  估算: 总工期{self.cpm_result.project_duration:.1f}, 关键路径{len(self.cpm_result.critical_ids)}任务")
        if self.has_doc:
            lines.append(f"  文档: 已生成 ({len(self.doc_content)}字)")
        if self.errors:
            lines.append(f"  错误: {len(self.errors)}个")
        return "\n".join(lines)

    def full_status(self) -> dict:
        """结构化状态，供LLM判断下一步"""
        return {
            "project_name": self.project_name,
            "completed_phases": self.completed_phases.copy(),
            "pending_phases": [p[1] for p in FULL_PHASE_SEQUENCE if p[0] not in self.completed_phases],
            "wbs_valid": self.wbs_valid,
            "wbs_issues": self.wbs_issues.copy(),
            "num_phases": len(self.phases),
            "has_cpm": self.cpm_result is not None,
            "has_report": bool(self.html_report_path),
            "errors": self.errors.copy(),
            "blocked": len(self.errors) > 0,
        }

    # ── 重置 ──

    def reset(self, phase: str = None):
        """重置指定阶段或全部"""
        if phase is None or phase == PHASE_WBS:
            self.wbs_result = None
            self.wbs_text_tree = ""
            self.wbs_json_str = ""
            self.wbs_svg = ""
            self.wbs_valid = False
            self.wbs_issues = []
        if phase is None or phase == PHASE_ESTIMATE:
            self.phases = []
            self.dependencies = {}
            self.cpm_result = None
            self.mc_results = {}
            self.overlap_results = {}
            self.estimate_summary = ""
            self.html_report_path = ""
        if phase is None or phase == PHASE_DOCS:
            self.doc_content = ""
            self.doc_path = ""
        if phase and phase in self.completed_phases:
            self.completed_phases.remove(phase)


    # ═══════════════════════════════════════════════
    # 强制全流程编排
    # ═══════════════════════════════════════════════

    def run_full(self, description: str = None,
                 project_name: str = None,
                 doc_template: str = None,
                 doc_mode: str = None,
                 mc_iterations: int = 2000) -> dict:
        """
        强制全流程：WBS分解 → 估算参数准备 → 紧前关系 → 估算计算 → 
        HTML报告 → 项目文档。
        
        WBS是新项目必做的第一步，项目文档是收尾的最终产出。
        全流程由代码硬编码顺序执行，不可跳过。

        这是推荐的主入口。所有阶段由代码硬编码顺序执行，不可跳过。
        LLM只需调用此函数，无需关心内部流程。

        参数:
            description: 项目描述（为空则使用self.description）
            project_name: 项目名（自动提取或手动指定）

        返回:
            {"status": "ok" | "blocked" | "error",
             "message": "...",
             "state": self}  # 读取state.get()获取详情
        """
        if description:
            self.description = description
        if project_name:
            self.project_name = project_name
        elif not self.project_name:
            self.project_name = _extract_project_name(self.description)

        # 若未显式传参，从全局设置读取文档参数
        if doc_template is None:
            doc_template = self.settings.get("doc_template") or None
        if doc_mode is None:
            doc_mode = self._resolve_doc_mode()

        self.current_phase = PHASE_FULL

        # ═══════════════════════════════════════════
        # Phase -1: WBS分解 — 全流程模式下必做
        # ═══════════════════════════════════════════
        # 全流程模式下WBS是必做的项目规划步骤，不可跳过。
        # 如果已有WBS结果（来自上一次调用），直接进入估算准备。
        # 如果描述中已有OMP信息，作为上下文传递给LLM参考。
        try:
            if self.wbs_result:
                # 已有WBS（来自LLM提供数据后重试），跳过此阶段
                pass
            else:
                # 尝试从描述中提取已有阶段参数作为上下文
                self._extract_phases_from_description()
                context = self.description
                if self.phases:
                    context += (f"\n（已从描述中识别出阶段信息: "
                                f"{[p['name'] for p in self.phases]}，"
                                f"请体现在WBS分解中）")

                raise LLMInteractionRequired(
                    phase="wbs",
                    prompt=(f"项目「{self.project_name}」全流程规划："
                            f"请提供WBS结构化分解数据。\n"
                            f"项目描述: {context[:400]}"),
                    schema={
                        "name": "项目名称",
                        "children": "[{name, children?, o?, m?, p?, deliverable?}]"
                    },
                )

            # 有WBS但还没准备估算参数 → 自动转换
            if self.wbs_result and not self.phases:
                self.prepare_estimation()
        except LLMInteractionRequired:
            raise  # 让顶层捕获，LLM提供数据后重试
        except Exception as e:
            self._handle_error("wbs_decision", e)
            return {"status": "error", "message": str(e), "state": self}

        if self.wbs_result and not self.phases:
            self.prepare_estimation()

        # ═══════════════════════════════════════════
        # WBS进入估算门控校验
        # ═══════════════════════════════════════════
        gate = self._wbs_passes_estimation_gate()
        if not gate["passed"]:
            return {"status": "blocked",
                    "message": f"WBS不满足进入估算条件: {'; '.join(gate['issues'])}",
                    "issues": gate["issues"],
                    "state": self,
                    "hint": "WBS门控校验未通过：请检查各阶段是否有OMP值和交付物描述，"
                            "补充缺失信息后重新调用 run_full()"}

        # ═══════════════════════════════════════════
        # Phase 2: 紧前关系规划 → 若 LLM 已设置则跳过
        # ═══════════════════════════════════════════
        if not self.dependencies:
            self._prompt_llm_for_dependencies()

        # ═══════════════════════════════════════════
        # Phase 3: 估算计算（全Python自动）
        # ═══════════════════════════════════════════
        try:
            self.run_estimate(mc_iterations=mc_iterations)
        except Exception as e:
            self._handle_error("estimation", e)
            return {"status": "error", "message": str(e), "state": self}

        # ═══════════════════════════════════════════
        # Phase 4: HTML报告生成
        # ═══════════════════════════════════════════
        self._generate_html_report()

        # Phase 5: 项目文档生成
        try:
            self.generate_docs(template_name=doc_template, mode=doc_mode)
        except Exception as e:
            self._handle_error("docs", e)

        # Phase 6: 三阶审计+自动修复
        self._audit_and_fix(mc_iterations=mc_iterations)

        # 文档生成失败不阻断
        has_doc_error = any(e.startswith("[docs]") for e in self.errors)
        if has_doc_error:
            return {"status": "ok",
                    "message": f"全流程完成（文档生成异常）: {len(self.phases)}阶段, "
                               f"总工期{self.cpm_result.project_duration:.1f}天",
                    "state": self}

        return {"status": "ok",
                "message": f"全流程完成: {len(self.phases)}阶段, "
                           f"总工期{self.cpm_result.project_duration:.1f}天, "
                           f"文档已生成: {self.doc_path or self.project_name}",
                "state": self}


    # ═══════════════════════════════════════════════
    # 分支逻辑 & LLM交互点
    # ═══════════════════════════════════════════════

    def _needs_wbs(self) -> bool:
        """
        判断是否需要WBS分解（仅用于单模式入口，如 run_pipeline(mode="estimate")）。
        run_full() 全流程模式下WBS必做，不经过此判断。
        
        规则（代码硬编码，不依赖LLM自觉）：
        - 描述含明确OMP模式（如"3天、5天、10天"）→ 不需要WBS
        - 描述含"帮我规划/分解/做个WBS"关键词 → 需要WBS
        - 描述只有领域名+模糊需求 → 需要WBS
        """
        desc = self.description.lower()

        # 关键词匹配：明确要求WBS
        wbs_keywords = ["帮我规划", "工作分解", "做个计划", "wbs"]
        for kw in wbs_keywords:
            if kw in desc:
                return True

        # OMP模式检测：描述中含 数字+天 模式且看起来像OMP
        omp_patterns = re.findall(r'(\d+)\s*天', desc)
        if len(omp_patterns) >= 3:
            # 描述里出现3个以上"X天" → 已经有OMP了，跳过WBS
            return False

        # 模糊需求检测：只有项目名/领域名，无具体参数
        has_task_params = any(kw in desc for kw in ["乐观", "悲观", "最可能", "o=", "m=", "p="])
        if has_task_params:
            return False

        # 简短描述（≤20字）→ 需要WBS来展开
        if len(desc.strip().split()) <= 5:
            return True

        # 默认：有OMP数据就跳过，否则做WBS
        return True

    def _extract_phases_from_description(self):
        """
        从描述中提取已有阶段参数。
        支持格式：
        - "前端3-5-8天，后端2-4-6天" → OMP模式
        - "前端5天，后端8天" → 只有M值
        """
        desc = self.description
        phases = []

        # 尝试匹配阶段模式：名称+OMP（如"前端 3/5/8"或"前端3-5-8"）
        segment_pattern = re.findall(
            r'([\u4e00-\u9fff\w]+)\s*(?:[:：])?\s*'
            r'(?:乐观)?(\d+)(?:[~/天,，\s]*)?'
            r'(?:最可能)?(\d+)?(?:[~/天,，\s]*)?'
            r'(?:悲观)?(\d+)?',
            desc
        )

        for match in segment_pattern:
            name = match[0].strip()
            if len(name) < 2:
                continue
            try:
                o = float(match[1]) if match[1] else None
                m = float(match[2]) if match[2] else o
                p = float(match[3]) if match[3] else (m or o)
            except (ValueError, IndexError):
                o = m = p = None

            if o is not None:
                phases.append({
                    "name": name, "o": o, "m": m or o, "p": p or (m or o)
                })

        if phases:
            self.phases = phases

    def _wbs_passes_estimation_gate(self) -> dict:
        """
        WBS进入估算的门控校验。
        不满足条件则阻塞流程，不进入估算。
        
        返回: {"passed": bool, "issues": [str]}
        """
        issues = []

        if self.phases:
            # 已有phases（非WBS路径）
            for i, p in enumerate(self.phases):
                name = p.get("name", f"阶段{i+1}")
                o, m_val, p_val = p.get("o"), p.get("m"), p.get("p")
                if not any([o, m_val, p_val]):
                    issues.append(f"「{name}」缺少OMP值")
                elif o and p_val and o > p_val:
                    issues.append(f"「{name}」O({o}) > P({p_val}), 违反O≤P")
                elif o and m_val and o > m_val:
                    issues.append(f"「{name}」O({o}) > M({m_val}), 违反O≤M")
                elif m_val and p_val and m_val > p_val:
                    issues.append(f"「{name}」M({m_val}) > P({p_val}), 违反M≤P")
            return {"passed": len(issues) == 0, "issues": issues}

        if not self.wbs_result:
            return {"passed": False, "issues": ["WBS结果为空"]}

        wps = self.wbs_result.work_packages

        if len(wps) == 0:
            issues.append("WBS无工作包（叶节点），请补充细项")

        if self.wbs_result.max_depth < 1:
            issues.append("WBS层级过浅（至少需要2层：根→工作包）")

        for wp in wps:
            if not any([wp.o, wp.m, wp.p]):
                issues.append(f"工作包「{wp.name}」缺少OMP值"
                              "（LLM请根据上下文估算）")
            elif wp.o and wp.p and wp.o > wp.p:
                issues.append(f"工作包「{wp.name}」O({wp.o}) > P({wp.p})")

        # 验证结果整合
        if not self.wbs_valid:
            for iss in (self.wbs_result.validation_issues or []):
                issues.append(f"WBS验证: {iss}")

        return {"passed": len(issues) == 0, "issues": issues}

    def _prompt_llm_for_wbs(self, description: str = None) -> dict:
        """
        LLM交互点：根据项目描述生成WBS结构化数据。
        抛出LLMInteractionRequired，由顶层捕获后等待LLM填充。
        
        返回格式:
            {"name": "项目名", "children": [
                {"name": "阶段1", "children": [
                    {"name": "任务1.1", "o": 3, "m": 5, "p": 8},
                    ...
                ]}
            ]}
        """
        desc = description or self.description
        raise LLMInteractionRequired(
            phase="wbs",
            prompt=(f"请为项目「{self.project_name or '未命名'}」提供WBS结构化数据。"
                    f"项目描述: {desc[:200]}"),
            schema={
                "name": "str, 项目名称",
                "children": "list, 子节点，每项含 name(必填)/children(可选)/o(可选)/m(可选)/p(可选)/deliverable(可选)"
            }
        )

    def _prompt_llm_for_omp(self, phase_name: str, context: str = "") -> dict:
        """
        LLM交互点：根据阶段名称估算OMP。
        抛出LLMInteractionRequired，由顶层捕获后等待LLM填充。
        
        返回: {"o": int, "m": int, "p": int}
        """
        raise LLMInteractionRequired(
            phase="omp",
            prompt=(f"请为阶段「{phase_name}」估算OMP（乐观/最可能/悲观 天数）。"
                    f"上下文: {context or self.description[:100]}"),
            schema={"o": "float(乐观天数)", "m": "float(最可能天数)", "p": "float(悲观天数)"}
        )

    def _prompt_llm_for_dependencies(self):
        """
        LLM交互点（占位）。

        LLM 在调用 run_estimate / prepare_estimation 之前，
        应直接设置 self.dependencies = {...}。
        此处仅做 fallback：若 LLM 未设置，用 wbs_to_dependencies。
        """
        if not self.phases:
            return
        if self.dependencies:
            return  # LLM 已提供
        if self.wbs_result:
            self.dependencies = wbs_to_dependencies(self.wbs_result)

    def _generate_html_report(self):
        """生成HTML评估报告（全Python自动）"""
        if not self.cpm_result:
            return

        # 警告：若LLM未提供风险分析
        if not hasattr(self, 'risk_analysis') or not self.risk_analysis:
            print("  [WARN] LLM未设置 state.risk_analysis，风险分析卡片为空。")
            print("         应调用 ctx = state.get_risk_context() 生成项目风险分析。")

        # 调用analysis_engine生成SVG（MC图表用SVG，甘特图改用HTML）
        mc_svg = ""
        try:
            if self.mc_results:
                mc_svg = generate_mc_svg(self.mc_results)
        except Exception as e:
            print(f"  [WARN] MC图表生成失败: {e}")

        # 组装HTML
        html = [self._build_html_header()]
        html.append(self._build_method_card_section())
        html.append(self._build_gantt_section(""))  # HTML-based Gantt
        html.append(self._build_overlap_section())   # 重叠分析
        html.append(self._build_param_table())       # 分组参数表
        html.append(self._build_wbs_tree_section())  # WBS树
        html.append(self._build_cpm_section())
        html.append(self._build_mc_section(mc_svg))
        html.append(self._build_analysis_section())
        html.append(self._build_html_footer())

        full_html = "\n".join(html)

        # 保存到文件
        # 保存到数据目录下的 reports/，不污染安装目录
        data_dir = os.path.normpath(os.path.join(
            SKILL_DIR, "..", ".standardization",
            os.path.basename(SKILL_DIR), "data", "reports"
        ))
        os.makedirs(data_dir, exist_ok=True)
        safe_name = self.project_name or "未命名"
        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in safe_name)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(data_dir, f"{safe_name}_{ts}.html")

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(full_html)

        self.html_report_path = report_path
        self.completed_phases.append("report")
        print(f"[OK] HTML报告已生成: {report_path}")

    def _build_html_header(self) -> str:
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="utf-8">
<title>{self.project_name or '项目'} - 活动历时估算报告</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Segoe UI','Microsoft YaHei',sans-serif;background:#f5f7fa;color:#333;max-width:1200px;margin:0 auto;padding:20px}}
h1{{color:#2c3e50;border-bottom:3px solid #3498db;padding-bottom:10px;margin-bottom:16px}}
h2{{color:#2c3e50;margin-bottom:12px}}
h3{{color:#34495e;margin:8px 0}}
.card{{background:#fff;border-radius:8px;padding:16px;margin:16px 0;box-shadow:0 1px 3px rgba(0,0,0,.1)}}
table{{border-collapse:collapse;width:100%;font-size:13px}}
th,td{{border:1px solid #ddd;padding:6px 10px;text-align:left}}
th{{background:#3498db;color:#fff;position:sticky;top:0}}
.tag{{display:inline-block;padding:2px 8px;border-radius:12px;font-size:11px;margin:2px}}
.tag-ok{{background:#27ae60;color:#fff}}
.tag-warn{{background:#f39c12;color:#fff}}
.tag-err{{background:#e74c3c;color:#fff}}
/* 甘特图 */
.gantt-container{{overflow-x:auto;overflow-y:visible;position:relative}}
.gantt{{position:relative;min-width:900px}}
.gantt-header{{display:flex;position:sticky;top:0;background:#f8f9fa;z-index:2;border-bottom:2px solid #333;font-size:12px;font-weight:bold;height:36px;align-items:flex-end}}
.gantt-label{{min-width:180px;padding:0 8px 4px 0;flex-shrink:0}}
.gantt-scale{{flex:1;display:flex;position:relative;height:36px}}
.gantt-tick{{position:absolute;font-size:10px;color:#666;top:16px;transform:translateX(-50%)}}
.gantt-phase{{display:flex;align-items:center;background:#f0f4f8;padding:6px 8px;margin:2px 0;border-radius:4px;font-size:13px;font-weight:bold;color:#2c3e50;border-left:4px solid}}
.gantt-row{{display:flex;align-items:center;padding:2px 0;font-size:12px;min-height:28px;border-bottom:1px solid #f0f0f0}}
.gantt-row:hover{{background:#f8f9ff}}
.gantt-row-label{{min-width:180px;padding:0 8px 0 0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex-shrink:0;font-size:12px}}
.gantt-track{{flex:1;position:relative;height:24px}}
.gantt-bar{{position:absolute;height:20px;border-radius:4px;top:2px;min-width:4px;box-shadow:0 1px 2px rgba(0,0,0,0.15);cursor:default}}
.gantt-bar:hover{{opacity:0.85;transform:scaleY(1.1)}}
.gantt-bar-critical{{border:2px solid #c0392b}}
.gantt-milestone{{position:absolute;width:0;height:0;border-left:7px solid transparent;border-right:7px solid transparent;border-bottom:10px solid #e67e22;top:7px;transform:translateX(-7px);cursor:default}}
.gantt-milestone-label{{position:absolute;font-size:9px;color:#e67e22;white-space:nowrap;top:-14px;transform:translateX(-50%);font-weight:bold}}
.phase-grid{{display:flex;flex:1;position:relative}}
.phase-grid-line{{position:absolute;top:0;bottom:0;border-left:1px dashed #ddd;z-index:0}}
</style></head><body>
<h1>{self.project_name or '项目'} - 活动历时估算报告</h1>
<p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>"""

    def _build_method_card_section(self) -> str:
        lines = ['<div class="card"><h2>概况</h2>']
        lines.append(f"<p><strong>阶段数:</strong> {len(self.phases)}</p>")
        if self.mc_results:
            lines.append(f"<p><strong>蒙特卡洛:</strong> PERT-Beta + 三角分布 + 泊松近似</p>")
        if self.cpm_result:
            lines.append(f"<p><strong>CPM关键路径:</strong> {len(self.cpm_result.critical_ids)}个关键任务</p>")
        lines.append('</div>')
        return "\n".join(lines)

    def _get_phase_groups(self):
        """从 phases 名称中提取 WBS 前缀分组，返回 {phase_num: {name, phases_indices, color}}"""
        import re
        phase_colors = [
            ('#3498db','#d6eaf8'), ('#e74c3c','#fadbd8'), ('#2ecc71','#d5f5e3'),
            ('#9b59b6','#e8daef'), ('#f39c12','#fef9e7'), ('#1abc9c','#d1f2eb'),
            ('#e67e22','#fdebd0'), ('#34495e','#d5dbdb'),
        ]
        groups = {}
        for i, p in enumerate(self.phases):
            name = p.get("name", "")
            m = re.match(r'^(\d+)\.', name.strip())
            if m:
                key = m.group(1)
                if key not in groups:
                    idx = min(len(groups), len(phase_colors)-1)
                    groups[key] = {
                        "title": f"Phase {key}",
                        "indices": [],
                        "color": phase_colors[idx][0],
                        "bg": phase_colors[idx][1],
                    }
                groups[key]["indices"].append(i)
        return groups

    def _build_param_table(self) -> str:
        lines = ['<div class="card"><h2>WBS分解与参数详情</h2>']
        groups = self._get_phase_groups()
        if not groups:
            # fallback flat table
            lines.append('<table><tr><th>#</th><th>阶段</th><th>O</th><th>M</th><th>P</th><th>交付物</th></tr>')
            for i, p in enumerate(self.phases, 1):
                lines.append(f"<tr><td>{i}</td><td>{p.get('name','')}</td>"
                             f"<td>{p.get('o','-')}</td><td>{p.get('m','-')}</td>"
                             f"<td>{p.get('p','-')}</td><td>{p.get('deliverable','-')}</td></tr>")
            lines.append('</table></div>')
            return "\n".join(lines)

        for key in sorted(groups.keys(), key=int):
            g = groups[key]
            indices = g["indices"]
            lines.append(f'<div style="margin:8px 0;border-left:4px solid {g["color"]};padding:0 0 0 8px">')
            lines.append(f'<h3 style="color:{g["color"]};margin:4px 0 6px 0">📋 Phase {key}</h3>')
            lines.append('<table><tr><th>#</th><th>任务</th><th>O</th><th>M</th><th>P</th><th>交付物</th></tr>')
            for idx in indices:
                p = self.phases[idx]
                tid = idx + 1
                is_cp = tid in (self.cpm_result.critical_ids or set()) if self.cpm_result else False
                marker = ' 🔴' if is_cp else ''
                lines.append(f'<tr><td>{tid}</td><td>{p.get("name","")}{marker}</td>'
                             f'<td>{p.get("o","-")}</td><td>{p.get("m","-")}</td>'
                             f'<td>{p.get("p","-")}</td><td>{p.get("deliverable","-")}</td></tr>')
            lines.append('</table>')
            lines.append('</div>')
        lines.append(
            '<p style="color:#999;font-size:12px;margin-top:4px">🔴 = 关键路径任务</p>'
            '</div>')
        return "\n".join(lines)

    def _build_gantt_section(self, svg: str) -> str:
        """构建HTML甘特图（div-based，支持大量任务）"""
        if not self.cpm_result or not self.phases:
            return ""

        # 准备甘特图数据
        import re
        phase_colors = {
            '1': {'bar':'#3498db','bg':'#d6eaf8'},
            '2': {'bar':'#e74c3c','bg':'#fadbd8'},
            '3': {'bar':'#2ecc71','bg':'#d5f5e3'},
            '4': {'bar':'#9b59b6','bg':'#e8daef'},
            '5': {'bar':'#f39c12','bg':'#fef9e7'},
            '6': {'bar':'#1abc9c','bg':'#d1f2eb'},
            '7': {'bar':'#e67e22','bg':'#fdebd0'},
            '8': {'bar':'#34495e','bg':'#d5dbdb'},
        }
        default_colors = {'bar':'#7f8c8d','bg':'#f0f0f0'}

        task_data = []
        min_time = float('inf')
        max_time = 0
        for tid in sorted(self.cpm_result.task_cpm.keys()):
            if tid <= len(self.phases):
                cd = self.cpm_result.task_cpm[tid]
                name = self.phases[tid-1]["name"]
                is_cp = tid in (self.cpm_result.critical_ids or set())
                m = re.match(r'^(\d+)\.', name.strip())
                phase_key = m.group(1) if m else '0'
                pc = phase_colors.get(phase_key, default_colors)
                task_data.append({
                    'tid': tid, 'name': name, 'phase': phase_key,
                    'start': cd['es'], 'end': cd['ef'],
                    'duration': cd['ef'] - cd['es'],
                    'is_critical': is_cp,
                    'bar_color': pc['bar'],
                })
                min_time = min(min_time, cd['es'])
                max_time = max(max_time, cd['ef'])

        time_range = max(max_time - min_time, 1)
        gantt_width = 700  # px for the track area

        def time_to_x(t):
            return (t - min_time) / time_range * gantt_width

        lines = ['<div class="card"><h2>甘特图</h2>'
                 f'<p style="font-size:12px;color:#666;margin-bottom:8px">'
                 f'总工期: {max_time:.0f}天 | 任务: {len(task_data)}个 | 色块=阶段分组 | 红框=关键路径</p>'
                 '<div class="gantt-container"><div class="gantt">']

        # Scale header
        lines.append('<div class="gantt-header">'
                     '<div class="gantt-label">任务名称</div>'
                     '<div class="gantt-scale">')
        ticks = 12
        for i in range(ticks + 1):
            t = min_time + time_range * i / ticks
            x = time_to_x(t)
            lines.append(f'<div class="gantt-tick" style="left:{x:.0f}px">{t:.0f}</div>')
            if i > 0 and i < ticks:
                lines.append(f'<div class="gantt-track" style="position:absolute;left:{x:.0f}px;top:0;bottom:0;border-left:1px dashed #ddd;height:36px;z-index:0"></div>')
        lines.append('</div></div>')

        # Phase headers + task rows
        prev_phase = None
        for t in task_data:
            # Phase group header
            if t['phase'] != prev_phase:
                pc = phase_colors.get(t['phase'], default_colors)
                lines.append(
                    f'<div class="gantt-phase" style="border-left-color:{pc["bar"]};background:{pc["bg"]}">'
                    f'Phase {t["phase"]}</div>')
                prev_phase = t['phase']

            # Task row
            sx = time_to_x(t['start'])
            bw = max(4, time_to_x(t['end']) - sx)
            critical_cls = ' gantt-bar-critical' if t['is_critical'] else ''
            dur_label = f'{t["duration"]:.0f}d' if bw > 50 else ''

            lines.append(f'<div class="gantt-row">'
                         f'<div class="gantt-row-label" title="{t["name"]}">{t["name"]}</div>'
                         f'<div class="gantt-track">'
                         f'<div class="gantt-bar{critical_cls}" '
                         f'style="left:{sx:.1f}px;width:{bw:.1f}px;background:{t["bar_color"]}" '
                         f'title="{t["name"]}: {t["start"]:.0f}→{t["end"]:.0f}天 ({t["duration"]:.0f}天)">'
                         f'{dur_label}</div></div></div>')

        # Phase transition milestones
        phase_boundaries = {}
        for t in task_data:
            if t['phase'] not in phase_boundaries:
                phase_boundaries[t['phase']] = {'first_start': t['start'], 'last_end': t['end']}
            else:
                phase_boundaries[t['phase']]['last_end'] = max(phase_boundaries[t['phase']]['last_end'], t['end'])

        for pk in sorted(phase_boundaries.keys(), key=int):
            pb = phase_boundaries[pk]
            mx = time_to_x(pb['last_end'])
            lines.append(f'<div class="gantt-milestone" style="left:{mx:.0f}px" '
                         f'title="Phase {pk} 完成({pb["last_end"]:.0f}天)"></div>')
            lines.append(f'<div class="gantt-milestone-label" style="left:{mx:.0f}px">♦P{pk}</div>')


        lines.append('</div></div></div>')
        return '\n'.join(lines)

    def _build_cpm_section(self) -> str:
        if not self.cpm_result:
            return ""
        lines = ['<div class="card"><h2>CPM关键路径</h2><table><tr><th>#</th><th>名称</th><th>ES</th><th>EF</th><th>LS</th><th>LF</th><th>TF</th><th>关键?</th></tr>']
        for tid, cd in self.cpm_result.task_cpm.items():
            name = self.phases[tid-1]["name"] if tid <= len(self.phases) else f"任务{tid}"
            is_critical = "✅" if tid in self.cpm_result.critical_ids else ""
            lines.append(f"<tr><td>{tid}</td><td>{name}</td><td>{cd['es']:.1f}</td>"
                         f"<td>{cd['ef']:.1f}</td><td>{cd['ls']:.1f}</td>"
                         f"<td>{cd['lf']:.1f}</td><td>{cd['tf']:.1f}</td><td>{is_critical}</td></tr>")
        lines.append(f'<tr><td colspan="8"><strong>总工期: {self.cpm_result.project_duration:.1f}</strong></td></tr>')
        lines.append('</table></div>')
        return "\n".join(lines)

    def _build_mc_section(self, svg: str) -> str:
        mc = self.mc_results.get("pert", {}) if self.mc_results else {}
        stats = mc.get("stats", {})
        quants = mc.get("quantiles", {})
        if not stats and not quants and not svg:
            return ""
        lines = ['<div class="card"><h2>蒙特卡洛模拟</h2>']
        if stats:
            lines.append(f"<p>均值={stats.get('mean',0):.1f}, σ={stats.get('stddev',0):.1f}</p>")
        if quants:
            lines.append(f"<p>P50={quants.get('p50',0):.1f}, P90={quants.get('p90',0):.1f}</p>")
        if svg:
            lines.append(svg)
        lines.append('</div>')
        return "\n".join(lines)

    def _build_overlap_section(self) -> str:
        """任务重叠分析"""
        if not self.overlap_results:
            return ""
        ov = self.overlap_results
        mc = ov.get("max_count", {})
        md = ov.get("max_duration", {})
        if not mc.get("count", 0) and not md.get("count", 0):
            return ""
        lines = ['<div class="card"><h2>任务重叠分析</h2>']

        if mc.get("count", 0) > 0:
            lines.append(f'<p><strong>最大并发任务数:</strong> {mc["count"]} 个任务同时执行</p>')
            lines.append(f'<p><strong>时间范围:</strong> {mc.get("start",0):.0f}天 → {mc.get("end",0):.0f}天'
                         f'（持续 {mc.get("duration",0):.0f}天）</p>')
            tasks = mc.get("tasks", [])
            if tasks:
                lines.append('<p><strong>涉及任务:</strong></p><ul>')
                for task_name in tasks[:10]:
                    lines.append(f'<li>{task_name}</li>')
                if len(tasks) > 10:
                    lines.append(f'<li>… 共{len(tasks)}个任务</li>')
                lines.append('</ul>')

        if md.get("duration", 0) > (mc.get("duration", 0) + 1):
            lines.append(f'<p style="margin-top:8px"><strong>最长重叠时段:</strong> '
                         f'{md.get("duration",0):.0f}天（{md.get("start",0):.0f}→{md.get("end",0):.0f}天），'
                         f'{md.get("count",0)}个任务并行</p>')

        lines.append('</div>')
        return "\n".join(lines)

    def _build_wbs_tree_section(self) -> str:
        """WBS文本树（层级结构展示）"""
        if not self.wbs_text_tree:
            return ""
        tree_html = self.wbs_text_tree.replace("\n", "<br>").replace(" ", "&nbsp;")
        return (
            f'<div class="card"><h2>WBS分解结构</h2>'
            f'<pre style="font-family:Consolas,monospace;font-size:12px;line-height:1.5;overflow-x:auto;'
            f'background:#f8f9fa;padding:12px;border-radius:4px">{tree_html}</pre></div>'
        )

    def get_risk_context(self) -> dict:
        """
        返回项目风险评估所需的全部数据（供 LLM 用于生成风险分析）。
        LLM 用法：
            ctx = state.get_risk_context()
            state.risk_analysis = llm_generate_risk(ctx)
        """
        mc_p50, mc_p90, mc_mean = 0, 0, 0
        if hasattr(self, 'mc_results') and self.mc_results:
            pert = self.mc_results.get("pert", {})
            st = pert.get("stats", {})
            q = pert.get("quantiles", {})
            mc_mean = st.get("mean", 0)
            mc_p50 = q.get("p50", 0)
            mc_p90 = q.get("p90", 0)

        cp_ids = []
        cp_names = []
        if hasattr(self, 'cpm_result') and self.cpm_result:
            cp_ids = list(self.cpm_result.critical_ids or [])
            cp_names = [self.phases[t-1]["name"] for t in sorted(cp_ids) if t <= len(self.phases)]

        overlap_info = {}
        if hasattr(self, 'overlap_results') and self.overlap_results:
            mc = self.overlap_results.get("max_count", {})
            overlap_info = {
                "max_concurrent": mc.get("count", 0),
                "time_range": f"{mc.get('start',0):.0f}→{mc.get('end',0):.0f}天",
                "duration": f"{mc.get('duration',0):.0f}天",
                "tasks": mc.get("tasks", []),
            }

        integration_tasks = [p.get("name","") for p in (self.phases or [])
                            if "集成" in p.get("name","") or "对接" in p.get("name","")]

        return {
            "project_name": getattr(self, 'project_name', ""),
            "description": getattr(self, 'description', ""),
            "total_phases": len(self.phases or []),
            "cpm_duration": self.cpm_result.project_duration if hasattr(self, 'cpm_result') and self.cpm_result else 0,
            "critical_path_count": len(cp_ids),
            "critical_path": cp_names,
            "mc_p50": mc_p50,
            "mc_p90": mc_p90,
            "mc_mean": mc_mean,
            "mc_p90_p50_gap": mc_p90 - mc_p50,
            "overlap": overlap_info,
            "integration_tasks": integration_tasks,
        }

    def _build_analysis_section(self) -> str:
        # LLM 提供了自定义风险分析 → 直接使用
        if hasattr(self, 'risk_analysis') and self.risk_analysis:
            return self.risk_analysis

        # fallback: 打印可用数据，提醒 LLM 应调用 get_risk_context() 生成分析
        ctx = self.get_risk_context()
        lines = ['<div class="card"><h2>项目风险分析</h2>',
                 f'<p style="color:#e74c3c;font-weight:bold">⚠️ 风险分析未生成</p>',
                 f'<p>LLM 生成报告中未调用 get_risk_context() 和设置 state.risk_analysis。</p>',
                 f'<p style="font-size:12px;color:#666">可用数据：CPM={ctx["cpm_duration"]:.0f}天, '
                 f'MC P50/P90={ctx["mc_p50"]:.0f}/{ctx["mc_p90"]:.0f}天, '
                 f'关键路径{ctx["critical_path_count"]}个任务, '
                 f'最大并发{ctx["overlap"].get("max_concurrent",0)}个任务</p>',
                 '</div>']

        # 但仍显示维度选择结果（不空手）
        active_dims = select_dimensions(context)
        if active_dims:
            lines.append('<div style="margin:8px 0;padding:8px;border-left:3px solid #e74c3c;background:#fff5f5">')
            lines.append('<p style="font-size:12px;color:#666">以下维度由系统自动匹配，LLM应根据这些维度+项目数据分析：</p>')
            for dim in active_dims:
                lines.append(f'<p><strong>{dim.get("icon","")} {dim["name"]}</strong> — {dim.get("guide","")}</p>')
            lines.append('</div>')

        lines.append('</div>')
        return "\n".join(lines)

    def _build_html_footer(self) -> str:
        return "</body></html>"


    # ═══════════════════════════════════════════════
    # WBS 阶段
    # ═══════════════════════════════════════════════

    def run_wbs(self, template: str = "deliverable",
                custom_data: dict = None) -> WBSResult:
        """(保持兼容原接口) 执行WBS分解"""
        self.current_phase = PHASE_WBS
        self.reset(PHASE_WBS)

        try:
            result = WBSResult()
            result.project_name = self.project_name or "未命名项目"
            result.method_name = WBS_TEMPLATES.get(template, {}).get("name", "交付成果式")

            if custom_data and "children" in custom_data:
                root = WBSNode(name=result.project_name, level=0)
                skeleton = custom_data.get("children", {})
                build_node_tree(skeleton, root)
                result.root = root
            else:
                root = WBSNode(name=result.project_name, level=0)
                result.root = root

            if result.root:
                assign_wbs_codes(result.root)
                result.max_depth = calc_max_depth(result.root)

            result.collect_work_packages()

            validate_wbs(result)
            self.wbs_valid = result.is_valid
            self.wbs_issues = result.validation_issues

            self.wbs_text_tree = format_text_tree(result)
            self.wbs_json_str = format_json(result)
            self.wbs_svg = format_svg_tree(result)

            self.wbs_result = result
            self.completed_phases.append(PHASE_WBS)

        except Exception as e:
            self._handle_error(PHASE_WBS, e)

        return self.wbs_result

    def wbs_add_nodes(self, children_data: dict):
        """(保持兼容原接口) 向已存在的WBS追加节点"""
        if not self.wbs_result or not self.wbs_result.root:
            self.run_wbs()
        build_node_tree(children_data, self.wbs_result.root)
        assign_wbs_codes(self.wbs_result.root)
        self.wbs_result.collect_work_packages()
        validate_wbs(self.wbs_result)
        self.wbs_valid = self.wbs_result.is_valid
        self.wbs_issues = self.wbs_result.validation_issues
        self.wbs_text_tree = format_text_tree(self.wbs_result)
        self.wbs_json_str = format_json(self.wbs_result)


    # ═══════════════════════════════════════════════
    # 估算阶段
    # ═══════════════════════════════════════════════

    def prepare_estimation(self, custom_phases: list[dict] = None,
                           custom_deps: dict = None):
        """(保持兼容原接口) 准备估算参数"""
        self.current_phase = PHASE_ESTIMATE

        if custom_phases:
            self.phases = custom_phases
        elif self.phases:
            pass  # 已通过 _extract_phases_from_description() 或直接赋值设置
        elif self.wbs_result:
            self.phases = wbs_to_phases(self.wbs_result)
        else:
            raise ValueError("prepare_estimation: 请提供custom_phases或先执行run_wbs()")

        if custom_deps:
            self.dependencies = custom_deps
        elif self.dependencies:
            pass  # 已通过直接赋值设置（LLM自行设计）
        elif self.wbs_result:
            # 有 WBS 数据 → 让 LLM 设计合理的依赖关系
            self.dependencies = wbs_to_dependencies(self.wbs_result)
            # 但给 LLM 一个机会来覆盖（由 run_full 中的 _prompt_llm_for_dependencies 触发）
        else:
            self.dependencies = auto_plan_dependencies(len(self.phases), self.phases)

        # 转换 0-based → 1-based
        deps_1based = {}
        for k, v in self.dependencies.items():
            k1 = k + 1 if isinstance(k, int) else k
            deps_1based[k1] = []
            for dep in v:
                if isinstance(dep, (list, tuple)):
                    pred_id = dep[0] + 1 if isinstance(dep[0], int) else dep[0]
                    dep_type = dep[1] if len(dep) >= 2 else "FS"
                    deps_1based[k1].append((pred_id, dep_type))
                else:
                    deps_1based[k1].append(dep + 1 if isinstance(dep, int) else dep)
        self.dependencies = deps_1based

        # ── 校验 LLM 设计的依赖（防幻觉） ──
        self._validate_dependencies()

    def _validate_dependencies(self):
        """校验依赖设计的合理性，防 LLM 幻觉"""
        if not self.dependencies or not self.phases:
            return

        n = len(self.phases)
        issues = []

        # 1. 可达性检查：所有任务（除1号）应为前驱或后继
        #    任务可能是前驱（被其他任务依赖）而不需要自己有dep定义
        all_referenced_as_pred = set()
        for tid, deps in self.dependencies.items():
            for dep, *_ in (deps if isinstance(deps, list) else [deps]):
                pd = dep[0] if isinstance(dep, (list, tuple)) else dep
                all_referenced_as_pred.add(pd)

        has_deps_defined = set(self.dependencies.keys())
        all_connected = has_deps_defined | all_referenced_as_pred

        disconnected = [tid for tid in range(1, n + 1)
                        if tid not in all_connected]
        if disconnected:
            names = [self.phases[tid-1]["name"] for tid in disconnected[:5]]
            issues.append(f"⚠️ {len(disconnected)}个任务既无前驱也无后继（孤立任务）: {', '.join(names)}")

        # 2. 自引用检查
        for tid, deps in self.dependencies.items():
            for dep, *_ in (deps if isinstance(deps, list) else [deps]):
                pd = dep[0] if isinstance(dep, (list, tuple)) else dep
                if pd == tid:
                    issues.append(f"❌ 任务 {tid} 依赖自身，死循环")

        # 3. 关键路径占比分析（估算CPM后才有意义，但可提前检查并行度）
        # 统计：有多少任务同时依赖同一个前驱（扇出 >3 说明有并行分支）
        fan_out = {}
        for tid, deps in self.dependencies.items():
            for dep, *_ in (deps if isinstance(deps, list) else [deps]):
                pd = dep[0] if isinstance(dep, (list, tuple)) else dep
                fan_out.setdefault(pd, []).append(tid)
        high_fan = {k: v for k, v in fan_out.items() if len(v) > 3}
        if high_fan:
            for pred_id, succs in high_fan.items():
                name = self.phases[pred_id-1]["name"] if pred_id <= n else f"任务{pred_id}"
                succ_names = [self.phases[s-1]["name"] for s in succs[:5] if s <= n]
                issues.append(f"ℹ️  {name} 完成后有 {len(succs)} 个并行分支: {', '.join(succ_names)}")

        # 4. 检查是否有任务被过度依赖（多个前置同时依赖同一个，可能是合并点）
        fan_in = {}
        for tid, deps in self.dependencies.items():
            for dep, *_ in (deps if isinstance(deps, list) else [deps]):
                pd = dep[0] if isinstance(dep, (list, tuple)) else dep
                fan_in.setdefault(tid, set()).add(pd)
        merge_points = {k: v for k, v in fan_in.items() if len(v) >= 3}
        for tid, preds in merge_points.items():
            name = self.phases[tid-1]["name"] if tid <= n else f"任务{tid}"
            pred_names = [self.phases[p-1]["name"] for p in preds if p <= n]
            issues.append(f"🔀 {name} 等待 {len(preds)} 个前置汇合: {', '.join(pred_names)}")

        # 5. 懒惰检测：全FS串联无并行 → 极可能是LLM偷懒没设计
        all_fs_chain = True
        seen = set()
        for tid in sorted(self.dependencies.keys()):
            deps = self.dependencies.get(tid, [])
            if not deps:
                continue  # 无前置的任务（如第一组的第一个）不算
            if len(deps) != 1:
                all_fs_chain = False
                break
            d = deps[0]
            pd = d[0] if isinstance(d, (list, tuple)) else d
            dep_type = d[1] if isinstance(d, (list, tuple)) and len(d) >= 2 else "FS"
            if dep_type != "FS":
                all_fs_chain = False
                break
            if pd != tid - 1:
                all_fs_chain = False
                break
            seen.add(pd)
        
        # 超过 5 个任务：有一个组无前置，其余全 FS i→i-1 → 懒惰
        has_root = any(not self.dependencies.get(tid, []) for tid in range(1, n+1))
        if all_fs_chain and has_root and n > 5:
            issues.append(
                f"❌ 全 FS 串行（{n}个任务全部1→2→3→...N），"
                f"无任何并行分支。这是 fallback 默认行为，不是 LLM 设计的依赖。"
                f"请根据项目经验重新设计依赖关系（设定并行分支、SS/FF 关系等）。"
            )

        if issues:
            print("\n─── 依赖合理性检查 ───")
            for iss in issues:
                print(f"  {iss}")
            print("")
        else:
            print("  ✅ 依赖检查通过（无异常）")

    def run_estimate(self, mc_iterations: int = 2000,
                     _run_audit: bool = True) -> dict:
        """(保持兼容原接口) 执行估算计算"""
        self.current_phase = PHASE_ESTIMATE

        if not self.phases:
            raise ValueError("run_estimate: 请先调用prepare_estimation()")

        self.cpm_result = None
        self.mc_results = {}
        self.overlap_results = {}
        self.estimate_summary = ""

        try:
            durations = {i+1: (p.get("m", 0) or 0) for i, p in enumerate(self.phases)}
            mc_phases = [(p["name"], p.get("o", 0), p.get("m", 0), p.get("p", 0))
                         for p in self.phases]
            deps_formatted = self.dependencies

            vr_input = validate_cpm_input(durations, deps_formatted)
            vr_mc = validate_mc_input(mc_phases)

            self.cpm_result = calc_cpm(durations, deps_formatted)

            if len(self.phases) >= 1:
                self.mc_results = monte_carlo_multi(
                    mc_phases, mc_iterations,
                    ['pert', 'triangular', 'poisson'],
                    dependencies=deps_formatted,
                    task_count=len(self.phases),
                )

            overlap_tasks = []
            if self.cpm_result:
                for tid, cd in self.cpm_result.task_cpm.items():
                    overlap_tasks.append({
                        "name": self.phases[tid-1]["name"] if tid <= len(self.phases) else f"任务{tid}",
                        "start": cd["es"],
                        "end": cd["ef"],
                        "id": tid,
                    })
            if overlap_tasks:
                self.overlap_results = calc_overlap(overlap_tasks)

            vr_cpm = validate_cpm_input(durations, deps_formatted)
            if self.mc_results:
                vr_mc_out = validate_mc_result(self.mc_results)

            lines = [f"项目总工期: {self.cpm_result.project_duration:.1f}"]
            if self.cpm_result.critical_path:
                lines.append(f"关键路径: {' → '.join(str(t) for t in self.cpm_result.critical_path)}")
            if self.mc_results:
                pert = self.mc_results.get("pert", {})
                stats = pert.get("stats", {})
                quants = pert.get("quantiles", {})
                lines.append(f"PERT-Beta: 均值={stats.get('mean',0):.1f}, σ={stats.get('stddev',0):.1f}")
                lines.append(f"P50={quants.get('p50',0):.1f}, P90={quants.get('p90',0):.1f}")
            self.estimate_summary = "\n".join(lines)

            self.completed_phases.append(PHASE_ESTIMATE)

            # 估算完成后自动审计+修复（由外部调用时触发，_audit_and_fix内部不触发）
            if _run_audit:
                self._audit_and_fix(mc_iterations=mc_iterations)

        except Exception as e:
            self._handle_error(PHASE_ESTIMATE, e)

        return {
            "summary": self.estimate_summary,
            "cpm": self.cpm_result,
            "mc": self.mc_results,
            "overlap": self.overlap_results,
        }


    # ═══════════════════════════════════════════════
    # 设置集成
    # ═══════════════════════════════════════════════

    def _resolve_doc_mode(self) -> str:
        """根据全局设置解析文档撰写模式"""
        mode = self.settings.get("doc_write_mode", "auto")
        tpl = self.settings.get("doc_template")
        if mode == "template" and not tpl:
            # 设置了 template 但 doc_template 为空 → 降级为 auto
            return "manual"
        if mode == "template":
            return "mixed"  # 有模板时按模板要求走混合模式
        return mode  # auto / manual

    def _get_setting(self, key: str) -> object:
        """快速获取设置值"""
        return self.settings.get(key)

    # ═══════════════════════════════════════════════
    # 文档阶段
    # ═══════════════════════════════════════════════

    def generate_docs(self, template_name: str = "立项申请书",
                      mode: str = "manual",
                      filled_sections: dict[str, str] = None,
                      output_file: bool = True) -> str:
        """(保持兼容原接口) 生成项目文档"""
        self.current_phase = PHASE_DOCS
        self.reset(PHASE_DOCS)

        try:
            tpl = load_template(template_name)

            pd = ProjectData()
            pd.project_name = self.project_name
            pd.project_description = self.description

            if self.wbs_result:
                pd.wbs_tree_text = self.wbs_text_tree
                pd.wbs_json = self.wbs_json_str
                pd.wbs_work_packages = [
                    {"code": wp.code, "name": wp.name,
                     "deliverable": wp.deliverable,
                     "o": wp.o, "m": wp.m, "p": wp.p}
                    for wp in self.wbs_result.work_packages
                ]

            if self.cpm_result:
                pd.project_duration = self.cpm_result.project_duration
                pd.critical_path = [str(t) for t in self.cpm_result.critical_path]
                pd.cpm_result = f"关键路径: {'→'.join(str(t) for t in self.cpm_result.critical_path)}, 总工期={self.cpm_result.project_duration:.1f}"

            if self.mc_results:
                pert = self.mc_results.get("pert", {})
                quants = pert.get("quantiles", {})
                stats = pert.get("stats", {})
                pd.p50 = quants.get("p50", 0)
                pd.p90 = quants.get("p90", 0)
                pd.estimation_result = f"P50={pd.p50}, P90={pd.p90}, 均值={stats.get('mean',0):.1f}±{stats.get('stddev',0):.1f}"

            if mode == "manual":
                self.doc_content = output_manual(tpl, pd)
            elif mode == "mixed":
                self.doc_content = assemble_mixed_document(tpl, pd, filled_sections or {})
            else:
                raise ValueError(f"不支持的模式: {mode}。可选: manual, mixed")

            if output_file:
                filename = tpl.get("output_filename", "{project_name}_文档.md")
                filename = filename.replace("{project_name}", self.project_name or "未命名项目")
                from project_docs_engine import save_document
                self.doc_path = save_document(self.doc_content, tpl, pd)

            self.completed_phases.append(PHASE_DOCS)

        except Exception as e:
            self._handle_error(PHASE_DOCS, e)

        return self.doc_content


    # ═══════════════════════════════════════════════
    # 内部
    # ═══════════════════════════════════════════════

    def _handle_error(self, phase: str, error: Exception):
        """统一错误处理（不抛出异常，由LLM读取state.errors）"""
        tb = traceback.format_exc()
        # 根据阶段给出解决指引
        hints = {
            "wbs": "WBS分解出错：请确认项目描述是否完整，或手动提供WBS结构化数据",
            "estimate": "估算计算出错：检查OMP值是否满足O≤M≤P，任务数量建议≤50",
            "docs": "文档生成出错：确认模板文件是否存在，或切换到手动模式 (`mode=\"manual\"`)",
            PHASE_WBS: "WBS执行异常：检查自定义数据格式是否正确",
        }
        hint = hints.get(phase, f"阶段「{phase}」执行异常")
        msg = f"[{phase}] {error}"
        self.errors.append(msg)
        self.errors.append(f"  💡 {hint}")
        self.last_error = msg

    def _generate_audit_report(self):
        """
        输出审核：验证所有计算结果的合理性，生成结构化审计报告。
        审计结果写入 self.audit_report（文本）和 self.audit_results（结构化）。
        自动调用，不依赖LLM自觉。
        """
        checks = []
        total_errors = 0
        total_warns = 0

        # ── 1. CPM输入验证 ──
        if self.phases and self.dependencies:
            durations = {i+1: (p.get("m", 0) or 0) for i, p in enumerate(self.phases)}
            vr = validate_cpm_input(durations, self.dependencies)
            if vr.passed:
                checks.append({"check": "CPM输入验证", "cat": "计算失真", "passed": True, "level": "OK", "issues": []})
            else:
                # 附上实际数据供LLM判断误报
                phase_data = [f"{p.get('name','?')}(M={p.get('m',0)})" for p in self.phases]
                enriched = []
                for iss in vr.issues:
                    enriched.append(f"{iss} | phases=[{'; '.join(phase_data)}]")
                total_errors += len(vr.issues)
                checks.append({"check": "CPM输入验证", "cat": "计算失真", "passed": False, "level": "ERROR",
                               "issues": enriched, "fix": "recalculate"})

        # ── 2. CPM输出验证 ──
        if self.cpm_result:
            vr = validate_cpm_result(self.cpm_result)
            if vr.passed:
                checks.append({"check": "CPM输出验证", "cat": "计算失真", "passed": True, "level": "OK", "issues": []})
            else:
                enriched = []
                for iss in vr.issues:
                    enriched.append(f"{iss} | total_duration={self.cpm_result.project_duration}")
                total_errors += len(vr.issues)
                checks.append({"check": "CPM输出验证", "cat": "计算失真", "passed": False, "level": "ERROR",
                               "issues": enriched, "fix": "recalculate"})

        # ── 3. MC输入验证 ──
        if self.phases:
            mc_phases = [(p["name"], p.get("o", 0), p.get("m", 0), p.get("p", 0))
                         for p in self.phases]
            vr = validate_mc_input(mc_phases)
            if vr.passed:
                checks.append({"check": "MC输入验证", "cat": "计算失真", "passed": True, "level": "OK", "issues": []})
            else:
                total_warns += len(vr.issues)
                mc_data = [f"{p.get('name','?')}(O={p.get('o',0)} M={p.get('m',0)} P={p.get('p',0)})"
                           for p in self.phases]
                enriched = [f"{iss} | phases=[{'; '.join(mc_data)}]"
                            for iss in vr.issues]
                checks.append({"check": "MC输入验证", "cat": "计算失真", "passed": False, "level": "WARN",
                               "issues": enriched, "fix": "recalculate"})

        # ── 4. MC输出验证 ──
        if self.mc_results:
            vr = validate_mc_result(self.mc_results)
            if vr.passed:
                checks.append({"check": "MC输出验证", "cat": "计算失真", "passed": True, "level": "OK", "issues": []})
            else:
                total_warns += len(vr.issues)
                checks.append({"check": "MC输出验证", "cat": "计算失真", "passed": False, "level": "WARN",
                               "issues": vr.issues, "fix": "recalculate"})

        # ── 5. 总工期合理性 ──
        if self.cpm_result:
            dur = self.cpm_result.project_duration
            if dur <= 0:
                total_errors += 1
                checks.append({"check": "总工期合理性", "cat": "计算失真", "passed": False, "level": "ERROR",
                               "issues": [f"总工期为 {dur}，应 > 0"], "fix": "recalculate"})
            elif dur > 3650:
                total_warns += 1
                checks.append({"check": "总工期合理性", "cat": "计算失真", "passed": False, "level": "WARN",
                               "issues": [f"总工期 {dur:.0f} 天 > 10年，可能输入有误"], "fix": "recalculate"})
            else:
                checks.append({"check": "总工期合理性", "cat": "计算失真", "passed": True, "level": "OK", "issues": []})

        # ── 6. 关键路径 ──
        if self.cpm_result:
            if self.cpm_result.critical_path:
                checks.append({"check": "关键路径", "cat": "规划失格", "passed": True, "level": "OK", "issues": []})
            else:
                total_warns += 1
                checks.append({"check": "关键路径", "cat": "规划失格", "passed": False, "level": "WARN",
                               "issues": ["未识别到关键路径"], "fix": "replan"})

        # ── 7. P50/P90合理性 ──
        if self.mc_results:
            pert = self.mc_results.get("pert", {})
            quants = pert.get("quantiles", {})
            p50 = quants.get("p50", 0)
            p90 = quants.get("p90", 0)
            if p50 > 0 and p90 >= p50:
                checks.append({"check": "P50/P90合理性", "cat": "计算失真", "passed": True, "level": "OK", "issues": []})
            elif p50 <= 0:
                total_warns += 1
                checks.append({"check": "P50/P90合理性", "cat": "计算失真", "passed": False, "level": "WARN",
                               "issues": ["P50 <= 0，MC模拟结果异常"], "fix": "recalculate"})
            else:
                total_warns += 1
                checks.append({"check": "P50/P90合理性", "cat": "计算失真", "passed": False, "level": "WARN",
                               "issues": [f"P50({p50}) > P90({p90})，分布异常"], "fix": "recalculate"})

        # ── 8. HTML报告完整性 ──
        if self.html_report_path:
            if os.path.isfile(self.html_report_path):
                size = os.path.getsize(self.html_report_path)
                if size > 500:
                    checks.append({"check": "HTML报告完整性", "cat": "内容失调", "passed": True, "level": "OK", "issues": []})
                else:
                    total_warns += 1
                    checks.append({"check": "HTML报告完整性", "cat": "内容失调", "passed": False, "level": "WARN",
                                   "issues": [f"HTML文件仅 {size} 字节"], "fix": "regenerate"})
            else:
                total_errors += 1
                checks.append({"check": "HTML报告完整性", "cat": "内容失调", "passed": False, "level": "ERROR",
                               "issues": [f"HTML路径 {self.html_report_path} 不存在"], "fix": "regenerate"})

        # ── 9. 文档逐节检查 ──
        if self.doc_content:
            try:
                from project_docs_engine import load_template, list_templates

                # 查找匹配的模板（按文档标题匹配）
                doc_title_line = self.doc_content.split("\n")[0] if self.doc_content else ""
                matched_tpl = None
                for tpl_name in list_templates().keys():
                    if tpl_name in doc_title_line:
                        matched_tpl = load_template(tpl_name)
                        break

                if matched_tpl:
                    sections = matched_tpl.get("sections", [])
                    doc_lines = self.doc_content.split("\n")
                    section_checks = []

                    for sec in sections:
                        sec_title = sec.get("title", "")
                        sec_key = sec.get("key", "")
                        sec_mode = sec.get("mode", "manual")
                        if not sec_title:
                            continue

                        # 查找本节在文档中的行区间
                        sec_start = None
                        for i, line in enumerate(doc_lines):
                            if line.strip().startswith(f"## {sec_title}"):
                                sec_start = i
                                break

                        if sec_start is None:
                            total_errors += 1
                            section_checks.append(
                                (f"文档章节「{sec_title}」", "ERROR",
                                 [f"模板定义 {sec_key} 但文档中缺少 ## {sec_title}"
                                  f" | doc.md:? | 模板共{len(sections)}节，当前文档仅包含"
                                  f" {sum(1 for l in doc_lines if l.strip().startswith('## '))} 个 H2 章节"]))
                            continue

                        # 提取本节的正文内容（直到下一个 ## 或文档结束）
                        sec_end = len(doc_lines)
                        for i in range(sec_start + 1, len(doc_lines)):
                            if doc_lines[i].strip().startswith("## "):
                                sec_end = i
                                break
                        sec_body = "\n".join(doc_lines[sec_start:sec_end])
                        sec_body_len = len(sec_body.strip())

                        # 按模式分段检查
                        doc_line = sec_start + 1  # 文档中第几行（1-based）
                        ctx_lines = doc_lines[max(0, sec_start):min(len(doc_lines), sec_start + 4)]
                        context_snippet = " | ".join(l.strip()[:50] for l in ctx_lines)
                        location = f"doc.md:{doc_line}"

                        if sec_mode == "manual":
                            # 手动模式：应有填写提示/占位符
                            has_hint = any(kw in sec_body for kw in
                                           ["填充提示", "在此处填写", "填写内容"])
                            if not has_hint:
                                total_warns += 1
                                section_checks.append(
                                    (f"文档章节「{sec_title}」(手动)", "WARN",
                                     [f"缺少填充提示或占位符 (doc.md:{doc_line}) "
                                      f"上下文: {context_snippet[:80]}"]))
                            else:
                                section_checks.append(
                                    (f"文档章节「{sec_title}」(手动)", "OK", []))

                        elif sec_mode == "auto":
                            # 自动模式：应有实质内容（>50字符），且不能含占位符
                            has_placeholder = "在此处填写" in sec_body
                            if sec_body_len < 50 or has_placeholder:
                                total_warns += 1
                                section_checks.append(
                                    (f"文档章节「{sec_title}」(自动)", "WARN",
                                     [f"内容{sec_body_len}字符{'且含占位符' if has_placeholder else ''}"
                                      f" (doc.md:{doc_line}) 上下文: {context_snippet[:80]}"]))
                            else:
                                section_checks.append(
                                    (f"文档章节「{sec_title}」(自动)", "OK", []))

                        elif sec_mode == "outline":
                            if sec_body_len < 20:
                                total_warns += 1
                                section_checks.append(
                                    (f"文档章节「{sec_title}」(概要)", "WARN",
                                     [f"概要内容仅{sec_body_len}字符 (doc.md:{doc_line})"
                                      f" 上下文: {context_snippet[:80]}"]))
                            else:
                                section_checks.append(
                                    (f"文档章节「{sec_title}」(概要)", "OK", []))

                    # 输出章节检查结果
                    for sc_name, sc_level, sc_issues in section_checks:
                        if sc_level == "OK":
                            checks.append({"check": sc_name, "cat": "内容失调",
                                           "passed": True, "level": "OK", "issues": []})
                        else:
                            checks.append({"check": sc_name, "cat": "内容失调",
                                           "passed": False, "level": sc_level,
                                           "issues": sc_issues, "fix": "regenerate"})

                    # WBS引用检查（在文档正文中搜索）
                    if self.wbs_result:
                        has_wbs_ref = any(kw in self.doc_content for kw in
                                          ["WBS", "工作分解", "工作包", "wbs"])
                        if not has_wbs_ref:
                            total_warns += 1
                            wp_count = len(self.wbs_result.work_packages)
                            checks.append({"check": "文档WBS引用", "cat": "内容失调",
                                           "passed": False, "level": "WARN",
                                           "issues": [f"已生成WBS（{wp_count}个工作包）但文档中未引用关键词: WBS/工作分解/工作包/wbs"
                                                      f" | doc.md:1 上下文: 文档首行 {doc_title_line[:60]}"],
                                           "fix": "regenerate"})

                    if self.cpm_result:
                        has_cpm_ref = any(kw in self.doc_content for kw in
                                          ["关键路径", "工期", "估算", "CPM", "P50", "P90"])
                        if not has_cpm_ref:
                            total_warns += 1
                            checks.append({"check": "文档CPM引用", "cat": "内容失调",
                                           "passed": False, "level": "WARN",
                                           "issues": ["已生成CPM但文档中未引用估算结果"],
                                           "fix": "regenerate"})
                else:
                    # 未匹配模板，回退到简单检查
                    content_len = len(self.doc_content)
                    is_manual = any(kw in self.doc_content for kw in
                                    ["填充提示", "在此处填写"])
                    if is_manual and content_len >= 50:
                        checks.append({"check": "文档完整性", "cat": "内容失调",
                                       "passed": True, "level": "OK", "issues": []})
                    elif content_len >= 200:
                        checks.append({"check": "文档完整性", "cat": "内容失调",
                                       "passed": True, "level": "OK", "issues": []})
                    else:
                        total_warns += 1
                        checks.append({"check": "文档完整性", "cat": "内容失调",
                                       "passed": False, "level": "WARN",
                                       "issues": [f"文档仅 {content_len} 字符"],
                                       "fix": "regenerate"})

            except Exception as e:
                # 模板加载失败时不阻断
                checks.append({"check": "文档检查", "cat": "内容失调",
                               "passed": True, "level": "OK",
                               "issues": [f"模板匹配失败: {e}"]})
        else:
            # 文档未生成（mode="manual"时正常；全流程模式才检查）
            if "docs" in self.completed_phases or "full" in self.completed_phases:
                total_errors += 1
                checks.append({"check": "文档完整性", "cat": "内容失调", "passed": False, "level": "ERROR",
                               "issues": ["文档未生成"], "fix": "regenerate"})

        # ── 构建审计报告文本 ──
        lines = []
        lines.append("")
        lines.append("─── 估算审计报告 ──────────────────────────────────")

        verdict = "pass" if total_errors == 0 else "fail"
        if total_errors == 0 and total_warns > 0:
            verdict = "warn"

        lines.append(f"  审计结论：{verdict}（ERROR={total_errors}, WARN={total_warns}）")
        lines.append("  ─── LLM误报筛查 ───")
        lines.append("  逐条检查以下FAIL/WARN，判断是否为误报：")
        lines.append("  是→确认安全，放行；否→触发自动修复或LLM介入修改")
        lines.append("")
        for c in checks:
            if c["level"] == "OK":
                lines.append(f"  ✅ {c['check']}：PASS")
            else:
                tag = "❌" if c["level"] == "ERROR" else "⚠️"
                lines.append(f"  {tag} {c['check']}：{c['level']} [{c.get('fix','?')}]")
                for iss in c["issues"][:3]:
                    lines.append(f"     - {iss}")
                    # 如果有location信息，附加输出
                    if isinstance(iss, dict):
                        if iss.get("location"):
                            lines.append(f"       位置: {iss['location']}")
                        if iss.get("context"):
                            ctx = iss["context"][:120]
                            lines.append(f"       上下文: {ctx}")
                    elif "phases[" in str(iss) or "doc" in str(iss).lower():
                        pass  # 已有位置信息在描述中

        lines.append("")

        audit_text = "\n".join(lines)
        print(audit_text)

        self.audit_report = audit_text
        self.audit_results = checks

    def _audit_and_fix(self, mc_iterations: int = 2000):
        """
        三阶审计+自动修复：先审，后修，再审。
        
        修复策略：
        - 计算失真 → recalculate（重新计算CPM/MC）
        - 内容失调 → regenerate（重新生成报告/文档）
        - 规划失格 → replan（重新规划依赖/WBS）
        """
        MAX_FIX_CYCLES = 3
        for cycle in range(1, MAX_FIX_CYCLES + 1):
            self._generate_audit_report()

            failed = [c for c in self.audit_results if not c["passed"]]
            if not failed:
                print(f"  ✅ 第{cycle}轮审计：全部通过")
                return

            print(f"  🔧 第{cycle}轮修复：{len(failed)} 项待修复")
            needs_recalc = any(c.get("fix") == "recalculate" for c in failed)
            needs_regen = any(c.get("fix") == "regenerate" for c in failed)
            needs_replan = any(c.get("fix") == "replan" for c in failed)

            # ── 修复1：计算失真 ──
            if needs_recalc and self.phases:
                print("  🔄 修复计算失真：重新执行估算...")
                self.run_estimate(mc_iterations=mc_iterations, _run_audit=False)

            # ── 修复2：内容失调 ──
            if needs_regen:
                print("  🔄 修复内容失调：重新生成报告和文档...")
                self._generate_html_report()
                try:
                    # 尝试重新生成文档（如果有模板）
                    from project_docs_engine import load_template
                    tpl_name = "立项申请书"
                    tpl = load_template(tpl_name)
                    if tpl:
                        self.generate_docs(template_name=tpl_name, mode="manual", output_file=False)
                        print(f"    文档已重新生成 ({len(self.doc_content)}字符)")
                except Exception:
                    print("    文档重新生成跳过（无模板或已是最佳）")

            # ── 修复3：规划失格 ──
            if needs_replan and self.phases:
                print("  🔄 修复规划失格：重新规划依赖...")
                from analysis_engine import auto_plan_dependencies
                self.dependencies = auto_plan_dependencies(len(self.phases), self.phases)
                # 重新编译依赖格式
                deps_1based = {}
                for k, v in self.dependencies.items():
                    k1 = k + 1 if isinstance(k, int) else k
                    deps_1based[k1] = []
                    for dep in v:
                        if isinstance(dep, (list, tuple)):
                            pred_id = dep[0] + 1 if isinstance(dep[0], int) else dep[0]
                            dep_type = dep[1] if len(dep) >= 2 else "FS"
                            deps_1based[k1].append((pred_id, dep_type))
                        else:
                            deps_1based[k1].append(dep + 1 if isinstance(dep, int) else dep)
                self.dependencies = deps_1based
                self.run_estimate(mc_iterations=mc_iterations, _run_audit=False)
                self._generate_html_report()

        # 3轮修复后仍有问题 → 输出最终报告，标记剩余项
        self._generate_audit_report()
        remaining = [c for c in self.audit_results if not c["passed"]]
        if remaining:
            print(f"  ⚠️  经{MAX_FIX_CYCLES}轮修复仍有 {len(remaining)} 项未解决：")
            for c in remaining:
                print(f"     - [{c['check']}] {c.get('fix','?')}: {'; '.join(c['issues'][:2])}")


# ═══════════════════════════════════════════════════
# 全流程一键入口（增强版）
# ═══════════════════════════════════════════════════

def run_full(description: str,
             project_name: str = None,
             doc_template: str = "立项申请书",
             doc_mode: str = "manual",
             mc_iterations: int = 2000) -> dict:
    """
    全流程一键执行（推荐入口）。
    项目管理的完整三环节：WBS分解 → 活动历时估算 → 项目文档生成。
    
    WBS 是新项目必做的第一步，即使已有OMP参数也需先分解。
    
    所有阶段由代码硬编码顺序驱动，不依赖LLM自觉。
    如果触发 LLMInteractionRequired，LLM 提供数据后再次调用 run_full() 即可继续。
    
    用法（LLM）:
        result = run_full("电商后台管理系统")
        # → 如果抛出 LLMInteractionRequired，提供WBS数据后重试：
        # state = PipelineState("电商后台")
        # state.run_wbs(custom_data={...})
        # result = state.run_full()  # 继续执行后续阶段
    
    返回:
        {"status": "ok" | "blocked" | "error",
         "message": str,
         "state": PipelineState}
    
    读取结果:
        state = result["state"]
        state.wbs_text_tree      → WBS文本树
        state.estimate_summary   → 估算摘要
        state.html_report_path   → HTML报告路径
        state.doc_content        → 文档内容
        state.doc_path           → 文档文件路径
    """
    state = PipelineState(description)
    state.project_name = project_name or _extract_project_name(description)
    return state.run_full(
        doc_template=doc_template,
        doc_mode=doc_mode,
        mc_iterations=mc_iterations
    )


def run_pipeline(
    description: str,
    mode: str = "full",
    project_name: str = None,
    wbs_template: str = "deliverable",
    wbs_custom_data: dict = None,
    doc_template: str = "立项申请书",
    doc_mode: str = "manual",
    doc_filled: dict[str, str] = None,
    mc_iterations: int = 2000,
    custom_phases: list[dict] = None,
) -> PipelineState:
    """
    传统全流程一键执行（保持向后兼容）。
    参见 run_full() 为新推荐入口。
    """
    state = PipelineState(description)
    state.project_name = project_name or _extract_project_name(description)

    try:
        if mode in ("full", "wbs"):
            state.run_wbs(template=wbs_template, custom_data=wbs_custom_data)
            if custom_phases:
                state.phases = custom_phases

        if mode in ("full", "estimate"):
            if custom_phases:
                state.prepare_estimation(custom_phases=custom_phases)
            elif state.phases:
                pass
            elif state.wbs_result:
                state.prepare_estimation()
            state.run_estimate(mc_iterations=mc_iterations)

        if mode in ("full", "docs"):
            state.generate_docs(
                template_name=doc_template,
                mode=doc_mode,
                filled_sections=doc_filled or {},
            )

    except Exception as e:
        state._handle_error("pipeline", e)

    return state


def _extract_project_name(description: str) -> str:
    """从项目描述中提取项目名（启发式）"""
    text = description.strip()
    prefixes = ["帮我", "请", "规划", "估算", "生成", "做", "搞", "开发", "做一个"]
    for p in prefixes:
        if text.startswith(p):
            text = text[len(p):].strip()
    for suffix in ["项目", "系统", "平台", "应用", "工具", "网站", "App"]:
        if suffix in text:
            idx = text.index(suffix)
            start = max(0, idx - 8)
            return text[start:idx + len(suffix)]
    return text[:12] or "未命名项目"


# ═══════════════════════════════════════════════════
# 工具查询
# ═══════════════════════════════════════════════════

def list_available_templates() -> str:
    """列出可用模板（供LLM读取）"""
    tpls = list_templates()
    lines = ["可用模板:"]
    for name, desc in tpls.items():
        lines.append(f"  - {name}: {desc[:40]}...")
    lines.append("")
    lines.append("WBS模板: deliverable / lifecycle / modular")
    return "\n".join(lines)


def get_pipeline_help() -> str:
    """输出run_pipeline/run_full的使用说明"""
    return """
===== 推荐入口 =====
run_full(description, ...) → {"status", "message", "state"}

自动判断是否需要WBS → 提取参数 → 紧前关系 → 估算 → 报告。
如触发 LLMInteractionRequired，按提示提供数据后重试。

参数:
  description: 项目描述（必填）
  project_name: 项目名（可选）

读取结果:
  result["state"].wbs_text_tree      → WBS文本树
  result["state"].estimate_summary   → 估算摘要
  result["state"].html_report_path   → HTML报告路径
  result["state"].doc_content        → 文档内容
  result["state"].errors             → 错误列表
  result["state"].status()           → 当前状态

===== 传统入口 =====
run_pipeline(description, mode="full", ...) → PipelineState

mode:
  "full"      → WBS + 估算 + 文档（兼容原行为）
  "wbs"       → 仅WBS
  "estimate"  → 仅估算
  "docs"      → 仅文档
"""
