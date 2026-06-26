---
name: daily-security-check
description: OpenClaw 每日安全巡检技能。按固定清单检查网关 loopback、防火墙提醒、API 密钥在 .env、SOUL.md 安全规则、认证异常，并执行 openclaw security audit 与 openclaw doctor，输出简短报告与 0–10 安全评分；可由 cron 定时触发，结果可投递到 Telegram 等。Use when user says "安全巡检", "daily-security-check", or "执行每日安全巡检"。
---

# daily-security-check（每日安全巡检）

## When to use this skill

- 用户或定时任务说「执行安全巡检」「按 daily-security-check 执行」或「每日安全巡检」时。
- 可由 cron 等定时任务在独立会话中触发，结果可发往 Telegram、飞书等（需自行配置）。

## 调用约定（重要）

- **仅在显式请求时执行**：一般情况下不要主动 @ 或加载本 skill；仅当用户明确要求「安全巡检」「daily-security-check」或 cron 到点触发时才执行。
- **assets 为备份/参考**：`assets/community-official-security-extras.md` 与 `assets/source-article-security-config.md` 为备份与溯源用文档，常规对话中不要调用或引用，仅在执行本 skill 时按需查阅。

## Who uses it

- **使用者**：任何在 OpenClaw 仓库中运行本技能的 agent 或用户。
- **定位**：对应 Bruce Van 文章《保姆级教程：7 步配置 OpenClaw》第 6 步；只做检查与报告，不自动修改配置。

## How to execute

1. **加载检查清单**：按 [references/CHECKLIST.md](references/CHECKLIST.md) 中的项逐项执行（网关 loopback、防火墙提醒、API 密钥在 .env、SOUL.md 安全规则、认证异常、身份与访问控制、工具与沙箱等）。
2. **运行官方审计**：在项目根或设置 `OPENCLAW_STATE_DIR` 后执行 `openclaw security audit`，将 Summary 及关键 WARN 纳入报告；详见 CHECKLIST 第 8 项。
3. **运行 OpenClaw doctor**：在项目根执行 `openclaw doctor`（若使用非默认状态目录，请先设置 `OPENCLAW_STATE_DIR`）。仅只读检查，不执行 `--fix`；若有建议修复则提醒用户本地手动执行 `openclaw doctor --fix`。详见 CHECKLIST 第 9 项。
4. **汇总输出**：按 [assets/report-template.md](assets/report-template.md) 的结构输出报告，包含安全评分（0–10）、结论、待办；发现异常时明确标出并提醒用户。
5. **保存报告**：将报告写入 **`workspace/docs/security-audit/security-report-YYYY-MM-DD.md`**（日期为巡检日，路径相对于 OpenClaw 项目根），便于留存与追溯；可选投递到 Telegram 等。
6. **不交互**：cron 触发时不要进行交互式询问，直接执行并输出报告；全文使用简体中文。
7. **回复仅限报告**：执行本技能时，**只输出一份结构化报告**（按 report-template 的格式）。不要输出「我注意到您使用了…」「我将执行…」「首先/然后…」等步骤说明；报告发出后无需再发任何总结、解释或重复执行描述。

## Constraints & safety

- **只做检查与报告**：不执行任何修改配置、重启服务等操作。
- **不输出敏感内容**：报告中不得包含 API Key、token、密码等明文；只写路径或字段名。
- **报告体量**：300–600 字内，便于投递到 Telegram。

## Success criteria

- 完成检查清单（含 security audit 与 doctor）并输出结构化报告；报告含 0–10 安全评分与一句结论；若有异常则列出待办。

## Source & related docs

- **原始参考（本 skill 内）**： [assets/source-article-security-config.md](assets/source-article-security-config.md) — Bruce Van 文章 7 步安全配置建议的整理，供溯源与扩展阅读。
- **扩展**：可在自己仓库中维护 `workspace/docs/security-daily-check-step6.md`、`workspace/docs/security-audit-*.md` 等文档供团队参考。
