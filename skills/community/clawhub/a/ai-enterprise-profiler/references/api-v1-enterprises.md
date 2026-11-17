# /api/v1 企业接口策略

## 端点

- `POST /api/v1/enterprises`
- 请求体为业务化 JSON，不暴露底层 DSL

## 推荐参数策略

- 单企业研究：优先传 `company`
- 别名补全：同一企业尝试英文名、简称、品牌名，必要时补到 `query`
- 赛道扫描：主题词放到 `query`，再用 `regions`、`tags_any`、`investors_any` 等条件缩圈
- 对团队/融资条件敏感的问题，优先使用结构化字段，减少仅靠 `query` 的误召回

## 最小调用序列

1. 调用 `POST /api/v1/enterprises` 检索候选
2. 按企业维度清洗与去重
3. 按统一字段输出画像
4. 形成对比与建议

## 常用请求体示例

```json
{
  "query": "具身智能",
  "regions": ["上海"],
  "investors_any": ["红杉"],
  "limit": 10
}
```

```json
{
  "company": "Anthropic",
  "limit": 5
}
```

```json
{
  "query": "世界模型",
  "team_background_keywords": ["字节跳动"],
  "has_founder": true,
  "sort_by": "updated_at",
  "sort_order": "desc"
}
```

## 鉴权

- `X-MCP-TOKEN: <token>`
- 运行脚本前需先设置环境变量 `JQZX_API_TOKEN`
