"""
报告引擎 — 从报告模板加载配置，调用可视化算子组装完整 HTML 报告。

报告模板为独立 JSON 文件，存储在 templates/reports/ 目录。
场景模板可通过 default_report 字段关联默认报告。

核心流程：
1. 按名加载报告模板 → 获取 sections 配置
2. 传入 Pipeline 执行结果（results dict）
3. 逐 section 调用可视化算子
4. 组装为完整 HTML

section types 与 viz 算子映射：
  metric_card              → viz.metric_card()
  judgment_card            → viz.judgment_card()
  data_table               → viz.data_table()
  bar_chart                → viz.bar_chart()
  te_breakdown             → viz.te_breakdown()
  te_judgment_section      → viz.te_judgment_section()
  measurement_uncertainty  → viz.measurement_uncertainty_section()
"""
import json
import os
from typing import Optional, Any


_SECTION_RENDERERS = {}

def _register(name: str):
    """装饰器：注册 section 类型到渲染器"""
    def wrapper(func):
        _SECTION_RENDERERS[name] = func
        return func
    return wrapper


def _resolve_source(source: str, results: dict, context: dict) -> Optional[Any]:
    """
    从 Pipeline 执行结果中解析数据源。

    支持语法：
      %步骤名%          — 该步骤的完整返回值
      %步骤名.字段名%   — 返回值中的某个字段
      %input%           — 原始输入
      literal value     — 直接使用的字面量
    """
    if not isinstance(source, str):
        return source
    if source.startswith("%") and source.endswith("%"):
        ref = source[1:-1]
        if ref == "input":
            return context.get("__input__")
        elif ref.startswith("input."):
            key = ref[6:]
            inp = context.get("__input__", {})
            return inp.get(key) if isinstance(inp, dict) else inp
        elif "." in ref:
            step, key = ref.split(".", 1)
            step_result = results.get(step, {})
            return step_result.get(key) if isinstance(step_result, dict) else step_result
        else:
            return results.get(ref)
    return source


# ─── 各 section type 的渲染器 ──────────────────────────

@_register("metric_card")
def _render_metric_card(section: dict, results: dict, context: dict) -> str:
    from scripts.operations.viz import metric_card
    data = _resolve_source(section.get("source", ""), results, context)
    if not isinstance(data, dict):
        return ""
    return metric_card(data, title=section.get("title", ""),
                       fields=section.get("fields"),
                       decimals=section.get("decimals", 4))


@_register("data_table")
def _render_data_table(section: dict, results: dict, context: dict) -> str:
    from scripts.operations.viz import data_table
    data = _resolve_source(section.get("source", ""), results, context)
    if not isinstance(data, dict):
        return ""
    return data_table(data, title=section.get("title", ""),
                      fields=section.get("fields"),
                      decimals=section.get("decimals", 4))


@_register("te_breakdown")
def _render_te_breakdown(section: dict, results: dict, context: dict) -> str:
    from scripts.operations.viz import te_breakdown
    data = _resolve_source(section.get("source", ""), results, context)
    if not isinstance(data, dict):
        return ""
    return te_breakdown(data, title=section.get("title", "总误差分量分解"))


@_register("te_judgment_section")
def _render_te_judgment(section: dict, results: dict, context: dict) -> str:
    from scripts.operations.viz import te_judgment_section
    judgment = _resolve_source(section.get("source", ""), results, context)
    te_source = section.get("te_source", "")
    te_data = _resolve_source(te_source, results, context) if te_source else None
    if not isinstance(judgment, dict):
        return ""
    return te_judgment_section(judgment, te_data)


@_register("measurement_uncertainty")
def _render_uncertainty(section: dict, results: dict, context: dict) -> str:
    from scripts.operations.viz import measurement_uncertainty_section
    uc = _resolve_source(section.get("uc_source", ""), results, context)
    ue = _resolve_source(section.get("ue_source", ""), results, context)
    components = _resolve_source(section.get("components_source", ""), results, context)
    k = section.get("k", 2.0)
    if uc is None or ue is None:
        return ""
    return measurement_uncertainty_section(
        uc, ue, components or [],
        k=k, title=section.get("title", "测量不确定度"))


@_register("judgment_card")
def _render_judgment_card(section: dict, results: dict, context: dict) -> str:
    from scripts.operations.viz import judgment_card
    return judgment_card(
        level=section.get("level", ""),
        label=section.get("label", ""),
        description=section.get("description", ""),
        status=section.get("status", "info"),
    )


@_register("bar_chart")
def _render_bar_chart(section: dict, results: dict, context: dict) -> str:
    from scripts.operations.viz import bar_chart
    labels = _resolve_source(section.get("labels", []), results, context)
    values = _resolve_source(section.get("values", []), results, context)
    if not labels or not values:
        return ""
    return bar_chart(labels, values,
                     title=section.get("title", ""),
                     xlabel=section.get("xlabel", ""),
                     ylabel=section.get("ylabel", ""))


