---
name: blueai-nano-banana
version: 0.1.0
description: 通过蓝标 BlueAI Relay 调用 Nano Banana / Gemini image preview 系列模型生成图片。一行命令：传入 prompt 和模型名，输出 PNG 到本地路径。适用场景：moodboard 出图、海报草图、社媒素材、demo 占位图、小红书/公众号配图、PPT 配图、产品视觉脑暴等需要"prompt → 图片"的轻量出图任务。底层走 BlueAI Relay（OpenAI 兼容 chat/completions 接口，模型返回 base64 PNG）。配合 blueai-media-storage 可一气呵成本地出图 → 上云拿公网 URL → 项目代码 src 引用。NOT for：高保真商业大图（用 Midjourney/DALL-E）、视频生成、图片编辑（Photoshop API）。NOT a replacement for 用户自己的 OpenAI/Gemini API key 直连——本 skill 强制走蓝标 relay 用部门统一额度。触发词：生图 / 出图 / 画一张 / nano banana / gemini 出图 / 给我一张图 / moodboard 图 / 配图 / 海报草图。
---

# BlueAI Nano Banana - 部门统一生图入口

蓝标内部所有 prompt → 图片任务的标准入口，走 BlueAI LLM Relay，使用部门统一额度。

## 谁该用

- 龙虾 / OpenClaw agent 需要在工作流里出图
- 项目 demo 需要快速占位图
- 内容策划脑暴 moodboard
- 给设计师准备视觉参考底稿（**不是终稿**——终稿走专业出图工具）

## 凭证

读 `~/.openclaw/.env`：

```
BLUEAI_RELAY_BASE=https://bmc-llm-relay.bluemediagroup.cn
BLUEAI_RELAY_KEY=sk-...
```

**没有这两个 key 时**：联系金明（@Dr-xiaoming）申领额度。**不要自己改 token，不要把 token 写进代码或 commit。**

## 用法

### 单图

```bash
set -a; source ~/.openclaw/.env; set +a
python3 ~/.openclaw/workspace/skills/blueai-nano-banana/scripts/gen-image.py \
  /tmp/out.png \
  gemini-3.1-flash-image-preview \
  "一只在赛博朋克城市天台上吃竹子的熊猫，霓虹灯反射在毛上，电影感打光"
```

输出：`OK /tmp/out.png (1,234,567 bytes, model=gemini-3.1-flash-image-preview, usage=1234 tokens)`

### 配合 blueai-media-storage 上云拿 URL

```bash
set -a; source ~/.openclaw/.env; set +a

# 1. 出图
python3 ~/.openclaw/workspace/skills/blueai-nano-banana/scripts/gen-image.py \
  /tmp/moodboard-01.png \
  gemini-3.1-flash-image-preview \
  "<prompt>"

# 2. 上云拿 URL
URL=$(python3 ~/.openclaw/workspace/skills/blueai-media-storage/scripts/upload.py \
  --target TOS --task-name moodboard /tmp/moodboard-01.png | jq -r '.url')

# 3. 项目代码里直接放 $URL
echo "$URL"
```

### 批量出图（shell 循环）

```bash
set -a; source ~/.openclaw/.env; set +a
for i in 1 2 3; do
  python3 ~/.openclaw/workspace/skills/blueai-nano-banana/scripts/gen-image.py \
    "/tmp/concept-${i}.png" \
    gemini-3.1-flash-image-preview \
    "concept ${i}: 极简主义产品摄影，白色背景，柔光"
done
```

## 支持的模型

| 模型名 | 用途 | 速度 |
|---|---|---|
| `gemini-3.1-flash-image-preview` | 默认推荐，质量/速度平衡 | 快 |
| `gemini-2.5-flash-image-preview` | 老版本，兼容性场景 | 快 |
| `nano-banana` | Google 官方 alias | 快 |

模型名透传到 BlueAI Relay，新模型上线后无需改 skill 即可使用。

## 失败排查

| 现象 | 原因 | 处理 |
|---|---|---|
| `RuntimeError: BLUEAI_RELAY_KEY not set` | `.env` 没加载或没 key | `set -a; source ~/.openclaw/.env; set +a` |
| HTTP 401 / 403 | key 失效或过期 | **联系金明**，不要自己换 |
| HTTP 429 | rate limit | 等 60s 重试，或换模型 |
| `could not extract base64` | 模型返回了文字而非图片（prompt 触发安全策略） | 改 prompt，去掉敏感词 |
| 超时 (180s) | relay 慢 / 大模型排队 | 重试，或换 flash 模型 |

## 红线

- ❌ **不要把 RELAY_KEY 写进代码** —— 永远从 `.env` 读
- ❌ **不要在 commit / PR / 聊天回复里复述 key 原值**
- ❌ **不要用本 skill 出商业终稿** —— 用 Midjourney / DALL-E / 设计师手作
- ❌ **不要批量大规模刷量** —— 部门统一额度，被薅干会影响所有人
- ✅ **使用前先 `clawhub update --all`** —— 同步最新版本

## 与其他 skill 的关系

- **blueai-media-storage** —— 出图后上云的下一步，强配套
- **catl-harness-pr** —— 出图给宁德项目用时，源文件可以走 PR 入档
- **canvas / meme-maker** —— 这些是图片"加工"，本 skill 是图片"生成"

## CHANGELOG

### v0.1.0 (2026-05-25)

- 初始封装，从 `~/.openclaw/workspace/scripts/gen-image.py` 提取
- RELAY_KEY 从硬编码改为读 `~/.openclaw/.env` 环境变量
- 三种 base64 提取格式兼容：data URL / 裸 base64 / JSON 包裹
- 默认 timeout 180s
