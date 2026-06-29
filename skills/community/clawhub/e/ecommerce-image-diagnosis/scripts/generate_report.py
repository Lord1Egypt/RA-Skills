#!/usr/bin/env python3
"""
电商主图&详情页诊断报告生成器
用法：python generate_report.py <diagnosis_json_file> [output_html_file]

diagnosis_json 格式：
{
  "product_name": "商品名称",
  "platform": "淘宝/拼多多/抖音/京东",
  "product_url": "商品链接（可选）",
  "diagnosis_date": "2026-06-18",
  "main_image": {
    "score": 72,
    "clarity": {"score": 16, "max": 20, "issues": [], "suggestions": []},
    "info_delivery": {"score": 18, "max": 25, "issues": [], "suggestions": []},
    "differentiation": {"score": 14, "max": 20, "issues": [], "suggestions": []},
    "trust": {"score": 14, "max": 20, "issues": [], "suggestions": []},
    "compliance": {"score": 10, "max": 15, "issues": [], "suggestions": []}
  },
  "detail_page": {
    "score": 65,
    "first_screen": {"score": 15, "max": 25, "issues": [], "suggestions": []},
    "info_structure": {"score": 18, "max": 25, "issues": [], "suggestions": []},
    "scene": {"score": 12, "max": 20, "issues": [], "suggestions": []},
    "trust_proof": {"score": 12, "max": 20, "issues": [], "suggestions": []},
    "conversion": {"score": 8, "max": 10, "issues": [], "suggestions": []}
  },
  "search_competition": {
    "visual_standout": "中等",
    "thumbnail_clarity": "良好",
    "title_image_coherence": "一般",
    "notes": ""
  },
  "overall_grade": "B",
  "overall_score": 68,
  "key_findings": [],
  "priority_actions": {
    "P0": [],
    "P1": [],
    "P2": []
  }
}
"""

import json
import sys
import os
from datetime import datetime

GRADE_CONFIG = {
    "S": {"label": "优秀", "color": "#27500A", "bg": "#EAF3DE", "bar": "#639922"},
    "A": {"label": "良好", "color": "#0C447C", "bg": "#E6F1FB", "bar": "#378ADD"},
    "B": {"label": "及格", "color": "#633806", "bg": "#FAEEDA", "bar": "#BA7517"},
    "C": {"label": "待改进", "color": "#993C1D", "bg": "#FAECE7", "bar": "#D85A30"},
    "D": {"label": "急需重做", "color": "#791F1F", "bg": "#FCEBEB", "bar": "#E24B4A"},
}

DIMENSION_NAMES = {
    "clarity": "视觉清晰度",
    "info_delivery": "信息传达",
    "differentiation": "差异化竞争力",
    "trust": "信任感建立",
    "compliance": "平台合规性",
    "first_screen": "首屏冲击力",
    "info_structure": "信息架构",
    "scene": "场景化呈现",
    "trust_proof": "信任背书",
    "conversion": "转化促进",
}

def get_score_grade(score):
    if score >= 85: return "S"
    if score >= 70: return "A"
    if score >= 55: return "B"
    if score >= 40: return "C"
    return "D"

def pct(score, max_score):
    return round(score / max_score * 100) if max_score else 0

def render_bar(score, max_score, color="#378ADD"):
    p = pct(score, max_score)
    return f"""<div style="display:flex;align-items:center;gap:8px;">
      <div style="flex:1;background:#F1EFE8;border-radius:4px;height:8px;overflow:hidden;">
        <div style="width:{p}%;background:{color};height:100%;border-radius:4px;transition:width .3s;"></div>
      </div>
      <span style="font-size:12px;color:#444441;min-width:42px;text-align:right;">{score}/{max_score}</span>
    </div>"""

def render_tag_list(items, tag_type="issue"):
    if not items: return "<span style='color:#888780;font-size:12px;'>暂无</span>"
    color = "#993C1D" if tag_type == "issue" else "#27500A"
    bg = "#FAECE7" if tag_type == "issue" else "#EAF3DE"
    html = ""
    for item in items:
        html += f'<span style="display:inline-block;background:{bg};color:{color};border-radius:4px;padding:2px 8px;font-size:12px;margin:2px 4px 2px 0;">{item}</span>'
    return html

def render_dimension_card(name, data, bar_color):
    issues_html = render_tag_list(data.get("issues", []), "issue")
    suggestions_html = render_tag_list(data.get("suggestions", []), "suggestion")
    bar_html = render_bar(data["score"], data["max"], bar_color)
    label = DIMENSION_NAMES.get(name, name)
    return f"""
    <div style="background:#fff;border:0.5px solid #D3D1C7;border-radius:12px;padding:16px;margin-bottom:12px;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
        <span style="font-size:13px;font-weight:500;color:#2C2C2A;">{label}</span>
        <span style="font-size:13px;color:#444441;">{pct(data['score'],data['max'])}分</span>
      </div>
      {bar_html}
      <div style="margin-top:10px;">
        <div style="font-size:12px;color:#888780;margin-bottom:4px;">发现问题</div>
        <div>{issues_html}</div>
      </div>
      <div style="margin-top:8px;">
        <div style="font-size:12px;color:#888780;margin-bottom:4px;">优化建议</div>
        <div>{suggestions_html}</div>
      </div>
    </div>"""

