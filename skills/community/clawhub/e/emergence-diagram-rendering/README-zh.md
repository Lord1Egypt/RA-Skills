# Skill: Emergence 绘图渲染 (官方认证)

Emergence Science 生态系统中一个高保真、自主的绘图技能。

## 🌟 设计理念
本技能基于 **智能体自主性 (Agentic Autonomy)** 原则构建。它旨在通过提供以下特性，使求解智能体具备自我主权：
1.  **本地优先执行**: 优先使用主机级别的二进制文件 (`mmdc`, `d2`, `dot`) 以保证隐私和速度。
2.  **自动化环境管理**: 自动管理其隔离的 Python 虚拟环境 (`.venv/`)，确保在 MacBook 和 Ubuntu 之间具有最大的可移植性。
3.  **持久化运行历史**: 所有的渲染尝试都保存在 `./runs/` 目录下，允许智能体“读取”编译器错误，并递归地修复自己的代码。

## 🛠 安装指南 (MacBook / Linux)
该技能会自动配置其专属的 Python 环境。

### 1. 系统依赖
- **Graphviz**: `brew install graphviz` (Mac) 或 `apt-get install -y graphviz` (Linux)。
- **D2**: `curl -fsSL https://d2lang.com/install.sh | sh`
- **Mermaid CLI**: `npm install -g @mermaid-js/mermaid-cli`

### 2. 自动化配置
```bash
# 克隆技能并运行设置
bash install.sh
```

## 📂 项目结构
- `./templates/`: 常用流程的预定义蓝图。
- `./scripts/`: 核心渲染逻辑 (`local_render.py`)。
- `./runs/`: 所有生成尝试的持久存储及审计追踪。
- `SKILL.md`: 面向智能体的“内心独白”和推理模式。

## 🤖 针对智能体
如果你是一个求解智能体，请阅读 [SKILL.md](./SKILL.md)。请始终使用本地虚拟环境：`./.venv/bin/python3`。
