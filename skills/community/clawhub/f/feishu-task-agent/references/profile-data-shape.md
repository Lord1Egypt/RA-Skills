# `daily.json` 数据结构

`scripts/build_daily_json.py` 始终往 `<应用根目录>/daily.json` 写入单个 JSON 文件。

## 正常状态

```json
{
  "来源日期": "2026-04-14",
  "来源相对路径": "memory/journal/daily/2026-04-14.md",
  "来源指纹": "sha256:...",
  "生成时间": "2026-04-14T23:30:12+08:00",
  "最后检查时间": "2026-04-14T23:30:12+08:00",
  "Todo_Agent_RecentHighlights_Field": [
    "重要的近期进展或结论"
  ],
  "Todo_Agent_TomorrowsFocus_Field": [
    "未闭环的后续动作或跟进项"
  ]
}
```

## 字段说明

- `来源日期`：被选中的日报文件名里的日期部分；来源文件按 `YYYY-MM-DD.md` 日期格式命名，例如 `2026-04-09.md`；没有来源时为 `null`
- `来源相对路径`：来源文件相对应用根目录的路径；没有来源时为 `null`
- `来源指纹`：来源 Markdown 内容的哈希；没有来源时为 `null`
- `生成时间`：最近一次完整重建结果的时间
- `最后检查时间`：最近一次检查工作区的时间
- `近期要点`：近期的重要进展、结论、变化或风险数组，对应的 json key 为 "Todo_Agent_RecentHighlights_Field"
- `明日关注`：未闭环的下一步动作、跟进、确认或修复数组，对应的 json key 为 "Todo_Agent_TomorrowsFocus_Field"


## 初始化占位状态

如果还没有任何匹配的日报，但又需要初始化 `daily.json`，脚本会写入：

```json
{
  "来源日期": null,
  "来源相对路径": null,
  "来源指纹": null,
  "生成时间": "2026-04-14T23:30:12+08:00",
  "最后检查时间": "2026-04-14T23:30:12+08:00",
  "Todo_Agent_RecentHighlights_Field": [],
  "Todo_Agent_TomorrowsFocus_Field": []
}
```

## 备注

- `近期要点` 和 `明日关注` 始终存在，并始终保持为数组。
- 优先写空数组，而不是编造占位文案。
- 当来源指纹没有变化时，脚本只更新 `最后检查时间`。
