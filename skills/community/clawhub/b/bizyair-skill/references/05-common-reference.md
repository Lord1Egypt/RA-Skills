# 05 公共约定

## 环境变量

```bash
export API_BASE="https://api.bizyair.cn"
export X_BASE="${API_BASE}/x/v1"
export Y_BASE="${API_BASE}/y/v1"
export W_BASE="${API_BASE}/w/v1"
export TOKEN="<api-key>"
```

鉴权头：`Authorization: Bearer ${TOKEN}` + `lang: zh`

## 分页

- `current`：页码，从 1 开始
- `page_size`：每页数量（建议 10/20/50）
- 返回：`{list, total, current, page_size}`（注意是 `list` 不是 `records`）

## 响应判断

```
HTTP 200 + code=20000 → 请求成功（但任务可能 Failed，看 data.status）
HTTP 202             → 异步模式 webapp create 成功（裸 body {request_id}）
HTTP 400 + code=20015 → 参数无效
HTTP 400 + code=40025 → webapp 缺 input_values
HTTP 500 + 空 body    → 参数类型错误（服务端未给 message）
```

## 常用枚举

- `model_types`：Model / Workflow / Application
- `sort`（bizy_models）：Recently / Most Forked / Most Used / Most Liked / Most Downloaded / Auto（**必填**）
- `sort`（modelzoo/list）：Auto / Recently / Most Used 等（**可选**）
- `sort`（creations）：Recently / Recommend / Hotest
- `call_type`：comfy_task / trd_api_record

## 错误码（可重试 vs 不可重试）

### 可重试（换 Key 或稍后重试可能恢复）

| 码 | 含义 | 建议 |
|---|---|---|
| 20049/20050/20051 | 余额不足 | 换有余额的 key |
| 30039 | 达到最大排队数量 | 稍后重试 |
| 30040 | 达到最大并行度 | 等当前任务完成 |
| 30015/30016/30018 | 无可用节点 | 该模型暂时不可用 |
| 50600-50604 | 限流 | 请求太频繁，稍后重试 |
| HTTP 429 | 网关限流 | 同上 |
| HTTP 402 | 付费问题 | 同余额不足 |

### 不可重试（客户端问题）

| 码 | 含义 |
|---|---|
| 20015 | 参数无效 |
| 20251 | 第三方 API 节点未找到 |
| 40025 | 缺少 input_values |

## 何时需要鉴权

通常可匿名：社区公开资源检索、公开详情、modelzoo 公共列表/详情/价格

通常需要鉴权：我的资源、用户资料、钱包、API Key、AI 应用任务、modelzoo 任务、调用记录

## 输出 URL 注意事项

- 大部分落 BizyAir 自家 OSS（`bizyair-prod.oss-cn-shanghai.aliyuncs.com` / `storage.bizyair.cn`）
- 部分渠道版落第三方临时存储（`tempfile.aiquickdraw.com` / `s3.6scloud.com`）
- AI 应用任务有 `expired_at`（~15 天后过期）
- **必须及时下载落地，不依赖原 URL 永久可访问**

## API Key 展示

响应里 key 都是脱敏的：`sk-wmul****...phzh`。skill 展示自己 key 时保持同样格式。

## cancel / interrupt

webapp 和 modelzoo 都没有公开的 cancel 端点（404）。用户问怎么取消时告知"BizyAir 公开 API 不支持取消"。
