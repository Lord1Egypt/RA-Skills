# Cron Playbook

## 目标

在宿主支持 OpenClaw cron jobs 时，优先用 cron 实现：

- 一次性提醒
- 重复提醒
- 每日任务推送

根据 OpenClaw 官方文档，cron jobs 是 Gateway 内置调度器，任务会持久化；但若 Gateway 不持续运行，计划任务不会自动执行。citeturn1search4turn1search7

## 一次性提醒建议

- schedule kind: `at`
- payload: 提醒文案 + alarm id
- delivery: `announce` 或主聊天投递

提醒文案模板：

> 【提醒】现在该处理：{title}
> 备注：{note}

## 每日任务推送建议

- schedule kind: `cron`
- expression: `0 8 * * *`
- timezone: 用户时区
- job action:
  1. 读取 todos
  2. 筛选今日任务
  3. 生成 digest
  4. 投递到 main 会话

## 工作日提醒建议

- cron: `0 9 * * 1-5`

## 每周提醒建议

- 每周一 09:00：`0 9 * * 1`

## 每月提醒建议

- 每月 1 号 10:00：`0 10 1 * *`

## 失败回退策略

如果无法创建 cron job：

- 不要伪造“已成功自动发送”
- 应明确提示：
  - 已记录任务
  - 已生成调度草案
  - 当前宿主缺少/未启用 cron，无法后台自动执行
