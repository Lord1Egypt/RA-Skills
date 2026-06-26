# GEO 标注协议

## 1. 标注单位

最小标注单位是 **一条 query 在一个模型上的一次回答**。不允许把多个模型结果合并后统一打分。

## 2. 标注顺序

第一步先判断 query 类型；第二步判断是否提及；第三步判断情感；第四步判断能力准确度；第五步判断生态准确度；最后决定是否需要 repair 和 repair_type。

## 3. 双人复核建议

| 场景 | 要求 |
|---|---|
| 日常监控 | 一人初标，一人抽检 |
| 周报入库 | 高优先级负向和错误样本必须复核 |
| 对外复盘 | 争议样本必须有二审结论 |

## 4. 必填字段

`run_id`、`query_id`、`query_type`、`model_id`、`response_text`、`mention_score`、`sentiment_score`、`capability_score`、`ecosystem_score`、`annotator`、`review_status`。

## 5. repair_type 枚举

- `none`
- `info_error`
- `negative_eval`
- `outdated`
- `competitor_insertion`
