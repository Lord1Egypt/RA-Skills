# 定时任务模板

仅在宿主提供 cron 或定时任务工具时使用；无法安排时按对应小节处理，不阻塞主流程。

独立会话没有历史上下文，也拿不到上一轮返回里的地点和 `businessData`，所以指令里必须写完整起点/终点、出发/目的城市全称和车型信息。

占位符统一写作 `<…>`（如 `<具体地点>`、`<城市全称>`、`<车型>`、`<宿主平台名称>`、`<规划场景 businessData 原值>`、`<订单场景 businessData 原值>`），使用前替换为真实值，不要保留尖括号字面量。

## 预约打车（cron 触发实时单）

```
执行定时打车：起点「<具体地点>」，出发城市「<城市全称>」；终点「<具体地点>」，目的城市「<城市全称>」；车型「<车型>」。请完整执行高德打车流程：调用 get_taxi_service（agent_name 传「<宿主平台名称>」；origin、origin_city、destination、destination_city 按上文；departure_time 与 arrival_time 均为空）→ 观察返回的 cardScene → 按场景行动（选点/规划），需要用户选择或确认时使用 AskUserQuestion。用户确认后调用 confirm_order（agent_name 传「<宿主平台名称>」，原样传入规划场景的 businessData 和 cardScene）。订单创建成功后输出订单信息，并按「订单状态回查」直接创建任务。
```

> 占位符写法见本文开头；这里额外强调 cron 特有的坑：指令文本里的占位符**不要加 `$` 当成 shell 变量**（不是 `$TIME`、`$CHAT_ID`）。

> 模板里的 `AskUserQuestion` 在宿主不提供时，按 `../SKILL.md`「用户交互方式」降级为普通文本提问。

## 订单状态回查（下单后 30 秒）

下单成功后直接创建一次定时查询，30 秒后执行一次，不重复。无法安排该任务时，将当前工具结果输出后，在当前会话等待 30 秒再查询一次。指令必须自包含，写入订单场景的 `businessData` 原值。

```
查询高德打车订单状态：调用 query_orders，agent_name 传「<宿主平台名称>」，scene 传「详情」，businessData 传「<订单场景 businessData 原值>」。按返回结果告知用户订单当前状态。
```
