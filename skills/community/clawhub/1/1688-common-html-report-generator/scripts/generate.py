#!/usr/bin/env python3
"""
data-report-visualizer 自动化生成器
用法：编写一个数据描述脚本调用 ReportBuilder，执行后自动生成可视化HTML。

示例：
    from generate import ReportBuilder
    r = ReportBuilder("报告标题")
    r.header("大标题", "副标题", ["时间:2026-05-14", "来源:XX"])
    r.nav([("核心指标","#kpi"), ("平台对比","#platform")])
    with r.section("kpi", "01", "核心指标", "描述..."):
        r.kpi("销量", "4.23", "亿件", "占21.1%")
    r.render("output.html")
"""

import json
import os
import re
from pathlib import Path


def _to_js(val):
    """将Python值转为JS字面量"""
    if val is None:
        return "null"
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, (int, float)):
        return str(val)
    if isinstance(val, str):
        return json.dumps(val, ensure_ascii=False)
    if isinstance(val, (list, tuple)):
        return "[" + ", ".join(_to_js(v) for v in val) + "]"
    if isinstance(val, dict):
        items = []
        for k, v in val.items():
            key = k if re.match(r"^[A-Za-z_$][A-Za-z0-9_$]*$", k) else json.dumps(k)
            items.append(f"{key}: {_to_js(v)}")
        return "{" + ", ".join(items) + "}"
    return str(val)


class _Section:
    """章节上下文"""
    def __init__(self, builder, sid, num, title, desc):
        self.builder = builder
        self.sid = sid
        self.num = num
        self.title = title
        self.desc = desc

    def __enter__(self):
        parts = [f'<div class="section" id="{self.sid}">']
        parts.append(f'<div class="section-title"><span class="num">{self.num}</span>{self.title}</div>')
        parts.append(f'<div class="section-desc">{self.desc}</div>')
        self.builder._sections_html.append("\n".join(parts))
        self.builder._in_section = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.builder._sections_html.append("</div>")
        self.builder._in_section = False


