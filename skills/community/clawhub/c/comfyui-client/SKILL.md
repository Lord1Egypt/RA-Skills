---
name: comfyui-client
description: 此技能应在用户需要通过 ComfyUI 生成图片或视频时使用。支持加载工作流、修改 prompt、提交任务、轮询结果并自动下载生成的图片和视频。需 ComfyUI 服务已启动。
version: 1.2.0
author: agent-js
---

# ComfyUI 工作流客户端

## 概述

本技能封装了 ComfyUI 工作流调用能力，用于通过 ComfyUI API 生成图片和视频。核心功能包括：加载工作流 JSON、修改 prompt 和图片节点、提交到 ComfyUI 队列、轮询任务状态、自动下载生成结果。

**适用场景：**
- 用户要求根据文本描述生成图片
- 用户要求根据参考图生成变体或编辑
- 用户要求生成图片转视频、图生视频
- 需要批量或自动化调用 ComfyUI 工作流

**前置条件：**
- ComfyUI 服务已启动（默认 `http://127.0.0.1:8188`）
- 工作流 JSON 文件可用
- 工作流所需模型已安装到 ComfyUI

## 触发条件

当满足以下条件时应使用此技能：

1. **用户表达生成意图**
   - 要求"用 ComfyUI 生成图片"、"根据 prompt 画图"
   - 要求"图生图"、"图片编辑"、"生成视频"
   - 提供文本描述并希望得到 AI 生成的图像

2. **技术上下文明确**
   - 用户提到 ComfyUI、工作流、txt2img、img2img 等
   - 用户提供工作流文件路径或项目内已知工作流

3. **服务可用**
   - 可先检查 ComfyUI 服务是否可访问
   - 若不可用，应提示用户启动 ComfyUI

## 捆绑资源

**脚本：** `scripts/comfyUIClient.js` - ComfyUI 工作流调用主脚本

**工作流：** `assets/workflows/` - 5 个常用工作流（Z-Image、Qwen 编辑、Wan 视频等）

**执行方式：**
- 技能内脚本：`node .claude/skills/comfyui-client/scripts/comfyUIClient.js [选项]`
- 项目脚本（等效）：`node scripts/comfyUIClient.js [选项]`

**路径解析：** 技能内脚本会自动解析项目根目录，工作流路径和输出目录支持相对路径（相对于项目根）。

## 核心能力

### 1. 文生图（txt2img）

使用文本 prompt 生成图片。

**基本用法：**
```bash
node scripts/comfyUIClient.js --workflow <工作流路径> --prompt "<提示词>"
```

**示例：**
```bash
# 使用技能内工作流（推荐）
node .claude/skills/comfyui-client/scripts/comfyUIClient.js \
  --workflow .claude/skills/comfyui-client/assets/workflows/image_z_image_turbo.json \
  --prompt "a beautiful landscape at sunset"

# 带负面提示词
node .claude/skills/comfyui-client/scripts/comfyUIClient.js \
  --workflow .claude/skills/comfyui-client/assets/workflows/image_z_image_turbo.json \
  --prompt "a beautiful landscape at sunset" \
  --negative-prompt "blurry, low quality, watermark"
```

**自动查找 prompt 节点：** 若不指定 `--prompt-node`，脚本会自动查找工作流中标题含 "Positive" 的 `CLIPTextEncode` 节点注入正面 prompt，标题含 "Negative" 的节点用于负面 prompt。对于 `TextEncodeQwenImageEditPlus`，优先选择有非空文本或标题含 "Positive" 的节点。

### 2. 指定 prompt 节点

当工作流中有多个 CLIPTextEncode 节点时，可指定要修改的节点 ID。

```bash
node scripts/comfyUIClient.js --workflow <工作流路径> --prompt-node "45" --prompt "新的提示词"
```

### 3. 图生图 / 图片编辑（img2img）

需要提供输入图片。可使用 `--image-path` 指定本地路径（自动上传到 ComfyUI），或先将图片放入 ComfyUI 的 `input/` 目录后使用 `--image-file` 指定文件名。

#### 3a. Z-Image Turbo + ControlNet（结构引导重绘）

基于 Canny 边缘检测提取输入图片轮廓，用 ControlNet 引导模型生成新图。适合风格转换、基于轮廓的重绘。

- **输入**：1 张图片 + 文本 prompt
- **速度**：快（9 步，CFG=1）
- **LoadImage 节点 ID**：`58`
- **Prompt 节点**：自动查找（子图内部 CLIPTextEncode 会被展开到顶层）

```bash
# 使用 --image-path 自动上传本地图片（推荐）
node .claude/skills/comfyui-client/scripts/comfyUIClient.js \
  --workflow .claude/skills/comfyui-client/assets/workflows/image_z_image_turbo_fun_union_controlnet.json \
  --prompt "oil painting style, vibrant colors" \
  --image-node 58 --image-path "path/to/input_photo.png"

# 或使用已上传到 ComfyUI input/ 的图片
node .claude/skills/comfyui-client/scripts/comfyUIClient.js \
  --workflow .claude/skills/comfyui-client/assets/workflows/image_z_image_turbo_fun_union_controlnet.json \
  --prompt "oil painting style, vibrant colors" \
  --image-node 58 --image-file "input_photo.png"
```

