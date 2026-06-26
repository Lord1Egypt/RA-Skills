# feishu-agent-config-helper

**飞书 Agent 配置助手**：简化 OpenClaw 与飞书机器人的集成过程。本技能将指导用户如何将飞书机器人配置到 `openclaw.json`，并与指定的 Agent 进行绑定。

**功能**：
- **生成配置片段**：根据用户提供的 App ID, App Secret, Agent ID 等信息，生成 `openclaw.json` 所需的配置代码。
- **配置指导**：提供详细的步骤，引导用户正确修改 `openclaw.json` 文件。
- **绑定说明**：解释如何进行账户级绑定和群聊级绑定，并提示优先级。
- **会话作用域设置**：指导用户设置 `session.dmScope` 以确保配置生效。
- **Gateway 重启提示**：提醒用户重启 OpenClaw Gateway 以加载新配置。

**使用场景**：
- 首次配置飞书机器人与 OpenClaw Agent。
- 为现有飞书机器人添加新的 Agent 绑定。
- 希望更方便、安全地管理飞书 Agent 配置的 OpenClaw 用户。

**本技能不会**：
- 直接修改您的 `openclaw.json` 文件（出于安全考量，配置更改需由用户手动完成）。
- 自动重启 OpenClaw Gateway。
- 提供飞书 App ID 和 App Secret 的申请通道。
