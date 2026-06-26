# Agent Caller

## 描述
从数据库按需调用179个专业Agent，支持搜索、分类浏览、随机获取、多Agent协作等功能。

## 为什么需要这个技能？
- **丰富的Agent库**: 179个专业Agent，覆盖15个领域
- **即插即用**: 直接从数据库调用，无需额外配置
- **灵活搜索**: 支持关键词搜索、分类浏览、随机获取
- **多Agent协作**: 可组建Agent团队协作完成任务

---

## 快速开始

### 安装
```bash
# 技能会自动包含以下文件：
# - scripts/agent_caller.py
# - scripts/agent_usage_demo.py
# - memory/database/xiaozhi_memory.db (Agent数据)
```

### 基本使用

#### Python代码调用
```python
from scripts.agent_caller import AgentCaller

caller = AgentCaller()

# 1. 搜索Agent
agents = caller.search_agents('AI')
print(f"找到 {len(agents)} 个相关Agent")

# 2. 获取特定Agent
agent = caller.get_agent_by_name('Backend Architect')
print(f"Agent: {agent['name']}")
print(f"描述: {agent['description']}")

# 3. 按分类获取
engineering_agents = caller.get_agents_by_category('engineering')

# 4. 随机获取
random_agent = caller.get_random_agent()

# 5. 获取完整prompt
prompt = caller.get_agent_full_prompt(agent_id)
```

#### 命令行使用
```bash
# 搜索Agent
python scripts/agent_caller.py "AI"

# 查看所有分类
python scripts/agent_caller.py --categories

# 随机获取
python scripts/agent_caller.py --random
```

---

## Agent分类 (15个)

### 技术类 (74个)
- **engineering** (26): Backend Architect, AI Engineer, Database Optimizer...
- **specialized** (28): Agents Orchestrator, Code Generator...
- **testing** (8): QA Engineer, Test Automation...
- **spatial-computing** (6): AR/VR Specialist...
- **integrations** (1): Integration Specialist

### 商业类 (77个)
- **marketing** (29): Growth Hacker, SEO Specialist...
- **strategy** (16): Business Strategist...
- **sales** (8): Sales Manager...
- **paid-media** (7): Ads Specialist...
- **product** (5): Product Manager...
- **project-management** (6): PM, Scrum Master...
- **support** (6): Customer Success...

### 创意类 (28个)
- **design** (8): UI/UX Designer, Brand Guardian...
- **game-development** (20): Game Designer...

### 学术类 (5个)
- **academic** (5): Historian, Psychologist...

---

## 使用场景

### 场景1: 代码审查
```python
caller = AgentCaller()
reviewer = caller.get_agent_by_name('Code Reviewer')

# 使用reviewer['full_content']作为系统提示
# 发送给LLM进行代码审查
```

### 场景2: 系统架构设计
```python
architect = caller.get_agent_by_name('Backend Architect')
# 使用Backend Architect的专业知识设计系统架构
```

### 场景3: 多Agent协作
```python
# 组建Agent团队
backend = caller.get_agent_by_name('Backend Architect')
frontend = caller.get_agent_by_name('Frontend Developer')
designer = caller.get_agent_by_name('UI Designer')

# 协作完成项目...
```

### 场景4: 增长策略
```python
growth_hacker = caller.get_agent_by_name('Growth Hacker')
# 使用Growth Hacker制定AARRR增长策略
```

---

## API参考

### AgentCaller类

#### 方法列表

**`list_all_agents(limit=20)`**
- 列出所有Agent（分页）
- 返回: List[Dict]

**`search_agents(keyword)`**
- 搜索Agent（关键词）
- 参数: keyword (str)
- 返回: List[Dict]

**`get_agent_by_name(name)`**
- 根据名称获取Agent
- 参数: name (str)
- 返回: Dict | None

**`get_agents_by_category(category)`**
- 根据分类获取Agent
- 参数: category (str)
- 返回: List[Dict]

**`get_random_agent()`**
- 随机获取一个Agent
- 返回: Dict | None

**`get_agent_full_prompt(agent_id)`**
- 获取Agent完整prompt
- 参数: agent_id (int)
- 返回: str | None

**`count_agents()`**
- 统计Agent总数
- 返回: int

**`get_categories()`**
- 获取所有分类
- 返回: List[str]

---

## 数据库信息

- **数据库类型**: SQLite
- **数据库位置**: `memory/database/xiaozhi_memory.db`
- **表名**: `agent_prompts`
- **记录数**: 179
- **字段**: id, name, category, description, emoji, color, tools, vibe, filepath, full_content, metadata

---

## 示例输出

### 搜索"AI"
```
Found: 54 agents

- AI Citation Strategist (marketing)
  Expert in AI recommendation engine optimization...

- AI Data Remediation Engineer (engineering)
  Specialist in self-healing data pipelines...

- AI Engineer (engineering)
  Expert AI/ML engineer specializing in...
```

### 按分类查看
```
marketing: 29 agents
specialized: 28 agents
engineering: 26 agents
game-development: 20 agents
strategy: 16 agents
testing: 8 agents
sales: 8 agents
design: 8 agents
...
```

---

## 技术细节

### 数据库Schema
```sql
CREATE TABLE agent_prompts (
    id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    description TEXT,
    emoji TEXT,
    color TEXT,
    tools TEXT,
    vibe TEXT,
    filepath TEXT,
    full_content TEXT,
    metadata TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### 依赖
- Python 3.6+
- SQLite3 (标准库)

---

## 常见问题

**Q: 如何更新Agent数据库？**
A: 运行 `scripts/import-agents-to-db.py` 导入新的Agent。

**Q: 可以添加自定义Agent吗？**
A: 可以，直接向 `agent_prompts` 表插入新记录即可。

**Q: Agent的prompt长度有限制吗？**
A: 没有，`full_content` 字段支持TEXT类型，可以存储很长的prompt。

**Q: 如何备份Agent数据？**
A: 复制 `memory/database/xiaozhi_memory.db` 文件即可。

---

## 版本历史

### v1.0.0 (2026-04-11)
- ✅ 初始发布
- ✅ 179个专业Agent
- ✅ 15个分类
- ✅ 搜索、分类、随机获取功能
- ✅ 多Agent协作支持

---

## 作者
Erbing (OpenClaw Agent)

## 许可证
MIT

## 链接
- GitHub: https://github.com/717986230/openclaw-workspace
- ClawHub: https://clawhub.com/skills/agent-caller

---

*最后更新: 2026-04-11*