def render_priority_list(items, p_level):
    if not items:
        return f'<p style="color:#888780;font-size:13px;">暂无 {p_level} 级问题</p>'
    color_map = {"P0": "#E24B4A", "P1": "#BA7517", "P2": "#378ADD"}
    bg_map = {"P0": "#FCEBEB", "P1": "#FAEEDA", "P2": "#E6F1FB"}
    color = color_map.get(p_level, "#378ADD")
    bg = bg_map.get(p_level, "#E6F1FB")
    html = ""
    for i, item in enumerate(items, 1):
        html += f"""<div style="display:flex;align-items:flex-start;gap:10px;padding:10px 12px;background:{bg};border-radius:8px;margin-bottom:8px;">
          <span style="background:{color};color:#fff;border-radius:4px;padding:1px 7px;font-size:12px;font-weight:500;flex-shrink:0;">{p_level}</span>
          <span style="font-size:13px;color:#2C2C2A;line-height:1.6;">{item}</span>
        </div>"""
    return html

def generate_html(data: dict) -> str:
    product_name = data.get("product_name", "商品诊断")
    platform = data.get("platform", "")
    product_url = data.get("product_url", "")
    diagnosis_date = data.get("diagnosis_date", datetime.now().strftime("%Y-%m-%d"))

    overall_score = data.get("overall_score", 0)
    overall_grade = data.get("overall_grade", get_score_grade(overall_score))
    grade_cfg = GRADE_CONFIG.get(overall_grade, GRADE_CONFIG["B"])

    mi = data.get("main_image", {})
    dp = data.get("detail_page", {})
    sc = data.get("search_competition", {})

    mi_score = mi.get("score", 0)
    dp_score = dp.get("score", 0)
    mi_grade = get_score_grade(mi_score)
    dp_grade = get_score_grade(dp_score)
    mi_cfg = GRADE_CONFIG[mi_grade]
    dp_cfg = GRADE_CONFIG[dp_grade]

    # main image dimensions
    mi_dims_html = ""
    for dim in ["clarity", "info_delivery", "differentiation", "trust", "compliance"]:
        if dim in mi:
            mi_dims_html += render_dimension_card(dim, mi[dim], mi_cfg["bar"])

    # detail page dimensions
    dp_dims_html = ""
    for dim in ["first_screen", "info_structure", "scene", "trust_proof", "conversion"]:
        if dim in dp:
            dp_dims_html += render_dimension_card(dim, dp[dim], dp_cfg["bar"])

    # key findings
    key_findings = data.get("key_findings", [])
    findings_html = ""
    for f in key_findings:
        findings_html += f'<li style="font-size:13px;color:#2C2C2A;line-height:1.8;margin-bottom:4px;">{f}</li>'
    if not findings_html:
        findings_html = '<li style="color:#888780;font-size:13px;">暂无核心发现</li>'

    # priority actions
    priority = data.get("priority_actions", {})
    p0_html = render_priority_list(priority.get("P0", []), "P0")
    p1_html = render_priority_list(priority.get("P1", []), "P1")
    p2_html = render_priority_list(priority.get("P2", []), "P2")

    # search competition
    sc_html = f"""
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-bottom:16px;">
      <div style="background:#F1EFE8;border-radius:8px;padding:12px;text-align:center;">
        <div style="font-size:12px;color:#888780;margin-bottom:4px;">视觉跳出率</div>
        <div style="font-size:15px;font-weight:500;color:#2C2C2A;">{sc.get('visual_standout','—')}</div>
      </div>
      <div style="background:#F1EFE8;border-radius:8px;padding:12px;text-align:center;">
        <div style="font-size:12px;color:#888780;margin-bottom:4px;">缩略图清晰度</div>
        <div style="font-size:15px;font-weight:500;color:#2C2C2A;">{sc.get('thumbnail_clarity','—')}</div>
      </div>
      <div style="background:#F1EFE8;border-radius:8px;padding:12px;text-align:center;">
        <div style="font-size:12px;color:#888780;margin-bottom:4px;">标题图片协同度</div>
        <div style="font-size:15px;font-weight:500;color:#2C2C2A;">{sc.get('title_image_coherence','—')}</div>
      </div>
    </div>
    """ + (f'<p style="font-size:13px;color:#444441;line-height:1.6;">{sc["notes"]}</p>' if sc.get("notes") else "")

    url_html = f'<a href="{product_url}" style="color:#185FA5;font-size:12px;word-break:break-all;">{product_url}</a>' if product_url else ""
    platform_badge = f'<span style="background:#E6F1FB;color:#185FA5;border-radius:4px;padding:2px 8px;font-size:12px;margin-left:8px;">{platform}</span>' if platform else ""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>电商主图&详情页诊断报告 — {product_name}</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0;}}
  body{{font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;background:#F1EFE8;color:#2C2C2A;}}
  .container{{max-width:860px;margin:0 auto;padding:24px 16px;}}
  h1{{font-size:20px;font-weight:500;}}
  h2{{font-size:15px;font-weight:500;margin-bottom:16px;border-left:3px solid #378ADD;padding-left:10px;}}
  h3{{font-size:14px;font-weight:500;margin-bottom:12px;}}
  section{{background:#fff;border-radius:16px;border:0.5px solid #D3D1C7;padding:20px 24px;margin-bottom:20px;}}
  .score-big{{font-size:48px;font-weight:500;line-height:1;}}
  .grade-badge{{display:inline-block;border-radius:6px;padding:3px 12px;font-size:13px;font-weight:500;}}
  @media(max-width:600px){{.container{{padding:16px 10px;}}.score-big{{font-size:36px;}}}}
</style>
</head>
<body>
<div class="container">

  <!-- 头部 -->
  <section>
    <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;">
      <div>
        <h1 style="margin-bottom:6px;">{product_name}{platform_badge}</h1>
        <div style="font-size:12px;color:#888780;">诊断日期：{diagnosis_date}</div>
        {f'<div style="margin-top:4px;">{url_html}</div>' if url_html else ''}
      </div>
      <div style="text-align:center;background:{grade_cfg['bg']};border-radius:12px;padding:16px 24px;">
        <div style="font-size:12px;color:{grade_cfg['color']};margin-bottom:4px;">综合评分</div>
        <div class="score-big" style="color:{grade_cfg['color']};">{overall_score}</div>
        <div class="grade-badge" style="background:{grade_cfg['bar']};color:#fff;margin-top:6px;">
          {overall_grade} 级 · {grade_cfg['label']}
        </div>
      </div>
    </div>
  </section>

  <!-- 评分总览 -->
  <section>
    <h2>评分总览</h2>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
      <div style="background:{mi_cfg['bg']};border-radius:12px;padding:16px;text-align:center;">
        <div style="font-size:12px;color:{mi_cfg['color']};margin-bottom:4px;">主图得分</div>
        <div style="font-size:36px;font-weight:500;color:{mi_cfg['color']};">{mi_score}</div>
        <div class="grade-badge" style="background:{mi_cfg['bar']};color:#fff;margin-top:6px;font-size:12px;">
          {mi_grade} · {GRADE_CONFIG[mi_grade]['label']}
        </div>
        {render_bar(mi_score, 100, mi_cfg['bar'])}
      </div>
      <div style="background:{dp_cfg['bg']};border-radius:12px;padding:16px;text-align:center;">
        <div style="font-size:12px;color:{dp_cfg['color']};margin-bottom:4px;">详情页得分</div>
        <div style="font-size:36px;font-weight:500;color:{dp_cfg['color']};">{dp_score}</div>
        <div class="grade-badge" style="background:{dp_cfg['bar']};color:#fff;margin-top:6px;font-size:12px;">
          {dp_grade} · {GRADE_CONFIG[dp_grade]['label']}
        </div>
        {render_bar(dp_score, 100, dp_cfg['bar'])}
      </div>
    </div>
  </section>

  <!-- 核心发现 -->
  <section>
    <h2>核心发现</h2>
    <ul style="padding-left:18px;list-style:disc;">
      {findings_html}
    </ul>
  </section>

  <!-- 优先改进行动 -->
  <section>
    <h2>优先改进行动</h2>
    <h3 style="color:#E24B4A;">P0 — 立即修复</h3>
    {p0_html}
    <h3 style="color:#BA7517;margin-top:16px;">P1 — 本周优化</h3>
    {p1_html}
    <h3 style="color:#378ADD;margin-top:16px;">P2 — 下次迭代</h3>
    {p2_html}
  </section>

  <!-- 主图详细诊断 -->
  <section>
    <h2>主图详细诊断</h2>
    {mi_dims_html if mi_dims_html else '<p style="color:#888780;font-size:13px;">未提供主图素材，无法进行详细诊断。</p>'}
  </section>

  <!-- 详情页详细诊断 -->
  <section>
    <h2>详情页详细诊断</h2>
    {dp_dims_html if dp_dims_html else '<p style="color:#888780;font-size:13px;">未提供详情页素材，无法进行详细诊断。</p>'}
  </section>

  <!-- 搜索竞争力 -->
  <section>
    <h2>搜索竞争力分析</h2>
    {sc_html}
  </section>

  <!-- 页脚 -->
  <div style="text-align:center;padding:16px;font-size:12px;color:#B4B2A9;">
    由 WorkBuddy 电商主图&详情页诊断 Skill 生成 · {diagnosis_date}
  </div>

</div>
</body>
</html>"""

def main():
    if len(sys.argv) < 2:
        print("用法: python generate_report.py <diagnosis_json_file> [output_html_file]")
        sys.exit(1)

    input_file = sys.argv[1]
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    html = generate_html(data)

    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        base = os.path.splitext(input_file)[0]
        output_file = base + "_report.html"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"报告已生成: {output_file}")

if __name__ == "__main__":
    main()
