---
name: feishu-agent-team
description: 在 OpenClaw 中构建多 Agent 团队协作系统。Coordinator（调度中心）接收 Feishu 群聊 @mention，自动路由任务到专业 Agent，支持自定义 Agent 角色和数量。适用于：(1) 需要 AI 团队处理多类型任务 (2) 希望用单一入口调度专家 Agent (3) 构建自动化工作流团队。
metadata:
  {
    "openclaw":
      {
        "requires": { "commands": ["python3"] },
        "install": [],
      },
  }
---

# Feishu Agent Team - 多 Agent 团队协作系统

## 概念

将多个 AI Agent 组织成"团队"：
- **1 个 Coordinator** - 调度中心，接收所有消息并分发
- **N 个 Specialist** - 专家 Agent，各司其职

```
                    ┌─→ Specialist-A (商分)
                    │
User @Coordinator ──┼─→ Specialist-B (市场)
    │               │
    │               └─→ Specialist-C (开发)
    │
    └──→ [State] ←──┘
```

## 核心功能

- **智能路由**：关键词匹配 → 自动分发到对应专家
- **Feishu 集成**：群 @mention 触发调度，支持多群配置
- **跨 Agent 通信**：MQ 消息队列异步协作
- **状态持久化**：LangGraph Checkpoint 支持断点恢复
- **可扩展**：添加任意数量的专家 Agent

## 安装

```bash
# 进入 OpenClaw workspace
cd ~/.openclaw/workspace

# 克隆项目
git clone <repo-url> feishu-agent-team

# 安装依赖
pip install langgraph langchain-openai feishu-oapi

# 初始化
python team.py init
```

## 快速配置

### 1. 定义团队角色

编辑 `config/team.yaml`:

```yaml
coordinator:
  name: "Coordinator"        # 调度中心名称
  mention_name: "coordinator" # 群里的 @ 名称

specialists:
  - name: "Analyst"          # 专家1
    specialty: "商业分析"
    keywords: ["分析", "市场", "投资", "趋势", "商分"]
    
  - name: "Developer"        # 专家2
    specialty: "技术开发"
    keywords: ["代码", "开发", "bug", "技术", "架构"]
    
  - name: "Marketer"          # 专家3
    specialty: "市场推广"
    keywords: ["推广", "增长", "内容", "运营"]
```

### 2. 配置 OpenClaw 绑定

```json
{
  "bindings": [
    {
      "agentId": "coordinator",
      "match": { "channel": "feishu", "accountId": "coordinator" }
    },
    {
      "agentId": "analyst",
      "match": { "channel": "feishu", "accountId": "analyst" }
    },
    {
      "agentId": "developer",
      "match": { "channel": "feishu", "accountId": "developer" }
    },
    {
      "agentId": "marketer",
      "match": { "channel": "feishu", "accountId": "marketer" }
    }
  ]
}
```

### 3. 配置 Feishu App

```json
{
  "channels": {
    "feishu": {
      "accounts": {
        "coordinator": {
          "appId": "cli_xxx",
          "appSecret": "xxx",
          "groupPolicy": "open",
          "groups": {
            "YOUR_GROUP_ID": {
              "enabled": true,
              "requireMention": true,
              "groupSessionScope": "group_sender"
            }
          }
        },
        "analyst": { "appId": "cli_yyy", "appSecret": "yyy" },
        "developer": { "appId": "cli_zzz", "appSecret": "zzz" },
        "marketer": { "appId": "cli_aaa", "appSecret": "aaa" }
      }
    }
  }
}
```

### 4. 启动 Agent 监听

```bash
# 每个 Specialist Agent 运行一个监听进程
python listeners/specialist_listener.py --agent analyst &
python listeners/specialist_listener.py --agent developer &
python listeners/specialist_listener.py --agent marketer &
```

## 使用方式

### 群里 @ Coordinator 发任务

```
@Coordinator 分析一下当前AI市场的投资趋势
```

Coordinator 自动识别 → 分发给 Analyst → Analyst 在群里回复。

