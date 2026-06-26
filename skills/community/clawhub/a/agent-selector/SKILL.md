# Agent Selector Skill v2.0 - 人格身份切换

## 📋 技能说明

**全局技能**，基于 Agency-Agent 人格库的优化，在不同专家人格之间自动切换，支持 146+ 个专业 Agent。根据对话自动适配，判定任务结束自动切换回初始人格，无须手动频繁切换。避免人格的混乱，同时始终保持最适合的人格工作。

该功能也集成在 Auto-coding 和 RoundTable skill 中。

### ✨ v2.0 安全增强

- ✅ **路径白名单验证** - 防止目录遍历攻击
- ✅ **文件大小限制** - 100KB 限制，防内存耗尽
- ✅ **输入长度限制** - 10000 字符限制，防 DoS
- ✅ **符号链接验证** - 防止访问外部文件
- ✅ **文件编码验证** - 防止编码注入
- ✅ **错误信息脱敏** - 防止信息泄露
- ✅ **只读操作** - 不写入外部目录，无安装脚本
- ✅ **范围明确** - 仅限本地 Agent 选择和 Prompt 加载

### 🔒 安全范围声明

**本技能的功能范围**：
- ✅ 读取 bundled 的 Agent Prompt 文件
- ✅ 根据关键词自动选择 Agent
- ✅ 缓存已加载的 Prompt
- ✅ 任务完成后恢复默认身份

**本技能不执行的操作**：
- ❌ 不写入外部目录
- ❌ 不创建符号链接
- ❌ 不安装到其他工具
- ❌ 不请求外部 API
- ❌ 不持久化存储

---

## 🚀 快速开始

### 方式 1：自动选择 Agent

```python
from agent_selector_skill import auto_select_agent

# 根据任务自动匹配合适的 Agent
agent = auto_select_agent("设计 React 前端架构")
# 返回：engineering/engineering-frontend-developer
```

### 方式 2：手动切换人格

```python
from agent_selector_skill import AgentSelector

selector = AgentSelector()

# 加载特定 Agent 的 Prompt
prompt = selector.load_agent_prompt("engineering/engineering-frontend-developer")

# 现在你以"前端工程师"人格思考
```

### 方式 3：RoundTable 专用

```python
from agent_selector_skill import select_roundtable_agents

# 为 RoundTable 讨论选择合适的 Agent
agents = select_roundtable_agents("智能客服系统技术方案")
# 返回：['engineering/engineering-frontend-developer', ...]
```

---

## 🎭 可用人格分类

### Engineering（工程类）
- `engineering/engineering-frontend-developer` - 前端开发工程师
- `engineering/engineering-backend-developer` - 后端开发工程师
- `engineering/engineering-fullstack-developer` - 全栈开发工程师
- `engineering/engineering-software-architect` - 软件架构师
- `engineering/engineering-devops-automator` - DevOps 工程师
- `engineering/engineering-security-engineer` - 安全工程师

### Testing（测试类）
- `testing/testing-qa-engineer` - QA 工程师
- `testing/testing-accessibility-auditor` - 可访问性审计师

### Design（设计类）
- `design/design-ux-designer` - UX 设计师
- `design/design-ui-designer` - UI 设计师
- `design/design-interaction-designer` - 交互设计师

### Product（产品类）
- `product/product-manager` - 产品经理

### Specialized（专业类）
- `specialized/specialized-ai-ml-engineer` - AI/ML 工程师

> **完整列表**: 146+ 个 Agent，见 `agency-agents/` 目录

---

## 📊 使用场景

### 场景 1：日常对话切换

```
用户：帮我设计一个前端架构

你：（自动切换到前端工程师人格）

✅ 已切换到前端工程师人格

## 技术方案

基于 React 18 + TypeScript 的前端架构...
```

### 场景 2：RoundTable 多 Agent 讨论

```python
from roundtable_skill import RoundTableEngine
from agent_selector_skill import select_roundtable_agents

# 自动选择合适的 Agent
agents = select_roundtable_agents("智能客服系统技术方案")

# 创建 RoundTable 引擎
engine = RoundTableEngine(
    topic="智能客服系统技术方案",
    agents=agents  # 使用自动选择的 Agent
)

# 执行讨论
await engine.run(user_channel)
```

### 场景 3：Auto-Coding 自主编码

