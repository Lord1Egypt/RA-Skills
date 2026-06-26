---
name: comfyui-api
description: 通过 HTTP API 与 ComfyUI 服务交互，支持工作流提交与执行、队列管理、文件上传和能力探测；自动检测视频工作流并使用合适超时；简洁输出执行结果；当用户需要使用 ComfyUI 生成图像、视频、音频或管理服务时使用
dependency:
  python:
    - requests>=2.28.0
    - websocket-client>=1.4.0
    - Pillow>=9.0.0
    - pyyaml>=6.0
---

# ComfyUI API 技能

## 任务目标
- 本技能用于：通过 HTTP API 与 ComfyUI 服务进行交互，自动化执行图像/视频生成工作流
- 能力包含：工作流提交与执行、队列管理、多类型文件上传、能力探测、内存管理
- 触发条件：用户需要使用 ComfyUI 生成图像/视频/音频、管理执行队列、上传文件或探测服务能力

## 前置准备

### 依赖说明
scripts 脚本所需的依赖包及版本：
```
requests>=2.28.0
websocket-client>=1.4.0
Pillow>=9.0.0
pyyaml>=6.0
```

### 服务地址
- 默认地址：`http://127.0.0.1:8188`
- 可通过 `--server-url` 参数指定其他地址

### 工作流目录
`workflows/` 目录用于存储用户上传的工作流 JSON 文件，便于复用和管理。

## 操作步骤

### 1. 工作流执行（核心功能）

**使用场景**：提交工作流 JSON 并获取生成的输出文件（支持图像、视频、音频等多种类型）

**执行步骤**：

#### 方式一：使用 workflows 目录中的工作流
```bash
python scripts/comfyui_executor.py --workflow my_workflow.json
```

#### 方式二：使用指定路径的工作流
```bash
python scripts/comfyui_executor.py \
  --workflow ./custom_workflow.json \
  --output-dir ./output
```

#### 方式三：指定服务器地址和超时时间
```bash
python scripts/comfyui_executor.py \
  --workflow my_workflow.json \
  --server-url http://192.168.1.100:8188 \
  --timeout 600
```

**参数说明**：
- `--workflow`：工作流 JSON 文件路径（必需）
- `--output-dir`：输出目录（默认：`output`）
- `--server-url`：ComfyUI 服务地址（默认：`http://127.0.0.1:8188`）
- `--timeout`：执行超时时间（秒，默认：图像 300 秒，视频 900 秒）
- `--poll-interval`：轮询间隔（秒，默认：2 秒）
- `--no-auto-detect`：禁用视频工作流自动检测

**支持的输出类型**：
- **图像**：PNG、JPEG、WebP、GIF、BMP、TIFF、EXR
- **视频**：MP4、AVI、MOV、MKV、WebM、FLV
- **音频**：MP3、WAV、OGG、FLAC、AAC、M4A
- **其他**：3D模型（OBJ、GLTF、GLB、FBX、STL）、GIF动画、数据文件等

**超时自动检测**：
- **图像工作流**：默认 300 秒（5 分钟）
- **视频工作流**：自动检测并使用 900 秒（15 分钟）
- **检测节点**：VHS_VideoCombine、AnimateDiff、FrameInterpolation 等

**输出示例**：
```
⏳ 执行中... 45 秒
✓ 已下载 2 个文件：图像 2 个
✓ 任务完成: abc123-def456

输出文件：
  output/image_001.png
  output/image_002.png
```

**智能体职责**：
- 根据用户需求选择或构建合适的工作流 JSON
- 解读执行结果和错误信息
- 提供优化建议（如调整参数、选择模型等）
- 根据输出类型建议后续处理方法

### 2. 工作流管理

#### 列出工作流
查看 `workflows/` 目录中存储的所有工作流：
```bash
python scripts/workflow_manager.py --action list
```

**输出内容**：
- 工作流名称
- 类型（txt2img/img2img/video）
- 节点数量
- 文件大小
- 修改时间

#### 查看工作流详情
查看指定工作流的详细信息和内容：
```bash
python scripts/workflow_manager.py --action show --name my_workflow.json
```

