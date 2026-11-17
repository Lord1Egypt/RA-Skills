# 事件清单与通知机制

## 事件结构

`{id, type, priority(critical|high|normal|low), shouldNotify, status(pending→notified→read), message, createdAt, ...}`。同一去重键 30 分钟内抑制重复；只保留最近 200 条（存 `data/events.json`；200 条/30 分钟为时点观测值，以所装版本实测为准）。

## 10 类事件全表

以 FMR 源码 `core/notifications.js` 的 `EVENT_TYPES` 为准。坑：FMR 包内 `references/event-system.md` 已过时——缺 `switchModel`/`modelDisabled`/`modelRescue`/`registrationReminder` 四类，以本表为准。

| type | 默认优先级 | event-check 是否输出 | 触发点 |
|---|---|---|---|
| `announce` | normal（可由 data.priority 提级） | ✓ | 控制服务器公告（含新版本发布，公告链接走白名单校验） |
| `switchModel` | high | ✓ | 手动切换主模型 |
| `modelFailover` | high | ✓（标"[已自动处理，无需操作]"） | 运行中故障自动切换 / 池内限流提升 |
| `modelUnavailable` | **critical** | ✓（标"已自动处理"） | 某渠道所有模型均不可用 |
| `modelDisabled` | high | ✓（标"已自动处理"） | 上游 401/404/410 自动禁用模型 |
| `modelRescue` | high | ✓（标"已自动处理"） | 兜底救援临时加回模型 |
| `dailyStatus` | normal | ✗（排除，单独处理） | Router 内部 24h 定时器 + 启动 60 秒后首条 |
| `providerAdded` / `providerRemoved` | normal | ✗（仅记录） | 控制服务器渠道同步 |
| `registrationReminder` | high | ✓ | 设备未注册提醒（Skill 形态场景） |

## event-check 行为

直读 `data/events.json`（不经 Router，Router 停着也能跑）：取 pending 且应通知的事件，按 critical>high>normal>low 排序输出 Markdown（URL 经白名单校验），**并自动把输出事件标为已读**——输出即消耗。无事件时输出"暂无事件通知"。

## 触发点纪律

`event-check` 只在两个触发点执行：①用户问及通知/掉线；②排障与升级开局顺带一次。**不做定期巡检**——Skill 形态的 OpenClaw cron 任务已定时消耗事件（北京时间 10/15/20 点 event-check、9 点 dailyStatus 推送），叠加巡检等于重复告警 + 加速清空事件。standalone 形态无 cron：事件积压在 `events.json`，靠上述两个触发点查询即可。

## 通知去向

无官网公告页。公告面 = announce 事件（event-check 可见）+ 官网首页微信群二维码。版本号不从官网读（站点版本信息失真），以 `GET /api/status` 与版本目录 `package.json` 为准。
