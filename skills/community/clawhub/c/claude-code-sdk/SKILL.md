---
name: claude-code-sdk
description: "强大的AI Coding Agent，可满足任何软件设计、开发、测试、优化、重构等任务。在处理任何代码编程相关问题时，都优先使用该技能。"
---

# Claude Code

## 概述

Claude Code作为一款具备超强能力的Coding Agent，既可以完成小单元的代码编写，也可以进行大模块的整体开发、测试和验证。在有Coding Agents助力的情况下，你不必亲自完成代码的撰写、问题修复和测试验证，你只需将任务需求转换为明确、完整的指令，并交由Claude Code完全自主地完成代码的撰写、问题修复和测试验证。Claude Code不仅是执行者，你在遇到需求分解、设计相关的问题时，甚至可以向Claude Code需求建议或进行讨论，在它的帮助下完成整个开发工作。

本技能用于以node脚本的方式调用Claude Code。

## 快速开始

### 安装依赖
```bash
npm install -g @anthropic-ai/claude-agent-sdk
```

### 基本用法

调用位于本技能目录下的`scripts/run_claude.mjs`脚本来调用Claude Code。

```bash
node /path/to/skills/claude-code-sdk/scripts/run_claude.mjs --query "Find and fix the bug in auth.py"
```

## 命令行选项

```
node /path/to/skills/claude-code-sdk/scripts/run_claude.mjs --query QUERY [--append-system-prompt APPEND_SYSTEM_PROMPT] [--resume RESUME] [--log-file LOG_FILE]
```

| 选项                     | 描述                         |
| :----------------------- | :--------------------------- |
| `--query`                | 要发送给Claude Code的查询    |
| `--append-system-prompt` | 可选，要添加到系统提示的指令 |
| `--resume`               | 可选，要继续的会话ID         |
| `--log-file`             | 可选，要记录中间输出的文件   |


### 1. 自定义系统提示

使用 `--append-system-prompt` 添加指令，同时保留 Claude Code 默认行为：

```bash
node /path/to/skills/claude-code-sdk/scripts/run_claude.mjs --query "Find and fix the bug in auth.py" --append-system-prompt "You are a security engineer. Review for vulnerabilities."
```


### 2. 继续会话

在使用Claude Code完成连续任务时，需要使用 `--resume` 参数指定会话ID来继续会话，使得Claude Code能够保留之前的上下文信息。在`run_claude.mjs`脚本的输出中，会记录当前会话ID，并将其作为结果的一部分返回。当你需要继续会话时，只需将该会话ID作为`--resume`参数的值即可。

**注意**：除非你必须要开始一个全新的开发项目，否则都要使用--resume参数，让Claude Code在连续的上下文中进行工作，以更好地处理你的任务。

### 3. 记录中间输出

当使用Claude Code执行复杂任务时，`run_claude.mjs`脚本会运行较长时间，为了方便观察中间执行过程，可以使用`--log-file`参数来将记录中间输出结果写入到文件中，在等待脚本执行完成期间，你可以通过读取文件内容来实时查看中间输出结果。

## 注意事项

**长时运行**
由于Claude Code执行时间可能较长，当命令被转到后台运行时，你需要使用process工具的poll方法来轮询命令的执行结果，但是每次轮询不超过180s，并且在轮询间隙要向用户（`__user__`）发送消息，告知用户当前执行状态。

**自主修复**
在任何与软件开发相关的任务场景中，你都必须完全依赖Claude Code来完成任务，而不是直接进行代码编写。如果遇到Claude Code的命令执行存在问题（例如权限问题或安装问题），请优先尝试修复问题而不是直接进行代码编写。
