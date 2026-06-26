# ComfyUI API Skill

## 中文

### 概述

完整的 ComfyUI API 集成技能，通过 HTTP API 提供工作流执行、队列管理、文件上传和能力探测等功能。

### 功能特性

- **工作流执行**：提交并执行工作流，自动检测超时时间
- **队列管理**：查看和中断正在运行的任务
- **文件上传**：支持多种文件类型（图像、视频、音频、模型）
- **能力探测**：查询可用节点、模型、embeddings 和扩展
- **内存管理**：释放 GPU 内存和清理执行历史
- **自动超时检测**：自动识别视频工作流并使用 15 分钟超时

### 环境要求

- Python 3.8+
- ComfyUI 服务运行在 `http://127.0.0.1:8188`（默认）

### 依赖包

```
requests>=2.28.0
websocket-client>=1.4.0
Pillow>=9.0.0
pyyaml>=6.0
```

### 快速开始

#### 1. 执行工作流

```bash
python scripts/comfyui_executor.py --workflow my_workflow.json
```

#### 2. 上传文件

```bash
python scripts/file_uploader.py --file ./reference.png
```

#### 3. 检查服务器能力

```bash
python scripts/capability_probe.py --type models
python scripts/capability_probe.py --type nodes
```

#### 4. 管理队列

```bash
# 查看队列
python scripts/queue_manager.py --action list

# 中断当前任务
python scripts/queue_manager.py --action interrupt
```

### 核心脚本

| 脚本 | 说明 |
|------|------|
| `comfyui_executor.py` | 工作流执行与结果下载 |
| `workflow_manager.py` | 列出、查看、删除工作流 |
| `queue_manager.py` | 队列查看与中断 |
| `file_uploader.py` | 多类型文件上传 |
| `capability_probe.py` | 查询节点、模型、embeddings 等 |
| `memory_manager.py` | 内存释放与历史清理 |

### 支持的输出类型

- **图像**：PNG、JPEG、WebP、GIF、BMP、TIFF、EXR
- **视频**：MP4、AVI、MOV、MKV、WebM、FLV
- **音频**：MP3、WAV、OGG、FLAC、AAC、M4A
- **其他**：3D模型（OBJ、GLTF、GLB、FBX、STL）、GIF动画、数据文件

### 超时设置

| 工作流类型 | 默认超时 | 自动检测 |
|-----------|---------|---------|
| 图像生成 | 300 秒（5 分钟） | - |
| 视频生成 | 900 秒（15 分钟） | ✓ 通过节点自动检测 |

**视频检测节点**：VHS_VideoCombine、AnimateDiff、FrameInterpolation 等

### 输出示例

```
⏳ 执行中... 45 秒
✓ 已下载 2 个文件：图像 2 个
✓ 任务完成: abc123-def456

输出文件：
  output/image_001.png
  output/image_002.png
```

### 高级用法

#### 自定义服务器地址

```bash
python scripts/comfyui_executor.py \
  --workflow my_workflow.json \
  --server-url http://192.168.1.100:8188 \
  --timeout 1200
```

#### 上传到子目录

```bash
python scripts/file_uploader.py \
  --file ./reference.png \
  --subfolder my_project
```

#### 查询特定模型文件夹

```bash
python scripts/capability_probe.py --type models --folder checkpoints
```

### API 参考

详见 [references/api-specification.md](references/api-specification.md)

### 工作流格式

详见 [references/workflow-format.md](references/workflow-format.md)

---

## License

MIT License

## Contributing

Issues and pull requests are welcome!
