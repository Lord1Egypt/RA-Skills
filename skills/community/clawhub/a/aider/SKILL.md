---
name: "Aider"
version: "1.0.0"
description: "Aider AI 编程助手，精通终端内 AI 编程、Git 集成、多模型支持、代码重构"
tags: ["ai-coding", "terminal", "aider", "git"]
author: "ClawSkills Team"
category: "developer-tools"
---
# Aider - 终端内 AI Pair Programming 工具

## 简介
Aider 是一款运行在终端中的 AI 结对编程工具，能直接编辑本地 Git 仓库中的代码。
它的核心理念是"对话即编程"——你用自然语言描述需求，Aider 自动修改代码并生成 Git commit。

## 核心功能
- **自动 Git Commit**：每次代码修改自动生成语义化的 commit message
- **多文件编辑**：一次对话中同时修改多个文件，保持跨文件一致性
- **文件管理**：通过 `/add` 和 `/drop` 精确控制 AI 可见的上下文范围
- **代码地图（Repo Map）**：基于 tree-sitter 构建仓库结构索引，帮助 AI 理解项目全貌
- **Linting 集成**：修改后自动运行 linter，发现问题自动修复

## 支持的模型
| 模型 | 推荐场景 | 配置方式 |
|------|---------|---------|
| Claude Sonnet 4 | 日常编码（默认推荐） | `--model sonnet` |
| Claude Opus 4 | 复杂架构重构 | `--model opus` |
| GPT-4o | OpenAI 生态用户 | `--model gpt-4o` |
| DeepSeek V3 | 高性价比选择 | `--model deepseek` |
| Ollama 本地模型 | 离线/隐私场景 | `--model ollama/qwen2.5-coder` |

## 常用命令
```bash
# 启动 Aider
aider                          # 当前目录启动
aider --model sonnet           # 指定模型
aider file1.py file2.py        # 预加载文件

# 会话内命令
/add src/main.py               # 添加文件到上下文
/drop src/test.py              # 从上下文移除文件
/undo                          # 撤销上一次 AI 修改（git undo）
/diff                          # 查看当前修改的 diff
/run pytest tests/             # 运行命令并将输出发给 AI
/test pytest tests/            # 运行测试，失败时自动修复
/architect                     # 切换到 Architect 模式
/ask                           # 只问不改代码
/clear                         # 清空对话历史
```

## 配置文件
在项目根目录创建 `.aider.conf.yml`：
```yaml
model: sonnet
auto-commits: true
gitignore: true
dark-mode: true
map-tokens: 2048
lint-cmd: "ruff check --fix"
test-cmd: "pytest tests/ -x"
```

环境变量配置（`~/.bashrc` 或 `~/.zshrc`）：
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
```

## Architect 模式
Architect 模式采用"先规划再编码"的两阶段策略：
1. **Architect 模型**（如 Opus）负责分析需求、制定修改方案
2. **Editor 模型**（如 Sonnet）负责执行具体的代码修改

启用方式：
```bash
aider --architect --model opus --editor-model sonnet
```
适合复杂重构任务，Architect 模型产出高质量方案，Editor 模型高效执行。

## 与同类工具对比
| 特性 | Aider | Claude Code | Cursor |
|------|-------|-------------|--------|
| 运行环境 | 纯终端 | 纯终端 | IDE |
| Git 集成 | 自动 commit | 手动 commit | 无 |
| 文件管理 | /add /drop 手动 | 自动检索 | 自动检索 |
| 上手难度 | 低 | 低 | 极低 |
| 适合场景 | 精确控制上下文 | 探索式开发 | GUI 偏好者 |

## 典型使用场景
- **快速修 Bug**：描述问题，Aider 定位并修复，自动 commit
- **添加新功能**：`/add` 相关文件，描述需求，多文件协同修改
- **代码重构**：Architect 模式规划方案，批量重命名/拆分/合并
- **写测试**：`/add` 源码文件，要求生成对应的单元测试
- **代码审查辅助**：`/ask` 模式分析代码逻辑，不做修改

## 安装
```bash
pip install aider-chat
# 或使用 pipx 隔离安装
pipx install aider-chat
```
