# 飞书多维表格建表字段

与 `build-bitable-records.mjs` 输出列名一致。创建数据表时建议使用 `feishu_bitable_app_table.create` 一次性传入 `fields`（见 `bitable-field-defs.json`）。

| 列名 | 类型码 | 说明 |
| --- | --- | --- |
| 模型ID | 1 文本 | 主键，用于更新匹配 |
| 模型名称 | 1 | |
| Slug | 1 | |
| 厂商 | 1 | model_creator.name |
| 智能指数 | 2 数字 | artificial_analysis_intelligence_index |
| 编程指数 | 2 | coding_index |
| 数学指数 | 2 | math_index |
| MMLU Pro(%) | 1 | 已转为百分数字符串 |
| 综合价格($/1M) | 2 | price_1m_blended_3_to_1 |
| 更新时间 | 1 | ISO 时间 |

完整字段列表运行 `build-bitable-records.mjs` 后查看 `bitable-field-defs.json`。
