---
name: doubao-maliang-image-gen
description: 小马良-豆包生图。Generate images with Doubao Seedream via Volcano Engine ARK. Supports Seedream 5.0 and other models. Use when the user invokes 小马良 or requests Doubao/Seedream/Volcano ARK image generation.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨",
        "requires": { "bins": ["python3"], "env": ["VOLCANO_ENGINE_API_KEY"] },
        "primaryEnv": "VOLCANO_ENGINE_API_KEY",
        "homepage": "https://github.com/JoannaXing/doubao-maliang-image-gen",
        "license": "MIT"
      },
  }
---

# 小马良-豆包生图 / Maliang Doubao Image Gen

> 🖌️ **关于「马良」**: 名字源自中国神话故事《神笔马良》—— 马良拥有一支神笔，画什么就会变成真的。这个 skill 就是你的「神笔」，用文字描绘，让 AI 为你生成图像。
> 
> 🖌️ **About "Maliang"**: Named after the Chinese legend *Shenbi Maliang* (Magic Brush Ma Liang) — who possessed a magic brush that brought drawings to life. This skill is your magic brush: describe with words, let AI generate the image.

基于火山引擎方舟 ARK 平台的豆包 Seedream 文生图服务。

Powered by Doubao Seedream text-to-image service via Volcano Engine ARK platform.

**默认模型 / Default Model**: `doubao-seedream-5-0-260128` (Seedream 5.0)

---

## ✨ 核心特色 / Key Features

1. **一键生图，自动回传 / One-Click Generation, Auto-Reply**
   
   在聊天窗口直接呼唤马良，描述你想要的图片，生成完成后**自动将图片发送回聊天界面**，无需手动查找文件。
   
   Simply invoke Maliang in chat, describe what you want, and the generated image is **automatically sent back to the chat window** — no need to manually locate files.

2. **本地备份 + 画廊 / Local Backup + Gallery**
   
   图片同时保存到本地，并生成可视化画廊页面，方便管理和回顾。
   
   Images are also saved locally with a visual gallery page for easy management and review.

---

## 🚀 快速开始 / Quick Start

### 1. 配置 API Key / Configure API Key

**推荐：使用 Skill 环境变量 / Recommended: Skill Environment Variables**

在 OpenClaw 配置中为该 skill 设置环境变量：
Set environment variables in OpenClaw config for this skill:

