---
name: flower-care
version: 1.0.0
description: "🌸 AI花卉识别与养护技能。上传花卉/植物照片，自动识别品种，提供浇水/光照/温度/土壤/施肥/病虫害六大维度专业养护指南，生成交互式HTML可视化报告。基于DashScope多模态大模型。覆盖观花植物/观叶植物/多肉/水生植物/藤本/木本等全品类。Triggers: 识花, 这是什么花, 花卉识别, 植物识别, 养花, 怎么养, 养护指南, 花生病了, 病虫害, 帮我看看这盆花, 植物养护, flower identification, plant care."
author: bettermen
tags: [flower, plant, identification, care-guide, dashscope, multimodal, gardening]
agent_created: true
allowed-tools: Read, Write, Bash, WebFetch
metadata:
  openclaw:
    requires:
      bins:
        - python.exe
      env:
        - DASHSCOPE_API_KEY
    emoji: "🌸"
    homepage: https://github.com/bettermen/flower-care
---

# 🌸 花卉识别与养护 Flower Care

> AI驱动的花卉识别与养护指导 | 拍照即识 | 6维养护指南 | 可视化报告

## 概述

上传任意花卉/植物照片，AI自动识别品种并生成专业养护指南。覆盖浇水、光照、温度、土壤、施肥、病虫害防治六大维度，生成包含雷达图、养护卡片和病虫害提示的交互式HTML可视化报告。

### 触发场景

- 用户说"这是什么花"、"识别一下这个植物"、"帮我看看这是什么"
- 用户说"怎么养"、"养护指南"、"这花怎么浇水"
- 用户说"花生病了"、"叶子黄了"、"长虫了"
- 用户分享植物照片并询问养护方法
- 用户询问某类植物的养护要点（可查询内置知识库）

### 核心功能

| 功能 | 说明 |
|------|------|
| 📸 拍照识花 | 上传照片，AI自动识别植物品种（含学名、科属） |
| 💚 健康评估 | 判断植物健康状态（健康/一般/较差）并预警 |
| 🌿 6维养护指南 | 浇水、光照、温度、土壤、施肥、病虫害防治 |
| 🛡️ 病虫害防治 | 识别常见病虫害，给出具体防治方案 |
| 📊 可视化报告 | Chart.js雷达图 + 养护卡片 + 健康预警 |
| 📚 内置知识库 | 60+常见植物养护数据，可离线查询 |

---

## 执行流程

### Step 1: 接收图片

用户提供图片路径或URL。如果用户没有提供路径，询问用户上传或拖拽图片。

如果用户没有图片只是询问养护知识，跳转到 Step 5 使用内置知识库回答。

### Step 2: 检查环境与 API Key

首次使用前需配置 DashScope API Key：

```bash
/c/Users/PC/.workbuddy/binaries/python/versions/3.13.12/python.exe -c "
import json, os
key = os.environ.get('DASHSCOPE_API_KEY', '')
if not key:
    cfg = os.path.expanduser('~/.workbuddy/config/dashscope.json')
    if os.path.exists(cfg):
        with open(cfg) as f:
            key = json.load(f).get('api_key', '')
print('API Key:', '已配置' if key and 'YOUR_' not in key else '未配置')
"
```

**如果未配置，两种方式设置：**

方式一（推荐）：编辑配置文件
```bash
# 编辑 C:/Users/PC/.workbuddy/config/dashscope.json
# 将 YOUR_DASHSCOPE_API_KEY_HERE 替换为实际的 API Key
```

方式二：设置环境变量
```bash
export DASHSCOPE_API_KEY="sk-xxxxxxxxxxxxx"
```

**获取 API Key：** https://dashscope.console.aliyun.com/apiKey

### Step 3: 运行花卉识别

使用技能内置脚本 `scripts/flower_care.py`：

```bash
/c/Users/PC/.workbuddy/binaries/python/versions/3.13.12/python.exe \
  /c/Users/PC/.workbuddy/skills/flower-care/scripts/flower_care.py \
  --image "<用户提供的图片路径>" \
  --output "/c/Users/PC/WorkBuddy/2026-06-18-11-18-38/flower_care_report.html"
```

**参数说明：**
| 参数 | 说明 |
|------|------|
| `--image PATH` | 植物照片路径（必填） |
| `--output PATH` | HTML报告输出路径（可选，默认当前目录） |
| `--model NAME` | DashScope模型，默认 qwen-vl-max（也可用 qwen-vl-plus） |

### Step 4: 展示结果

脚本执行完成后：
1. 在对话中展示识别结果摘要（植物名称+养护要点）
2. 使用 `present_files` 预览并交付HTML报告

### Step 5: 无需图片的养护咨询（使用内置知识库）

