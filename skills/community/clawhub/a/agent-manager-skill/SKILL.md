***

name: agent-manager
description: Manage OpenClaw Agents. Create new agents, configure workspaces, manage Feishu bot integrations (QR code scanning, bindings), and verify multi-bot routing.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Agent 管理专家 (Agent Manager)

本技能用于帮助用户快速创建、配置和管理 OpenClaw Agent 及其飞书绑定。

## 核心流程（必须严格遵守）

### 1. 需求确认 (Triage) - ⚠️ 关键原则：信息收集完才能发确认

在执行任何操作前，你需要收集齐以下所有信息：

- Agent 的中文名称（如果用户说了主要用途或者功能描述，你可以帮忙拟名字）
- Agent 的主要用途/功能描述（用户自己说，或者你根据用户提供的信息去补充）
- 是否需要绑定飞书机器人（默认需要创建新的机器人）

**收集规则：**
信息都收集齐全后，使用下面的模板向用户发送确认卡片。

**最终确认模板：**

```
📋 创建计划确认

请确认以下信息：
- **Agent 中文名**：[用户提供的名称]
- **Agent ID**：[自动推断的英文ID，例如 sales-assistant]
- **工作区路径**：`~/.openclaw/workspace-[ID]`
- **功能描述**：[用户提供的功能描述]
- **飞书机器人**：[新建（默认）/绑定已有/暂不绑定]
- **机器人权限**：[全部放开（默认）/需要认证]

确认请回复"确认"或"是"，如有修改请说明。
```

### 2. 飞书快捷创建流程 (Feishu Quick Setup Flow)

如果用户选择了“新建”飞书机器人，**在确认计划后，你需要执行以下交互式步骤**：

1. **获取授权链接**：运行以下脚本生成飞书授权 URL：
   ```bash
   python3 ~/.openclaw/workspace/skills/agent-manager/scripts/feishu_auth.py generate
   ```
2. **发送快捷授权卡片给用户**：脚本运行后会输出 `URL=https://...`。请**使用 Markdown 的链接语法包装成一个醒目的按钮/卡片形式**发送给用户，并提示他们点击授权。

   **必须使用的回复格式示例：**
   > 请点击下方按钮完成飞书机器人授权：
   >
   > 🔗 **[👉 点击这里快捷创建飞书机器人 👈](这里填入脚本输出的URL)**
   >
   > *(授权完成后，请回复“好了”或“已完成”)*
3. **轮询结果**：当用户回复“好了”之后，运行轮询脚本获取 `app_id` 和 `app_secret`：
   ```bash
   python3 ~/.openclaw/workspace/skills/agent-manager/scripts/feishu_auth.py poll
   ```

### 3. 执行创建 (Execution)

在完成确认（和飞书凭证获取）后，使用提供的脚本创建 Agent：

```bash
# 如果不需要绑定飞书
python3 ~/.openclaw/workspace/skills/agent-manager/scripts/manage_agent.py create \
  --name "销售助手" \
  --id "sales-assistant" \
  --description "负责处理销售数据和客户跟进"

# 如果需要绑定飞书，且权限为【全部放开（默认，open）】
python3 ~/.openclaw/workspace/skills/agent-manager/scripts/manage_agent.py create \
  --name "销售助手" \
  --id "sales-assistant" \
  --description "负责处理销售数据和客户跟进" \
  --app-id "cli_xxx" \
  --app-secret "yyy"

# 如果需要绑定飞书，且用户明确要求【需要认证（pairing）】
python3 ~/.openclaw/workspace/skills/agent-manager/scripts/manage_agent.py create \
  --name "销售助手" \
  --id "sales-assistant" \
  --description "负责处理销售数据和客户跟进" \
  --app-id "cli_xxx" \
  --app-secret "yyy" \
  --require-pairing
```

### 4. 收尾工作 (Cleanup & Restart)

**必须按顺序严格执行以下步骤：**

1. **执行完毕后，先向用户汇报**：“✅ Agent [中文名] 及其相关配置已经创建完毕！为了避免 Git 嵌套冲突，我已经自动清理了它的 `.git` 目录。”
2. **询问是否重启**：向用户询问：“一切准备就绪，需要现在为您重启 OpenClaw 网关以使新机器人上线吗？”
3. **等待用户回复**：只有当用户明确回复“重启”、“好的”或类似同意的指令后。
4. **执行重启**：
   - 发消息：“🔄 正在重启网关，请稍候（约30秒）...”
   - 执行命令：`openclaw gateway restart`
   - 检查状态：`openclaw gateway status`
   - 发消息告知：“✅ 网关重启成功！[中文名]已上线，可以开始使用了。”

## 附带资源 (Bundled Resources)

- `scripts/manage_agent.py`: 核心创建脚本（自动创建 Agent，写入配置并清理工作区）。
- `scripts/feishu_auth.py`: 飞书快捷授权链接生成与轮询脚本。
- `scripts/verify_bindings.py`: 验证飞书账号与 Agent 的绑定关系。