```json
{
  "skills": {
    "doubao-maliang-image-gen": {
      "env": {
        "VOLCANO_ENGINE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

文件位置 / File location: `~/.openclaw/config.json`

**替代方式：系统环境变量 / Alternative: System Environment Variables**

```bash
export VOLCANO_ENGINE_API_KEY="your-api-key-here"
```

**兼容的变量名 / Compatible Variable Names**（按优先级 / in priority order）：
- `VOLCANO_ENGINE_API_KEY` （推荐 / recommended）
- `ARK_API_KEY`
- `SEEDREAM_API_KEY`

> ⚠️ **安全提示 / Security Note**: 永远不要将 API key 直接写在命令行参数或脚本里。使用环境变量避免密钥泄露。
> 
> Never write API keys directly in command line arguments or scripts. Use environment variables to prevent credential leaks.

### 2. 获取 API Key / Get API Key

**中文步骤：**
1. 访问 [火山方舟控制台](https://console.volcengine.com/ark/)
2. 创建或进入已有项目
3. 在「API Key 管理」中创建新密钥
4. 开通「图像生成」权限（Doubao Seedream 模型）

**English Steps:**
1. Visit [Volcano Engine ARK Console](https://console.volcengine.com/ark/)
2. Create or enter an existing project
3. Create a new key in "API Key Management"
4. Enable "Image Generation" permission for Doubao Seedream model

---

## 🎯 触发条件 / When to Use

使用本 skill 的场景（中英文均可触发）：
Use this skill when (works in both Chinese and English):

- 用户点名 **小马良** / User invokes **Maliang**
  - 可触发关键词 / Trigger words: "小马良", "马良", "Maliang", "Little Maliang"
  
- 用户明确要求使用 **豆包 / Doubao / Seedream / 火山方舟 / Volcano ARK** 生图
  - 可触发关键词 / Trigger words: "豆包", "Doubao", "Seedream", "火山方舟", "Volcano ARK", "Volcano Engine"
  
- 用户希望图片生成走 Maliang 路径 / User requests the Maliang image generation path

> 💡 **提示 / Tip**: 无论用中文还是英文呼唤，马良都能听懂！
> 
> Maliang understands both Chinese and English invocations!

---

## 💬 使用示例 / Usage Examples

**中文示例：**

> 用户：小马良，帮我画一只穿着宇航服的猫咪，在月球上散步，卡通风格
> 
> 马良：✨ 已为你生成图片！（图片自动发送到聊天窗口）

**English Example:**

> User: Maliang, draw me a cat in an astronaut suit walking on the moon, cartoon style
> 
> Maliang: ✨ Here's your image! (Image automatically sent to chat)

**更多示例 / More Examples:**

| 场景 / Scenario | 对话示例 / Chat Example |
|--------------|---------------------|
| 产品设计 / Product Design | "马良，帮我生成一个极简风格的咖啡杯产品图，白色背景，柔和光线" |
| 插画创作 / Illustration | "小马良，画一幅赛博朋克风格的城市夜景，霓虹灯，雨天街道" |
| 头像生成 / Avatar | "马良，给我生成一张卡通风格的程序员头像，戴眼镜，友善的表情" |
| 概念图 / Concept Art | "帮我画一片秋日森林，金色阳光透过树叶，风景摄影风格" |

---

## 💡 Prompt 建议 / Prompt Tips

豆包 Seedream 支持多种风格描述，建议包含：
Doubao Seedream supports various style descriptions. Recommended elements:

| 要素 / Element | 说明 / Description | 示例 / Example |
|--------------|------------------|--------------|
| **主体 / Subject** | 画面中有什么 / What's in the image | a vintage sports car |
| **场景 / Scene** | 环境、背景 / Environment, background | on a coastal highway at dusk |
| **风格 / Style** | 摄影、插画、3D 等 / Photography, illustration, 3D, etc. | cinematic photography |
| **构图 / Composition** | 近景、全景等 / Close-up, wide shot, etc. | wide-angle shot |
| **光线/色调 / Lighting/Color** | 光线、色彩 / Light, color scheme | golden hour lighting, warm tones |
| **质感 / Texture** | 材质 / Material quality | glossy metallic finish |

**示例 / Example:**
> "Editorial fashion portrait, model in seafoam silk dress, gold jewelry, soft natural window light, clean beige background, high-end magazine style"

---

## 📤 输出说明 / Output Structure

图片会同时输出到两个地方：
Images are delivered to two places simultaneously:

1. **聊天窗口 / Chat Window** — 生成完成后**自动发送**到当前对话 ✨
   
2. **本地文件夹 / Local Folder**：

```
~/.openclaw/workspace/tmp/doubao-maliang-image-gen-<timestamp>/
├── <prompt-slug>-1.png    # 生成的图片 / Generated image
├── manifest.json          # 生成记录（包含 prompt、模型、时间戳）/ Generation record
└── index.html             # 本地画廊页面 / Local gallery page
```

---

## 🔧 技术细节 / Technical Details

### 命令行生成 / CLI Generation

如果需要通过命令行直接生成（而非聊天触发）：
If you need to generate via command line (instead of chat invocation):

**基础用法 / Basic Usage：**
```bash
python3 "$SKILL_DIR/scripts/gen.py" --prompt "a serene mountain landscape at sunset"
```

**多图生成 / Multiple Images：**
```bash
python3 "$SKILL_DIR/scripts/gen.py" --prompt "minimalist coffee cup product shot" --count 2
```

**指定尺寸 / Specify Size：**
```bash
python3 "$SKILL_DIR/scripts/gen.py" --prompt "cyberpunk city street" --size 1K
# 支持 / Supported: 1K (1024x1024), 2K (2048x2048)
```

### 切换模型 / Switch Models

#### 通过环境变量（全局）/ Via Environment Variables (Global)
```bash
export SEEDREAM_MODEL="doubao-seedream-5-0-260128"
export SEEDREAM_API_ENDPOINT="https://ark.cn-beijing.volces.com/api/v3/images/generations"
```

#### 通过命令行参数（单次）/ Via Command Line (One-time)
```bash
python3 "$SKILL_DIR/scripts/gen.py" \
  --prompt "abstract art composition" \
  --model "doubao-seedream-5-0-260128" \
  --endpoint "https://ark.cn-beijing.volces.com/api/v3/images/generations"
```

#### 支持的模型 / Supported Models

| 模型 ID / Model ID | 说明 / Description |
|-------------------|-------------------|
| `doubao-seedream-5-0-260128` | Seedream 5.0 (默认 / default) |

> 如需使用其他模型，请先在方舟控制台开通对应模型的调用权限。
> 
> To use other models, please enable the corresponding model permissions in the ARK console first.

### API 信息 / API Info

- **API 端点 / API Endpoint**: `https://ark.cn-beijing.volces.com/api/v3/images/generations`
- **协议 / Protocol**: OpenAI-compatible HTTP API
- **默认尺寸 / Default Size**: 2K (2048x2048)
- **单次最大数量 / Max per Request**: 4 张 / images
- **超时设置 / Timeout**: 300 秒 / seconds

---

## 🐛 故障排除 / Troubleshooting

| 问题 / Issue | 解决方案 / Solution |
|-------------|-------------------|
| "Missing API key" | 检查 VOLCANO_ENGINE_API_KEY 环境变量是否设置 / Check if VOLCANO_ENGINE_API_KEY env var is set |
| "API failed (401)" | API Key 无效或过期，检查密钥是否正确 / API Key invalid or expired |
| "API failed (429)" | 请求过于频繁，稍后重试 / Too many requests, retry later |
| "no images returned" | 检查 prompt 是否为空或包含违规内容 / Check if prompt is empty or contains prohibited content |

---

## License

MIT