> 注意：该工作流使用子图（subgraph），脚本会自动展开子图内部节点。

#### 3b. Qwen 图片编辑（语义级多图编辑）

基于 Qwen 视觉语言模型的智能编辑。支持自然语言编辑指令和最多 3 张参考图片。适合材质替换、风格迁移、多图参考编辑。

- **输入**：1-3 张图片 + 自然语言编辑指令
- **速度**：中等（20 步，CFG=4）
- **LoadImage 节点 ID**：主图 `41`，参考图2 `83`，参考图3 `87`（默认禁用）
- **Prompt 节点 ID**：正面 `68`，负面 `69`
- 可选 Lightning LoRA 加速到 4 步（节点 74，默认禁用）

```bash
# 单图编辑
node .claude/skills/comfyui-client/scripts/comfyUIClient.js \
  --workflow .claude/skills/comfyui-client/assets/workflows/image_qwen_image_edit_2511.json \
  --prompt-node 68 --prompt "将背景改为海边夕阳" \
  --image-node 41 --image-file "sofa.png"

# 多图材质替换（图1 主图 + 图2 参考材质）
node .claude/skills/comfyui-client/scripts/comfyUIClient.js \
  --workflow .claude/skills/comfyui-client/assets/workflows/image_qwen_image_edit_2511.json \
  --prompt-node 68 --prompt "Change the furniture leather in image 1 to the fur material in image 2." \
  --image-node 41 --image-file "leather_sofa.png" \
  --image-node2 83 --image-file2 "texture_fur.png"
```

> 注意：Qwen Edit 工作流的 prompt 节点不是 CLIPTextEncode，需使用 `--prompt-node 68` 明确指定。

#### 3c. 两种图片编辑工作流如何选择

| 维度 | **Qwen 图片编辑** | **Z-Image Turbo + ControlNet** |
|------|------------------|--------------------------------|
| 技术路线 | Qwen 视觉语言模型，语义理解 | Canny 边缘 + ControlNet 结构引导 |
| 输入 | 1–3 张图 + 自然语言指令 | 1 张图 + 文本 prompt |
| 速度 | 较慢（约 20 步） | 快（9 步） |
| 结构保持 | 依赖模型理解，可能变化 | 强约束，轮廓基本不变 |

**Qwen 编辑适用场景：**
- 材质替换（如「把图 1 的皮质换成图 2 的毛绒材质」）
- 多图参考编辑（主图 + 1–2 张参考图）
- 语义级修改（背景、颜色、风格等需理解图像内容的编辑）
- 自然语言编辑指令（支持「将背景改为海边夕阳」等描述）

**ControlNet 适用场景：**
- 风格转换（保持轮廓，只改风格，如照片→油画、素描）
- 轮廓重绘（基于边缘线生成新图，构图基本不变）
- 线稿上色、结构保持的变体
- 追求速度、快速出图

**快速选择：**
- 需要**理解图像内容**做语义修改 → 选 **Qwen 编辑**
- 需要**保持构图/轮廓**做风格转换 → 选 **ControlNet**

### 4. 视频生成

支持 img2video、flf2video 等工作流。视频生成耗时较长，建议适当增加超时时间。

```bash
node .claude/skills/comfyui-client/scripts/comfyUIClient.js --workflow .claude/skills/comfyui-client/assets/workflows/video_wan2_2_14B_i2v.json --prompt "视频描述" --timeout 900
```

## 命令行选项

| 选项 | 说明 | 默认值 |
|-----|------|--------|
| `--workflow <file>` | 工作流 JSON 文件路径（必需） | - |
| `--server <url>` | ComfyUI 服务器地址 | `http://127.0.0.1:8188` |
| `--client-id <id>` | 客户端 ID | 自动生成 |
| `--prompt-node <node_id>` | 要修改的 prompt 节点 ID | 自动查找 |
| `--prompt <text>` | 新的 prompt 文本 | - |
| `--negative-prompt-node <node_id>` | 负面 prompt 节点 ID | 自动查找 |
| `--negative-prompt <text>` | 负面 prompt 文本 | - |
| `--image-node <node_id>` | 主图 LoadImage 节点 ID | - |
| `--image-file <filename>` | 主图已上传文件名（或上传后的目标名） | - |
| `--image-path <path>` | 主图本地路径，将自动上传 | - |
| `--image-node2 <node_id>` | 第二张参考图 LoadImage 节点 ID | - |
| `--image-file2 <filename>` | 第二张参考图已上传文件名 | - |
| `--image-path2 <path>` | 第二张图本地路径，将自动上传 | - |
| `--image-node3 <node_id>` | 第三张参考图 LoadImage 节点 ID | - |
| `--image-file3 <filename>` | 第三张参考图已上传文件名 | - |
| `--image-path3 <path>` | 第三张图本地路径，将自动上传 | - |
| `--output-dir <dir>` | 输出目录 | `./work_dir/comfyui_output` |
| `--session-name <name>` | 会话名称 | 自动生成时间戳 |
| `--timeout <seconds>` | 超时时间（秒） | 600 |
| `--poll-interval <ms>` | 轮询间隔（毫秒） | 1000 |
| `--help` | 显示帮助信息 | - |

