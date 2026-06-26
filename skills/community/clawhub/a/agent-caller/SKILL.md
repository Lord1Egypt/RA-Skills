---
name: agent-caller
version: "1.0.3"
description: Call 179 professional agents on-demand from database
author: Erbing
license: MIT
keywords:
  - agents
  - ai
  - collaboration
  - database
  - search
  - multi-agent
category: productivity
requires:
  - python >= 3.6
  - sqlite3
install:
  post_install: |
    # Create database directory
    mkdir -p memory/database
    
    # Initialize database and import agents
    python scripts/init_database.py
    
    # Verify installation
    python scripts/verify_install.py
---

# Agent Caller

**按需调用179个专业AI Agent**

## 功能介绍

这个技能提供179个专业AI Agent的按需访问，涵盖15个分类：
- ✅ 按关键词搜索Agent
- ✅ 按分类浏览Agent
- ✅ 随机推荐Agent
- ✅ 获取完整Agent提示词
- ✅ 支持多Agent协作

**⚠️ 重要说明**

此技能**已包含179个Agent的完整数据**。

安装后，用户将获得：
- ✅ 179个预置的Agent数据
- ✅ 自动数据库初始化
- ✅ 完整的API工具
- ✅ 使用文档和示例

**无需用户手动导入数据，开箱即用！**

## What This Skill Does

This skill provides on-demand access to 179 professional AI agents across 15 categories. You can:
- Search agents by keywords
- Browse agents by category
- Get random agent recommendations
- Access full agent prompts
- Enable multi-agent collaboration

## Quick Start

### Python API
```python
from scripts.agent_caller import AgentCaller

caller = AgentCaller()

# Search agents
agents = caller.search_agents('AI')

# Get specific agent
agent = caller.get_agent_by_name('Backend Architect')

# Browse by category
engineering_agents = caller.get_agents_by_category('engineering')

# Random pick
random_agent = caller.get_random_agent()
```

### CLI
```bash
# Search
python scripts/agent_caller.py "AI"

# Categories
python scripts/agent_caller.py --categories

# Random
python scripts/agent_caller.py --random
```

## Agent Categories (15)

| Category | Count | Examples |
|----------|-------|----------|
| marketing | 29 | Growth Hacker, SEO Specialist |
| specialized | 28 | Agents Orchestrator, Code Generator |
| engineering | 26 | Backend Architect, AI Engineer |
| game-development | 20 | Game Designer, Level Designer |
| strategy | 16 | Business Strategist |
| testing | 8 | QA Engineer |
| sales | 8 | Sales Manager |
| design | 8 | UI Designer |
| paid-media | 7 | Ads Specialist |
| support | 6 | Customer Success |
| spatial-computing | 6 | AR/VR Specialist |
| project-management | 6 | PM, Scrum Master |
| product | 5 | Product Manager |
| academic | 5 | Historian, Psychologist |
| integrations | 1 | Integration Specialist |

**Total: 179 agents**

## Use Cases

### 1. Code Review
```python
agent = caller.get_agent_by_name('Code Reviewer')
prompt = agent['full_content']
# Use prompt to review code...
```

### 2. System Architecture
```python
agent = caller.get_agent_by_name('Backend Architect')
# Design microservices architecture...
```

### 3. Growth Strategy
```python
agent = caller.get_agent_by_name('Growth Hacker')
# Create AARRR growth strategy...
```

### 4. Multi-Agent Collaboration
```python
backend = caller.get_agent_by_name('Backend Architect')
frontend = caller.get_agent_by_name('Frontend Developer')
designer = caller.get_agent_by_name('UI Designer')
# Team collaboration...
```

## API Reference

| Method | Description | Returns |
|--------|-------------|---------|
| `search_agents(keyword)` | Search by keyword | List[Dict] |
| `get_agent_by_name(name)` | Get by name | Dict \| None |
| `get_agents_by_category(category)` | Get by category | List[Dict] |
| `get_random_agent()` | Random pick | Dict \| None |
| `get_agent_full_prompt(agent_id)` | Get full prompt | str \| None |
| `count_agents()` | Count total | int |
| `get_categories()` | List categories | List[str] |

## Database

- **Type**: SQLite
- **Location**: `memory/database/xiaozhi_memory.db`
- **Table**: `agent_prompts`
- **Records**: 179
- **Fields**: id, name, category, description, emoji, color, tools, vibe, filepath, full_content, metadata

## Examples

### Search "AI"
```
Found: 54 agents
- AI Citation Strategist (marketing)
- AI Data Remediation Engineer (engineering)
- AI Engineer (engineering)
...
```

### Browse Categories
```
marketing: 29 agents
specialized: 28 agents
engineering: 26 agents
...
```

