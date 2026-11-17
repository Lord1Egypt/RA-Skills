---
name: schedule
description: "当用户需要操作 Doxent / 读写笔记里的真实日程、提醒、待办或任务，包括查看、创建、修改、删除、完成、移动，或用自然语言表达时间安排，如明天开会、今晚提醒、周五前完成时使用。"
---

# doxent schedule

## 概览

这个模块负责 Doxent / 读写笔记里的真实日程与任务操作。
只要用户是在表达安排时间、创建事件、添加提醒、记录待办、完成任务、调整时间、移动任务、删除日程，不管是否明确说出“日程 / event / task / 提醒 / 任务”这些词，都按本模块处理。像“明天早上9点开晨会”“下周一下午三点和张三一对一”“提醒我今晚交周报”“给我加个周五前完成的待办”“把下午会议改到4点”“完成那个报销任务”这类自然语言都应直接命中本模块。

## 触发优先级

- 用户只要在 Doxent / 读写笔记 / 办公本 语境里表达“什么时候做什么”，优先判定为本模块
- 对“开会、约时间、提醒、待办、任务、行程、日程、安排、改期、延期、提前、完成、删除”这类动作要放宽匹配
- 即使没有出现 `日程`、`event`、`task`、`提醒` 关键词，只要语义是在创建或修改真实时间安排，也直接进入本模块
- 如果一句话同时包含时间信息和动作对象，默认优先理解成创建或更新事件/任务，而不是普通聊天或文本润色

## 开始前

- 先读 `references/open-model-schedule-api.md`
- 遵循 `../shared/port-and-health.md`
- 遵循 `../shared/write-and-sync.md`
- **【强制】所有 API 调用必须通过 `../shared/scripts/doxent_api.py` 发送，用法见主 SKILL.md "网络请求规则"**

## 核心流程

1. 通过 `doxent_api.py` 发起请求；脚本会自动检查服务、唤醒 CLI 并处理端口回退
2. 先做查询再做写操作
3. 读操作优先用 `/open-model-schedule/overview`
4. 单条详情用 `/open-model-schedule/item`
5. 写操作统一走 `/open-model-schedule/create`、`/open-model-schedule/update`、`/open-model-schedule/delete`、`/open-model-schedule/operate`
6. 删除、完成、移动前先确认对象

## 接口范围

- `/open-model-schedule/health`
- `/open-model-schedule/overview`
- `/open-model-schedule/item`
- `/open-model-schedule/create`
- `/open-model-schedule/update`
- `/open-model-schedule/delete`
- `/open-model-schedule/operate`
- `/open-model/sync`

## 时间戳规则

**在计算任何事件的 startTime / endTime / remindTime 之前，必须先执行以下命令获取当前时间戳，不得凭内部知识估算年份：**

```powershell
# 获取当前时间戳（毫秒）
$nowMs = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
Write-Host "当前时间戳(ms): $nowMs"

# 同时输出当地时间供核验
Write-Host "当前本地时间: $([DateTimeOffset]::Now.ToString('yyyy-MM-dd HH:mm:ss zzz'))"
```

- 以 `$nowMs` 为基准，用毫秒偏移量计算目标时间（1天 = 86400000ms，1小时 = 3600000ms）
- 计算完成后，将结果转回可读时间字符串核验，确认年份正确后再写入请求体
- **严禁**直接凭记忆或推算写死年份

## 工作规则

- 不要承诺 `events/*`、`tasks/*`、`task-lists/*` 旧接口
- 当前真实接口不提供任务清单 CRUD
- 事件提醒优先按 `remindTime` 理解和写入，尽量推测一下提醒时间，默认应该为日程开始前30分钟
- 创建或更新任务时，用户说“截止到 / 截止时间 / deadline / 周五前 / 今晚前”等，都必须把解析出的截止时间写入 `expireTime`；有具体时分的截止时间会按非全天任务显示，并默认提前 5 分钟提醒。
- 任务提醒时间用 `advanceTime` 表达提前毫秒数；传入非 `-1` 的 `advanceTime` 会打开提醒，关闭提醒时才传 `advanceTime: -1`，不要额外用 `hasScheduleTime` 兜底。
- `operate` 只用于任务项


## 响应风格

- `结果`
- `命中项`
- `补充说明`
- `下一步`
