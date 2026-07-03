#!/usr/bin/env python3
"""Flower Care — AI-powered flower/plant identification and care guide using DashScope multimodal API.

Usage:
    python flower_care.py --image path/to/flower.jpg [--output report.html] [--model qwen-vl-max]
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

# Fix Windows console encoding for emoji output
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# --- Constants ---
CARE_DIMENSIONS = ["浇水", "光照", "温度", "土壤", "施肥", "病虫害防治"]
DIMENSION_ICONS = {
    "浇水": "💧", "光照": "☀️", "温度": "🌡️",
    "土壤": "🪴", "施肥": "🧪", "病虫害防治": "🛡️"
}
DIMENSION_COLORS = {
    "浇水": "#2196F3", "光照": "#FF9800", "温度": "#F44336",
    "土壤": "#795548", "施肥": "#4CAF50", "病虫害防治": "#9C27B0"
}

DIFFICULTY_COLORS = {
    "容易": "#4CAF50", "中等": "#FF9800", "较难": "#F44336",
    "easy": "#4CAF50", "medium": "#FF9800", "hard": "#F44336"
}

MIME_MAP = {
    ".jpg": "jpeg", ".jpeg": "jpeg", ".png": "png",
    ".webp": "webp", ".bmp": "bmp", ".gif": "gif"
}

DASHSCOPE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"


def find_api_key():
    """Find DashScope API key from env or config file."""
    key = os.environ.get("DASHSCOPE_API_KEY", "")
    if key:
        return key

    key = os.environ.get("OPENAI_API_KEY", "")
    if key:
        return key

    config_paths = [
        os.path.expanduser("~/.workbuddy/config/dashscope.json"),
        os.path.expanduser("~/.dashscope/config.json"),
    ]
    for cfg in config_paths:
        if os.path.exists(cfg):
            try:
                with open(cfg, encoding="utf-8") as f:
                    data = json.load(f)
                    if "api_key" in data:
                        return data["api_key"]
                    if "DASHSCOPE_API_KEY" in data:
                        return data["DASHSCOPE_API_KEY"]
            except Exception:
                pass
    return ""


def encode_image(image_path):
    """Encode image to base64 data URL."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"图片不存在: {image_path}")

    ext = path.suffix.lower()
    mime = MIME_MAP.get(ext, "jpeg")

    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    return f"data:image/{mime};base64,{data}", mime


def build_prompt():
    """Build the analysis prompt for flower/plant identification and care."""
    return """你是一位资深园艺师和植物学家。请仔细分析这张照片中的植物/花卉，提供专业的识别和养护建议。

分析步骤：
1. 先判断图片中是否有植物/花卉，如果没有人请说明
2. 识别植物的种类（中文名、学名、科属）
3. 评估植物的健康状态
4. 提供详细的养护指南

请严格返回以下JSON格式，不要包含任何其他内容：
{
  "has_plant": true/false,
  "plant_name": "植物中文名",
  "scientific_name": "学名",
  "family": "科属分类",
  "plant_type": "观花植物/观叶植物/多肉植物/水生植物/藤本植物/木本植物/其他",
  "health_status": "健康/一般/较差",
  "health_note": "一句话健康评估（如：叶片饱满色泽正常/有轻微黄叶现象等）",
  "difficulty": "容易/中等/较难",
  "water": {"frequency": "浇水频率（如：3-5天一次）", "method": "浇水方法（如：见干见湿，浇则浇透）", "note": "浇水注意事项"},
  "light": {"requirement": "光照需求（如：全日照/散射光/半阴）", "hours": "每日光照时长建议", "note": "光照注意事项"},
  "temperature": {"range": "适宜温度范围（如：15-28°C）", "min": "最低耐受温度带单位", "note": "温度注意事项"},
  "soil": {"type": "土壤类型（如：疏松排水好的沙壤土）", "ph": "酸碱度偏好", "note": "土壤注意事项"},
  "fertilizer": {"schedule": "施肥频率（如：生长期每10天一次）", "type": "肥料类型", "note": "施肥注意事项"},
  "diseases": [{"name": "常见病虫害名称", "symptom": "症状描述", "treatment": "防治方法"}],
  "tips": ["养护小贴士1", "养护小贴士2", "养护小贴士3"],
  "description": "一句话植物简介（30字以内）",
  "care_score": {"watering": 0.0-1.0, "light": 0.0-1.0, "temperature": 0.0-1.0, "soil": 0.0-1.0, "fertilizer": 0.0-1.0, "pest_control": 0.0-1.0}
}

care_score含义（养护难度评分，越高越需要关注）：
- watering: 浇水需要关注的程度
- light: 光照需要关注的程度
- temperature: 温度需要关注的程度
- soil: 土壤要求严格程度
- fertilizer: 施肥需要关注的程度
- pest_control: 病虫害风险程度

如果图片中没有植物，has_plant设为false，其他字段留空字符串或默认值。"""
    return prompt


