"""hooks.py — 标准化输出钩子

每个场景函数在 return 前调用 publish()，强制输出 markdown 表格。
可选参数 chart_fn/figure 生成 HTML 报告。
"""
import sys, os
from .markdown import dict_to_md, df_to_md, concat_md
from .renderer import build_html, save_html


def publish(data, title=None, md_extra=None, figure=None, chart_js_fn=None, html_filename=None):
    """
    强制输出钩子 — 所有场景函数末尾必须调用。

    Parameters
    ----------
    data : dict or pd.DataFrame
        计算结果
    title : str, optional
        报告标题
    md_extra : str, optional
        额外的 markdown 内容
    figure : matplotlib.figure.Figure, optional
        可视化图片（回退用）
    chart_js_fn : callable, optional
        返回 Chart.js JS 代码的函数
    html_filename : str, optional
        HTML 文件名（不传则不生成 HTML）
    """
    md_parts = []

    if title:
        md_parts.append(f"## {title}\n")

    # 通用 dict/DataFrame → markdown
    _append_md(data, md_parts)

    if md_extra:
        md_parts.append(md_extra.strip() + "\n")

    md_body = concat_md(*md_parts)

    # 1. print markdown（强制）
    print(md_body)

    # 2. 生成 HTML（可选）
    if html_filename:
        chart_code = chart_js_fn() if chart_js_fn else None
        html = build_html(md_body, chart_js_code=chart_code, fig=figure, title=title or "分析报告")
        path = save_html(html, filename=html_filename)
        print(f"\nHTML 报告已保存：{path}")


def _append_md(data, parts):
    """递归展开 dict/DataFrame 为 markdown 段落"""
    if hasattr(data, 'columns'):
        # DataFrame 优先
        parts.append(df_to_md(data))
    elif isinstance(data, dict):
        # dict — 尝试作为 key-value 表输出
        d = data
        # 提取非表字段（跳过嵌套 DataFrame/Figure）
        simple = {}
        for k, v in d.items():
            if hasattr(v, 'columns'):
                continue  # 嵌套 DataFrame 另发 publish
            elif hasattr(v, 'to_dict'):
                continue  # 嵌套 dict-like 另发 publish
            elif isinstance(v, (list, tuple)):
                if v.__class__.__module__ == 'matplotlib.figure':
                    continue
                if len(v) > 0 and not isinstance(v[0], (int, float, str)):
                    continue
                simple[k] = v
            elif not callable(v) and v is not None:
                # 跳过 matplotlib Figure
                if v.__class__.__module__ == 'matplotlib.figure':
                    continue
                simple[k] = v
        if simple:
            parts.append(dict_to_md(simple))
