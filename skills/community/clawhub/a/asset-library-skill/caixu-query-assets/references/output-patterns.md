# Output Patterns

## Filter normalization response

当先用 agent 归一化自然语言查询时，优先贴近下面的 shape：

```json
{
  "material_types": ["proof"],
  "keyword": null,
  "semantic_query": "暑期实习申请可复用的证明材料",
  "tag_filters_any": ["use:summer_internship_application", "doc:proof"],
  "tag_filters_all": [],
  "limit": 12,
  "validity_statuses": [],
  "explanation": "Mapped internship-ready proof materials to canonical filters.",
  "next_recommended_skill": ["check-lifecycle"]
}
```

- 只归一化 filter，不改写数据库命中内容
- 没有关键词时返回 `null`
- `semantic_query` 是默认精确检索的语义化查询文本；只有在用户明确要求“相似/相关材料”时才交给 `query_assets_vector`
- `tag_filters_any` / `tag_filters_all` 优先使用 `doc:` / `use:` / `entity:` / `risk:` 受控标签
- 没有下一步建议时返回空数组
