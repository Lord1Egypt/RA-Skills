---
name: canvas-workspace
description: >
  画布工作区操作能力。当需要生成图片、编辑图片、将图片推送到画布、或处理用户画布标记时激活。
  包含：(1) Qwen 图片生成/编辑案例脚本（文生图与编辑图分离，作为可复制的 MVP 模板），
  (2) 画布操作 API（推送图片、查看状态、批量注入图片），
  (3) 画布图片协议（用户标记/选中图片后的 JSON 文件解析）。
  触发场景：用户要求生图、画图、修图、把图片放到画布上、或消息中包含画布图片文件 URL。
  关键词匹配：当用户消息中出现以下关键词时应加载本 skill：
  画布、canvas、生图、生成图片、画图、绘图、修图、编辑图片、图片编辑、
  推送到画布、放到画布、添加到画布、inject、gen_image、标记、marker、
  图生图、文生图、AI生图、设计图、海报、画布图片文件、canvas_images。
metadata:
  clawdbot:
    emoji: "🎨"
    requires:
      env: ["QWEN_TEXT_IMAGE_API_KEY"]
      bins: ["python3", "npx"]
      os: ["linux", "darwin", "win32"]
    primaryEnv: "QWEN_TEXT_IMAGE_API_KEY"
    files: ["scripts/*"]
---

# 画布工作区

## !! 激活后立即执行以下流程

**当此 skill 被激活时，你必须按顺序执行以下步骤，不要跳过任何一步。**

### 步骤 1：启动画布工作区

```bash
npx deepminer-claw-canvas@latest
```

**启动过程说明**（告知用户）：
1. 首次运行会自动安装 Python 依赖（可能需要 1-2 分钟）
2. 依赖安装完成后启动服务（可能需要 10-30 秒）
3. **看到 `Application startup complete` 才表示启动成功**
4. 启动成功后会自动打开浏览器
5. 默认地址：**http://localhost:39301/claw**
6. 如果端口被占用会自动切换到下一个可用端口，**以终端输出的实际地址为准**

> 如需指定端口：`CLAW_PORT=8080 npx deepminer-claw-canvas@latest`

**重要**：
- 服务启动后保持终端运行
- 后续的 `gen`/`edit`/`push` 命令需要**在新终端中执行**
- 如果服务端口不是默认的 39301，执行脚本时需指定：`CLAW_PORT=实际端口 npx deepminer-claw-canvas@latest gen ...`

### 步骤 2：收集图片模型环境变量

**主动向用户询问**图片模型配置。必须明确说明：**生图模型** 和 **编辑图模型** 是两种用途，建议分开配置。

同时提醒用户：**如果 Claw Agent 所用底模具备多模态能力（能看图），处理图片编辑、标记理解、附件理解时效果通常更好；但这不是强制要求，是否切换模型由用户自行决定。**

对用户这样说：

> 画布的图片能力需要两类模型：**文生图模型** 和 **编辑图模型**，请分别提供对应的 API Key。
>
> 目前项目内置了 Qwen 的案例脚本，可以直接使用。如果你有 Qwen（通义万象 / DashScope）的 API Key，只需提供一个 Key 即可同时用于文生图和编辑图。
>
> 如果你想接入其他模型，可以参考内置脚本的写法，新写一个独立 Python 脚本。内置脚本在 npm 包内的 `skills/canvas-workspace/scripts/` 目录。
>
> 如果暂时没有 API Key，画布基础能力（查看状态、推送已有图片）仍可使用，但无法生成或编辑新图片。

### 步骤 3：设置环境变量

用户提供变量后，**必须设置为系统永久环境变量**，不要设置临时变量（临时变量关闭终端后就失效）。

每类模型需要三个变量：**API_KEY**（必填）、**MODEL**（模型名）、**BASE_URL**（API 地址）。

#### 使用 Qwen 案例脚本（默认）

Windows（设置永久用户环境变量）：