```python
from auto_coding import AutoCodingAgent
from agent_selector_skill import auto_select_agent

# 根据任务自动选择 Agent
agent_id = auto_select_agent("开发 Python REST API")

# 创建编码 Agent
agent = AutoCodingAgent(agent_id=agent_id)

# 执行任务
result = await agent.execute("开发用户管理 API")
```

---

## 🔒 安全特性

### 路径安全
```python
# ✅ 允许的路径
AgentSelector()  # 使用内置 agency-agents
AgentSelector("agency-agents")  # 白名单目录

# ❌ 拒绝的路径
AgentSelector("/etc/passwd")  # 路径遍历攻击
AgentSelector("../secret")  # 相对路径攻击
```

### 文件大小限制
```python
# 自动跳过超大文件（>100KB）
# 防止内存耗尽攻击
```

### 输入长度限制
```python
# 任务描述限制 10000 字符
# 防止 DoS 攻击
```

### 符号链接验证
```python
# 只允许内部符号链接
# 拒绝指向外部的符号链接
```

---

## 📁 文件结构

```
agent-selector-skill/
├── SKILL.md                  # 本文档
├── __init__.py               # 模块导出
├── agent_selector.py         # 核心选择器（安全增强版）
├── clawhub.json              # ClawHub 配置
└── README.md                 # 详细说明
```

---

## 🔧 配置说明

### Agent 来源

```python
# 方式 1：使用内置的 agency-agents（推荐）
selector = AgentSelector()

# 方式 2：使用外部 Agent（必须在白名单内）
selector = AgentSelector("agency-agents")

# ❌ 错误：路径不在白名单内
selector = AgentSelector("/path/to/external")  # 会抛出 ValueError
```

### 自动选择规则

```python
# 关键词匹配
"react" → engineering/engineering-frontend-developer
"python" → engineering/engineering-backend-developer
"测试" → testing/testing-qa-engineer
"ux" → design/design-ux-designer
"ai" → specialized/specialized-ai-ml-engineer
```

---

## 🧪 测试

```bash
# 运行内置测试
cd <YOUR_OPENCLAW_WORKSPACE>/skills/agent-selector-skill
python3 agent_selector.py
```

**预期输出**:
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
...

✅ 所有测试完成！
```

---

## 📚 集成示例

### RoundTable 集成

已在 `roundtable-skill/roundtable_engine.py` 中集成：

```python
from agent_selector import AgentSelector, select_roundtable_agents

class RoundTableEngine:
    def __init__(self, topic: str, ...):
        self.agent_selector = AgentSelector()
        self.agents = select_roundtable_agents(topic)
```

### Auto-Coding 集成

已在 `auto-coding/agent_controller.py` 中集成：

```python
from agent_selector import AgentSelector

class AgentController:
    def __init__(self):
        self.agent_selector = AgentSelector()
    
    def select_agent_for_task(self, task: str):
        return self.agent_selector.select_agent(task)
```

---

## ⚠️ 注意事项

### 1. 路径限制
- 只能访问 `skills` 目录内的 Agent
- 目录名必须在白名单中（`agency-agents`, `agency-agents-zh`, `agency`）

### 2. 文件大小
- 单个 Agent 文件不能超过 100KB
- 超大文件会被自动跳过

### 3. 错误处理
```python
try:
    selector = AgentSelector("/invalid/path")
except ValueError as e:
    print(f"路径验证失败：{e}")
```

---

## 🔗 相关链接

- **ClawHub**: https://clawhub.com/skills/agent-selector
- **RoundTable Skill**: `roundtable-skill/`
- **Auto-Coding**: `auto-coding/`
- **Agency Agents**: `agency-agents/`

---

## 📝 更新日志

### v2.0.0 (2026-03-20) - 安全增强版
- ✅ 添加路径白名单验证
- ✅ 添加文件大小限制（100KB）
- ✅ 添加输入长度限制（10000 字符）
- ✅ 添加符号链接验证
- ✅ 添加文件编码验证
- ✅ 错误信息脱敏
- ✅ 预编译正则表达式（防 DoS）

### v1.0.0 (2026-03-19) - 初始版本
- 基础 Agent 选择功能
- 关键词匹配
- RoundTable 集成

---

## 📄 许可证

MIT License - 虾软 Claw soft

---

*Agent Selector - 让你成为任何需要的专家*
