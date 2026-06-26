# soul-forge

> 从家庭群聊记录提炼数字人格。一份聊天导出 → soul.md + persona 文件集。

## 快速安装

### 方法一：ClawHub（推荐）

在 OpenClaw 中说：
```
安装 skill soul-forge
```

### 方法二：手动安装

```bash
# 克隆到 OpenClaw skills 目录
git clone https://github.com/zengury/soul-forge ~/.openclaw/workspace/skills/soul-forge

# 安装 Python 依赖
pip install -r ~/.openclaw/workspace/skills/soul-forge/requirements.txt
```

## 使用

在 OpenClaw 对话中说：

```
帮我分析这份聊天记录：/path/to/群聊_三头怪.json
```

或：

```
soul-forge 运行 ~/Downloads/wechat_export.json
```

Agent 会自动处理四个阶段，完成后输出：

```
soul-forge-output/
├── soul.md          ← AI agent 人格底座
├── persona_dad.md
├── persona_mom.md
└── persona_child.md
```

## 需要什么

- Python 3.9+
- `ANTHROPIC_API_KEY` 环境变量
- 微信群聊 JSON 导出（用 WeFlow 工具）

## 成本

一份 2-3 年群聊（约 500 对话块）：**$3-6 一次性**

## 方法论

基于数字民族志（Digital Ethnography）。
Geertz 的「厚描」理论：soul.md 不是行为清单，而是理解这个家庭的解释框架。

---

作者：[@zengury](https://github.com/zengury)
License: MIT