如果用户只是问"绿萝怎么养"、"多肉浇水频率"等，直接参考 `references/plant_care_db.md` 知识库回答，无需调用API。

知识库覆盖 60+ 常见植物，按类别索引：
- 观花植物 (#1-15)：月季、玫瑰、茉莉、栀子、兰花、蝴蝶兰等
- 观叶植物 (#16-30)：绿萝、吊兰、虎皮兰、龟背竹、琴叶榕等
- 多肉植物 (#31-33)：多肉通用、仙人掌、玉露
- 香草/食用 (#34-36)：薄荷、迷迭香、薰衣草
- 其他：水生植物、空气净化植物、年宵花、藤本、盆景、网红植物

查询方式：用 `grep` 在知识库中搜索植物名：
```bash
grep -A 10 "^### .*绿萝" /c/Users/PC/.workbuddy/skills/flower-care/references/plant_care_db.md
```

---

## API 配置

脚本自动从以下位置读取 DashScope API Key（按优先级）：

1. 环境变量 `DASHSCOPE_API_KEY`
2. 环境变量 `OPENAI_API_KEY`（兼容模式）
3. 配置文件 `~/.workbuddy/config/dashscope.json`

**DashScope API 端点：**
```
POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
Model: qwen-vl-max (推荐，识别最准确) 或 qwen-vl-plus (更快更省)
```

---

## 养护维度说明

| 维度 | Emoji | 说明 |
|------|-------|------|
| 浇水 💧 | | 浇水频率、方法、注意事项 |
| 光照 ☀️ | | 光照需求、每日时长、摆放位置 |
| 温度 🌡️ | | 适宜范围、最低/最高耐受、季节调整 |
| 土壤 🪴 | | 土壤类型、酸碱度、透气排水要求 |
| 施肥 🧪 | | 施肥频率、肥料类型、休眠期停肥 |
| 病虫害 🛡️ | | 常见病害、典型症状、防治药剂和方法 |

---

## 独立使用（直接调用 API）

不运行脚本时，可直接用以下代码调用 DashScope API 进行花卉识别：

```python
import base64, json, os
import urllib.request

def identify_flower(image_path):
    api_key = os.environ.get("DASHSCOPE_API_KEY", "")
    if not api_key:
        cfg = os.path.expanduser("~/.workbuddy/config/dashscope.json")
        if os.path.exists(cfg):
            with open(cfg) as f:
                api_key = json.load(f).get("api_key", "")

    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    ext = os.path.splitext(image_path)[1].lower()
    mime_map = {".jpg": "jpeg", ".jpeg": "jpeg", ".png": "png", ".webp": "webp"}
    mime = mime_map.get(ext, "jpeg")

    prompt = """你是一位资深园艺师。请识别图片中的植物并提供养护建议。
返回JSON：{"plant_name":"","scientific_name":"","family":"","plant_type":"",
"health_status":"健康/一般/较差","difficulty":"容易/中等/较难",
"water":{"frequency":"","method":"","note":""},
"light":{"requirement":"","hours":"","note":""},
"temperature":{"range":"","min":"","note":""},
"soil":{"type":"","ph":"","note":""},
"fertilizer":{"schedule":"","type":"","note":""},
"diseases":[{"name":"","symptom":"","treatment":""}],
"tips":[""],"description":"",
"care_score":{"watering":0.5,"light":0.5,"temperature":0.5,"soil":0.5,"fertilizer":0.5,"pest_control":0.5}}"""

    payload = json.dumps({
        "model": "qwen-vl-max",
        "messages": [{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/{mime};base64,{img_b64}"}},
            {"type": "text", "text": prompt}
        ]}],
        "temperature": 0.3, "max_tokens": 1500
    }).encode()

    req = urllib.request.Request(
        "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())
```

---

## 文件结构

```
flower-care/
├── SKILL.md                       # 本文件
├── scripts/
│   └── flower_care.py             # 主脚本：图片→API→报告
├── assets/
│   └── report_template.html       # HTML报告模板（含雷达图+养护卡片）
└── references/
    └── plant_care_db.md           # 60+常见植物养护知识库
```

---

## 常见问题

**Q: 识别不准确怎么办？**
- 确保照片清晰、光线充足，花朵/叶片特征明显
- 尽量包含花朵和叶片，多角度拍摄效果更好
- 避免背景过于杂乱

**Q: API Key 从哪里获取？**
- 访问 https://dashscope.console.aliyun.com/apiKey
- 新用户有免费额度
- qwen-vl-max 约 ¥0.003/千tokens，识别一张图约消耗 1000-2000 tokens

**Q: 没有图片也能用吗？**
- 可以！直接说出植物名称（如"绿萝怎么养"），会从内置知识库查询养护指南
