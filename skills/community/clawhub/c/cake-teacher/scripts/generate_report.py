#!/usr/bin/env python3
"""
🎂 蛋糕烘焙教学报告生成器
生成交互式 HTML 可视化报告，包含配方卡片、步骤时间轴、翻车预警、工具清单、大师技巧。
"""

import argparse
import json
import sys
import os
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(description="蛋糕烘焙教学报告生成器")
    parser.add_argument("--title", default="蛋糕烘焙教学报告", help="报告标题")
    parser.add_argument("--category", default="基础蛋糕", help="蛋糕品类")
    parser.add_argument("--output", default="cake_report.html", help="输出文件路径")
    parser.add_argument("--stdin", action="store_true", help="从标准输入读取JSON数据")
    return parser.parse_args()


def generate_html(data):
    """生成完整的交互式 HTML 报告"""
    title = data.get("title", "蛋糕烘焙教学报告")
    category = data.get("category", "基础蛋糕")
    recipe = data.get("recipe", {})
    steps = data.get("steps", [])
    tips = data.get("tips", [])
    diagnosis = data.get("diagnosis", {})
    equipment = data.get("equipment", [])
    alerts = data.get("alerts", [])
    description = data.get("description", "")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
    background: linear-gradient(135deg, #fdf2f8 0%, #fce7f3 25%, #fff1f2 50%, #fef3c7 100%);
    min-height: 100vh;
    padding: 20px;
    color: #1e293b;
}}
.container {{ max-width: 900px; margin: 0 auto; }}
.header {{
    background: linear-gradient(135deg, #ec4899, #f97316);
    border-radius: 20px;
    padding: 40px 30px;
    color: white;
    text-align: center;
    margin-bottom: 24px;
    box-shadow: 0 10px 40px rgba(236, 72, 153, 0.3);
    position: relative;
    overflow: hidden;
}}
.header::before {{
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
    animation: shimmer 3s ease-in-out infinite;
}}
@keyframes shimmer {{
    0%, 100% {{ transform: translate(0, 0); }}
    50% {{ transform: translate(5%, 5%); }}
}}
.header .emoji {{ font-size: 64px; display: block; margin-bottom: 8px; }}
.header h1 {{ font-size: 28px; font-weight: 700; margin-bottom: 8px; }}
.header .subtitle {{ font-size: 14px; opacity: 0.9; }}
.header .badge {{
    display: inline-block;
    background: rgba(255,255,255,0.25);
    padding: 4px 16px;
    border-radius: 20px;
    font-size: 13px;
    margin-top: 12px;
    backdrop-filter: blur(4px);
}}

/* 配方卡片 */
.recipe-card {{
    background: white;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    border-left: 5px solid #f97316;
}}
.recipe-card h2 {{
    font-size: 18px;
    color: #f97316;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}}
.ingredient-group {{
    margin-bottom: 16px;
}}
.ingredient-group h3 {{
    font-size: 14px;
    color: #64748b;
    margin-bottom: 8px;
    padding-bottom: 4px;
    border-bottom: 1px dashed #e2e8f0;
}}
.ingredient-list {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 8px;
}}
.ingredient-item {{
    display: flex;
    justify-content: space-between;
    padding: 6px 12px;
    background: #f8fafc;
    border-radius: 8px;
    font-size: 14px;
}}
.ingredient-item .name {{ color: #334155; }}
.ingredient-item .amount {{ color: #f97316; font-weight: 600; }}

/* 烘焙参数 */
.bake-params {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 12px;
    margin-top: 16px;
}}
.param-item {{
    text-align: center;
    padding: 12px;
    background: linear-gradient(135deg, #fef3c7, #fce7f3);
    border-radius: 12px;
}}
.param-item .param-icon {{ font-size: 24px; }}
.param-item .param-value {{ font-size: 16px; font-weight: 700; color: #ec4899; margin-top: 4px; }}
.param-item .param-label {{ font-size: 11px; color: #94a3b8; margin-top: 2px; }}

/* 步骤时间轴 */
.timeline {{
    position: relative;
    padding-left: 30px;
    margin-bottom: 20px;
}}
.timeline::before {{
    content: '';
    position: absolute;
    left: 12px;
    top: 0;
    bottom: 0;
    width: 3px;
    background: linear-gradient(to bottom, #ec4899, #f97316, #eab308);
    border-radius: 2px;
}}
.step-card {{
    background: white;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    position: relative;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    transition: transform 0.2s, box-shadow 0.2s;
    cursor: pointer;
}}
.step-card:hover {{
    transform: translateX(4px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}}
.step-card::before {{
    content: attr(data-step);
    position: absolute;
    left: -42px;
    top: 18px;
    width: 28px;
    height: 28px;
    background: linear-gradient(135deg, #ec4899, #f97316);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 700;
}}
.step-card .step-title {{ font-size: 16px; font-weight: 600; color: #1e293b; margin-bottom: 6px; }}
.step-card .step-desc {{ font-size: 14px; color: #64748b; line-height: 1.6; }}
.step-card .step-time {{ font-size: 12px; color: #f97316; margin-top: 8px; font-weight: 500; }}
.step-card .step-alert {{
    background: #fef2f2;
    border-radius: 8px;
    padding: 8px 12px;
    margin-top: 8px;
    font-size: 13px;
    color: #dc2626;
    border-left: 3px solid #ef4444;
}}

/* 大师技巧卡片 */
.tips-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 12px;
    margin-bottom: 20px;
}}
.tip-card {{
    background: white;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    display: flex;
    gap: 12px;
    align-items: flex-start;
}}
.tip-card .tip-icon {{ font-size: 28px; flex-shrink: 0; }}
.tip-card .tip-content h4 {{ font-size: 14px; font-weight: 600; color: #334155; margin-bottom: 4px; }}
.tip-card .tip-content p {{ font-size: 13px; color: #64748b; line-height: 1.5; }}

/* 诊断模块 */
.diagnosis-card {{
    background: white;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    border: 2px solid #fecaca;
}}
.diagnosis-card h2 {{ color: #dc2626; font-size: 18px; margin-bottom: 16px; }}
.diag-item {{
    padding: 12px;
    margin-bottom: 10px;
    background: #fef2f2;
    border-radius: 10px;
    border-left: 4px solid #ef4444;
}}
.diag-item h4 {{ font-size: 15px; color: #dc2626; margin-bottom: 4px; }}
.diag-item .probability {{
    display: inline-block;
    background: #dc2626;
    color: white;
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 10px;
    margin-left: 8px;
}}
.diag-item p {{ font-size: 13px; color: #64748b; line-height: 1.5; }}
.diag-item .solution {{ font-size: 13px; color: #16a34a; font-weight: 500; margin-top: 6px; }}

/* 工具清单 */
.equipment-section {{
    background: white;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
}}
.equipment-item {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid #f1f5f9;
}}
.equipment-item:last-child {{ border-bottom: none; }}
.equipment-item .eq-icon {{ font-size: 24px; }}
.equipment-item .eq-name {{ font-weight: 500; flex: 1; }}
.equipment-item .eq-note {{ font-size: 12px; color: #94a3b8; }}

/* 安全提示 */
.safety-section {{
    background: linear-gradient(135deg, #fef3c7, #fef9c3);
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 20px;
    border: 2px solid #fde047;
}}
.safety-section h3 {{ color: #a16207; margin-bottom: 12px; font-size: 16px; }}
.safety-item {{
    display: flex;
    align-items: flex-start;
    gap: 8px;
    padding: 4px 0;
    font-size: 13px;
    color: #713f12;
}}

/* 响应式 */
@media (max-width: 600px) {{
    body {{ padding: 10px; }}
    .header {{ padding: 24px 16px; }}
    .header h1 {{ font-size: 22px; }}
    .ingredient-list {{ grid-template-columns: 1fr; }}
    .tips-grid {{ grid-template-columns: 1fr; }}
    .bake-params {{ grid-template-columns: repeat(2, 1fr); }}
}}

.footer {{
    text-align: center;
    padding: 24px;
    color: #94a3b8;
    font-size: 12px;
}}

/* 标签切换 */
.tabs {{
    display: flex;
    gap: 8px;
    margin-bottom: 16px;
    flex-wrap: wrap;
}}
.tab {{
    padding: 8px 20px;
    border-radius: 20px;
    border: 1px solid #e2e8f0;
    background: white;
    cursor: pointer;
    font-size: 13px;
    transition: all 0.2s;
    color: #64748b;
}}
.tab.active, .tab:hover {{
    background: linear-gradient(135deg, #ec4899, #f97316);
    color: white;
    border-color: transparent;
}}
.tab-content {{ display: none; }}
.tab-content.active {{ display: block; }}
</style>
</head>
<body>
<div class="container">

<!-- Header -->
<div class="header">
    <span class="emoji">🎂</span>
    <h1>{title}</h1>
    <p class="subtitle">{description or '专业蛋糕烘焙教学 · 零基础到大师'}</p>
    <span class="badge">{category}</span>
</div>
"""

    # Tab navigation
    html += """<div class="tabs">
    <button class="tab active" onclick="switchTab('recipe')">📋 配方</button>
    <button class="tab" onclick="switchTab('steps')">📝 步骤</button>
    <button class="tab" onclick="switchTab('tips')">💡 技巧</button>
"""

    if diagnosis:
        html += """<button class="tab" onclick="switchTab('diagnosis')">🔍 诊断</button>"""

    if equipment:
        html += """<button class="tab" onclick="switchTab('equipment')">🔧 工具</button>"""
    html += "</div>\n"

    # Recipe tab
    html += """<div class="tab-content active" id="tab-recipe">"""

    if recipe.get("ingredients"):
        html += """<div class="recipe-card">
    <h2>📋 食材清单（精确称量）</h2>
"""
        for group_name, items in recipe["ingredients"].items():
            html += f"""    <div class="ingredient-group">
        <h3>{group_name}</h3>
        <div class="ingredient-list">
"""
            for item in items:
                name = item.get("name", "")
                amount = item.get("amount", "")
                html += f"""            <div class="ingredient-item">
                <span class="name">{name}</span>
                <span class="amount">{amount}</span>
            </div>
"""
            html += "        </div>\n    </div>\n"
        html += "    </div>\n"

    if recipe.get("bake"):
        bake = recipe["bake"]
        html += f"""    <div class="recipe-card">
        <h2>🔥 烘烤参数</h2>
        <div class="bake-params">
            <div class="param-item">
                <div class="param-icon">🌡</div>
                <div class="param-value">{bake.get('temperature', '-')}</div>
                <div class="param-label">烘烤温度</div>
            </div>
            <div class="param-item">
                <div class="param-icon">⏱</div>
                <div class="param-value">{bake.get('time', '-')}</div>
                <div class="param-label">烘烤时间</div>
            </div>
            <div class="param-item">
                <div class="param-icon">📐</div>
                <div class="param-value">{bake.get('mold', '-')}</div>
                <div class="param-label">模具尺寸</div>
            </div>
            <div class="param-item">
                <div class="param-icon">📊</div>
                <div class="param-value">{bake.get('position', '-')}</div>
                <div class="param-label">烤箱层位</div>
            </div>
        </div>
    </div>
"""
    html += "</div>\n"

    # Steps tab
    html += """<div class="tab-content" id="tab-steps">\n"""
    if steps:
        html += """<div class="recipe-card">
    <h2>📝 制作步骤</h2>
</div>
<div class="timeline">
"""
        for i, step in enumerate(steps, 1):
            step_time = step.get('time', '')
            step_alert = step.get('alert', '')
            html += f"""    <div class="step-card" data-step="{i}">
        <div class="step-title">步骤 {i}：{step.get('title', '')}</div>
        <div class="step-desc">{step.get('desc', '')}</div>
"""
            if step_time:
                html += f'        <div class="step-time">⏱ 预计时间：{step_time}</div>\n'
            if step_alert:
                html += f'        <div class="step-alert">⚠️ {step_alert}</div>\n'
            html += "    </div>\n"
        html += "</div>\n"
    else:
        html += """<div class="recipe-card">
    <h2>📝 制作步骤</h2>
    <p style="color:#94a3b8;text-align:center;padding:40px;">请描述你想学习的蛋糕品类，我将为你生成详细步骤</p>
</div>"""
    html += "</div>\n"

    # Tips tab
    html += """<div class="tab-content" id="tab-tips">\n"""
    if tips:
        html += """<div class="recipe-card">
    <h2>💡 大师技巧</h2>
</div>
<div class="tips-grid">
"""
        tips_icons = ["🔥", "🧊", "⚡", "🎯", "✨", "💪", "🔑", "🌟", "🧠", "🍰"]
        for i, tip in enumerate(tips):
            icon = tips_icons[i % len(tips_icons)]
            html += f"""    <div class="tip-card">
        <span class="tip-icon">{icon}</span>
        <div class="tip-content">
            <h4>{tip.get('title', '')}</h4>
            <p>{tip.get('desc', '')}</p>
        </div>
    </div>
"""
        html += "</div>\n"
    else:
        html += """<div class="recipe-card">
    <h2>💡 大师技巧</h2>
    <p style="color:#94a3b8;text-align:center;padding:40px;">选择蛋糕品类后，我将为你展示该品类的大师级技巧</p>
</div>"""
    html += "</div>\n"

    # Diagnosis tab (if exists)
    if diagnosis:
        html += """<div class="tab-content" id="tab-diagnosis">\n"""
        html += f"""<div class="diagnosis-card">
    <h2>🔍 翻车诊断报告</h2>
    <p style="color:#64748b;margin-bottom:16px;">问题描述：{diagnosis.get('problem', '')}</p>
"""
        for diag in diagnosis.get("causes", []):
            prob = diag.get('probability', '')
            prob_html = f'<span class="probability">{prob}</span>' if prob else ''
            html += f"""    <div class="diag-item">
        <h4>{diag.get('cause', '')}{prob_html}</h4>
        <p>{diag.get('detail', '')}</p>
        <div class="solution">✅ 解决方案：{diag.get('solution', '')}</div>
    </div>
"""
        html += "</div>\n</div>\n"

    # Equipment tab
    if equipment:
        html += """<div class="tab-content" id="tab-equipment">\n"""
        html += """<div class="equipment-section">
    <h2>🔧 所需工具</h2>
"""
        for eq in equipment:
            html += f"""    <div class="equipment-item">
        <span class="eq-icon">{eq.get('icon', '🔧')}</span>
        <span class="eq-name">{eq.get('name', '')}</span>
        <span class="eq-note">{eq.get('note', '')}</span>
    </div>
"""
        html += "</div>\n</div>\n"

    # Safety section
    if alerts:
        html += """<div class="safety-section">
    <h3>⚠️ 安全与注意事项</h3>
"""
        for alert in alerts:
            html += f"""    <div class="safety-item">{alert.get('icon', '⚠️')} {alert.get('text', '')}</div>
"""
        html += "</div>\n"

    # Footer
    html += f"""<div class="footer">
    🎂 AI 蛋糕烘焙培训老师 · 生成时间：{now} · 祝你烘焙愉快！
</div>

</div>

<script>
function switchTab(tabName) {{
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.querySelector(`#tab-${{tabName}}`).classList.add('active');
    event.target.classList.add('active');
}}
</script>
</body>
</html>"""

    return html


def sanitize_text(text):
    """Remove lone surrogates that cause UnicodeEncodeError on Windows."""
    if isinstance(text, str):
        return text.encode("utf-8", errors="surrogateescape").decode("utf-8", errors="replace")
    return text


def sanitize_data(obj):
    """Recursively sanitize all string values in a dict/list."""
    if isinstance(obj, str):
        return sanitize_text(obj)
    elif isinstance(obj, dict):
        return {k: sanitize_data(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_data(i) for i in obj]
    return obj


def main():
    args = parse_args()

    if args.stdin:
        raw = sys.stdin.buffer.read().decode("utf-8", errors="surrogateescape")
        raw = raw.strip()
        if raw:
            data = json.loads(raw)
        else:
            data = {}
    else:
        data = {}

    # Sanitize all text to avoid surrogate encoding issues
    data = sanitize_data(data)

    # Ensure required fields
    if not data.get("title"):
        data["title"] = args.title
    if not data.get("category"):
        data["category"] = args.category

    html = generate_html(data)

    output_path = args.output
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    with open(output_path, "w", encoding="utf-8", errors="surrogateescape") as f:
        f.write(html)

    print(f"Report generated: {output_path}")
    print(f"  Title: {data['title']}")
    print(f"  Category: {data['category']}")


if __name__ == "__main__":
    main()
