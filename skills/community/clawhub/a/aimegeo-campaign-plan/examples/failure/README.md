# 失败样例：时间漂移、拍摄冲突和缺事实就绪

输入 [campaign.json](campaign.json) 是专门构造的错误数据，不是用户活动案例：

1. F03 的用户时间原话仍为“下周”，事件时间却改成“这周末”。
2. 同一窗口 S01 占用 B 的 0–5 分钟，S02 占用 B 的 3–8 分钟，两人拍摄也不能让同一个 B 同时做两项任务。
3. 01 稿依赖尚缺的 F07 展位信息，却被标为 `ready_for_review`。

```sh
python3 scripts/check_campaign.py examples/failure/campaign.json
```

预期退出码 **1**，返回 `TIME_RAW_CHANGED`、`SHOOT_CONFLICT`、`DRAFT_FACT_GATE`。完整输出见 [expected-report.json](expected-report.json)。修复方式是恢复时间原话、把 S02 移到 5 分钟之后、补充有来源的展位事实或将稿件标为 `awaiting_facts`。不能为了通过校验直接把未知值填成已确认。