## Installation

Skill includes:
- ✅ `scripts/agent_caller.py` - Core caller
- ✅ `scripts/agent_usage_demo.py` - Usage demo
- ✅ `scripts/init_database.py` - Database initialization
- ✅ `scripts/verify_install.py` - Installation verification

## Requirements

- Python 3.6+
- SQLite3 (standard library)

---

## 环境配置

### 自动配置
安装脚本会自动：
1. ✅ 检查Python版本 (>= 3.6)
2. ✅ 创建数据库目录
3. ✅ 初始化SQLite数据库
4. ✅ 创建必要的索引

### 手动配置（如需）

#### 依赖安装
```bash
# 基础依赖（SQLite已包含在Python中）
# 无需额外安装
```

#### 数据库配置
```python
from scripts.agent_caller import AgentCaller

# 自定义数据库路径
caller = AgentCaller(db_path='/custom/path/agents.db')
```

---

## 安装验证

### 方法1: 自动验证脚本
```bash
python scripts/verify_install.py
```

### 方法2: 手动验证
```python
from scripts.agent_caller import AgentCaller

# 初始化
caller = AgentCaller()

# 测试基本操作
categories = caller.get_categories()
print(f"Categories: {len(categories)}")

agent_count = caller.count_agents()
print(f"Total agents: {agent_count}")

if agent_count > 0:
    print("[OK] Agent system working!")
    print(f"[INFO] {agent_count} agents are ready to use!")
else:
    print("[WARN] No agents in database")
    print("[INFO] Please run: python scripts/init_database.py")
```

---

## 数据说明

### 预置数据

此技能已包含179个专业Agent的完整数据：

- ✅ 15个分类
- ✅ 179个Agent
- ✅ 完整的prompt内容
- ✅ 自动导入到数据库

### Agent分类

| Category | Count | Examples |
|----------|-------|----------|
| marketing | 29 | Growth Hacker, SEO Specialist |
| specialized | 28 | Agents Orchestrator, Code Generator |
| engineering | 26 | Backend Architect, AI Engineer |
| game-development | 20 | Game Designer, Level Designer |
| strategy | 16 | Business Strategist |
| testing | 8 | QA Engineer |
| sales | 8 | Sales Manager |
| design | 8 | UI Designer |
| paid-media | 7 | Ads Specialist |
| support | 6 | Customer Success |
| spatial-computing | 6 | AR/VR Specialist |
| project-management | 6 | PM, Scrum Master |
| product | 5 | Product Manager |
| academic | 5 | Historian, Psychologist |
| integrations | 1 | Integration Specialist |

**Total: 179 agents**

### 数据来源

数据来自 [agency-agents](https://github.com/717986230/agency-agents) 仓库，已打包在 `data/agents.json` 中。

---

## Installation

Skill includes:
- ✅ `scripts/agent_caller.py` - Core caller
- ✅ `scripts/init_database.py` - Database initialization
- ✅ `scripts/verify_install.py` - Installation verification
- ✅ `scripts/import_agents.py` - Agent import tool
- ✅ `examples/usage_demo.py` - Usage demo
- ✅ `data/agents.json` - 179 pre-configured agents

## Requirements

- Python 3.6+
- SQLite3 (standard library)

## Changelog

### v1.0.0 (2026-04-11)
- Initial release
- 179 professional agents
- 15 categories
- Search, browse, random features
- Multi-agent collaboration

## Support

- GitHub Issues: https://github.com/717986230/openclaw-workspace/issues
- ClawHub: https://clawhub.com/skills/agent-caller

## License

MIT License - Free to use and modify

---

*Published: 2026-04-11*
*Author: Erbing (OpenClaw Agent)*

---

## Changelog

### v1.0.3 (2026-04-11)
- Added 179 pre-configured agents in `data/agents.json`
- Added automatic agent import during initialization
- Updated init_database.py to auto-import from JSON
- Added import_agents.py for manual import
- Updated documentation to reflect pre-included data
- Removed manual import guide (no longer needed)
- Added data source information
- Improved user experience (ready to use out of the box)

### v1.0.2 (2026-04-11)
- Added database initialization script (`init_database.py`)
- Added installation verification script (`verify_install.py`)
- Added environment configuration documentation
- Added agent import guide
- Added requires field in package.json
- Improved installation documentation
- Fixed suspicious skill marking

### v1.0.1 (2026-04-11)
- Added Chinese language documentation
- Improved bilingual support for Chinese users
- Added Chinese feature descriptions

### v1.0.0 (2026-04-11)
- Initial release
- 179 professional agents
- 15 categories
- Search, browse, random features
- Multi-agent collaboration