```powershell
[Environment]::SetEnvironmentVariable("QWEN_TEXT_IMAGE_API_KEY", "用户提供的值", "User")
[Environment]::SetEnvironmentVariable("QWEN_TEXT_IMAGE_MODEL", "qwen-image-2.0-pro", "User")
[Environment]::SetEnvironmentVariable("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/api/v1", "User")

[Environment]::SetEnvironmentVariable("QWEN_EDIT_IMAGE_API_KEY", "用户提供的值", "User")
[Environment]::SetEnvironmentVariable("QWEN_EDIT_IMAGE_MODEL", "qwen-image-edit", "User")
```

> 设置后需要**重启终端**才能生效。

Mac/Linux（追加到 ~/.bashrc 或 ~/.zshrc）：

```bash
echo 'export QWEN_TEXT_IMAGE_API_KEY="用户提供的值"' >> ~/.bashrc
echo 'export QWEN_TEXT_IMAGE_MODEL="qwen-image-2.0-pro"' >> ~/.bashrc
echo 'export QWEN_BASE_URL="https://dashscope.aliyuncs.com/api/v1"' >> ~/.bashrc

echo 'export QWEN_EDIT_IMAGE_API_KEY="用户提供的值"' >> ~/.bashrc
echo 'export QWEN_EDIT_IMAGE_MODEL="qwen-image-edit"' >> ~/.bashrc

source ~/.bashrc
```

> 如果文生图和编辑图使用同一个 Qwen Key，两个 API_KEY 填同一个值即可。
> `QWEN_BASE_URL` 有默认值，不设也行；如果用新加坡地域需改成 `https://dashscope-intl.aliyuncs.com/api/v1`。

#### 使用自定义模型

如果用户要接入其他生图/编辑图模型，需要：

1. 参考内置 Qwen 脚本（npm 包内 `skills/canvas-workspace/scripts/` 目录），新写一个 Python 脚本；
2. 在脚本中定义该模型自己的环境变量（命名建议：`{PROVIDER}_TEXT_IMAGE_API_KEY`、`{PROVIDER}_TEXT_IMAGE_MODEL`、`{PROVIDER}_BASE_URL` 等）；
3. 设置永久环境变量。

示例（假设接入 Gemini 文生图，Windows）：

```powershell
[Environment]::SetEnvironmentVariable("GEMINI_TEXT_IMAGE_API_KEY", "用户提供的值", "User")
[Environment]::SetEnvironmentVariable("GEMINI_TEXT_IMAGE_MODEL", "gemini-3.1-flash-image", "User")
[Environment]::SetEnvironmentVariable("GEMINI_BASE_URL", "https://api.example.com/v1", "User")
```

设置完成后告知用户画布已就绪，可以开始使用。

**以上 3 步完成后，画布工作区已就绪。后续用户发送的生图/编辑请求，按下方「决策指引」处理。**

---

## 决策指引

| 用户意图 | 操作 |
| --- | --- |
| 文生图（Qwen） | `npx deepminer-claw-canvas gen --prompt "..."` |
| 文生图（Gemini） | `npx deepminer-claw-canvas gen --prompt "..." --provider gemini` |
| 标记编辑（消息含画布图片文件 URL） | `npx deepminer-claw-canvas edit --prompt "..." --markers-file "<画布图片文件URL>"` |
| 自由编辑 / 图生图 / 多图融合 | `npx deepminer-claw-canvas edit --prompt "..." --raw-image <图片URL>` |
| 推送已有图片到画布 | `npx deepminer-claw-canvas push --url "..."` |
| 查看画布当前状态 | `Invoke-RestMethod -Uri "http://localhost:<端口>/api/canvas/sync/debug"` |

## 能力边界

| 允许 | 禁止 |
| --- | --- |
| 生成/编辑图片 | 删除画布上的图片 |
| 查看画布状态 | 移动、缩放、旋转画布上的图片 |
| 用 Qwen 案例脚本作为其他模型接入模板 | 在画布上添加标记（仅用户可操作） |

## Qwen 案例脚本

Qwen 脚本是 **MVP 样板**，不是统一 provider 框架。

如果未来要接别的模型：

1. 复制 Qwen 脚本结构；
2. 使用目标模型自己的 SDK；
3. 定义该模型自己的 ENV；
4. 保持相同的调用风格与输出 JSON（尽量一致）。

### 工具模块

脚本目录下提供了可复用的工具模块，用户构建自定义脚本时可直接导入使用：