# ─── 新增 section renderers ──────────────────────────

@_register("precision_summary")
def _render_precision_summary(section: dict, results: dict, context: dict) -> str:
    from scripts.operations.viz import precision_summary
    data = _resolve_source(section.get("source", ""), results, context)
    if not isinstance(data, dict):
        return ""
    per_level = data.get("per_level", [])
    return precision_summary(
        per_level, data.get("synthetic_std", 0),
        data.get("synthetic_rsd", 0), data.get("overall_mean", 0))


@_register("control_chart_section")
def _render_control_chart(section: dict, results: dict, context: dict) -> str:
    from scripts.operations.viz import control_chart_section
    data = _resolve_source(section.get("source", ""), results, context)
    if not isinstance(data, dict):
        return ""
    return control_chart_section(data, title=section.get("title", "质控图统计"))


@_register("anova_summary")
def _render_anova_summary(section: dict, results: dict, context: dict) -> str:
    from scripts.operations.viz import anova_summary
    data = _resolve_source(section.get("source", ""), results, context)
    if not isinstance(data, dict):
        return ""
    return anova_summary(data, title=section.get("title", "ANOVA方差分析"))


@_register("group_means_chart")
def _render_group_means(section: dict, results: dict, context: dict) -> str:
    from scripts.operations.viz import group_means_chart
    data = _resolve_source(section.get("source", ""), results, context)
    if isinstance(data, dict):
        gm = data.get("group_means", {})
        if gm:
            return group_means_chart(gm, title=section.get("title", "各组均值对比"))
    return ""


@_register("calibration_summary")
def _render_calibration_summary(section: dict, results: dict, context: dict) -> str:
    from scripts.operations.viz import calibration_summary
    data = _resolve_source(section.get("source", ""), results, context)
    if not isinstance(data, dict):
        return ""
    return calibration_summary(data, title=section.get("title", "校准曲线参数"))


@_register("lod_loq_card")
def _render_lod_loq(section: dict, results: dict, context: dict) -> str:
    from scripts.operations.viz import lod_loq_card
    data = _resolve_source(section.get("source", ""), results, context)
    if not isinstance(data, dict):
        return ""
    return lod_loq_card(data, title=section.get("title", "检出限/定量限"))


@_register("uncertainty_curve_card")
def _render_uncertainty_curve(section: dict, results: dict, context: dict) -> str:
    from scripts.operations.viz import uncertainty_curve_card
    data = _resolve_source(section.get("source", ""), results, context)
    if not isinstance(data, dict):
        return ""
    return uncertainty_curve_card(data, title=section.get("title", "曲线不确定度"))


@_register("trend_summary_card")
def _render_trend_summary(section: dict, results: dict, context: dict) -> str:
    from scripts.operations.viz import trend_summary_card
    data = _resolve_source(section.get("source", ""), results, context)
    if isinstance(data, dict):
        ss = data.get("stats_summary", {})
        if ss:
            return trend_summary_card(ss, title=section.get("title", "趋势监控摘要"))
    return ""


@_register("alert_section")
def _render_alert_section(section: dict, results: dict, context: dict) -> str:
    from scripts.operations.viz import alert_section
    data = _resolve_source(section.get("source", ""), results, context)
    if isinstance(data, dict):
        alerts = data.get("alerts", [])
        return alert_section(alerts, title=section.get("title", "预警信息"))
    return ""


# ═══════════════════════════════════════════════════════
# 加载报告配置
# ═══════════════════════════════════════════════════════

