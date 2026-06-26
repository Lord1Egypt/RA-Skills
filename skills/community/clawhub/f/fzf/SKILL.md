---
name: fzf
description: fzf - 通用命令行模糊查找器
version: 0.1.2
metadata:
  openclaw:
    requires:
      bins:
        - fzf
    emoji: 🔍
    homepage: https://github.com/junegunn/fzf
---

# fzf 通用命令行模糊查找器

## 技能概述

本技能帮助用户在命令行中高效使用 fzf 进行模糊查找，适用于以下场景：

- **文件查找**: 快速模糊搜索目录树中的文件并打开
- **历史命令**: 交互式搜索并重用 Shell 历史命令
- **进程管理**: 模糊搜索并终止进程
- **Git 工作流**: 交互式选择分支、提交、文件差异
- **目录跳转**: 快速切换工作目录
- **管道集成**: 与任何产生文本输出的命令组合使用

**主要特点**: 极速模糊匹配、交互式预览、键绑定丰富、与 Shell 深度集成、可嵌入任意脚本

## 使用流程

AI 助手将引导你完成以下步骤：

1. 安装 fzf（如未安装）
2. 配置 Shell 集成（键绑定与补全）
3. 学习核心用法与快捷键
4. 结合常用命令构建高效工作流

## 关键章节导航

- [安装指南](./guides/01-installation.md)
- [快速开始](./guides/02-quickstart.md)
- [高级用法](./guides/03-advanced-usage.md)
- [常见问题](./troubleshooting.md)

## AI 助手能力

当你向 AI 描述查找需求时，AI 会：

- 自动检测系统环境并安装 fzf
- 根据需求生成最优的 fzf 命令组合
- 配置 Shell 集成以启用快捷键
- 构建带预览的交互式文件/内容浏览器
- 生成可复用的 fzf 函数放入 Shell 配置文件
- 集成 fzf 到 Git、Docker、kubectl 等工作流
- 诊断并修复 fzf 配置问题

## 核心功能

- 极速模糊匹配（基于 Smith-Waterman 算法的改进）
- 支持精确模式（`'word`）、前缀匹配（`^word`）、后缀匹配（`word$`）
- 多选模式（`--multi`，Tab 键选择）
- 实时预览窗口（`--preview`）
- 支持 ANSI 颜色代码
- Shell 集成：`CTRL-T`（文件）、`CTRL-R`（历史）、`ALT-C`（目录）
- 自定义按键绑定与动作
- 支持 `fd`、`ripgrep`、`bat` 等现代工具联动
- 支持 Vim/Neovim 插件集成

## 命令速查表

### 基础用法

```bash
# 启动交互式文件选择（当前目录递归）
fzf

# 从标准输入选择
echo -e "foo\nbar\nbaz" | fzf

# 选中后执行命令
vim $(fzf)

# 多选（Tab 选择，Enter 确认）
cat $(fzf --multi)
```

### 搜索语法

```bash
# 精确匹配（不做模糊）
fzf --query "'exact-word"

# 多词搜索（空格分隔，AND 逻辑）
fzf --query "foo bar"

# OR 逻辑
fzf --query "foo | bar"

# 前缀匹配
fzf --query "^prefix"

# 后缀匹配
fzf --query "suffix$"

# 排除匹配（! 取反）
fzf --query "!unwanted"
```

### 预览窗口

```bash
# 预览文件内容
fzf --preview 'cat {}'

# 用 bat 高亮预览（推荐）
fzf --preview 'bat --color=always {}'

# 预览窗口位置与大小
fzf --preview 'cat {}' --preview-window=right:50%

# 预览当前行内容
fzf --preview 'echo {}'
```

### Shell 快捷键（安装 Shell 集成后）

```bash
# CTRL-T  ：在命令行插入选中的文件路径
# CTRL-R  ：搜索并重用历史命令
# ALT-C   ：cd 进入选中目录
```

### 常用参数

```bash
# 指定初始查询
fzf --query "initial"

# 反向显示（列表在上，输入框在下）
fzf --reverse

# 显示边框
fzf --border

# 高度模式（不占满全屏）
fzf --height=40%

# 不排序（保持输入顺序）
fzf --no-sort

# 退出码为 0 时清空输出
fzf --exit-0

# 指定分隔符和字段
echo "foo:bar:baz" | fzf --delimiter=: --with-nth=2
```

## 安装要求

- macOS / Linux / Windows（WSL 或 Git Bash）
- 可选：`fd`（更快的文件查找）、`bat`（语法高亮预览）、`ripgrep`（内容搜索）

## 许可证

MIT License

## 项目链接

- GitHub: https://github.com/junegunn/fzf
- Wiki: https://github.com/junegunn/fzf/wiki
- 示例脚本: https://github.com/junegunn/fzf/wiki/examples