#### 删除工作流
删除不需要的工作流：
```bash
python scripts/workflow_manager.py --action delete --name old_workflow.json
```

**智能体职责**：
- 根据用户需求创建工作流 JSON 文件并保存到 `workflows/` 目录
- 帮助用户选择合适的工作流
- 解释工作流参数和配置

### 3. 队列管理

**使用场景**：查看当前执行队列或中断正在执行的任务

**查看队列**：
```bash
python scripts/queue_manager.py --action list
```

**中断执行**：
```bash
python scripts/queue_manager.py --action interrupt
```

**智能体职责**：
- 根据队列状态判断是否需要等待或调整执行策略
- 建议用户是否中断当前任务

### 4. 文件上传

**使用场景**：上传各种类型的文件到 ComfyUI（图像、视频、音频、模型等）

**支持的文件类型**：
- **图像**：PNG、JPG、WebP、GIF、BMP、TIFF、EXR
- **视频**：MP4、AVI、MOV、MKV、WebM、FLV
- **音频**：MP3、WAV、OGG、FLAC、AAC、M4A
- **模型**：OBJ、GLTF、GLB、FBX、STL
- **其他**：JSON、TXT、CSV 等

**自动检测类型上传**：
```bash
# 自动检测文件类型
python scripts/file_uploader.py --file ./reference.png
python scripts/file_uploader.py --file ./video.mp4
python scripts/file_uploader.py --file ./audio.wav
python scripts/file_uploader.py --file ./model.glb
```

**指定类型上传**：
```bash
# 上传图像
python scripts/file_uploader.py --type image --file ./reference.png

# 上传蒙版
python scripts/file_uploader.py --type mask --file ./mask.png --subfolder input

# 上传视频
python scripts/file_uploader.py --type video --file ./input_video.mp4

# 上传音频
python scripts/file_uploader.py --type audio --file ./background_music.mp3

# 上传 3D 模型
python scripts/file_uploader.py --type model --file ./character.obj
```

**上传到指定子目录**：
```bash
python scripts/file_uploader.py --file ./reference.png --subfolder my_project
```

**输出示例**：
```
✓ 文件上传成功
文件名: reference.png
类型: image
子文件夹: input
大小: 1.2 MB

在工作流中使用：
  路径: input/reference.png
```

**智能体职责**：
- 准备符合格式要求的文件
- 自动检测文件类型或建议合适的类型
- 确定合适的 subfolder 路径
- 将上传后的文件路径集成到工作流 JSON 中

### 5. 能力探测

**使用场景**：了解 ComfyUI 服务支持的节点、模型、embeddings 和系统状态

**获取节点定义**：
```bash
# 获取所有节点
python scripts/capability_probe.py --type nodes

# 获取单个节点详情
python scripts/capability_probe.py --type nodes --node-class KSampler
```

**获取模型列表**：
```bash
# 获取所有模型
python scripts/capability_probe.py --type models

# 获取特定文件夹的模型
python scripts/capability_probe.py --type models --folder checkpoints
```

**获取其他资源**：
```bash
# 获取 embeddings 列表
python scripts/capability_probe.py --type embeddings

# 获取已安装扩展
python scripts/capability_probe.py --type extensions

# 获取服务器功能特性
python scripts/capability_probe.py --type features

# 获取工作流模板
python scripts/capability_probe.py --type templates

# 获取模型元数据
python scripts/capability_probe.py --type metadata --model sd_xl_base.safetensors

# 获取系统状态
python scripts/capability_probe.py --type system
```

**智能体职责**：
- 分析可用节点和模型，帮助用户选择合适的组件
- 根据系统状态建议是否执行任务（如 GPU 内存不足时）
- 解释节点参数和用法
- 推荐合适的 embeddings 和扩展

### 6. 内存和历史管理

**使用场景**：管理 ComfyUI 内存使用和清理执行历史

**释放内存**：
```bash
# 基本内存释放
python scripts/memory_manager.py --action free

# 卸载所有模型
python scripts/memory_manager.py --action free --unload-models

# 释放 50% 内存
python scripts/memory_manager.py --action free --free-memory 0.5
```