| 模块 | 用途 |
| --- | --- |
| `image_to_base64.py` | 将图片地址（网络 URL 或本地路径）转为 base64 data URL |
| `push_to_canvas.py` | 将图片推送到画布（远程 URL 会自动下载转为本地 URL） |

**使用示例**（在自定义脚本中）：

```python
from image_to_base64 import image_to_base64
from push_to_canvas import push_to_canvas

# 图片转 base64，用于传给 AI 模型
base64_url = image_to_base64("https://example.com/image.png")

# 推送图片到画布（远程 URL 自动转本地，避免跨域问题）
element_id, local_url = push_to_canvas("https://example.com/result.png")
```

### 1) 文生图脚本

```bash
# 使用 Qwen（默认）
npx deepminer-claw-canvas gen --prompt "一张极简海报，蓝白配色"

# 使用 Gemini
npx deepminer-claw-canvas gen --prompt "一张极简海报" --provider gemini
```

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--prompt` | 是 | 文生图提示词 |
| `--size` | 否 | 输出尺寸，如 `1024*1024` |
| `--provider` | 否 | 模型提供商（qwen/gemini），默认 qwen |

生成的图片默认推送到画布。

### 2) 编辑图脚本

两种调用方式（互斥），生成的图片默认推送到画布：

```bash
# 标记编辑：从画布图片文件读取原图/标记图（URL 从用户消息中获取）
npx deepminer-claw-canvas edit --prompt "把<<标记点1>>修改为蓝色" --markers-file "<画布图片文件URL>"

# 自由编辑：直接传原图（URL 从用户消息中获取）
npx deepminer-claw-canvas edit --prompt "变成卡通风格" --raw-image "<图片URL>"

# 自由编辑（多图）
npx deepminer-claw-canvas edit --prompt "把图一的人物放到图二的背景上" --raw-image "img1.png" --raw-image "img2.png"
```

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--prompt` | 是 | 编辑指令 |
| `--markers-file` | 与 --raw-image 二选一 | 画布图片文件 URL 或本地路径（标记编辑模式） |
| `--raw-image` | 与 --markers-file 二选一 | 原图 URL 或本地路径，可多次传入（自由编辑模式） |

### 3) 推送图片脚本

直接将已有图片 URL 推送到画布：

```bash
npx deepminer-claw-canvas push --url "https://example.com/image.png"
```

### 输出约定

脚本输出 JSON，格式尽量一致：

```json
{"status":"ok","url":"https://...","local_url":"http://localhost:39301/uploads/...","element_id":"gen_xxx","pushed":true}
```

说明：

- `url`：AI 模型返回的原始图片 URL（可能是远程 OSS 地址）
- `local_url`：推送到画布的本地 URL（远程图片会自动下载转存）
- `element_id`：画布上的元素 ID
- `pushed`：是否成功推送到画布，`false` 表示推送失败但图片生成/编辑本身已成功

## 画布操作 API

| 接口 | 用途 |
| --- | --- |
| `POST /api/canvas/sync/gen_image` | 推送图片到画布 |
| `GET /api/canvas/sync/debug` | 查看画布状态 |
| `POST /api/canvas/sync/inject_image` | 批量注入图片 |

### API 详情

#### POST /api/canvas/sync/gen_image

推送图片到画布。

```bash
curl -X POST http://localhost:<端口>/api/canvas/sync/gen_image \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/image.png"}'
```

#### GET /api/canvas/sync/debug

查看画布当前状态（图片列表、标记等）。

```bash
curl http://localhost:<端口>/api/canvas/sync/debug
```


## 画布图片协议

用户在画布上选择图片或标记图片后发消息，消息末尾附带画布图片文件 URL。文件中包含所有与画布相关的图片信息。

消息示例：

```
请把 <<标记点1>> 修改为蓝色，参考我选中的那张图片的配色

画布图片文件: http://localhost:<端口>/uploads/canvas_images_xxx.json
```

### 文件结构

```json
{
  "canvas_markers": [
    {
      "id": "img_B",
      "raw_image": "http://localhost:<端口>/uploads/original_B.png",
      "marked_image": "http://localhost:<端口>/uploads/marked_B.png",
      "markers": [1, 2]
    }
  ],
  "selected_images": [
    {
      "id": "img_A",
      "raw_image": "http://localhost:<端口>/uploads/selected_A.png"
    }
  ]
}
```

