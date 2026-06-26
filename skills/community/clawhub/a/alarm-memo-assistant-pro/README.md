# Alarm Memo Assistant Pro

一个面向 OpenClaw / ClawHub 的“闹钟 + 备忘录 + 待办 + 每日任务推送”综合技能。

## 设计目标

这个技能不是简单回答“你可以记一下”，而是把以下需求统一成一个工作流：

- 一次性闹钟
- 重复提醒
- 普通备忘录
- 待办事项
- 带截止时间的任务
- 每日任务摘要
- 定时自动推送

## 适合的用户话术

- 帮我设个闹钟
- 提醒我明天交报告
- 记个备忘录
- 记一下今天要办的事
- 每天早上 8 点发我今日任务
- 把这段内容整理成待办
- 两小时后提醒我喝药

## 技术边界（重要）

根据 OpenClaw 官方文档，Skill 本质是一个包含 `SKILL.md` 的目录，由 OpenClaw 在新会话中加载；真正的后台定时任务应依赖 Gateway 的 cron jobs，且 Gateway 需要持续运行，否则定时任务不会自动触发。citeturn0search1turn1search4turn1search7

这意味着：

1. 这个技能**可以**利用 OpenClaw 的 cron / session / file 等宿主能力做“提醒、记录、每日推送”。citeturn1search4turn1search8turn0search4
2. 这个技能**不能保证**直接控制电脑原生“闹钟”或“备忘录”应用，除非你的 OpenClaw 环境额外提供对应插件/API。OpenClaw 官方 FAQ 也强调，缺少原生集成时通常需要自定义 skills / 插件或浏览器自动化。citeturn0search3

## 建议的数据文件

- `data/alarms.json`
- `data/todos.json`
- `data/memos.md`
- `data/daily_digest.md`

## 推荐的自动化用法

### 每日任务推送

推荐策略：

- 每天 08:00 读取 todos
- 找出今天到期、逾期未完成、高优先级事项
- 生成摘要
- 投递到主聊天会话

### 重复提醒

支持：

- 每天
- 工作日
- 每周几
- 每月某日
- 自定义 cron

## 文件说明

- `SKILL.md`：主技能说明、触发词、工作流、输出规范
- `references/triggers-and-routing.md`：触发词与意图路由
- `references/storage-schema.md`：建议的数据结构
- `references/cron-playbook.md`：每日推送、循环提醒的调度打法
- `references/output-templates.md`：统一回复模板
- `references/limitations-and-desktop-control.md`：能力边界与真实限制

## 上手测试句子

- 帮我设一个明天早上 7:30 的闹钟
- 记一下：下周二前交合同
- 两小时后提醒我拿快递
- 每天 8 点把今天要做的事情发给我
- 给我一个今天的任务总览
- 把这段聊天整理成备忘录
