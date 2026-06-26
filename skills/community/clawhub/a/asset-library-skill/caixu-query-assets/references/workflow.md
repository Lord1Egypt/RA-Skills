# Workflow

## Trigger examples

- “我有哪些可用材料”
- “查一下证书类材料”
- “看看哪些可用于实习申请”

## Filter normalization

### material_types

- `证明类` -> `proof`
- `经历类` -> `experience`
- `权益类` -> `rights`
- `财务类` -> `finance`
- `协议类` -> `agreement`

### validity_statuses

- `有效` -> `valid`
- `快过期` -> `expiring`
- `已过期` -> `expired`
- `长期有效` -> `long_term`
- `未知` -> `unknown`

### semantic_query / tag filters

- `实习申请` -> `semantic_query = "暑期实习申请可复用的材料"`
- `可用于实习申请` -> `tag_filters_any += ["use:summer_internship_application"]`
- `语言证书` -> `tag_filters_any += ["entity:language_certificate"]`
- `成绩单` -> `tag_filters_any += ["doc:transcript", "entity:transcript"]`

## Default behavior

- 完全无过滤条件时，做安全的有界查询，不要直接 dump 全库。
- 用户明确要求自然语言检索，且库疑似来自旧版本时，先触发一次 `reindex_library_search`。
- 默认查询走 `tag_filters + FTS + 结构过滤`。
- 用户明确要求“找相似材料”“找相关材料”“语义扩展召回”时，才额外调用 `query_assets_vector`。
- 向量不可用时，不应让默认查询失败；只需说明可选语义召回当前不可用。
