---
name: feishu-team-manager
description: 自动化招聘新 Agent，配置独立飞书/ Discord 机器人并重构多账号路由
requires:
  binaries: [openclaw]
  env: [HOME]
  credentials:
    - description: 飞书 App ID（机器人应用凭证）
      env: LARK_APP_ID
    - description: 飞书 App Secret（机器人应用凭证）
      env: LARK_APP_SECRET
    - description: Discord Bot Token（可选，如需 Discord 绑定）
      env: DISCORD_BOT_TOKEN
---

# feishu-team-manager (HR 大姐头)

飞书/Discord 多 Agent 团队管理 Skill。基于"大姐头"招聘方案，实现 Agent 招聘、独立 Bot 绑定与环境自适配。

> **适用范围**：飞书（主推）| Discord（可选支持）—— 通过独立账户级路由为每个 Agent 绑定专属机器人。

## 依赖要求

- **OpenClaw >= 2026.3.20**
- 系统需安装 `openclaw` CLI 并配置在 PATH 中

## 路由绑定方案

本 Skill 采用 **2026-04-21 实践通过** 的"账户级路由"方案，确保每个机器人拥有独立的身份、头像和快捷指令。

### 核心逻辑
- **独立身份 (Account)**：每个机器人对应飞书开放平台的一个独立应用。
- **精准映射 (Binding)**：通过 `accountId` 将特定机器人发来的消息路由到指定的物理工作空间。

## 技能结构

```
feishu-team-manager/
├── index.js              # 安装引导与环境适配器（含用户确认、依赖检查、配置文件备份）
├── SKILL.md              # 本文档
├── _meta.json            # 元数据与安全声明
├── assets/
│   ├── templates/        # HR Agent 身份模板 (IDENTITY/SOUL/AGENTS)
│   └── cards/            # 飞书消息卡片模板
├── scripts/
│   ├── recruit_agent.py  # 物理空间创建与 Agent 初始化
│   ├── bind_bot.py       # 核心配置注入，重构 openclaw.json（含自愈与冲突检测）
│   ├── check_env.py      # 团队状态巡检
│   └── monitor_usage.py  # 使用量监控
└── promotion/            # 推广素材
```

## 使用方式

### 1. 招聘新员工
直接对"大姐头"说："招聘一个运维 Agent，起名叫运维小弟"。

执行流程：
1. 创建 `~/.openclaw/agents/{agent_name}` 工作目录
2. 注入专属的 `IDENTITY.md` / `SOUL.md` / `AGENTS.md`
3. 提示你提供该员工对应的飞书机器人凭据

### 2. 绑定机器人
说："帮运维小弟绑定机器人，App ID 是 cli_xxx，Secret 是 yyy"。

执行流程：
1. 自动注入 `channels.feishu.accounts` 配置
2. 自动设置 `bindings` 路由
3. 执行 `openclaw doctor --fix` 校验配置
4. 执行 `openclaw gateway restart` 重启生效

### 3. 安装首次部署

当此 Skill 首次运行时，`index.js` 会：

1. **依赖检查** — 确认 `openclaw` CLI 可用，配置文件存在
2. **用户确认** — 显示操作清单（创建工作空间、注入身份文件、注册 Agent），询问你是否继续
3. **配置文件备份** — 自动生成 `.bak_[时间戳]` 格式备份
4. **执行部署** — 创建 HR 工作空间、复制技能文件、注册 Agent
5. **引导提示** — 提示运行 `openclaw gateway restart` 生效

> 所有修改 `openclaw.json` 的操作前都会自动备份，你随时可以回滚。

## 安全说明

- **高权限操作需确认**：首次部署、绑定机器人等操作在交互环境下会先询问你的同意
- **自动备份**：每次修改配置前生成备份文件
- **冲突拦截**：绑定机器人时会检查 App ID 是否已被占用
- **配置验证**：修改后自动运行 `openclaw doctor --fix` 校验完整性
- **恢复方法**：如遇到问题，使用备份文件 `~/.openclaw/openclaw.json.bak_[时间戳]` 手动恢复

## 注意事项

- **保留现有配置**：现有 `appId/appSecret` 完全不动
- **dmScope 自动设置**：`bind_bot.py` 自动设置 `dmPolicy: "open"`
- **Gateway 重启**：重启后约 10-30 秒恢复服务

## 支持作者

如果你觉得这个技能对你有帮助，可以考虑支持作者继续开发：

- **微信赞赏码**：<image url="https://gitee.com/noahtao/wordpress-auto-publisher/raw/main/images/wechat_donate.png"/>
- **支付宝**：<image url="https://gitee.com/noahtao/wordpress-auto-publisher/raw/main/images/alipay_donate.jpg"/>
- **GitHub Sponsors**：https://github.com/sponsors/htf0513
- **定制服务**：联系微信/邮箱获取企业级定制
