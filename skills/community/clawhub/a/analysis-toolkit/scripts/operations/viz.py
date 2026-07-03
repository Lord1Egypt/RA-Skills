"""
可视化算子 — 分析结果的 HTML 可视化组件

每个算子接受分析结果 dict 和配置参数，返回一段自包含的 HTML/CSS/JS 片段。
可嵌入由 report_engine 组装的自定义 HTML 报告中。

算子分类：
  - 卡片类: metric_card, judgment_card
  - 表格类: data_table
  - 图表类: bar_chart, pie_chart, comparison_chart
  - 专用类: te_breakdown, control_chart_plot, calibration_plot, youden_plot
"""
import json
import uuid
import math


# ═══════════════════════════════════════════════════════
# 辅助
# ═══════════════════════════════════════════════════════

def _fmt(v, decimals=4):
    """格式化显示数值"""
    if isinstance(v, float):
        if abs(v) < 0.0001 and v != 0:
            return f"{v:.2e}"
        return f"{v:.{decimals}f}"
    return str(v)


def _make_id(prefix="viz"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


# ═══════════════════════════════════════════════════════
# 卡片类算子
# ═══════════════════════════════════════════════════════

def metric_card(data: dict, title: str = "关键指标",
                fields: list = None, decimals: int = 4) -> str:
    """
    指标卡片组 — 显示关键数值指标的网格卡片。

    Parameters
    ----------
    data : dict — 包含指标数据的字典
    title : str — 卡片组标题
    fields : list[str], optional — 要显示的字段列表（默认全部数值字段）
    decimals : int — 小数位数

    Returns
    -------
    str — HTML 片段
    """
    if fields is None:
        fields = [k for k, v in data.items()
                  if isinstance(v, (int, float)) and not k.startswith("_")]

    cards_html = ""
    for f in fields:
        val = data.get(f)
        if val is None or not isinstance(val, (int, float)):
            continue
        cards_html += f"""
        <div class="metric-card">
            <div class="metric-label">{f}</div>
            <div class="metric-value">{_fmt(val, decimals)}</div>
        </div>"""

    if not cards_html:
        return ""

    return f"""
    <div class="report-section">
        <h2>{title}</h2>
        <div class="metric-grid">
            {cards_html}
        </div>
    </div>"""


def judgment_card(level: str, label: str, description: str = "",
                  status: str = "info") -> str:
    """
    判定结果卡片 — 带有颜色编码的结论卡片。

    Parameters
    ----------
    level : str — 判定等级 (excellent/good/acceptable/unacceptable)
    label : str — 判定标签
    description : str — 补充说明
    status : str — 状态色: info/success/warning/danger

    Returns
    -------
    str — HTML 片段
    """
    COLOR_MAP = {
        "info": {"bg": "#E6F1FB", "border": "#378ADD", "text": "#0C447C", "icon": "ℹ"},
        "success": {"bg": "#EAF3DE", "border": "#639922", "text": "#27500A", "icon": "✓"},
        "warning": {"bg": "#FAEEDA", "border": "#BA7517", "text": "#633806", "icon": "⚠"},
        "danger": {"bg": "#FCEBEB", "border": "#E24B4A", "text": "#791F1F", "icon": "✗"},
    }
    c = COLOR_MAP.get(status, COLOR_MAP["info"])

    return f"""
    <div class="report-section">
        <div class="judgment-card" style="background:{c['bg']};border-left:4px solid {c['border']};">
            <div class="judgment-icon" style="color:{c['border']};">{c['icon']}</div>
            <div class="judgment-body">
                <div class="judgment-level" style="color:{c['text']};">{label}</div>
                <div class="judgment-desc" style="color:{c['text']};">{level}{(' — ' + description) if description else ''}</div>
            </div>
        </div>
    </div>"""


# ═══════════════════════════════════════════════════════
# 表格类算子
# ═══════════════════════════════════════════════════════

def data_table(data: dict, title: str = "详细数据",
               fields: list = None, decimals: int = 4) -> str:
    """
    key-value 数据表格。

    Parameters
    ----------
    data : dict — 数据字典
    title : str — 表格标题
    fields : list[str], optional — 要显示的字段
    decimals : int

    Returns
    -------
    str — HTML 片段
    """
    if fields is None:
        fields = [k for k, v in data.items()
                  if isinstance(v, (int, float, str)) and not k.startswith("_")]

    rows_html = ""
    for f in fields:
        val = data.get(f)
        if val is None:
            continue
        rows_html += f"<tr><td>{f}</td><td>{_fmt(val, decimals) if isinstance(val, float) else val}</td></tr>\n"

    if not rows_html:
        return ""

    return f"""
    <div class="report-section">
        <h2>{title}</h2>
        <table class="data-table">
            <thead><tr><th>指标</th><th>值</th></tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>"""


# ═══════════════════════════════════════════════════════
# 图表类算子（基于 Chart.js）
# ═══════════════════════════════════════════════════════

def _chart_container(title: str = "", chart_type: str = "bar",
                     dataset: dict = None, options: dict = None) -> str:
    """生成 Chart.js 图表的通用包装"""
    chart_id = _make_id("chart")
    dataset_json = json.dumps(dataset or {})
    options_json = json.dumps(options or {})

    return f"""
    <div class="report-section">
        <h2>{title}</h2>
        <div class="chart-box">
            <canvas id="{chart_id}"></canvas>
        </div>
        <script>
        (function() {{
            var ctx = document.getElementById('{chart_id}').getContext('2d');
            new Chart(ctx, {{
                type: '{chart_type}',
                data: {dataset_json},
                options: Object.assign({{
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {{ legend: {{ position: 'bottom' }} }}
                }}, {options_json})
            }});
        }})();
        </script>
    </div>"""


def bar_chart(labels: list, values: list, title: str = "柱状图",
              xlabel: str = "", ylabel: str = "", color: str = "#378ADD") -> str:
    """简单柱状图"""
    dataset = {
        "labels": labels,
        "datasets": [{
            "label": title,
            "data": values,
            "backgroundColor": color,
            "borderRadius": 4,
        }]
    }
    opts = {
        "scales": {
            "x": {"title": {"display": bool(xlabel), "text": xlabel}},
            "y": {"title": {"display": bool(ylabel), "text": ylabel}},
        }
    }
    return _chart_container(title, "bar", dataset, opts)


def pie_chart(labels: list, values: list, title: str = "") -> str:
    """饼图"""
    colors = ["#378ADD", "#1D9E75", "#D85A30", "#BA7517",
              "#7F77DD", "#D4537E", "#639922", "#888780"]
    dataset = {
        "labels": labels,
        "datasets": [{
            "data": values,
            "backgroundColor": colors[:len(labels)],
        }]
    }
    return _chart_container(title, "pie", dataset, {})


# ═══════════════════════════════════════════════════════
# 专用分析图表算子
# ═══════════════════════════════════════════════════════

def te_breakdown(te_result: dict, title: str = "总误差分量分解") -> str:
    """
    总误差分量分解图 — 显示偏倚(bias)和随机误差(t_crit x SD)的堆叠柱状图。

    Parameters
    ----------
    te_result : dict — calc_te_from_values() 的返回值
    title : str

    Returns
    -------
    str — HTML 片段
    """
    bias_abs = te_result.get("bias_abs", 0)
    random_err = te_result.get("random_error", 0)
    te_val = te_result.get("te", 0)

    chart_id = _make_id("te")

    return f"""
    <div class="report-section">
        <h2>{title}</h2>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">偏倚 |bias|</div>
                <div class="metric-value">{_fmt(bias_abs)}</div>
            </div>
            <div class="metric-card" style="background:#E6F1FB;">
                <div class="metric-label">随机误差 t x SD</div>
                <div class="metric-value">{_fmt(random_err)}</div>
            </div>
            <div class="metric-card" style="background:#FAEEDA;">
                <div class="metric-label">总误差 TE</div>
                <div class="metric-value" style="color:#BA7517;">{_fmt(te_val)}</div>
            </div>
        </div>
        <div class="chart-box">
            <canvas id="{chart_id}"></canvas>
        </div>
        <script>
        (function() {{
            var ctx = document.getElementById('{chart_id}').getContext('2d');
            new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: ['总误差 TE'],
                    datasets: [
                        {{
                            label: '偏倚 (bias)',
                            data: [{bias_abs}],
                            backgroundColor: '#D85A30'
                        }},
                        {{
                            label: '随机误差 (t × SD)',
                            data: [{random_err}],
                            backgroundColor: '#378ADD'
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    scales: {{
                        x: {{ stacked: true }},
                        y: {{ stacked: true, beginAtZero: true,
                              title: {{ display: true, text: '值' }} }}
                    }}
                }}
            }});
        }})();
        </script>
    </div>"""


def te_judgment_section(judgment: dict, te_result: dict = None) -> str:
    """
    总误差判定结果卡片 + 详细指标。

    Parameters
    ----------
    judgment : dict — calc_te_judgment() 的返回值
    te_result : dict, optional — calc_te_from_values() 的返回值

    Returns
    -------
    str
    """
    level = judgment.get("level", "")
    te_rel = judgment.get("te_relative", 0)
    tea = judgment.get("te_allowable", 0)
    ratio = judgment.get("ratio", 0)

    status_map = {
        "excellent": "success",
        "good": "success",
        "acceptable": "info",
        "unacceptable": "danger",
    }
    label_map = {
        "excellent": "优秀 (≤ 1/3 TEa)",
        "good": "良好 (≤ 2/3 TEa)",
        "acceptable": "可接受 (≤ TEa)",
        "unacceptable": "不可接受 (> TEa)",
    }

    parts = [judgment_card(level, label_map.get(level, level),
                           f"TE%={te_rel:.2f}%, TEa%={tea:.2f}%, ratio={ratio:.2f}",
                           status=status_map.get(level, "info"))]

    if te_result:
        parts.append(data_table(te_result, "总误差分量",
                                ["te", "te_relative", "bias", "bias_abs",
                                 "mean", "sd", "random_error", "t_crit", "reference"]))

    return "\n".join(parts)


def measurement_uncertainty_section(
        u_combined: float, u_expanded: float, components: list,
        k: float = 2.0, title: str = "测量不确定度报告") -> str:
    """
    测量不确定度报告可视化。
    """
    chart_id = _make_id("mu")

    comp_labels = json.dumps([c.get("name", f"u{i+1}") for i, c in enumerate(components)])
    comp_values = json.dumps([c.get("value", 0) for c in components])
    comp_colors = json.dumps(["#378ADD", "#1D9E75", "#BA7517",
                               "#7F77DD", "#D4537E"][:len(components)])

    return f"""
    <div class="report-section">
        <h2>{title}</h2>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">合成不确定度 uc</div>
                <div class="metric-value">{_fmt(u_combined)}</div>
            </div>
            <div class="metric-card" style="background:#E6F1FB;">
                <div class="metric-label">扩展不确定度 U (k={k})</div>
                <div class="metric-value">{_fmt(u_expanded)}</div>
            </div>
            <div class="metric-card" style="background:#F1EFE8;">
                <div class="metric-label">包含因子 k</div>
                <div class="metric-value">{k}</div>
            </div>
        </div>
        <div class="chart-box">
            <canvas id="{chart_id}"></canvas>
        </div>
        <script>
        (function() {{
            var ctx = document.getElementById('{chart_id}').getContext('2d');
            new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: {comp_labels},
                    datasets: [{{
                        label: '标准不确定度分量',
                        data: {comp_values},
                        backgroundColor: {comp_colors},
                        borderRadius: 4
                    }}]
                }},
                options: {{
                    responsive: true,
                    scales: {{
                        y: {{ beginAtZero: true, title: {{ display: true, text: '不确定度' }} }}
                    }}
                }}
            }});
        }})();
        </script>
    </div>"""


# ═══════════════════════════════════════════════════════
# 室内质控专用
# ═══════════════════════════════════════════════════════

def precision_summary(per_level: list, synthetic_std: float,
                      synthetic_rsd: float, overall_mean: float) -> str:
    """
    精密度分析摘要 — 各水平统计表 + 合成结果卡片。

    Parameters
    ----------
    per_level : list[dict] — 每水平 {"level", "mean", "sd", "rsd", "n"}
    synthetic_std : float — 合成标准差
    synthetic_rsd : float — 合成 RSD%
    overall_mean : float — 总均值

    Returns
    -------
    str — HTML 片段
    """
    # 合成卡片
    cards = f"""
    <div class="metric-grid">
        <div class="metric-card"><div class="metric-label">总均值</div><div class="metric-value">{_fmt(overall_mean)}</div></div>
        <div class="metric-card"><div class="metric-label">合成标准差</div><div class="metric-value">{_fmt(synthetic_std)}</div></div>
        <div class="metric-card" style="background:#E6F1FB;"><div class="metric-label">合成 RSD%</div><div class="metric-value">{_fmt(synthetic_rsd, 2)}%</div></div>
    </div>"""

    # 各水平表格
    rows = ""
    for p in per_level:
        rows += f"<tr><td>{p.get('level', '')}</td><td>{_fmt(p.get('mean', 0))}</td><td>{_fmt(p.get('sd', 0))}</td><td>{_fmt(p.get('rsd', 0), 2)}%</td><td>{p.get('n', 0)}</td></tr>\n"

    table = f"""
    <table class="data-table">
        <thead><tr><th>水平</th><th>均值</th><th>SD</th><th>RSD%</th><th>n</th></tr></thead>
        <tbody>{rows}</tbody>
    </table>"""

    return f"""
    <div class="report-section"><h2>精密度分析结果</h2>{cards}{table}</div>"""


def control_chart_section(chart_stats: dict, title: str = "质控图统计") -> str:
    """
    质控图统计卡片组。

    Parameters
    ----------
    chart_stats : dict — {"mean": float, "sd": float, "ucl": float, "lcl": float, ...}
    title : str

    Returns
    -------
    str
    """
    mean = chart_stats.get("mean", 0)
    sd = chart_stats.get("sd", 0)
    ucl = chart_stats.get("ucl", mean + 3 * sd)
    lcl = chart_stats.get("lcl", mean - 3 * sd)

    return f"""
    <div class="report-section">
        <h2>{title}</h2>
        <div class="metric-grid">
            <div class="metric-card"><div class="metric-label">中心线 (CL)</div><div class="metric-value">{_fmt(mean)}</div></div>
            <div class="metric-card" style="background:#E6F1FB;"><div class="metric-label">标准差 (SD)</div><div class="metric-value">{_fmt(sd)}</div></div>
            <div class="metric-card" style="background:#FAECE7;"><div class="metric-label">上控制限 (UCL)</div><div class="metric-value">{_fmt(ucl)}</div></div>
            <div class="metric-card" style="background:#FCEBEB;"><div class="metric-label">下控制限 (LCL)</div><div class="metric-value">{_fmt(lcl)}</div></div>
        </div>
    </div>"""


# ═══════════════════════════════════════════════════════
# 室间比对 / ANOVA 专用
# ═══════════════════════════════════════════════════════

def anova_summary(anova_result: dict, title: str = "ANOVA 方差分析结果") -> str:
    """
    ANOVA 结果可视化 — F检验判定 + ANOVA 表。

    Parameters
    ----------
    anova_result : dict — interlab_comparison() 的返回值
    title : str

    Returns
    -------
    str
    """
    f_val = anova_result.get("f_value", 0)
    f_crit = anova_result.get("f_critical", 0)
    sig = anova_result.get("significant", False)
    conclusion = anova_result.get("conclusion", "")

    status = "success" if sig else "danger"
    label = "各组均值存在显著差异" if sig else "各组均值无显著差异"

    cards = f"""
    <div class="metric-grid">
        <div class="metric-card"><div class="metric-label">F 值</div><div class="metric-value">{_fmt(f_val, 4)}</div></div>
        <div class="metric-card"><div class="metric-label">F 临界值</div><div class="metric-value">{_fmt(f_crit, 4)}</div></div>
        <div class="metric-card" style="background:{'#EAF3DE' if sig else '#FCEBEB'};">
            <div class="metric-label">判定</div>
            <div class="metric-value" style="color:{'#27500A' if sig else '#791F1F'};font-size:16px;">{'✓ 显著' if sig else '✗ 不显著'}</div>
        </div>
    </div>
    <p style="margin-top:8px;color:#5F5E5A;font-size:13px;">{conclusion}</p>"""

    return f"""
    <div class="report-section"><h2>{title}</h2>{cards}</div>"""


def group_means_chart(group_means: dict, title: str = "各组均值对比") -> str:
    """
    各组均值柱状图（Chart.js）。

    Parameters
    ----------
    group_means : dict — {"组A": 50.2, "组B": 53.1, ...}
    title : str

    Returns
    -------
    str
    """
    labels = list(group_means.keys())
    values = list(group_means.values())
    return bar_chart(labels, values, title=title, ylabel="均值")


# ═══════════════════════════════════════════════════════
# 方法验证专用
# ═══════════════════════════════════════════════════════

def calibration_summary(curve_result: dict, title: str = "校准曲线参数") -> str:
    """
    校准曲线参数卡片 + 回归统计。

    Parameters
    ----------
    curve_result : dict — calibration_curve() 的返回值
    title : str

    Returns
    -------
    str
    """
    return f"""
    <div class="report-section">
        <h2>{title}</h2>
        <div class="metric-grid">
            <div class="metric-card"><div class="metric-label">斜率 (slope)</div><div class="metric-value">{_fmt(curve_result.get('slope', 0), 6)}</div></div>
            <div class="metric-card"><div class="metric-label">截距 (intercept)</div><div class="metric-value">{_fmt(curve_result.get('intercept', 0), 6)}</div></div>
            <div class="metric-card" style="background:#E6F1FB;"><div class="metric-label">R²</div><div class="metric-value">{_fmt(curve_result.get('r2', 0), 4)}</div></div>
            <div class="metric-card" style="background:#F1EFE8;"><div class="metric-label">Sy/x</div><div class="metric-value">{_fmt(curve_result.get('syx', 0), 4)}</div></div>
        </div>
        <p style="margin-top:8px;font-size:13px;color:#5F5E5A;">方程: {curve_result.get('equation', '')}</p>
    </div>"""


def lod_loq_card(lod_loq_result: dict, title: str = "检出限 / 定量限") -> str:
    """
    LOD/LOQ 结果卡片。

    Parameters
    ----------
    lod_loq_result : dict — calc_lod_loq() 的返回值
    title : str

    Returns
    -------
    str
    """
    return f"""
    <div class="report-section">
        <h2>{title}</h2>
        <div class="metric-grid">
            <div class="metric-card" style="background:#FAEEDA;"><div class="metric-label">检出限 LOD</div><div class="metric-value" style="color:#BA7517;">{_fmt(lod_loq_result.get('lod', 0), 4)}</div></div>
            <div class="metric-card" style="background:#E6F1FB;"><div class="metric-label">定量限 LOQ</div><div class="metric-value">{_fmt(lod_loq_result.get('loq', 0), 4)}</div></div>
            <div class="metric-card"><div class="metric-label">方法</div><div class="metric-value" style="font-size:16px;">{lod_loq_result.get('method', '')}</div></div>
        </div>
        <p style="margin-top:8px;font-size:13px;color:#5F5E5A;">{lod_loq_result.get('lod_expression', '')}</p>
        <p style="font-size:13px;color:#5F5E5A;">{lod_loq_result.get('loq_expression', '')}</p>
    </div>"""


def uncertainty_curve_card(uncertainty_result: dict, title: str = "曲线不确定度") -> str:
    """
    曲线不确定度结果卡片。

    Parameters
    ----------
    uncertainty_result : dict — curve_uncertainty() 的返回值
    title : str

    Returns
    -------
    str
    """
    return f"""
    <div class="report-section">
        <h2>{title}</h2>
        <div class="metric-grid">
            <div class="metric-card"><div class="metric-label">样品浓度</div><div class="metric-value">{_fmt(uncertainty_result.get('sample_concentration', 0), 4)}</div></div>
            <div class="metric-card" style="background:#FAEEDA;"><div class="metric-label">相对不确定度</div><div class="metric-value" style="color:#BA7517;">{_fmt(uncertainty_result.get('relative_uncertainty', 0) * 100, 2)}%</div></div>
            <div class="metric-card" style="background:#E6F1FB;"><div class="metric-label">合成不确定度</div><div class="metric-value">{_fmt(uncertainty_result.get('combined_uncertainty', 0), 4)}</div></div>
        </div>
    </div>"""


# ═══════════════════════════════════════════════════════
# 趋势监控专用
# ═══════════════════════════════════════════════════════

def trend_summary_card(stats_summary: dict, title: str = "趋势监控摘要") -> str:
    """
    趋势监控摘要卡片。

    Parameters
    ----------
    stats_summary : dict — monitoring_dashboard() 返回的 stats_summary
    title : str

    Returns
    -------
    str
    """
    alert = stats_summary.get("超出警戒", False)
    alert_color = "#D85A30" if alert else "#1D9E75"
    alert_text = "⚠ 超出警戒" if alert else "✓ 正常"

    return f"""
    <div class="report-section">
        <h2>{title}</h2>
        <div class="metric-grid">
            <div class="metric-card"><div class="metric-label">总记录数</div><div class="metric-value">{stats_summary.get('总记录数', 0)}</div></div>
            <div class="metric-card"><div class="metric-label">时间跨度</div><div class="metric-value" style="font-size:14px;">{stats_summary.get('时间跨度', '')}</div></div>
            <div class="metric-card"><div class="metric-label">总均值</div><div class="metric-value">{_fmt(stats_summary.get('总均值', 0))}</div></div>
            <div class="metric-card"><div class="metric-label">总标准差</div><div class="metric-value">{_fmt(stats_summary.get('总标准差', 0))}</div></div>
            <div class="metric-card" style="background:{'#FAECE7' if alert else '#EAF3DE'};">
                <div class="metric-label">警戒状态</div>
                <div class="metric-value" style="font-size:16px;color:{alert_color};">{alert_text}</div>
            </div>
            <div class="metric-card"><div class="metric-label">当前值</div><div class="metric-value">{_fmt(stats_summary.get('当前值', 0))}</div></div>
        </div>
    </div>"""


def alert_section(alerts: list, title: str = "预警信息") -> str:
    """
    预警信息列表。

    Parameters
    ----------
    alerts : list[dict] — [{"组别": str, "增长率": str, "预警": str}, ...]
    title : str

    Returns
    -------
    str
    """
    if not alerts:
        return f"""
        <div class="report-section">
            <h2>{title}</h2>
            <div class="judgment-card" style="background:#EAF3DE;border-left:4px solid #639922;">
                <div class="judgment-icon" style="color:#639922;">✓</div>
                <div class="judgment-level" style="color:#27500A;">无预警，趋势正常</div>
            </div>
        </div>"""

    rows = ""
    for a in alerts:
        rows += f"<tr><td>{a.get('组别', '')}</td><td>{a.get('增长率', '')}</td><td style='color:#D85A30;'>⚠ {a.get('预警', '')}</td></tr>\n"

    return f"""
    <div class="report-section">
        <h2>{title}</h2>
        <table class="data-table">
            <thead><tr><th>组别</th><th>增长率</th><th>预警</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>"""


# ═══════════════════════════════════════════════════════
# Z表 / P表 专用
# ═══════════════════════════════════════════════════════

def z_table_section(z_result: dict, title: str = "Z 值显著性分析") -> str:
    """
    Z 值 → p 值可视化卡片。

    Parameters
    ----------
    z_result : dict — calc_z_to_p_two_tailed(), calc_p_from_t(), calc_p_from_f() 返回值
    title : str

    Returns
    -------
    str
    """
    p_val = z_result.get("p_value", z_result.get("p_two_tailed", 0))
    z_val = z_result.get("z_statistic", z_result.get("t_statistic", z_result.get("f_statistic", 0)))
    sig_005 = z_result.get("significant_005", p_val < 0.05)
    sig_001 = z_result.get("significant_001", p_val < 0.01)
    summary = z_result.get("summary", "")

    if sig_001:
        status, label = "danger", "高度显著 (p < 0.01) ***"
    elif sig_005:
        status, label = "warning", "显著 (p < 0.05) **"
    else:
        status, label = "success", "不显著 (p ≥ 0.05)"

    return f"""
    <div class="report-section">
        <h2>{title}</h2>
        <div class="metric-grid">
            <div class="metric-card"><div class="metric-label">统计量</div><div class="metric-value" style="font-size:18px;">{_fmt(z_val, 4)}</div></div>
            <div class="metric-card" style="background:{'#FCEBEB' if sig_005 else '#EAF3DE'};">
                <div class="metric-label">p 值</div><div class="metric-value" style="font-size:18px;">{_fmt(p_val, 4)}</div>
            </div>
            <div class="metric-card" style="background:{'#FAECE7' if sig_001 else '#EAF3DE'};">
                <div class="metric-label">显著性</div><div class="metric-value" style="font-size:14px;color:{'#791F1F' if sig_005 else '#27500A'};">{label}</div>
            </div>
        </div>
        <p style="margin-top:8px;color:#5F5E5A;font-size:13px;">{summary}</p>
    </div>"""


__all__ = [
    "data_table",
    "bar_chart", "pie_chart",
    "te_breakdown", "te_judgment_section",
    "measurement_uncertainty_section",
    "precision_summary", "control_chart_section",
    "anova_summary", "group_means_chart",
    "calibration_summary", "lod_loq_card", "uncertainty_curve_card",
    "trend_summary_card", "alert_section",
    "z_table_section",
]