| 字段 | 含义 |
| --- | --- |
| `canvas_markers` | 有标记的图片列表（原图 + 标记图 + 标记点编号） |
| `selected_images` | 用户选中但未标记的图片列表（仅原图） |
| `raw_image` | 无标记的原始图 URL |
| `marked_image` | 带彩色标记框的合成图 URL |
| `markers` | 标记点编号列表，对应消息中的 `<<标记点N>>` |

### 处理规则

1. 从消息末尾提取画布图片文件 URL
2. **消息中有「画布图片文件」URL** → 直接传给 `edit --markers-file <URL>`，脚本内部会自动下载和解析
3. **消息中只有普通图片 URL**（无标记） → 调用 `edit --raw-image <URL>`
4. 两者都有 → 根据用户意图决定调用方式

## 环境变量参考

### Qwen 文生图

| 环境变量 | 何时必填 | 默认值 |
| --- | --- | --- |
| `QWEN_TEXT_IMAGE_API_KEY` | 使用 Qwen 文生图时 | — |
| `QWEN_TEXT_IMAGE_MODEL` | 否 | `qwen-image-2.0-pro` |
| `QWEN_BASE_URL` | 否 | `https://dashscope.aliyuncs.com/api/v1` |

### Qwen 编辑图

| 环境变量 | 何时必填 | 默认值 |
| --- | --- | --- |
| `QWEN_EDIT_IMAGE_API_KEY` | 使用 Qwen 编辑图时 | — |
| `QWEN_EDIT_IMAGE_MODEL` | 否 | `qwen-image-edit` |

### Gemini 文生图

| 环境变量 | 何时必填 | 默认值 |
| --- | --- | --- |
| `GEMINI_TEXT_IMAGE_API_KEY` | 使用 Gemini 文生图时 | — |
| `GEMINI_TEXT_IMAGE_MODEL` | 否 | `gemini-3.1-flash-image` |
| `GEMINI_BASE_URL` | 否 | `https://api.mmw.ink` |

### 公共配置

| 环境变量 | 何时必填 | 默认值 |
| --- | --- | --- |
| `CANVAS_SERVER` | 否 | `http://localhost:<端口>`（默认 39301） |

## Windows 环境注意事项

- **`curl` 在 PowerShell 中是 `Invoke-WebRequest` 的别名**，参数不兼容。获取 HTTP 数据请使用 `Invoke-RestMethod -Uri "<URL>"`，不要用 `curl`。
- **`web_fetch` 等 MCP 工具无法访问 localhost 地址**，获取本地服务数据必须用命令行。
- 执行 shell 命令时使用 PowerShell 语法，不要使用 cmd 语法（`&` 串联命令在 PowerShell 中报错）。
- PowerShell 中文错误输出可能显示为乱码（GBK/UTF-8 编码冲突），遇到乱码时根据上下文推断含义，不要将乱码原文展示给用户。

## External Endpoints

| URL | 发送的数据 |
|-----|-----------|
| `https://dashscope.aliyuncs.com/api/v1` | Qwen 文生图/编辑图请求（prompt、图片 URL） |
| `https://api.mmw.ink` | Gemini 文生图请求（prompt） |
| `http://localhost:<端口>/api/canvas/sync/*` | 本地画布服务（图片推送、状态查询） |

## Security & Privacy

- **会离开本机的数据**：用户输入的 prompt、待编辑图片的 URL（发送至 Qwen/Gemini API）
- **不会离开本机的数据**：本地文件内容、环境变量值、画布状态数据
- 所有对外网络请求均通过 HTTPS 加密传输
- 本地画布服务仅监听 localhost，不暴露到外网

## Model Invocation Note

本 Skill 可能由 OpenClaw 在对话中自主调用，属正常行为。
如不希望自动调用，可在 OpenClaw 设置中关闭该 Skill 的自动触发权限。

## Trust Statement

使用本 Skill 时，您的 prompt 和图片 URL 将发送至阿里云 DashScope（Qwen）或第三方 Gemini 代理服务。
请仅在信任这些服务的前提下安装和使用本 Skill。