def call_dashscope(api_key, image_data_url, model="qwen-vl-max"):
    """Call DashScope multimodal API for plant analysis."""
    import urllib.request
    import urllib.error

    payload = json.dumps({
        "model": model,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": image_data_url}},
                {"type": "text", "text": build_prompt()}
            ]
        }],
        "temperature": 0.3,
        "max_tokens": 1500
    }).encode()

    req = urllib.request.Request(
        DASHSCOPE_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        raise RuntimeError(f"API请求失败 (HTTP {e.code}): {error_body}")


def parse_response(api_result):
    """Parse DashScope API response into structured result."""
    try:
        content = api_result["choices"][0]["message"]["content"]
        content = content.strip()
        if content.startswith("```"):
            lines = content.split("\n")
            if lines[0].startswith("```json"):
                content = "\n".join(lines[1:])
            else:
                content = "\n".join(lines[1:])
            if content.endswith("```"):
                content = content[:-3].strip()

        result = json.loads(content)

        # Build structured result with defaults
        has_plant = result.get("has_plant", False)
        care_score = result.get("care_score", {})

        return {
            "has_plant": has_plant,
            "plant_name": result.get("plant_name", ""),
            "scientific_name": result.get("scientific_name", ""),
            "family": result.get("family", ""),
            "plant_type": result.get("plant_type", ""),
            "health_status": result.get("health_status", "未知"),
            "health_note": result.get("health_note", ""),
            "difficulty": result.get("difficulty", "中等"),
            "description": result.get("description", ""),
            "water": result.get("water", {}),
            "light": result.get("light", {}),
            "temperature": result.get("temperature", {}),
            "soil": result.get("soil", {}),
            "fertilizer": result.get("fertilizer", {}),
            "diseases": result.get("diseases", []),
            "tips": result.get("tips", []),
            "care_score": {
                "watering": care_score.get("watering", 0.5),
                "light": care_score.get("light", 0.5),
                "temperature": care_score.get("temperature", 0.5),
                "soil": care_score.get("soil", 0.5),
                "fertilizer": care_score.get("fertilizer", 0.5),
                "pest_control": care_score.get("pest_control", 0.5),
            },
            "raw": result
        }
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        raw_text = api_result.get("choices", [{}])[0].get("message", {}).get("content", str(api_result))
        return {
            "has_plant": False,
            "plant_name": "",
            "scientific_name": "",
            "family": "",
            "plant_type": "",
            "health_status": "未知",
            "health_note": "",
            "difficulty": "未知",
            "description": "",
            "water": {},
            "light": {},
            "temperature": {},
            "soil": {},
            "fertilizer": {},
            "diseases": [],
            "tips": [],
            "care_score": {"watering": 0.5, "light": 0.5, "temperature": 0.5, "soil": 0.5, "fertilizer": 0.5, "pest_control": 0.5},
            "raw": {"error": str(e), "raw_text": raw_text[:200]}
        }


def generate_html_report(result, image_path, output_path):
    """Generate interactive HTML report."""
    template_path = Path(__file__).parent.parent / "assets" / "report_template.html"
    if template_path.exists():
        with open(template_path, encoding="utf-8") as f:
            html = f.read()
    else:
        html = _get_default_template()

    # Encode image for embedding
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    ext = Path(image_path).suffix.lower()
    mime = MIME_MAP.get(ext, "jpeg")
    img_src = f"data:image/{mime};base64,{img_b64}"

    # Build care score chart data
    care_score = result.get("care_score", {})
    care_chart_data = [
        {"name": "浇水", "value": care_score.get("watering", 0.5), "color": DIMENSION_COLORS["浇水"], "icon": "💧"},
        {"name": "光照", "value": care_score.get("light", 0.5), "color": DIMENSION_COLORS["光照"], "icon": "☀️"},
        {"name": "温度", "value": care_score.get("temperature", 0.5), "color": DIMENSION_COLORS["温度"], "icon": "🌡️"},
        {"name": "土壤", "value": care_score.get("soil", 0.5), "color": DIMENSION_COLORS["土壤"], "icon": "🪴"},
        {"name": "施肥", "value": care_score.get("fertilizer", 0.5), "color": DIMENSION_COLORS["施肥"], "icon": "🧪"},
        {"name": "病虫害", "value": care_score.get("pest_control", 0.5), "color": DIMENSION_COLORS["病虫害防治"], "icon": "🛡️"},
    ]

    # Build diseases HTML
    diseases_html = ""
    if result.get("diseases"):
        for d in result["diseases"]:
            diseases_html += f"""<div class="disease-card">
                <div class="disease-name">🦠 {d.get('name', '未知病害')}</div>
                <div class="disease-symptom">📋 症状：{d.get('symptom', '')}</div>
                <div class="disease-treatment">💊 防治：{d.get('treatment', '')}</div>
            </div>"""

    # Build tips HTML
    tips_html = ""
    if result.get("tips"):
        for i, tip in enumerate(result["tips"]):
            tips_html += f'<div class="tip-item"><span class="tip-num">{i+1}</span>{tip}</div>'

    # Replace placeholders
    difficulty = result.get("difficulty", "中等")
    diff_color = DIFFICULTY_COLORS.get(difficulty, "#999")

    html = html.replace("{{IMAGE_SRC}}", img_src)
    html = html.replace("{{PLANT_NAME}}", result.get("plant_name", "未知植物"))
    html = html.replace("{{SCIENTIFIC_NAME}}", result.get("scientific_name", ""))
    html = html.replace("{{FAMILY}}", result.get("family", ""))
    html = html.replace("{{PLANT_TYPE}}", result.get("plant_type", ""))
    html = html.replace("{{HEALTH_STATUS}}", result.get("health_status", "未知"))
    html = html.replace("{{HEALTH_NOTE}}", result.get("health_note", ""))
    html = html.replace("{{DIFFICULTY}}", difficulty)
    html = html.replace("{{DIFFICULTY_COLOR}}", diff_color)
    html = html.replace("{{DESCRIPTION}}", result.get("description", ""))

    # Additional template placeholders
    plant_type_icons = {"观花植物": "🌸", "观叶植物": "🌿", "多肉植物": "🌵", "水生植物": "🪷", "藤本植物": "🌱", "木本植物": "🌳"}
    html = html.replace("{{PLANT_TYPE_ICON}}", plant_type_icons.get(result.get("plant_type", ""), "🌺"))
    health_icons = {"健康": "✅", "一般": "🔔", "较差": "⚠️"}
    html = html.replace("{{HEALTH_ICON}}", health_icons.get(result.get("health_status", ""), "❓"))
    diff_pct = {"容易": "25", "中等": "55", "较难": "85"}
    html = html.replace("{{DIFFICULTY_PCT}}", diff_pct.get(difficulty, "50"))
    html = html.replace("{{TIMESTAMP}}", time.strftime("%Y-%m-%d %H:%M:%S"))

    # Care guide - build placeholders
    key_cn_map = {"water": "浇水", "light": "光照", "temperature": "温度", "soil": "土壤", "fertilizer": "施肥"}
    for key in ["water", "light", "temperature", "soil", "fertilizer"]:
        data = result.get(key, {})
        upper = key.upper()
        val_freq = data.get("frequency") or data.get("schedule") or data.get("requirement") or data.get("range") or ""
        val_method = data.get("method") or data.get("hours") or data.get("min") or data.get("type") or ""
        val_note = data.get("note", "")
        icon = DIMENSION_ICONS.get(key_cn_map[key], "📌")

        html = html.replace("{{" + upper + "_FREQ}}", val_freq)
        html = html.replace("{{" + upper + "_METHOD}}", val_method)
        html = html.replace("{{" + upper + "_NOTE}}", val_note)
        html = html.replace("{{" + upper + "_ICON}}", icon)

    html = html.replace("{{DISEASES_HTML}}", diseases_html or '<div class="empty-hint">未检测到明显病虫害风险 🌿</div>')
    html = html.replace("{{TIPS_HTML}}", tips_html or '<div class="empty-hint">暂无特殊养护提示</div>')
    html = html.replace("{{CARE_CHART_DATA}}", json.dumps(care_chart_data, ensure_ascii=False))

    # Write output
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path


def generate_summary(result):
    """Generate a text summary for the conversation."""
    if not result.get("has_plant"):
        return "⚠️ 未在图片中识别到植物，请上传清晰的花卉/植物照片。"

    lines = [
        f"## 🌸 花卉识别结果",
        "",
        f"**{result['plant_name']}** ({result.get('scientific_name', '')})",
        f"",
        f"| 项目 | 详情 |",
        f"|------|------|",
        f"| 📝 科属 | {result.get('family', '未知')} |",
        f"| 🌿 类型 | {result.get('plant_type', '未知')} |",
        f"| 💚 健康 | {result.get('health_status', '未知')} {result.get('health_note', '')} |",
        f"| 📊 难度 | {result.get('difficulty', '中等')} |",
        f"| 📖 简介 | {result.get('description', '')} |",
        "",
        f"### 💧 浇水",
        f"{result.get('water', {}).get('frequency', '见干见湿')} — {result.get('water', {}).get('method', '')}",
        f"> {result.get('water', {}).get('note', '')}",
        "",
        f"### ☀️ 光照",
        f"{result.get('light', {}).get('requirement', '散射光')}，{result.get('light', {}).get('hours', '')}",
        f"> {result.get('light', {}).get('note', '')}",
        "",
        f"### 🌡️ 温度",
        f"{result.get('temperature', {}).get('range', '15-25°C')}",
        f"> {result.get('temperature', {}).get('note', '')}",
        "",
        f"### 🪴 土壤",
        f"{result.get('soil', {}).get('type', '疏松排水好的土壤')}",
        f"> {result.get('soil', {}).get('note', '')}",
        "",
        f"### 🧪 施肥",
        f"{result.get('fertilizer', {}).get('schedule', '')} — {result.get('fertilizer', {}).get('type', '')}",
        f"> {result.get('fertilizer', {}).get('note', '')}",
    ]

    if result.get("diseases"):
        lines.append("")
        lines.append("### 🛡️ 病虫害防治")
        for d in result["diseases"]:
            lines.append(f"- **{d.get('name', '')}**：{d.get('treatment', '')}")

    if result.get("tips"):
        lines.append("")
        lines.append("### 💡 养护贴士")
        for tip in result["tips"]:
            lines.append(f"- {tip}")

    return "\n".join(lines)


def _get_default_template():
    """Return a minimal default HTML template."""
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>花卉识别与养护报告</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;background:linear-gradient(135deg,#e8f5e9 0%,#c8e6c9 50%,#a5d6a7 100%);min-height:100vh;padding:20px}
.card{background:#fff;border-radius:20px;box-shadow:0 10px 40px rgba(0,0,0,.1);max-width:680px;margin:0 auto;overflow:hidden}
.header{background:linear-gradient(135deg,#43a047,#66bb6a);color:#fff;padding:24px 30px;text-align:center}
.header h1{font-size:24px;margin-bottom:4px}
.header .sci-name{font-size:14px;opacity:.85;font-style:italic;margin-bottom:8px}
.header .meta{display:flex;justify-content:center;gap:16px;flex-wrap:wrap}
.header .meta span{background:rgba(255,255,255,.2);padding:4px 12px;border-radius:20px;font-size:13px}
.image-section{padding:20px;text-align:center;background:#f1f8e9}
.image-section img{max-width:100%;max-height:350px;border-radius:12px;box-shadow:0 4px 15px rgba(0,0,0,.1)}
.section{padding:20px 24px}
.section h3{font-size:16px;color:#333;margin-bottom:12px;display:flex;align-items:center;gap:8px}
.care-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.care-card{background:#f8f9fa;border-radius:12px;padding:14px;border-left:4px solid #43a047}
.care-card .care-icon{font-size:20px;margin-bottom:6px}
.care-card .care-title{font-size:12px;color:#999;margin-bottom:4px}
.care-card .care-value{font-size:13px;color:#333;line-height:1.5}
.disease-card{background:#fff3e0;border-radius:10px;padding:12px;margin-bottom:8px;border-left:4px solid #ff9800}
.disease-name{font-weight:600;color:#e65100;margin-bottom:4px}
.disease-symptom,.disease-treatment{font-size:13px;color:#555;margin:2px 0}
.tip-item{background:#e8f5e9;border-radius:8px;padding:10px 14px;margin-bottom:8px;font-size:13px;color:#333;display:flex;align-items:flex-start;gap:10px}
.tip-num{background:#43a047;color:#fff;width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;flex-shrink:0}
.chart-section{padding:10px 24px 20px}
.chart-container{position:relative;height:280px}
.empty-hint{text-align:center;color:#999;padding:20px;font-size:14px}
.footer{text-align:center;padding:16px;color:#bbb;font-size:12px;border-top:1px solid #eee}
</style>
</head>
<body>
<div class="card">
<div class="header">
<h1>🌸 {{PLANT_NAME}}</h1>
<div class="sci-name">{{SCIENTIFIC_NAME}}</div>
<div class="meta">
<span>{{FAMILY}}</span><span>{{PLANT_TYPE}}</span><span>难度：{{DIFFICULTY}}</span>
</div>
</div>
<div class="image-section"><img src="{{IMAGE_SRC}}" alt="{{PLANT_NAME}}"></div>
<div class="section">
<h3>🌿 养护指南</h3>
<div class="care-grid" id="careGrid"></div>
</div>
<div class="section" id="diseaseSection">
<h3>🛡️ 病虫害防治</h3>
{{DISEASES_HTML}}
</div>
<div class="section">
<h3>💡 养护贴士</h3>
{{TIPS_HTML}}
</div>
<div class="chart-section">
<h3>📊 养护关注度雷达图</h3>
<div class="chart-container"><canvas id="careChart"></canvas></div>
</div>
<div class="footer">🌸 AI花卉识别与养护 · {{TIMESTAMP}}</div>
</div>
<script>
var careData = {{CARE_CHART_DATA}};
var cards = [
{icon:'💧',title:'浇水',val1:'{{WATER_FREQ}}',val2:'{{WATER_METHOD}}',note:'{{WATER_NOTE}}'},
{icon:'☀️',title:'光照',val1:'{{LIGHT_FREQ}}',val2:'{{LIGHT_METHOD}}',note:'{{LIGHT_NOTE}}'},
{icon:'🌡️',title:'温度',val1:'{{TEMP_FREQ}}',val2:'{{TEMP_METHOD}}',note:'{{TEMP_NOTE}}'},
{icon:'🪴',title:'土壤',val1:'{{SOIL_FREQ}}',val2:'{{SOIL_METHOD}}',note:'{{SOIL_NOTE}}'},
{icon:'🧪',title:'施肥',val1:'{{FERT_FREQ}}',val2:'{{FERT_METHOD}}',note:'{{FERT_NOTE}}'},
];
document.getElementById('careGrid').innerHTML = cards.map(function(c){
return '<div class="care-card"><div class="care-icon">'+c.icon+'</div><div class="care-title">'+c.title+'</div><div class="care-value"><b>'+c.val1+'</b><br>'+c.val2+'</div><div class="care-value" style="font-size:12px;color:#888;margin-top:4px">'+c.note+'</div></div>';
}).join('');
new Chart(document.getElementById('careChart'),{
type:'radar',
data:{labels:careData.map(function(d){return d.icon+' '+d.name}),datasets:[{label:'关注度',data:careData.map(function(d){return d.value}),backgroundColor:'rgba(67,160,71,0.15)',borderColor:'#43a047',borderWidth:2.5,pointBackgroundColor:careData.map(function(d){return d.color}),pointBorderColor:'#fff',pointBorderWidth:2,pointRadius:5}]},
options:{responsive:true,maintainAspectRatio:false,scales:{r:{min:0,max:1,ticks:{stepSize:.2,display:false}}},plugins:{legend:{display:false}}}
});
</script>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="AI花卉识别与养护")
    parser.add_argument("--image", required=True, help="植物照片路径")
    parser.add_argument("--output", default=None, help="HTML报告输出路径")
    parser.add_argument("--model", default="qwen-vl-max", help="DashScope模型名称")
    args = parser.parse_args()

    if args.output is None:
        img_stem = Path(args.image).stem
        args.output = f"flower_care_{img_stem}.html"

    api_key = find_api_key()
    if not api_key:
        print("ERROR: 未找到 API Key。请设置环境变量 DASHSCOPE_API_KEY")
        print("你可以在 https://dashscope.console.aliyun.com/ 获取 DashScope API Key")
        sys.exit(1)

    print(f"🌸 花卉识别中...")
    print(f"   图片: {args.image}")

    try:
        image_data_url, _ = encode_image(args.image)
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    try:
        api_result = call_dashscope(api_key, image_data_url, args.model)
    except RuntimeError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    result = parse_response(api_result)

    if not result.get("has_plant") and not result.get("plant_name"):
        print("⚠️ 未在图片中识别到植物，请上传清晰的花卉/植物照片")
        print(f"   API原始返回摘要: {json.dumps(result['raw'], ensure_ascii=False)[:300]}")
        sys.exit(1)

    output_path = generate_html_report(result, args.image, args.output)

    print()
    print(generate_summary(result))
    print()
    print(f"📄 报告已生成: {output_path}")
    print(f"REPORT_PATH: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    main()
