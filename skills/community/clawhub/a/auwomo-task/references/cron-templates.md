# cron-templates

定期任务模板，用于系统级 cron 部署。

> **ops 消费说明**：实际部署的 prompt 在 `auwomo-ops/desired-state/30-daily-report/prompts/` 中维护。
> 此文件作为参考文档，描述各模板的设计意图和行为。

---

## 角色感知机制

所有汇报类 prompt 都包含 **Step 0: 身份与权限检查**：

1. 读取 `$OPENCLAW_DISPLAY_NAME` 作为用户称呼
2. `auwomo identity whoami --format json` — 确认身份可用
3. `auwomo identity subordinates --format json` — 判断 has_team
4. 后续命令如返回 auth 错误 → 进入未初始化模式

这使得同一个 prompt 可以根据用户角色自动切换个人/团队视角。

## 未初始化状态处理

当检测到 `need_user_authorization` 或类似认证错误时，不输出技术性报错，改为输出友好引导消息：介绍自身能力、说明当前状态、引导用户完成配置。

---

## 昨日简报（周二至周六 08:00）

- 个人视角：基于 `task context --duration 1d -d` 概括昨日进展
- 团队视角（has_team=true）：
  - `task context --duration 1d -d --team` — 按 assignee 分组简报
  - `task missing --range 2d --team` — 缺失记录提醒
  - 停滞主线检查（>7天/14天阈值，使用同理心表述）

## 今日记录提醒（周一至周五 18:00）

- 检查可挂载任务 → 提醒用户记录今日进展
- 纯个人视角，不含团队内容
- 语气低负担、易回复

## 周汇报（周日 16:00）

- 个人周报：基于 `task context --duration 7d -d`
  - 本周完成/进行中/受阻
  - 下周建议
  - 个人停滞自检（>3天无记录的主线）
- 团队周报（has_team=true）：
  - `task context --duration 7d -d --team` — 按 assignee 分组周报
  - `task missing --range 7d --team` — 缺失记录统计
  - 停滞主线检查（7-14天/14天+阈值，使用同理心表述）

## 停滞阈值汇总

| 场景 | 阈值 | 触发条件 |
|------|------|---------|
| 个人主线自提醒 | 3天 | 自己的主线 updated_at > 3d |
| 团队主线提醒 | 7天 | 下属的主线 updated_at > 7d |
| 团队主线警告 | 14天 | 下属的主线 updated_at > 14d |
| 缺交记录提醒 | 2天 | task missing count > 0 |

## 同理心表述规则

详见 [task-report.md](task-report.md) 的"同理心表述规则"章节。所有涉及"某人没做某事"的表述必须遵循该规则。

## 部署方式

实际 prompt 文件在 `auwomo-ops` 仓库中维护：
- `desired-state/30-daily-report/prompts/yesterday-report.md`
- `desired-state/30-daily-report/prompts/end-of-day-record.md`
- `desired-state/30-daily-report/prompts/weekly-report.md`

调度配置在 `desired-state/30-daily-report/crons.yaml` 中定义。
通过 `reconcile_crons` playbook 部署到各容器。
