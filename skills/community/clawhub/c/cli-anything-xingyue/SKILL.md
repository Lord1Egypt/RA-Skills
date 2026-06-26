---
name: cli-anything
description: 基于 HKUDS/CLI-Anything 仓库重构的 OpenClaw Skill。为任意软件生成 CLI 工具，让 AI Agent 可以控制它。通过分析软件源代码，自动生成可被 AI 调用的命令行接口。支持 GIMP、Blender、LibreOffice、OBS 等软件。
version: 1.0.0
author: HKUDS
homepage: https://github.com/HKUDS/CLI-Anything
commands:
  - /cli-list - 列出所有可用的 CLI 工具
  - /cli-install <名称> - 安装预生成的 CLI（如 gimp, blender）
  - /cli-build <路径> - 为新软件构建 CLI（需要 Claude Code/Codex）
  - /cli-refine <路径> - 优化已构建的 CLI
  - /cli-validate <路径> - 验证生成的 CLI
metadata: {"clawdbot":{"emoji":"🔧","requires":{"bins":["git","python3","pip"],"env":[]},"install":[{"id":"git","kind":"system","label":"Git"},{"id":"python","kind":"system","label":"Python 3.10+"},{"id":"pip","kind":"system","label":"pip"}]}}
---

# CLI-Anything for OpenClaw

> 🔧 基于 [HKUDS/CLI-Anything](https://github.com/HKUDS/CLI-Anything) 仓库重构

让任意软件都能被 AI Agent 驱动。

## 什么是 CLI-Anything？

**今天的软件为人而生，明天的用户是 Agent。**

CLI-Anything 连接 AI Agent 与全世界软件的桥梁，通过一行命令让任意软件变成 Agent 可控的工具。

### 核心特性

- 🌍 **通用性** - 任何软件都可以变成 CLI 工具
- 📦 **开箱即用** - 11+ 预生成的 CLI（GIMP, Blender, LibreOffice 等）
- 🔗 **无缝集成** - 无需 API、无需 GUI 重建
- 📝 **自描述** - `--help` 自动生成文档
- 🤖 **Agent 优先** - 结构化 JSON 输出

## 快速命令

### 查看可用 CLI

```
/cli-list
```

**当前可用的 CLI：**
- gimp - 图像编辑
- blender - 3D 建模/渲染
- libreoffice - 办公套件
- obs-studio - 屏幕录制/直播
- kdenlive - 视频编辑
- shotcut - 视频编辑
- audacity - 音频编辑
- inkscape - 矢量图形
- drawio - 流程图
- zoom - 视频会议
- anygen - AI 内容生成

### 安装 CLI

```
/cli-install gimp
/cli-install blender
```

安装后即可使用：
```bash
cli-anything-gimp --help
cli-anything-blender --help
```

### 构建新 CLI（高级）

```
/cli-build ./my-software
/cli-build https://github.com/user/repo
```

⚠️ 完整构建需要在 **Claude Code** 或 **Codex** 环境中进行。

### 优化 CLI

```
/cli-refine ./gimp
/cli-refine ./gimp "添加图像批处理功能"
```

### 验证 CLI

```
/cli-validate ./gimp
```

## 使用示例

### GIMP 图像编辑

```bash
# 查看帮助
cli-anything-gimp --help

# 创建新项目
cli-anything-gimp project new --width 1920 --height 1080 -o poster.json

# 添加图层
cli-anything-gimp --json layer add -n "Background" --type solid --color "#1a1a2e"

# 导出
cli-anything-gimp export png -o output.png

# 交互式 REPL
cli-anything-gimp
```

### Blender 3D

```bash
# 创建场景
cli-anything-blender scene new -o scene.json

# 添加立方体
cli-anything-blender object add cube --location 0 0 0

# 渲染
cli-anything-blender render output.png --samples 128
```

### LibreOffice 文档

```bash
# 打开文档
cli-anything-libreoffice document open report.odt

# 添加内容
cli-anything-libreoffice text add "Hello World"

# 导出 PDF
cli-anything-libreoffice export pdf -o report.pdf
```

## 工作原理

CLI-Anything 自动执行 7 阶段流水线：

1. 🔍 **分析** — 扫描源码，将 GUI 操作映射到 API
2. 📐 **设计** — 规划命令分组、状态模型
3. 🔨 **实现** — 构建 Click CLI（REPL、JSON、撤销/重做）
4. 📋 **规划测试** — 生成测试计划
5. 🧪 **编写测试** — 实现测试套件
6. 📝 **文档** — 更新使用文档
7. 📦 **发布** — 生成 setup.py

## 注意事项

- 首次使用 `/cli-list` 会自动克隆 CLI-Anything 仓库
- 预生成的 CLI 无需额外配置，安装后可直接使用
- 构建新软件 CLI 需要 Claude Code 或 Codex 环境
- 已安装的 CLI 可通过 `pip uninstall` 卸载
