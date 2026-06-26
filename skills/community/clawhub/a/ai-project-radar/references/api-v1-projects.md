# /api/v1 项目接口策略

## 端点

- `GET /api/v1/projects`
  - 必填：`keyword`
  - 可选：`page`、`per_page`
- `GET /api/v1/projects/:id`
  - 必填：`id`

## 推荐参数策略

- 常规扫描：`per_page=10`，先拉取 1 页候选
- 方向盘点：`per_page=20` 并翻页，扩大覆盖范围
- 资源补全：对候选逐个请求 `projects/:id`

## 最小调用序列

1. `projects` 获取候选
2. 选取高相关 `id`
3. `projects/:id` 拉取资源详情
4. 产出可执行选型建议

## 鉴权

- `X-MCP-TOKEN: <token>`
- 运行脚本前需先设置环境变量 `JQZX_API_TOKEN`
