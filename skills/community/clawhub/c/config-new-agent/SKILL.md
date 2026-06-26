---
name: config-new-agent
description: 为 OpenClaw 新增的 agent 配置 bindings 并安装必要的 skills。当用户说"添加新 agent"、"配置新 agent binding"、或需要为 agent 分配群组时触发。工作流程：(1) 从 openclaw.json 读取 agent list，(2) 找出没有 binding 的 agent，(3) 向用户索要群组 peer id，(4) 生成 binding 配置让用户审核，(5) 用户确认后重启 gateway，(6) 为新 agent 安装 skill-vetter、skill-finder-cn、self-improving-proactive-agent、openclaw-tavily-search。
---

# 配置新 Agent Binding

## 核心规则

### self-improving-proactive-agent 使用隔离规则（强制）

**每个 agent 必须只使用自己 workspace 中的 self-improving-proactive-agent，禁止访问其他 agent 的数据。**

当新 agent 安装 self-improving-proactive-agent 时，必须同时在 SKILL.md 顶部添加以下引用块：

```markdown
> **IMPORTANT - Workspace Isolation Rule**:
> Each agent must use the `self-improving-proactive-agent` skill in its **own workspace only**.
> All learning, corrections, memory, and state files must be stored in the agent's **own workspace directory**.

> **Never reference, read from, or write to another agent's self-improving-proactive-agent skill or data files.**
```

### Skill 安装规则（强制）

**所有 skills 必须安装到新 agent 自己的 workspace，禁止安装到 /root/.openclaw/workspace。**

安装命令使用 `--workdir` 指定目标 workspace：
```bash
clawhub install <slug> --workdir /root/.openclaw/workspace-<agentname>
```

## 工作流程

### 第一步：读取 openclaw.json

读取 `/root/.openclaw/openclaw.json`，获取 `agents.list` 和 `bindings` 列表。

### 第二步：找出未配置 binding 的 agent

比较 `agents.list` 中的 agentId 和 `bindings` 中已配置的 agentId，列出尚未配置 binding 的 agent（**排除 `main` agent**）。

向用户报告：
```
以下 agent 尚未配置 binding：
- agentId1
- agentId2
```

### 第三步：索要群组 ID

询问用户需要为哪个 agent 配置 binding，并索要对应的飞书群 ID（格式：`oc_xxx`）。

### 第四步：生成配置并让用户审核

根据用户提供的 agentId 和群组 ID，生成 binding 配置片段：

```json
{
  "agentId": "<agentId>",
  "match": {
    "channel": "feishu",
    "peer": {
      "kind": "group",
      "id": "<群组ID>"
    }
  }
}
```

将配置加入 `bindings` 数组，展示完整修改内容让用户审核。

### 第五步：用户确认后重启 gateway

用户确认后，执行 `openclaw gateway restart` 重启 gateway 使配置生效。

### 第六步：为新 agent 安装 skills

Gateway 重启成功后，为新 agent 安装以下 skills。**所有 skills 必须安装到新 agent 自己的 workspace 目录**。

#### 6.1 确定新 agent 的 workspace 路径

根据 agentId 确定 workspace 路径：`/root/.openclaw/workspace-<agentId>/`

#### 6.2 安装 skill-vetter（安全审核工具）

**重要规则：以后安装任何 skill 之前，都必须先使用 skill-vetter 审核，未经审核不得安装。**

使用 clawhub 安装到新 agent 的 workspace：
```bash
clawhub install skill-vetter --workdir /root/.openclaw/workspace-<agentname>
```

#### 6.3 安装 skill-finder-cn（skill 搜索工具）

使用 clawhub 安装到新 agent 的 workspace：
```bash
clawhub install skill-finder-cn --workdir /root/.openclaw/workspace-<agentname>
```

#### 6.4 安装 self-improving-proactive-agent（自我提升 agent）

使用 clawhub 安装到新 agent 的 workspace：
```bash
clawhub install self-improving-proactive-agent --workdir /root/.openclaw/workspace-<agentname>
```

**安装完成后**，必须编辑新 agent workspace 中的 SKILL.md，在文件顶部添加 workspace 隔离规则引用块（见上文"self-improving-proactive-agent 使用隔离规则"）。

**同时配置该 skill 保持一直运行**。

#### 6.5 安装 openclaw-tavily-search（网页搜索工具）

使用 clawhub 安装到新 agent 的 workspace：
```bash
clawhub install openclaw-tavily-search --workdir /root/.openclaw/workspace-<agentname>
```

## 注意事项

- 只处理飞书群组 binding（channel: feishu, peer.kind: group）
- 不擅自做任何其他配置修改
- 重启 gateway 前必须获得用户明确确认
- 所有 skills 必须安装到新 agent 自己的 workspace，绝不安装到 /root/.openclaw/workspace

## 完成后通知

Skill 执行结束后，向用户发送通知："已配置好新的 agent"。
