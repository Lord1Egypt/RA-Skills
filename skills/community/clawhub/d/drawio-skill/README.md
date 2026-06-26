# Draw.io Skill

`drawio-skill` is a Codex skill for creating and editing draw.io diagrams through a configured `drawio` MCP server.

`drawio-skill` 是一个 Codex Skill，用于通过已经配置好的 `drawio` MCP server 创建和编辑 draw.io 图表。

It is designed for:

适用场景包括：

- flowcharts
- architecture and deployment diagrams
- ML model diagrams such as LSTM, Transformer, and CNN
- Chinese labels and Chinese output
- animated connectors
- `.drawio` and `.svg` export workflows

- 流程图
- 架构图与部署图
- LSTM、Transformer、CNN 等机器学习模型图
- 中文标签与中文输出
- 动画连接器
- `.drawio` 与 `.svg` 导出工作流

## What This Skill Does

## 这个 Skill 能做什么

This skill teaches Codex how to use a draw.io MCP server in a stable workflow:

这个 Skill 会告诉 Codex 如何以稳定的流程使用 draw.io MCP server：

1. start a draw.io session
2. create diagrams from full XML
3. read the current diagram before editing
4. export editable and shareable outputs

1. 启动 draw.io 会话
2. 通过完整 XML 创建图表
3. 编辑前先读取当前图表
4. 导出可编辑和可分享的结果

It also includes rules for:

它还包含以下规则：

- diagram naming conventions
- Chinese labeling
- architecture-focused layouts
- ML model diagram layouts
- animated connector export behavior

- 图表命名规范
- 中文标注规则
- 偏架构图的布局规则
- 机器学习模型图的布局规则
- 动画连接器的导出规则

## Requirements

## 使用前提

This repository contains the skill only. It does not bundle the MCP server itself.

这个仓库只包含 skill 本身，不包含 MCP server。

You need a working `drawio` MCP server in Codex before using this skill.

在使用这个 skill 之前，你需要先在 Codex 中配置可用的 `drawio` MCP server。

One common setup is:

一种常见的配置方式如下：

```bash
codex mcp add drawio -- npx -y @next-ai-drawio/mcp-server@latest
```

After configuring the server, restart Codex or reload the IDE window if the tools do not appear.

配置完成后，如果工具没有出现，请重启 Codex 或重新加载 IDE 窗口。

## Install

## 安装方式

### Option 1: Clone directly into Codex skills

### 方式一：直接克隆到 Codex skills 目录

Clone this repository into your Codex skills directory and keep the folder name as `drawio-skill`.

把这个仓库克隆到你的 Codex skills 目录中，并保持文件夹名称为 `drawio-skill`。

Typical locations:

常见目录如下：

- Windows: `%USERPROFILE%\\.codex\\skills\\drawio-skill`
- macOS/Linux: `~/.codex/skills/drawio-skill`

### Option 2: Copy the files manually

### 方式二：手动复制文件

Copy these files into a folder named `drawio-skill` inside your Codex skills directory:

将以下文件复制到 Codex skills 目录下名为 `drawio-skill` 的文件夹中：

- `SKILL.md`
- `agents/openai.yaml`

## Usage

## 使用示例

Example prompts:

示例提示词：

```text
Use $drawio-skill to create a cloud architecture diagram.
```

```text
Use $drawio-skill to draw a Chinese-labeled order flowchart and export drawio + svg.
```

```text
Use $drawio-skill to create an animated LSTM architecture diagram.
```

## Repository Layout

## 仓库结构

```text
drawio-skill/
├── SKILL.md
├── README.md
├── LICENSE
└── agents/
    └── openai.yaml
```

## License

## 许可证

This repository is licensed under `MIT-0`.

本仓库采用 `MIT-0` 许可证。
