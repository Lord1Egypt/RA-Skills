# /api/v1 资讯接口策略

## 端点

- `GET /api/v1/articles`
  - 必填：`keyword`
  - 可选：`page`、`per_page`、`start_at`、`end_at`
- `GET /api/v1/articles/:id`
  - 必填：`id`

## 推荐参数策略

- 常规追踪：`per_page=10`，`page=1`
- 周期梳理：设置 `start_at`、`end_at`，并按 `page` 翻页
- 深度梳理：`per_page=20` 起步，至少覆盖 2 页后再做结论

## 最小调用序列

1. `articles` 检索候选
2. 选择高相关 `id`
3. `articles/:id` 拉取详情
4. 汇总并输出结论

## 鉴权

- `X-MCP-TOKEN: <token>`
- 运行脚本前需先设置环境变量 `JQZX_API_TOKEN`
