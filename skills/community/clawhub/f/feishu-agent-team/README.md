# Feishu Agent Team

在 OpenClaw 中构建多 Agent 团队协作系统。

## 概念

将多个 AI Agent 组织成"团队"：
- **1 个 Coordinator** - 调度中心，接收所有消息并分发
- **N 个 Specialist** - 专家 Agent，各司其职

## 快速开始

### 1. 克隆项目

```bash
cd ~/.openclaw/projects
git clone <repo-url> feishu-agent-team
cd feishu-agent-team
```

### 2. 安装依赖

```bash
pip install pyyaml
```

### 3. 配置团队

编辑 `config/team.yaml` 自定义团队角色和关键词。

### 4. 测试路由

```bash
python team.py route "分析AI市场趋势"
# → Analyst
```

### 5. 查看团队

```bash
python team.py info
```

## 配置说明

编辑 `config/team.yaml`:

```yaml
coordinator:
  name: "Coordinator"
  mention_name: "coordinator"  # Feishu 群里的 @ 名称

specialists:
  - name: "Analyst"
    keywords: ["分析", "市场", "投资", ...]
    session_key: "agent:analyst:main"
```

## 工作原理

1. 用户在 Feishu 群 @Coordinator 发送任务
2. Coordinator 接收消息，提取任务内容
3. 路由函数分析关键词，匹配专家
4. 任务分发到对应专家 Agent
5. Specialist 回复到群里

## 许可证

MIT License