def load_report_config(report_name: str) -> dict:
    """
    按名称加载报告模板的 report 配置。

    Parameters
    ----------
    report_name : str — 报告模板名（不含 .json）

    Returns
    -------
    dict — {"title": str, "sections": list[dict]}

    Raises
    ------
    FileNotFoundError — 报告模板不存在
    """
    from scripts.pipeline.registry import _REPORT_DIR, _USER_DIR

    for base_dir in [_USER_DIR, _REPORT_DIR]:
        path = os.path.join(base_dir, f"{report_name}.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                report = data.get("report")
                if report:
                    return report

    raise FileNotFoundError(f"未找到报告模板: {report_name}")


def get_default_report_name(scenario_name: str) -> Optional[str]:
    """
    获取场景模板的默认报告模板名。

    Parameters
    ----------
    scenario_name : str — 场景模板名

    Returns
    -------
    str or None — 默认报告名，未配置则返回 None
    """
    try:
        from scripts.pipeline.registry import load_template
        pipe = load_template(scenario_name)
        return pipe.default_report or None
    except (FileNotFoundError, Exception):
        return None


# ═══════════════════════════════════════════════════════
# 报告生成器
# ═══════════════════════════════════════════════════════

def render_report(report_config: dict, pipeline_results: dict,
                  context: dict = None) -> str:
    """
    根据报告配置和 Pipeline 执行结果，生成完整 HTML 报告。

    Parameters
    ----------
    report_config : dict
        {"title": str, "sections": list[dict]}
    pipeline_results : dict — Pipeline.run() 的返回值
    context : dict, optional — 额外上下文（传递 %input% 引用）

    Returns
    -------
    str — 完整的 HTML 文档
    """
    if context is None:
        context = {}

    title = report_config.get("title", "分析报告")
    sections = report_config.get("sections", [])

    body_parts = []
    chart_js_needed = False

    for sec in sections:
        sec_type = sec.get("type", "")
        renderer = _SECTION_RENDERERS.get(sec_type)
        if not renderer:
            body_parts.append(f'<div class="report-section report-error"><h2>section 类型未注册</h2><p>"{sec_type}" — 请检查报告模板配置，或通过 register_section_type() 注册自定义类型。</p></div>')
            chart_js_needed = True
            continue

        try:
            html = renderer(sec, pipeline_results, context)
            if html:
                body_parts.append(html)
                if sec_type not in ("metric_card", "data_table", "judgment_card"):
                    chart_js_needed = True
        except Exception as e:
            body_parts.append(f'<div class="report-section report-error"><h2>section 渲染失败</h2><p>类型: {sec_type}<br>错误: {e}</p></div>')
            chart_js_needed = True

    body_html = "\n".join(body_parts)
    js_include = '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>' if chart_js_needed else ""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
{js_include}
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
       max-width: 960px; margin: 0 auto; padding: 24px; background: #f5f6fa; color: #2c3e50; }}
h1 {{ font-size: 22px; font-weight: 600; color: #1a1a2e; margin-bottom: 24px; }}
h2 {{ font-size: 16px; font-weight: 600; color: #2c3e50; margin-bottom: 12px; }}
.report-section {{ background: white; border-radius: 10px; padding: 20px;
                   margin-bottom: 16px; border: 1px solid #e8ecf1; }}
.metric-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
                gap: 12px; }}
.metric-card {{ background: #f8f9fc; border-radius: 8px; padding: 14px 16px;
                text-align: center; }}
.metric-label {{ font-size: 12px; color: #7f8c8d; margin-bottom: 6px;
                 white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.metric-value {{ font-size: 22px; font-weight: 600; color: #2c3e50; }}
.judgment-card {{ display: flex; align-items: flex-start; gap: 14px;
                  padding: 18px 20px; border-radius: 8px; }}
.judgment-icon {{ font-size: 24px; font-weight: bold; line-height: 1.2; }}
.judgment-level {{ font-size: 15px; font-weight: 600; margin-bottom: 4px; }}
.judgment-desc {{ font-size: 13px; opacity: 0.85; }}
table.data-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
table.data-table th {{ background: #f0f2f5; color: #2c3e50; font-weight: 600;
                       padding: 10px 14px; text-align: left; border-bottom: 2px solid #ddd; }}
table.data-table td {{ padding: 8px 14px; border-bottom: 1px solid #eee; }}
table.data-table tr:hover td {{ background: #f8f9fc; }}
.chart-box {{ margin-top: 16px; max-height: 350px; }}
.report-error {{ border-left: 4px solid #E24B4A !important; background: #FCEBEB !important; }}
.report-error h2 {{ color: #791F1F; font-size: 14px; }}
.report-error p {{ color: #A32D2D; font-size: 13px; }}
</style>
</head>
<body>
<h1>{title}</h1>
{body_html}
</body>
</html>"""


def render_from_template(scenario_name: str, pipeline_results: dict,
                         context: dict = None,
                         report_name: str = None) -> str:
    """
    从场景模板加载，使用指定报告模板或默认报告渲染 HTML。

    Parameters
    ----------
    scenario_name : str — 场景模板名
    pipeline_results : dict — Pipeline.run() 的返回值
    context : dict, optional
    report_name : str, optional — 指定报告模板名，不传则用 default_report

    Returns
    -------
    str — 完整 HTML 文档
    """
    if report_name is None:
        report_name = get_default_report_name(scenario_name)
        if report_name is None:
            raise ValueError(
                f"场景 '{scenario_name}' 未配置 default_report，"
                "请提供 report_name 参数指定报告模板"
            )

    report_config = load_report_config(report_name)
    return render_report(report_config, pipeline_results, context)


# ═══════════════════════════════════════════════════════
# 注册自定义 section 类型
# ═══════════════════════════════════════════════════════

def register_section_type(name: str, render_func):
    """
    注册自定义 section 类型。

    Parameters
    ----------
    name : str — section type 名称
    render_func : callable(section, results, context) → str
    """
    _SECTION_RENDERERS[name] = render_func


__all__ = [
    "load_report_config", "get_default_report_name",
    "render_report", "render_from_template",
    "register_section_type",
]
