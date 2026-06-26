# /api/v1 洞察接口策略

## 端点

- `GET /api/v1/insights`
  - 必填：`keyword`
  - 可选：`page`、`per_page`、`start_at`、`end_at`
- `GET /api/v1/insights/:id`
  - 必填：`id`

## 推荐参数策略

- 常规解读：`per_page=10`，优先最近 1-2 页
- 周期复盘：结合 `start_at`、`end_at` 固定窗口
- 深度调研：`per_page=20` 并翻页，抽取多个 `id` 做详情阅读

## 最小调用序列

1. `insights` 检索候选
2. 选择目标 `id`
3. `insights/:id` 拉取全文
4. 分层输出结论

## 鉴权

- `X-MCP-TOKEN: <token>`
- 运行脚本前需先设置环境变量 `JQZX_API_TOKEN`
