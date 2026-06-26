---
name: agent-s-bridge
version: 1.0.0
description: Agent-S 计算机使用智能体桥接器 — 让 DeepSeek TUI 通过 Agent-S 控制浏览器和桌面。支持自然语言指令驱动的全桌面自动化。OSWorld 基准 72.6%（超人类）。
---

# Agent-S Bridge

> 包装 simular-ai/Agent-S，让 DeepSeek TUI 用自然语言控制电脑和浏览器。

## 能力定位

| 工具 | 覆盖范围 | 智能程度 | 速度 |
|------|---------|---------|------|
| OpenCLI | 浏览器（页面操作） | 脚本化 | 快 |
| Playwright | 浏览器（程序化） | 需要写代码 | 极快 |
| **Agent-S** | **整个桌面 + 浏览器** | **AI 自主决策** | 中 |
| Skyvern | 浏览器（AI 视觉） | AI 视觉 | 慢 |

Agent-S 是唯一能跨桌面 + 浏览器的工具。不只是点网页——能打开 VS Code、操作文件管理器、控制任何 GUI 程序。

## 安装

```bash
pip install gui-agents
```

### 前置条件

- API Key: OpenAI 或 Anthropic（Agent-S 推理需要）
- 定位模型: UI-TARS-1.5-7B（HuggingFace 推理端点，用于像素级 UI 元素定位）
- 单显示器（Agent-S 设计为单屏操作）

## 命令

```bash
# 启动 Agent-S 交互模式
python agent_s_bridge.py run "打开浏览器搜索中医"

# 浏览器特化模式（限制在浏览器内操作）
python agent_s_bridge.py browse "登录网站并填写表单"

# 检查依赖和配置
python agent_s_bridge.py check
```

## 与 DeepSeek TUI 的集成

```
你（DeepSeek TUI） → exec_shell → agent_s_bridge.py run "指令"
                                  ↓
                            Agent-S 控制桌面/浏览器
                                  ↓
                            结果返回给你
```

## API 要求

在 `~/.agent-s.env` 中配置：
```
OPENAI_API_KEY=sk-xxx
# 或 ANTHROPIC_API_KEY=sk-ant-xxx
```

定位模型可本地部署或使用 HuggingFace 推理端点。
