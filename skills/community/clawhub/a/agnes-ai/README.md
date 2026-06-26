# agnes-ai

AI Agent 技能 — 封装 Agnes AI 的图像与视频生成能力，OpenAI 兼容协议。
适用于任何支持 Skill 机制的 AI Agent 平台（WorkBuddy、OpenClaw、Hermes 等）。

> 具体可看：https://mp.weixin.qq.com/s/YKNlgJfTfNlPGGrzRFoEUA

## 功能

- **文生图**：通过自然语言描述生成图片，默认模型 `agnes-image-2.1-flash`（高密度图像优化）
- **图生图**：根据提示词对现有图像进行转换或优化，模型 `agnes-image-2.0-flash`
- **多图合成**：将多张参考图合成为一张新图像，模型 `agnes-image-2.0-flash`
- **文生视频**：通过自然语言描述生成视频，模型 `agnes-video-v2.0`（异步生成，自动轮询等待结果）

## 模型选择策略

| 用户意图 | 使用模型 | 说明 |
|---|---|---|
| 文生图（默认） | `agnes-image-2.1-flash` | 高密度图像优化，适合复杂视觉细节 |
| 图生图 / 图像编辑 | `agnes-image-2.0-flash` | 支持构图保持、风格迁移 |
| 多图合成 | `agnes-image-2.0-flash` | 支持多张参考图输入 |
| 文生视频 | `agnes-video-v2.0` | 异步生成，自动轮询 |

## 安装

### 自动安装（推荐）

给 Agent 发 Prompt：

```bash
安装skill：https://github.com/songxf1024/skills/tree/main/agnes-ai
```

### 手动安装

将本目录放置到你的 AI Agent 的 skills 目录下：

```
agnes-ai/
├── SKILL.md              # 技能定义（触发条件、调用流程）
├── README.md             # 本文件
├── scripts/
│   └── generate.py       # 命令行工具（纯标准库，零依赖）
└── references/
    └── api.md            # API 端点参考文档
```

**各平台安装路径**

| 平台 | 技能目录 |
|---|---|
| WorkBuddy | `~/.workbuddy/skills/` |
| OpenClaw / Hermes | 按其约定的 skills 目录 |
| 通用 | 克隆到任意目录，确保 AI Agent 能访问 `scripts/generate.py` |

## 配置 API Key

> 先登录 https://apihub.agnes-ai.com 获取 API Key

### 自动配置

给 Agent 发 Prompt：

```bash
agnes key是sk-GqbtQSGGxxxx
```

### 手动配置

**方法 1：环境变量（推荐）**

```bash
export AGNES_API_KEY="你的API密钥"
```

**方法 2：配置文件**

将 Key 写入本地文件：

```bash
mkdir -p ~/.agnes-ai
echo "你的API密钥" > ~/.agnes-ai/api_key
```

> 优先级：环境变量 > `~/.agnes-ai/api_key` > `scripts/api_key`（脚本同级目录）

## 使用方式

### 在 AI Agent 对话中使用

安装后直接在对话中下达指令，技能会自动触发：

| 你说的 | 发生的事情 |
|---|---|
| "用 Agnes 生成一张日落海景图" | → 调用 `agnes-image-2.1-flash`（文生图） |
| "用这张图生成赛博朋克风格" + 上传图片 | → 调用 `agnes-image-2.0-flash`（图生图） |
| "把这两张图合成一个战斗场景" + 上传两张图 | → 调用 `agnes-image-2.0-flash`（多图合成） |
| "用 Agnes 做一个 5 秒的星空延时视频" | → 调用 `agnes-video-v2.0` |

### 命令行直接调用

```bash
# 文生图（默认 agnes-image-2.1-flash）
python3 scripts/generate.py image \
  --prompt "A serene mountain landscape at sunset" \
  --size 1024x1024 \
  --output sunset.png

# 图生图（自动使用 agnes-image-2.0-flash）
python3 scripts/generate.py image \
  --prompt "Transform to cyberpunk style, neon lights, night scene" \
  --image https://example.com/input.png \
  --size 1024x768 \
  --output output.png

# 多图合成（agnes-image-2.0-flash）
python3 scripts/generate.py image \
  --prompt "Combine characters into a battle scene" \
  --image url1 url2 \
  --output combined.png

# 生成视频
python3 scripts/generate.py video \
  --prompt "A drone flying over a city skyline" \
  --duration 5 \
  --output skyline.mp4
```

### 图片尺寸

| 尺寸 | 方向 |
|---|---|
| `1024x1024` | 正方形（默认） |
| `1792x1024` | 横版 |
| `1024x1792` | 竖版 |
| `1024x768` | 宽屏（自定义） |
| `768x1024` | 长竖版（自定义） |

## Prompt 编写建议

### 文生图（agnes-image-2.1-flash）

推荐使用结构化 Prompt：

```
[主体] + [场景/环境] + [风格] + [光照] + [构图] + [质量要求]
```

示例：

```
A futuristic city marketplace filled with flying vehicles, holographic signs, dense crowds, neon lighting, cinematic realism, ultra-detailed, high-information-density composition
```

### 图生图（agnes-image-2.0-flash）

明确描述需要改变的内容和需要保持不变的内容：

```
把场景转换成雨夜赛博朋克风格，霓虹倒影，同时保持原始构图和主要主体不变。
```

## 依赖

- Python 3.8+（纯标准库，零外部依赖）
- 有效的 Agnes AI API Key

## API 地址

```
https://apihub.agnes-ai.com/v1
```

## 安全

- 仅向 Agnes AI 官方 API 地址（`apihub.agnes-ai.com`）发起请求
- API Key 仅存储于本地，不会上传至任何第三方
- 零外部依赖，代码完全透明
