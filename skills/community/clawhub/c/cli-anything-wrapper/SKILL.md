---
name: cli-anything-wrapper
description: 包装 CLI-Anything，让 OpenClaw 能调用任意软件的 CLI 功能
created: 2026-03-31
---

# CLI-Anything Wrapper

让 OpenClaw 可以调用 CLI-Anything 控制各种软件（GIMP、Blender、LibreOffice等）。

## 前置条件

1. CLI-Anything 已安装
2. Python 3.10+
3. 目标软件已安装

## 使用方法

### 查看支持的软件
```bash
openclaw run cli-anything-wrapper --list
openclaw run cli-anything-wrapper --list --category AI
```

### 调用软件
```bash
openclaw run cli-anything-wrapper --app <软件名> --args "<参数>"
```

### 常用示例
```bash
# 图像处理 - GIMP
openclaw run cli-anything-wrapper --app gimp --args "photo.jpg --filter blur"

# 3D 渲染 - Blender
openclaw run cli-anything-wrapper --app blender --args "scene.blend --render"

# 文档转换 - LibreOffice
openclaw run cli-anything-wrapper --app libreoffice --args "doc.docx --pdf"

# AI 绘画 - ComfyUI
openclaw run cli-anything-wrapper --app comfyui --args "workflow.json"

# 本地模型 - Ollama
openclaw run cli-anything-wrapper --app ollama --args "run llama3.2"
```

### 其他选项
```bash
# 显示详细信息
openclaw run cli-anything-wrapper --info

# 安装 CLI-Anything
openclaw run cli-anything-wrapper --install

# 模拟运行（测试参数）
openclaw run cli-anything-wrapper --app gimp --args "test.jpg" --dry-run

# JSON 格式输出
openclaw run cli-anything-wrapper --list --json
```

## 支持的软件

| 软件 | 类别 | 描述 |
|------|------|------|
| gimp | 设计 | 图像编辑、滤镜 |
| blender | 3D | 建模、渲染、动画 |
| inkscape | 设计 | 矢量图处理 |
| libreoffice | 办公 | 文档转换 |
| audacity | 音视频 | 音频编辑 |
| obs | 音视频 | 直播控制 |
| comfyui | AI | AI绘画工作流 |
| ollama | AI | 本地大模型管理 |
| kdenlive | 音视频 | 视频剪辑 |
| mermaid | 办公 | 流程图生成 |
| zotero | 学术 | 文献管理 |