class ReportBuilder:
    """报告构建器"""

    # 预定义颜色
    C_DOUYIN = "#f76c8b"
    C_TAOBAO = "#6c7af7"
    C_XIAOHONGSHU = "#6cf7c2"
    C_ORANGE = "#f7c96c"
    C_PURPLE = "#c96cf7"
    COLORS = [C_DOUYIN, C_TAOBAO, C_XIAOHONGSHU, C_ORANGE, C_PURPLE]

    def __init__(self, title: str):
        self.title = title
        self._header_title = title
        self._header_sub = "数据可视化分析报告"
        self._header_meta = []
        self._nav = []
        self._sections_html = []
        self._charts = []
        self._footer = ""
        self._in_section = False

    # ---------- 页面级配置 ----------

    def header(self, title: str, subtitle: str = "", meta: list = None):
        self._header_title = title
        self._header_sub = subtitle
        self._header_meta = meta or []
        return self

    def nav(self, links: list):
        """links: [(label, href), ...]"""
        self._nav = links
        return self

    def footer(self, text: str):
        self._footer = text
        return self

    # ---------- 章节 ----------

    def section(self, sid: str, num: str, title: str, desc: str = ""):
        return _Section(self, sid, num, title, desc)

    def _ensure_section(self):
        if not self._in_section:
            raise RuntimeError("必须在 section 上下文中添加内容")

    def _add_html(self, html: str):
        self._ensure_section()
        self._sections_html.append(html)

    # ---------- KPI ----------

    def kpi_grid(self):
        self._add_html('<div class="kpi-grid">')
        return self

    def kpi_end(self):
        self._add_html('</div>')
        return self

    def kpi(self, label: str, value: str, unit: str = "", change: str = "", down: bool = False):
        grad = "linear-gradient(135deg,#f76c8b,#be185d)" if down else "linear-gradient(135deg,#6c7af7,#8b5cf6)"
        cls = "kpi-change down" if down else "kpi-change"
        change_html = f'<div class="{cls}">{change}</div>' if change else ""
        html = (
            f'<div class="kpi-card" style="--grad:{grad}">'
            f'<div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}<span class="kpi-unit">{unit}</span></div>'
            f'{change_html}'
            f'</div>'
        )
        self._add_html(html)
        return self

    # ---------- 布局 ----------

    def grid(self, cols: int = 2):
        self._add_html(f'<div class="grid-{cols}">')
        return self

    def grid_end(self):
        self._add_html('</div>')
        return self

    # ---------- 卡片与图表 ----------

    def card(self, title: str = "", dot_color: str = None):
        dot = f'<span class="dot" style="background:{dot_color or self.C_TAOBAO}"></span>' if dot_color != "" else ""
        t = f'<div class="card-title">{dot}{title}</div>' if title else ""
        self._add_html(f'<div class="card">{t}')
        return self

    def card_end(self):
        self._add_html('</div>')
        return self

    def chart(self, cid: str, size: str = "normal"):
        cls = "chart chart-lg" if size == "lg" else "chart"
        self._add_html(f'<div id="{cid}" class="{cls}"></div>')
        return self

    def raw_html(self, html: str):
        self._add_html(html)
        return self

    # ---------- 数据表格 ----------

    def table(self, headers: list, rows: list):
        ths = "".join(f"<th>{h}</th>" for h in headers)
        trs = ""
        for row in rows:
            tds = "".join(f"<td>{cell}</td>" for cell in row)
            trs += f"<tr>{tds}</tr>"
        html = f'<table class="data-table"><thead><tr>{ths}</tr></thead><tbody>{trs}</tbody></table>'
        self._add_html(html)
        return self

    # ---------- 进度条组件 ----------

    def progress_group(self):
        """开始一组进度条"""
        self._add_html('<div class="progress-group">')
        return self

    def progress_group_end(self):
        self._add_html('</div>')
        return self

    def progress_bar(self, label: str, value: float, max_val: float = 100,
                     color: str = None, suffix: str = ""):
        """
        渐变进度条。
        label: 左侧标签
        value: 当前值
        max_val: 最大值（用于计算宽度百分比）
        color: 渐变起始色，自动生成终止色；或传 [color1, color2] 自定义渐变
        suffix: 右侧补充文字（如"高退货""严重"等）
        """
        pct = min(value / max_val * 100, 100) if max_val > 0 else 0
        if isinstance(color, (list, tuple)) and len(color) >= 2:
            grad = f"linear-gradient(90deg,{color[0]},{color[1]})"
        elif color:
            grad = f"linear-gradient(90deg,{color},{self._darken(color)})"
        else:
            grad = f"linear-gradient(90deg,{self.C_DOUYIN},{self._darken(self.C_DOUYIN)})"
        suffix_html = f'<div class="progress-suffix">{suffix}</div>' if suffix else ""
        html = (
            f'<div class="progress-item">'
            f'<div class="progress-label">{label}</div>'
            f'<div class="progress-track">'
            f'<div class="progress-fill" style="width:{pct:.1f}%;background:{grad}">{value}%</div>'
            f'</div>'
            f'{suffix_html}'
            f'</div>'
        )
        self._add_html(html)
        return self

    @staticmethod
    def _darken(hex_color: str) -> str:
        """将十六进制颜色加深，用于渐变终止色"""
        hex_color = hex_color.lstrip("#")
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        factor = 0.6
        r, g, b = int(r * factor), int(g * factor), int(b * factor)
        return f"#{r:02x}{g:02x}{b:02x}"

    # ---------- 数字卡片网格 ----------

    def metric_grid(self):
        """开始数字卡片网格"""
        self._add_html('<div class="metric-grid">')
        return self

    def metric_end(self):
        self._add_html('</div>')
        return self

    def metric(self, value: str, unit: str = "", desc: str = "", color: str = None):
        """
        单个数字卡片。
        value: 核心数字
        unit: 单位（如 %、亿元）
        desc: 下方说明文字
        color: 数字颜色，同时用于背景透明色
        """
        c = color or self.C_TAOBAO
        # 从hex提取rgb用于背景透明色
        hex_c = c.lstrip("#")
        r, g, b = int(hex_c[0:2], 16), int(hex_c[2:4], 16), int(hex_c[4:6], 16)
        bg = f"rgba({r},{g},{b},0.06)"
        unit_html = f'<span class="metric-unit">{unit}</span>' if unit else ""
        html = (
            f'<div class="metric-card" style="background:{bg}">'
            f'<div class="metric-value" style="color:{c}">{value}{unit_html}</div>'
            f'<div class="metric-desc">{desc}</div>'
            f'</div>'
        )
        self._add_html(html)
        return self

    # ---------- 洞察框 ----------

    def insight(self, title: str, bullets: list):
        lis = "".join(f"<li>{b}</li>" for b in bullets)
        html = f'<div class="insight-box"><h4>{title}</h4><ul>{lis}</ul></div>'
        self._add_html(html)
        return self

    # ---------- 图表脚本 ----------

    def chart_script(self, cid: str, option: dict):
        """注册一个ECharts图表配置（Python dict → JS object）"""
        js_opt = _to_js(option)
        code = (
            f'const {cid} = echarts.init(document.getElementById("{cid}"));\n'
            f'{cid}.setOption({js_opt});'
        )
        self._charts.append(code)
        return self

    def chart_bar(self, cid: str, categories: list, series: list, yname: str = "",
                  legend: list = None, dual_y: bool = False, size: str = "normal",
                  show_label: bool = False):
        """
        柱状图/条形图（支持双Y轴组合图）。

        series 中每个元素支持的字段：
          name, data, color, type("bar"/"line"), yAxisIndex,
          barWidth, symbolSize, lineWidth,
          gradient: [color1, color2] 渐变色（仅 bar 类型有效）
        show_label: 是否在柱子顶部显示数值标签
        """
        opt = {
            **self._common(),
            "xAxis": {"type": "category", "data": categories,
                      "axisLine": {"lineStyle": {"color": "rgba(255,255,255,0.05)"}},
                      "axisLabel": {"color": "#8b92a8", "rotate": 25 if len(categories) > 6 else 0, "fontSize": 10}},
            "yAxis": {"type": "value", "name": yname,
                      "axisLine": {"show": False}, "splitLine": {"lineStyle": {"color": "rgba(255,255,255,0.05)"}},
                      "axisLabel": {"color": "#8b92a8"}},
            "series": []
        }
        if dual_y:
            opt["yAxis"] = [
                {"type": "value", "name": yname, "axisLine": {"show": False},
                 "splitLine": {"lineStyle": {"color": "rgba(255,255,255,0.05)"}}, "axisLabel": {"color": "#8b92a8"}},
                {"type": "value", "axisLine": {"show": False}, "splitLine": {"show": False}, "axisLabel": {"color": "#8b92a8"}}
            ]
        for i, s in enumerate(series):
            item = {
                "name": s["name"],
                "type": s.get("type", "bar"),
                "data": s["data"],
                "itemStyle": {"borderRadius": [4, 4, 0, 0]},
                "barWidth": s.get("barWidth", 18)
            }
            # 渐变色支持：gradient: [topColor, bottomColor]
            if "gradient" in s and s.get("type", "bar") == "bar":
                g = s["gradient"]
                item["itemStyle"]["color"] = {
                    "type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                    "colorStops": [
                        {"offset": 0, "color": g[0]},
                        {"offset": 1, "color": g[1]}
                    ]
                }
            elif "color" in s:
                item["itemStyle"]["color"] = s["color"]
            if "yAxisIndex" in s:
                item["yAxisIndex"] = s["yAxisIndex"]
            if s.get("type") == "line":
                item["symbol"] = "circle"
                item["symbolSize"] = s.get("symbolSize", 5)
                item["lineStyle"] = {"width": s.get("lineWidth", 2)}
                if "color" in s:
                    item["itemStyle"] = {"color": s["color"]}
                del item["barWidth"]
            # 数据标签
            if show_label:
                item["label"] = {"show": True, "position": "top", "color": "#8b92a8", "fontSize": 10}
            opt["series"].append(item)
        if legend:
            opt["legend"] = {"data": legend, "textStyle": {"color": "#8b92a8"}, "bottom": 0}
        return self.chart_script(cid, opt)

    def chart_pie(self, cid: str, data: list, inner_radius: str = "45%", outer_radius: str = "70%"):
        """data: [{"value":78.6,"name":"直播","color":"#f76c8b"}, ...]"""
        opt = {
            **self._common(),
            "tooltip": {"trigger": "item", "backgroundColor": "rgba(24,27,34,0.95)", "borderColor": "#232733", "textStyle": {"color": "#e0e3eb"}, "padding": 12, "borderRadius": 8, "formatter": "{b}：{d}%"},
            "legend": {"orient": "vertical", "right": 10, "top": "center", "textStyle": {"color": "#8b92a8"}},
            "series": [{
                "type": "pie",
                "radius": [inner_radius, outer_radius],
                "center": ["40%", "50%"],
                "avoidLabelOverlap": True,
                "itemStyle": {"borderRadius": 8, "borderColor": "#181b22", "borderWidth": 2},
                "label": {"show": False},
                "emphasis": {"label": {"show": False}},
                "data": [{"value": d["value"], "name": d["name"], "itemStyle": {"color": d.get("color", self.COLORS[i % len(self.COLORS)])}} for i, d in enumerate(data)]
            }]
        }
        return self.chart_script(cid, opt)

    def chart_radar(self, cid: str, indicators: list, data: list):
        """
        indicators: [{"name":"维度A","max":100}, ...]
        data: [{"name":"系列A","value":[80,90,...],"color":"#6c7af7"}, ...]
        """
        opt = {
            **self._common(),
            "legend": {"data": [d["name"] for d in data], "textStyle": {"color": "#8b92a8"}, "bottom": 0},
            "radar": {
                "indicator": indicators,
                "shape": "polygon",
                "splitNumber": 4,
                "axisName": {"color": "#8b92a8", "fontSize": 12},
                "splitLine": {"lineStyle": {"color": "rgba(255,255,255,0.05)"}},
                "splitArea": {"areaStyle": {"color": ["rgba(108,122,247,0.02)", "rgba(108,122,247,0.05)"]}},
                "axisLine": {"lineStyle": {"color": "rgba(255,255,255,0.05)"}}
            },
            "series": [{
                "type": "radar",
                "data": [{
                    "value": d["value"],
                    "name": d["name"],
                    "areaStyle": {"color": d.get("areaColor", f"rgba({d['color']},0.2)")},
                    "lineStyle": {"color": d["color"], "width": 2},
                    "itemStyle": {"color": d["color"]}
                } for d in data]
            }]
        }
        return self.chart_script(cid, opt)

    def chart_heatmap(self, cid: str, x_labels: list, y_labels: list, data: list):
        """data: [[x_index, y_index, value], ...]"""
        # 根据 x 轴标签数量和文字长度自适应布局参数
        max_x_len = max((len(str(l)) for l in x_labels), default=2)
        num_x = len(x_labels)
        rotate = 45 if num_x > 6 or max_x_len > 4 else 30
        bottom = 130 if rotate == 45 else 80
        # y 轴标签越长，左边距越大
        max_y_len = max((len(str(l)) for l in y_labels), default=2)
        left = max(100, max_y_len * 13)
        # 不使用 _common() 避免其 tooltip(trigger:"axis") 覆盖自定义 formatter
        y_labels_js = _to_js(y_labels)
        opt_body = {
            "textStyle": {"fontFamily": "PingFang SC, Microsoft YaHei, sans-serif"},
            "legend": {"show": False},
            "grid": {"left": left, "right": 30, "top": 10, "bottom": bottom},
            "xAxis": {"type": "category", "data": x_labels,
                      "axisLine": {"lineStyle": {"color": "rgba(255,255,255,0.05)"}},
                      "axisLabel": {"color": "#8b92a8", "rotate": rotate, "fontSize": 10, "interval": 0}},
            "yAxis": {"type": "category", "data": y_labels,
                      "axisLine": {"lineStyle": {"color": "rgba(255,255,255,0.05)"}},
                      "axisLabel": {"color": "#8b92a8", "fontSize": 11}},
            "visualMap": {
                "min": min(d[2] for d in data), "max": max(d[2] for d in data),
                "calculable": True, "orient": "horizontal", "left": "center", "bottom": 0,
                "inRange": {"color": ["#1e1b4b", "#312e81", "#4c1d95", "#7c3aed", "#a855f7", "#c084fc", "#d8b4fe"]},
                "textStyle": {"color": "#8b92a8"}
            },
            "series": [{
                "name": "热度", "type": "heatmap", "data": data,
                "label": {"show": True, "color": "#fff", "fontSize": 12, "fontWeight": "bold"},
                "itemStyle": {"borderColor": "#1a1a2e", "borderWidth": 2},
                "emphasis": {"itemStyle": {"shadowBlur": 10, "shadowColor": "rgba(0,0,0,0.5)"}}
            }]
        }
        js_body = _to_js(opt_body)
        # 在 { 后插入含 JS function 的 tooltip（_to_js 无法序列化 JS 函数）
        tooltip_js = (
            f'tooltip: {{trigger: "item", backgroundColor: "rgba(24,27,34,0.95)", '
            f'borderColor: "#232733", textStyle: {{color: "#e0e3eb"}}, padding: 12, borderRadius: 8, '
            f'formatter: function(p){{var yl={y_labels_js};'
            f'return "<b>"+p.name+"</b><br/>"+yl[p.data[1]]+": <b>"+p.data[2]+"</b>";}}}}, '
        )
        js_opt = "{" + tooltip_js + js_body[1:]
        code = (
            f'const {cid} = echarts.init(document.getElementById("{cid}"));\n'
            f'{cid}.setOption({js_opt});'
        )
        self._charts.append(code)
    def chart_stacked_bar(self, cid: str, categories: list, series: list):
        """series: [{"name":"系列A","data":[1,2,3],"color":"#6c7af7"}, ...]"""
        opt = {
            **self._common(),
            "legend": {"data": [s["name"] for s in series], "textStyle": {"color": "#8b92a8"}, "bottom": 0},
            "xAxis": {"type": "category", "data": categories,
                      "axisLine": {"lineStyle": {"color": "rgba(255,255,255,0.05)"}},
                      "axisLabel": {"color": "#8b92a8"}},
            "yAxis": {"type": "value", "name": "占比%",
                      "axisLine": {"show": False}, "splitLine": {"lineStyle": {"color": "rgba(255,255,255,0.05)"}},
                      "axisLabel": {"color": "#8b92a8"}},
            "series": [{
                "name": s["name"], "type": "bar", "stack": "total", "data": s["data"],
                "itemStyle": {"color": s.get("color", self.COLORS[i % len(self.COLORS)])},
                "barWidth": 40
            } for i, s in enumerate(series)]
        }
        return self.chart_script(cid, opt)

    # ---------- 内部辅助 ----------

    def _common(self):
        return {
            "textStyle": {"fontFamily": "PingFang SC, Microsoft YaHei, sans-serif"},
            "tooltip": {
                "trigger": "axis",
                "backgroundColor": "rgba(24,27,34,0.95)", "borderColor": "#232733",
                "textStyle": {"color": "#e0e3eb"}, "padding": 12, "borderRadius": 8,
                "axisPointer": {"type": "shadow", "shadowStyle": {"color": "rgba(108,122,247,0.08)"}}
            },
            "legend": {"textStyle": {"color": "#8b92a8"}, "bottom": 0},
            "grid": {"left": 60, "right": 30, "top": 40, "bottom": 50, "containLabel": True}
        }

    # ---------- 渲染 ----------

    def render(self, out_path: str):
        skill_dir = Path(__file__).parent
        tmpl_path = skill_dir / "template.html"
        tmpl = tmpl_path.read_text(encoding="utf-8")

        # 构建导航HTML
        nav_links = []
        for i, (label, href) in enumerate(self._nav):
            cls = ' class="active"' if i == 0 else ""
            nav_links.append(f'<a href="{href}"{cls}>{label}</a>')
        nav_html = "".join(nav_links)

        # 构建header meta
        meta_html = "".join(f'<span>{m}</span>' for m in self._header_meta)

        # 构建sections
        sections_html = "\n".join(self._sections_html)

        # 构建chart scripts
        charts_js = "\n".join(self._charts)
        chart_vars = [line.split("=")[0].strip().replace("const ", "") for line in self._charts if line.startswith("const ")]
        instances_str = ", ".join(chart_vars)

        # 替换占位符
        tmpl = tmpl.replace("{{TITLE}}", self.title)
        tmpl = tmpl.replace("{{HEADER_TITLE}}", self._header_title)
        tmpl = tmpl.replace("{{HEADER_SUBTITLE}}", self._header_sub)
        tmpl = tmpl.replace("{{HEADER_META}}", meta_html)
        tmpl = tmpl.replace("{{NAV_LINKS}}", nav_html)
        tmpl = tmpl.replace("{{SECTIONS}}", sections_html)
        tmpl = tmpl.replace("{{FOOTER}}", self._footer)
        tmpl = tmpl.replace("{{CHART_SCRIPTS}}", charts_js)
        tmpl = tmpl.replace("__CHART_INSTANCES__", f"[{instances_str}]")

        Path(out_path).write_text(tmpl, encoding="utf-8")
        print(f"[OK] 报告已生成: {out_path}")
        return out_path


# ---------- 便捷入口 ----------

def build(out_path: str, title: str, config_fn):
    """
    便捷入口。config_fn 接收一个 ReportBuilder 实例进行配置。
    示例：
        build("report.html", "市场数据", lambda r: (
            r.header("市场数据", "", ["2026-05-14"]),
            r.nav([("指标","#kpi")]),
            r.section("kpi","01","核心指标","").__enter__(),
            r.kpi("销量","4.23","亿件","占21.1%"),
            None
        ))
    """
    r = ReportBuilder(title)
    config_fn(r)
    return r.render(out_path)


if __name__ == "__main__":
    # 最小验证示例
    r = ReportBuilder("验证报告")
    r.header("验证报告", "模板测试", ["时间:2026-05-14"])
    r.nav([("测试", "#test")])
    with r.section("test", "01", "测试章节", "验证模板渲染"):
        r.card("测试图表", r.C_TAOBAO)
        r.chart("testChart")
        r.card_end()
        r.chart_bar("testChart",
                    categories=["A", "B", "C"],
                    series=[{"name": "数值", "data": [120, 200, 150], "color": r.C_TAOBAO}])
    r.footer("验证测试")
    r.render("template-test-py.html")
