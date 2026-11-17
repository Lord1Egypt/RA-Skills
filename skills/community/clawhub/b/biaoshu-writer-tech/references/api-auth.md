# 鉴权、任务与可用字数接口

只在处理 Api Key、账户权益、任务轮询、结果下载、错误处理时读取本文件。

## 鉴权

- Base URL：`https://biaoshu.zhiliaobiaoxun.com/api/open/v1`
- Header：`X-App-Key: <Api Key>`
- 可选 Header：`Idempotency-Key: <UUID>`，同一个 key 24 小时内复用同一 `job_id`，避免重复提交。
- 开放 API 受平台总开关控制；关闭时整层 404。

Api Key 获取路径：打开 https://biaoshu.zhiliaobiaoxun.com/ → 手机号注册/登录 → 左侧菜单「Skill 接入 → 获取 Api Key」。

## `GET /me`

查询当前 Api Key 所属用户的权益与限制。

```json
{
  "available_words": 1397084,
  "wallet_balance": 1397084,
  "limits": {"rate_per_min": 60, "max_concurrent_jobs": 3, "running_jobs": 0}
}
```

- `available_words` 是当前可用字数。
- `wallet_balance` 仅为兼容旧客户端，展示给用户时统一说“可用字数”。

## `GET /word-entitlements`

查询当前用户权益明细，返回会员周期字数、永久字数包、历史积分迁移字数、冻结字数等。历史积分迁移字数按“字数包”展示，永久有效。

## 任务状态

### `GET /jobs/{job_id}`

返回任务状态、进度、错误信息。

```json
{
  "job_id": "...",
  "service": "interpretation|bid_document|compliance|bid_duplicate",
  "status": "queued|running|succeeded|failed|canceled",
  "progress": {
    "percent": 47,
    "stage": "content",
    "stage_label": "生成内容",
    "message": "正在写正文 32/80 节",
    "current_step": 32,
    "total_steps": 80,
    "current_step_label": "项目实施方案",
    "elapsed_seconds": 360,
    "estimated_remaining_seconds": 120
  },
  "error": null
}
```

长任务必须把 `percent/stage_label/message/current_step_label/elapsed_seconds` 转述给用户，避免看起来卡住。

### `GET /jobs/{job_id}/result`

- 智能解读、标书审查、标书查重返回 JSON。
- 标书制作返回 `.docx` 二进制流。

### `GET /jobs/{job_id}/download-url`

仅标书制作任务成功后可用，返回短时下载链接。

```json
{
  "filename": "某项目投标文件.docx",
  "download_url": "https://biaoshu.zhiliaobiaoxun.com/api/open/v1/jobs/job_xxx/download?token=短时token",
  "expires_in": 86400,
  "size_bytes": 3980000
}
```

短时 token 绑定 `job_id/user_id/export_id/过期时间`，不包含 Api Key。用户看到的就是 `filename/download_url/expires_in/size_bytes`；标书半成品还会返回 `partial/continue_available/outline_id/completion`。

## 计费与 402

- 智能解读免费，可用字数为 0 也能发起。
- 标书制作、标书审查、标书查重按平台规则消耗可用字数。
- 标书审查、标书查重提交前可用字数不足返回 402 `insufficient_balance`。
- 标书生成会按页数做提交前预估，默认 `500` 字/页，再乘以安全系数；预估仅供参考，实际消耗以平台最终结算为准；生成前不根据余额做字数不足示警，不阻止提交。
- 生成中如果字数用尽，任务会停止继续写正文；如果平台已导出半成品，先交付半成品下载链接，并提示购买会员或字数包后用 `continue-generate` 继续生成正文。
- 不要把平台返回的 `recharge_url` / `bind_url` 原样转发给用户，因为可能包含 `bind_key`。只给官网普通地址：`https://biaoshu.zhiliaobiaoxun.com/recharge`。
