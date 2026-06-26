# daily-security-check（每日安全巡检）

OpenClaw 的「每日安全巡检」技能：按固定清单检查网关 loopback、防火墙、API 密钥、SOUL.md 安全规则、身份与访问控制等，并执行 `openclaw security audit` 与 `openclaw doctor`，输出简短报告与 0–10 安全评分。

## 功能说明

- **只读检查**：不修改任何配置，仅执行检查并生成报告。
- **检查项**：网关绑定、防火墙提醒、明文凭证、SOUL.md 安全监控规则、认证异常、身份与访问控制、工具与沙箱策略、官方 security audit、openclaw doctor。
- **输出**：结构化 Markdown 报告（300–600 字）、安全评分（0–10）、结论与待办；可保存到 `workspace/docs/security-audit/security-report-YYYY-MM-DD.md`。

## 使用方式

### 何时触发

- 用户说「执行安全巡检」「daily-security-check」或「每日安全巡检」时。
- 可由 cron 等定时任务在独立会话中触发，结果可发往 Telegram、飞书等（需自行配置）。

### 安装（Cursor / 本地 skill）

将本目录放到你的 skill 目录下，例如：

- **项目内**：`.cursor/skills/daily-security-check/` 或 OpenClaw 的 `skills/daily-security-check/`
- **全局**：`~/.cursor/skills/daily-security-check/`

确保目录内包含 `SKILL.md`、`references/CHECKLIST.md`、`assets/` 等文件。

### 通过 ClawHub 安装（OpenClaw）

```bash
clawhub install daily-security-check
```

（发布到 ClawHub 后，用户可用上述命令安装。）

## 依赖与要求

- **运行环境**：在 OpenClaw 项目根或已配置 `OPENCLAW_STATE_DIR` 的环境中执行。
- **命令**：需已安装 OpenClaw CLI，并能执行 `openclaw security audit`、`openclaw doctor`。
- **报告路径**：报告默认写入 `workspace/docs/security-audit/`（相对于项目根），请确保该目录存在或 agent 有权限创建。

## 目录结构

```
daily-security-check/
├── SKILL.md              # 技能主说明（必读）
├── clawhub.json          # ClawHub 发布元数据
├── README.md             # 本文件
├── CHANGELOG.md          # 版本变更
├── references/
│   └── CHECKLIST.md      # 检查清单
└── assets/
    ├── report-template.md
    ├── source-article-security-config.md
    ├── gateway-port-security.md
    └── community-official-security-extras.md
```

## 许可与致谢

- **许可证**：MIT
- **参考**：Bruce Van《保姆级教程：7 步配置 OpenClaw》第 6 步；OpenClaw 官方安全文档与社区实践。

## 问题与反馈

请在 GitHub 仓库的 Issues 中提交问题或建议。
