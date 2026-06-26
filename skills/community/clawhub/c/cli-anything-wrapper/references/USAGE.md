# CLI-Anything Wrapper 使用指南

## 快速开始

### 1. 检查 CLI-Anything 是否安装

```bash
openclaw run cli-anything-wrapper --info
```

### 2. 安装 CLI-Anything（如果未安装）

```bash
openclaw run cli-anything-wrapper --install
```

或手动安装：
```bash
git clone --recursive https://github.com/HKUDS/CLI-Anything \
  ~/.openclaw/workspace/CLI-Anything
cd ~/.openclaw/workspace/CLI-Anything
./setup.sh
```

### 3. 查看支持的软件

```bash
openclaw run cli-anything-wrapper --list
```

### 4. 调用软件

```bash
# GIMP 图片处理
openclaw run cli-anything-wrapper --app gimp --args "input.jpg --filter blur"

# Blender 渲染
openclaw run cli-anything-wrapper --app blender --args "scene.blend --render"

# LibreOffice 文档转换
openclaw run cli-anything-wrapper --app libreoffice --args "doc.docx --pdf"
```

## 支持的软件

| 软件 | 类别 | 用途 |
|------|------|------|
| gimp | 设计 | 图像编辑、滤镜、批处理 |
| blender | 3D | 建模、渲染、动画 |
| inkscape | 设计 | 矢量图处理 |
| libreoffice | 办公 | 文档转换、批处理 |
| audacity | 音视频 | 音频编辑 |
| obs | 音视频 | 直播控制、录制 |
| comfyui | AI | AI绘画工作流 |
| ollama | AI | 本地大模型管理 |
| kdenlive | 音视频 | 视频剪辑 |
| mermaid | 办公 | 流程图生成 |
| zotero | 学术 | 文献管理 |

## 高级用法

### 按分类筛选
```bash
openclaw run cli-anything-wrapper --list --category AI
```

### 模拟运行（测试参数）
```bash
openclaw run cli-anything-wrapper --app blender --args "test.blend" --dry-run
```

### JSON 输出
```bash
openclaw run cli-anything-wrapper --list --json
```

## 故障排除

### 问题：软件未找到
确保软件已安装：
```bash
which gimp  # 检查 GIMP 是否在 PATH 中
```

### 问题：Harness 未找到
确保 CLI-Anything 完整克隆：
```bash
git clone --recursive https://github.com/HKUDS/CLI-Anything
```

### 问题：执行超时
某些操作（如渲染）可能需要较长时间，目前超时设置为 5 分钟。

## 注意事项

1. CLI-Anything 本身不是 OpenClaw 原生 skill，本 wrapper 提供了桥接
2. 每个软件需要单独安装（GIMP、Blender 等）
3. 首次运行可能需要下载依赖

## 相关链接

- CLI-Anything: https://github.com/HKUDS/CLI-Anything
- OpenClaw: https://openclaw.ai
- ClawHub: https://clawhub.ai