### 支持多类型任务

```
@Coordinator 开发一个用户登录模块
@Coordinator 推广我们的新产品
@Coordinator 分析竞品情况
```

### CLI 方式

```bash
# 测试任务路由
python team.py route "我想推广新产品"  # → Marketer

# 运行任务
python team.py run "分析竞争对手"

# 查看团队状态
python team.py info
```

### Python API

```python
from src.api import TeamGraphAPI

api = TeamGraphAPI()

# 执行任务
result = api.process("市场调研报告", team_config="config/team.yaml")
print(result["specialist"])  # 自动路由到对应专家
```

## 自定义指南

### 添加新的专家 Agent

1. 在 `config/team.yaml` 添加:

```yaml
specialists:
  - name: "Designer"
    specialty: "UI设计"
    keywords: ["设计", "界面", "UI", "UX", "图标", "海报"]
```

2. 创建监听器:

```python
# listeners/designer_listener.py
from src.listeners.base import SpecialistListener

class DesignerListener(SpecialistListener):
    name = "designer"
    specialty = "UI设计"

if __name__ == "__main__":
    DesignerListener().start()
```

3. 添加 OpenClaw 绑定和 Feishu 账号

4. 启动监听: `python listeners/designer_listener.py &`

### 修改路由逻辑

编辑 `src/graph.py` 中的路由函数:

```python
def route_to_specialist(state: TeamState) -> str:
    task = state["task"].lower()
    
    # 自定义路由规则
    if any(kw in task for kw in ["分析", "研究", "报告"]):
        return "analyst"
    elif any(kw in task for kw in ["开发", "代码", "bug"]):
        return "developer"
    # ... 更多规则
    
    return "coordinator"  # 默认保留给调度者处理
```

### 多群支持

配置多个群组 ID:

```json
{
  "channels": {
    "feishu": {
      "accounts": {
        "coordinator": {
          "groups": {
            "GROUP_ID_1": { "enabled": true, "requireMention": true },
            "GROUP_ID_2": { "enabled": true, "requireMention": true },
            "GROUP_ID_3": { "enabled": true, "requireMention": true }
          }
        }
      }
    }
  }
}
```

## 工作原理

```
1. 用户在 Feishu 群 @Coordinator 发送任务
                          ↓
2. Coordinator 接收消息，提取任务内容
                          ↓
3. 任务路由函数分析关键词，匹配专家
                          ↓
4. 通过 MQ 消息队列分发任务给对应专家
                          ↓
5. Specialist Agent 接收任务，在群里回复
```

## 技术栈

- **状态机**: LangGraph
- **持久化**: SQLite Checkpoint
- **消息队列**: 轻量级 MQ 实现
- **飞书集成**: feishu-oapi

## 项目结构

```
feishu-agent-team/
├── SKILL.md
├── README.md
├── config/
│   └── team.yaml           # 团队配置（角色、关键词）
├── src/
│   ├── __init__.py
│   ├── api.py              # Python API
│   ├── graph.py            # LangGraph 图定义
│   ├── nodes.py            # 节点逻辑
│   ├── state.py            # 状态定义
│   ├── routing.py          # 路由逻辑
│   ├── feishu_group.py     # Feishu 群操作
│   └── persistence/         # Checkpoint 持久化
├── listeners/
│   ├── base.py              # 监听器基类
│   ├── analyst_listener.py
│   ├── developer_listener.py
│   └── marketer_listener.py
├── team.py                 # CLI 入口
└── tests/
```

## 常见问题

**Q: 需要多少个 Feishu App？**
A: 最少 2 个（1 个 Coordinator + 1 个 Specialist），最多 N+1 个。

**Q: 如何添加更多专家？**
A: 见"自定义指南 - 添加新的专家 Agent"。

**Q: 任务失败怎么办？**
A: Coordinator 会保留任务状态，可通过 `python team.py retry <task_id>` 重试。

## 许可证

MIT License - 免费使用

## 支持

遇到问题提交 Issue
