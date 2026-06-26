---
name: cli-anything-gimp
description: GIMP 图像编辑 via CLI-Anything. 用于处理图片编辑任务，如创建项目、添加图层、调整图像、导出等。当用户需要用 GIMP 处理图片时使用此技能。
allowed-tools: Bash(cli-anything-gimp:*)
---

# GIMP CLI-Anything Skill

基于 CLI-Anything 生成的 GIMP 命令行工具，让 AI Agent 可以控制 GIMP 进行图像编辑。

## 虚拟环境

此 skill 使用独立虚拟环境：
- **路径**: `~/.openclaw/workspace/cli-anything-venv/bin/`
- **命令**: `~/.openclaw/workspace/cli-anything-venv/bin/cli-anything-gimp`

## 前置条件

确保虚拟环境已激活且 GIMP CLI 已安装。如遇问题，尝试重新安装：

```bash
# 激活虚拟环境并安装
source ~/.openclaw/workspace/cli-anything-venv/bin/activate
pip install click numpy Pillow prompt-toolkit
cd ~/.openclaw/workspace/CLI-Anything/gimp/agent-harness
pip install -e .
```

## 核心命令

```bash
# 获取帮助
cli-anything-gimp --help

# 进入交互模式 (REPL)
cli-anything-gimp

# 项目管理
cli-anything-gimp project new --width 1920 --height 1080 -o poster.json
cli-anything-gimp project open poster.json

# 图层操作
cli-anything-gimp layer add -n "Background" --type solid --color "#1a1a2e"
cli-anything-gimp layer list
cli-anything-gimp layer remove "Layer 1"

# 画布操作
cli-anything-gimp canvas resize --width 1024 --height 768

# 导出
cli-anything-gimp export png -o output.png
cli-anything-gimp export jpg -q 90 -o output.jpg

# 滤镜
cli-anything-gimp filter blur --radius 5
cli-anything-gimp filter sharpen
cli-anything-gimp filter gaussian-blur --radius 2.5

# 绘画操作
cli-anything-gimp draw brush -n "Circle (19)" --size 10 --color "#FF0000"
cli-anything-gimp draw erase --size 20
```

## 常用工作流

### 1. 创建新图像
```bash
cli-anything-gimp project new --width 800 --height 600 -o my_image.json
cli-anything-gimp layer add -n "Background" --type solid --color "#FFFFFF"
cli-anything-gimp layer add -n "Text Layer" --type text --text "Hello"
cli-anything-gimp export png -o my_image.png
```

### 2. 编辑现有图像
```bash
cli-anything-gimp media open input.jpg
cli-anything-gimp filter blur --radius 3
cli-anything-gimp layer add -n "Watermark" --type text --text "©2026"
cli-anything-gimp export png -o output.png
```

### 3. 批量处理
```bash
# 在 REPL 模式下可以连续执行多条命令
cli-anything-gimp repl < commands.txt
```

## 输出格式

```bash
# JSON 格式输出 (便于程序解析)
cli-anything-gimp --json layer list

# 人类可读格式 (默认)
cli-anything-gimp layer list
```

## 注意事项

1. GIMP 必须在系统上已安装才能进行实际图像处理
2. 某些高级功能可能需要 GIMP Python 插件
3. 复杂操作建议在 REPL 交互模式下完成

## 故障排除

- **命令找不到**: 检查虚拟环境路径是否正确
- **模块缺失**: `pip install numpy Pillow prompt-toolkit`
- **GIMP 未安装**: 使用 Homebrew 安装 `brew install gimp`
