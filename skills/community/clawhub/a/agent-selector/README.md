# Agent Selector Skill v2.0 - 发布说明

**版本**: 2.0.0  
**发布日期**: 2026-03-20  
**作者**: Krislu  
**许可证**: MIT

---

## 📦 安装包内容

```
agent-selector-skill/
├── SKILL.md                  # 技能文档
├── README.md                 # 本文件
├── __init__.py               # 模块导出
├── agent_selector.py         # 核心选择器（安全增强版）
└── clawhub.json              # ClawHub 配置
```

---

## 🚀 安装方法

### 方法 1：从 ClawHub 安装（推荐）

```bash
clawhub install agent-selector
```

### 方法 2：本地安装

```bash
# 复制技能目录到 skills 文件夹
cp -r agent-selector-skill <YOUR_OPENCLAW_WORKSPACE>/skills/
```

**注意**：技能包已包含完整的 agency-agents 目录，无需额外配置符号链接。

---

## 🎯 快速开始

### 1. 自动选择 Agent

```python
from agent_selector_skill import auto_select_agent

agent = auto_select_agent("设计 React 前端架构")
print(f"推荐 Agent: {agent}")
# 输出：engineering/engineering-frontend-developer
```

### 2. 手动切换人格

```python
from agent_selector_skill import AgentSelector

selector = AgentSelector()
prompt = selector.load_agent_prompt("engineering/engineering-frontend-developer")

# 现在你以"前端工程师"人格思考
```

### 3. RoundTable 多 Agent 讨论

```python
from agent_selector_skill import select_roundtable_agents

agents = select_roundtable_agents("智能客服系统技术方案")
print(f"推荐 Agent: {', '.join(agents)}")
# 输出：engineering/engineering-frontend-developer, engineering/engineering-backend-developer, ...
```

---

## 🔒 安全特性

v2.0 版本添加了全面的安全加固：

### 1. 路径白名单验证
```python
# ✅ 允许
AgentSelector()
AgentSelector("agency-agents")

# ❌ 拒绝（抛出 ValueError）
AgentSelector("/etc/passwd")
AgentSelector("../secret")
```

### 2. 文件大小限制
- 单个文件最大：100KB
- 防止内存耗尽攻击

### 3. 输入长度限制
- 任务描述最大：10000 字符
- 防止 DoS 攻击

### 4. 符号链接验证
- 只允许内部符号链接
- 拒绝指向外部的符号链接

### 5. 文件编码验证
- 只接受 UTF-8 编码
- 防止编码注入

### 6. 错误信息脱敏
- 不暴露完整路径
- 不暴露内部错误详情

---

## 📊 支持的 Agent

### 总计：146+ 个专业 Agent

#### Engineering（工程类）
- engineering-frontend-developer
- engineering-backend-developer
- engineering-fullstack-developer
- engineering-software-architect
- engineering-devops-automator
- engineering-security-engineer
- ... (40+ 个)

#### Design（设计类）
- design-ux-architect
- design-ui-designer
- design-ux-researcher
- design-interaction-designer
- ... (20+ 个)

#### Testing（测试类）
- testing-qa-engineer
- testing-accessibility-auditor
- testing-security-auditor
- ... (15+ 个)

#### Product（产品类）
- product-manager
- product-owner
- ... (10+ 个)

#### Specialized（专业类）
- specialized-ai-ml-engineer
- specialized-blockchain-developer
- ... (30+ 个)

> **完整列表**: 见 `agency-agents/` 目录

---

## 🔗 集成示例

### RoundTable 集成

已在 `roundtable-skill` 中集成：

```python
# roundtable-skill/roundtable_engine.py
from agent_selector import AgentSelector, select_roundtable_agents

class RoundTableEngine:
    def __init__(self, topic: str, ...):
        self.agents = select_roundtable_agents(topic)
```

### Auto-Coding 集成

已在 `auto-coding` 中集成：

```python
# auto-coding/agent_controller.py
from agent_selector import AgentSelector

class AgentController:
    def __init__(self):
        self.agent_selector = AgentSelector()
    
    def execute(self, task: str):
        agent_id = self.agent_selector.select_agent(task)
        # 使用选中的 Agent 执行任务
```

---

## 🧪 测试

### 运行内置测试

```bash
cd agent-selector-skill
python3 agent_selector.py
```

### 预期输出

```
============================================================
Agent Selector - 安全增强版测试
============================================================

📊 可用 Agent 数量：146

============================================================
任务匹配测试：
============================================================

任务：设计一个 React 前端架构
匹配 Agent: engineering/engineering-frontend-developer
------------------------------------------------------------

任务：编写 Python 后端 API
匹配 Agent: engineering/engineering-backend-developer
------------------------------------------------------------

...

✅ 所有测试完成！
```

---

## ⚠️ 注意事项

### 1. 路径限制
- 只能访问 `skills` 目录内的 Agent
- 目录名必须在白名单中

### 2. 符号链接
- 需要手动创建 `agency-agents` 符号链接
- 指向 `agency-agents-zh` 目录

### 3. 错误处理
```python
try:
    selector = AgentSelector("/invalid/path")
except ValueError as e:
    print(f"路径验证失败：{e}")
```

---

## 📝 更新日志

### v2.0.0 (2026-03-20) - 安全增强版

**新增功能**:
- ✅ 路径白名单验证
- ✅ 文件大小限制（100KB）
- ✅ 输入长度限制（10000 字符）
- ✅ 符号链接验证
- ✅ 文件编码验证
- ✅ 错误信息脱敏
- ✅ 预编译正则表达式（防 DoS）

**改进**:
- 支持多级 Agent 路径（如 `game-development/unity/unity-developer`）
- 优化 Agent 扫描性能
- 改进错误处理

**修复**:
- 修复路径遍历漏洞
- 修复符号链接跟随问题
- 修复错误信息泄露

### v1.0.0 (2026-03-19) - 初始版本

- 基础 Agent 选择功能
- 关键词匹配
- RoundTable 集成

---

## 📄 许可证

MIT License

Copyright (c) 2026 虾软 Claw soft

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

---

## 🔗 相关链接

- **ClawHub**: https://clawhub.com/skills/agent-selector
- **GitHub**: https://github.com/openclaw/skills/agent-selector
- **文档**: https://docs.openclaw.ai/skills/agent-selector

---

## 📞 支持

如有问题，请：
1. 查看 [SKILL.md](SKILL.md) 详细文档
2. 运行 `python3 agent_selector.py` 测试
3. 提交 Issue 到 ClawHub

---

*Agent Selector - 让你成为任何需要的专家*
