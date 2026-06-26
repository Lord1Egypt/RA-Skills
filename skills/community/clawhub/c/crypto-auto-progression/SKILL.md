---
name: crypto-auto-progression
description: 为 crypto-hedge-backtest 启用并维护“真实执行驱动”的自动推进（cron）。当用户要求每N分钟自动推进、自动汇报阶段成果、排查 cron 持续报错、或将自动化流程固化为可复用方案时使用。
---

# Crypto Auto Progression

为 `projects/crypto-hedge-backtest` 提供可复用的自动推进流程。

## 目标
- 用 cron 驱动周期推进，而不是空提醒。
- 每次触发至少做一项真实执行：`跑脚本 / 改代码 / 产出文件`。
- 仅在有阶段成果时汇报，避免重复话术刷屏。

## 标准任务模板

### 1) 5分钟推进任务（主任务）
- schedule: `every 5m`
- sessionTarget: `main`
- payload.kind: `systemEvent`
- payload.text 必须强调“真实执行 + 阶段成果汇报 + 无成果不重复提醒”

### 2) 30分钟健康检查（守护任务）
- schedule: `every 30m`
- 检查最近30分钟是否有真实产出（新文件/新commit/新报告）
- 无产出要告警并说明阻塞点

### 3) 每日日报（可选）
- schedule: `cron 30 21 * * *` + `Asia/Manila`
- 汇总：完成项、关键结果、风险点、明日计划

## 创建与验证（强制顺序）
1. 先创建 **1个** 5分钟主任务。
2. 立即 `cron run --force` 手动触发一次。
3. 用 `cron runs` 确认 `status=ok`。
4. 再创建 30 分钟健康检查和每日日报。
5. 用 `cron list` 复核 `enabled=true` 和 `nextRunAtMs`。

## 故障排查（高频问题）
- `invalid cron.add params ... required property 'name/schedule/sessionTarget/payload'`
  - 原因：job 体缺字段或传了空 `job:{}`。
  - 处理：按完整 job 结构重发，禁止盲目重试同一坏请求。

- `openclaw-cn cron disable ... --json` 报 `unknown option '--json'`
  - 原因：`cron disable` 不支持 `--json`。
  - 处理：去掉 `--json`。

- Binance 拉数偶发 `SSL: UNEXPECTED_EOF_WHILE_READING`
  - 处理：在数据拉取层加入网络重试 + 指数退避；重试后再继续 scan 链路。

## 汇报规范（本项目）
- 有实质成果时汇报：
  - 新增/更新文件
  - 关键指标/结论
  - 下一步动作
- 状态语句使用二选一：
  - `继续推进中（无需你回复）`
  - `我已暂停推进，等待你决策`
