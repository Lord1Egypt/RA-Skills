# /api/v1 企业接口策略

## 端点

- `GET /api/v1/enterprises`
  - 必填：`keyword`
  - 可选：`page`、`per_page`

## 推荐参数策略

- 单企业研究：`per_page=10`，关键词用企业主名称
- 别名补全：同一企业尝试英文名、简称、品牌名
- 赛道扫描：关键词使用细分方向并翻页扩样本

## 最小调用序列

1. `enterprises` 检索候选
2. 按企业维度清洗与去重
3. 按统一字段输出画像
4. 形成对比与建议

## 鉴权

- `X-MCP-TOKEN: <token>`
- 运行脚本前需先设置环境变量 `JQZX_API_TOKEN`