## 环境变量

- `COMFYUI_SERVER_URL` - ComfyUI 服务器地址，可覆盖 `--server` 默认值

## 输出结构

每次执行会创建独立会话目录：

```
work_dir/comfyui_output/
└── comfyui_<时间戳>/
    ├── session_info.json    # 会话配置信息
    ├── workflow.json        # 实际提交的工作流（含修改后参数）
    ├── result.json          # 执行结果（prompt_id、生成文件列表等）
    ├── <nodeId>_<filename>  # 生成的图片/视频文件
    └── error.json          # 失败时的错误信息（如有）
```

## 捆绑工作流（assets/workflows）

本技能在 `assets/workflows/` 目录下捆绑了常用工作流，优先使用：

| 工作流 | 路径 | 用途 | Prompt 节点 | Image 节点 |
|-------|------|------|------------|-----------|
| z_image_turbo | `.claude/skills/comfyui-client/assets/workflows/image_z_image_turbo.json` | 文生图（快速出图，9 步） | 自动 | - |
| z_image_turbo_controlnet | `.claude/skills/comfyui-client/assets/workflows/image_z_image_turbo_fun_union_controlnet.json` | ControlNet 结构引导重绘 | 自动（子图展开后） | `58` |
| qwen_image_edit | `.claude/skills/comfyui-client/assets/workflows/image_qwen_image_edit_2511.json` | Qwen 多图语义编辑 | `68`（正面），`69`（负面） | `41`（主图），`83`（参考2），`87`（参考3） |
| wan_i2v | `.claude/skills/comfyui-client/assets/workflows/video_wan2_2_14B_i2v.json` | Wan 2.2 图生视频 | 自动 | - |
| wan_flf2v | `.claude/skills/comfyui-client/assets/workflows/video_wan2_2_14B_flf2v.json` | Wan 2.2 首尾帧视频 | 自动 | - |

## 其他工作流（项目内）

| 工作流 | 路径 | 用途 |
|-------|------|------|
| txt2img | `scripts/githubToXPost/workflows/txt2img.json` | 文生图 |
| img_edit | `scripts/githubToXPost/workflows/img_edit.json` | 图片编辑 |
| controlnet | `scripts/githubToXPost/workflows/controlnet.json` | ControlNet 图生图 |
| img2video | `scripts/githubToXPost/workflows/img2video.json` | 图生视频 |
| flf2video | `scripts/githubToXPost/workflows/flf2video.json` | 首尾帧生成视频 |

## 模块引用

脚本支持作为 Node.js 模块引用，用于集成到其他工作流（如 githubToXPost 的 imageGenerator）。

```javascript
const ComfyUIClient = require('./scripts/comfyUIClient');

const client = new ComfyUIClient({
    workflowFile: 'scripts/githubToXPost/workflows/txt2img.json',
    prompt: 'a beautiful landscape',
    serverUrl: 'http://127.0.0.1:8188',
    outputDir: './work_dir/comfyui_output'
});

const result = await client.execute();
console.log('生成文件:', result.generatedFiles);
```

## 工作流格式说明

脚本支持两种工作流格式：

1. **ComfyUI 完整格式**（含 `nodes`、`links` 数组）- 自动转换为 API 格式
2. **API 格式**（以节点 ID 为 key 的对象）- 直接使用

**自动预处理：**
- **子图展开**：包含 `definitions.subgraphs` 的工作流会自动展开子图内部节点到顶层，重映射连接关系
- **旁路节点处理**：`mode=4`（旁路）的节点自动透传输入到输出；`mode=2`（静音）的节点自动移除
- **非执行节点**：MarkdownNote、Note 等非执行节点会自动跳过

## 错误处理

### 常见问题

**1. ComfyUI 服务不可用**
- 确认 ComfyUI 已启动
- 检查 `--server` 或 `COMFYUI_SERVER_URL` 是否正确
- 可访问 `http://127.0.0.1:8188` 验证

**2. 工作流文件不存在**
- 确认 `--workflow` 路径正确
- 从项目根目录执行，或使用绝对路径

**3. 任务超时**
- 视频生成等耗时任务可增加 `--timeout`（如 900 或 1200）
- 检查 ComfyUI 队列是否堆积

**4. 模型缺失**
- 工作流所需模型需预先下载到 ComfyUI 的 `models/` 目录
- 参考工作流内的 Model links 或 MarkdownNote 说明

## 最佳实践

1. **执行目录**：始终从项目根目录执行，确保相对路径正确
2. **超时设置**：图片生成默认 600 秒，视频生成建议 900 秒以上
3. **工作流选择**：根据需求选择合适工作流（文生图、图生图、视频等）
4. **结果位置**：生成文件在 `work_dir/comfyui_output/<会话名>/`，便于查找和管理