**清理历史**：
```bash
# 清空所有历史
python scripts/memory_manager.py --action clear-history

# 删除特定历史记录
python scripts/memory_manager.py --action clear-history --prompt-id task-id
```

**查看队列状态**：
```bash
python scripts/memory_manager.py --action status
```

**智能体职责**：
- 根据 GPU 内存使用情况建议是否释放内存
- 在长时间运行后建议清理历史
- 监控队列状态并提供建议

## 资源索引

### 参考文档
- API 规范：见 [references/api-specification.md](references/api-specification.md)（详细的 API 端点、请求/响应格式）
- 工作流格式：见 [references/workflow-format.md](references/workflow-format.md)（工作流 JSON 结构与示例）

### 核心脚本
- 核心执行：见 [scripts/comfyui_executor.py](scripts/comfyui_executor.py)（工作流提交与结果获取）
- 工作流管理：见 [scripts/workflow_manager.py](scripts/workflow_manager.py)（列出、查看、删除工作流）
- 队列管理：见 [scripts/queue_manager.py](scripts/queue_manager.py)（队列查看与中断）
- 文件上传：见 [scripts/file_uploader.py](scripts/file_uploader.py)（多类型文件上传）
- 能力探测：见 [scripts/capability_probe.py](scripts/capability_probe.py)（节点、模型、embeddings、扩展等）
- 内存管理：见 [scripts/memory_manager.py](scripts/memory_manager.py)（内存释放、历史清理）

## 注意事项

### 工作流管理
- **存储位置**：工作流默认存储在 `workflows/` 目录
- **命名规范**：建议使用有意义的文件名，如 `txt2img_default.json`、`img2img_portrait.json`
- **版本管理**：建议对重要工作流进行版本控制

### 执行相关
- **服务可用性**：执行前确认 ComfyUI 服务正在运行且可访问
- **超时设置**：
  - 图像生成：默认 5 分钟，可通过 `--timeout` 调整
  - 视频生成：自动检测并使用 15 分钟，或手动指定更长时间
  - 长时间任务：建议设置更长的超时时间（如 `--timeout 1200` 表示 20 分钟）
- **自动检测**：系统会自动识别视频工作流节点（如 VHS_VideoCombine、AnimateDiff 等）
- **输出显示**：执行过程显示简洁进度，结果只显示关键信息
- **并发限制**：ComfyUI 默认按队列顺序执行任务，避免同时提交大量工作流

### 安全性
- **API Key**：如果 ComfyUI 启用了 API Key 鉴权，可通过 `--api-key` 参数或环境变量设置
- **敏感信息**：不要将包含 API Key 的配置文件提交到公开仓库

## 使用示例

### 示例 1：执行基础文生图

**步骤**：
1. 智能体创建工作流并保存到 `workflows/` 目录
2. 执行工作流（自动检测超时）：
   ```bash
   python scripts/comfyui_executor.py --workflow txt2img_default.json
   ```

### 示例 2：执行视频生成工作流

**步骤**：
1. 视频工作流会自动使用 15 分钟超时：
   ```bash
   python scripts/comfyui_executor.py --workflow video_gen.json
   ```
2. 或手动指定更长的超时时间：
   ```bash
   python scripts/comfyui_executor.py --workflow video_gen.json --timeout 1200
   ```

### 示例 3：使用自定义配置执行

**步骤**：
临时使用不同的服务器地址和超时时间：
```bash
python scripts/comfyui_executor.py \
  --workflow my_workflow.json \
  --server-url http://192.168.1.100:8188 \
  --timeout 1200
```

### 示例 4：管理多个工作流

**步骤**：
1. 列出所有工作流：
   ```bash
   python scripts/workflow_manager.py --action list
   ```
2. 智能体分析并推荐合适的工作流
3. 执行选定的工作流

### 示例 5：探测服务器能力

**步骤**：
1. 获取可用模型：
   ```bash
   python scripts/capability_probe.py --type models
   ```
2. 智能体根据模型列表推荐合适的工作流配置
3. 执行工作流
