# Work Status

Script: `scripts/work.py`

## Lifecycle of an async task

Except for a few synchronous endpoints (image `create`, digital human `say`, ad clone `analyze`), all other capabilities are asynchronous:

```
submit → get workspace_id → poll status → fetch result_url
```

`status` has four possible values: `pending` (queued), `processing` (generating), `completed` (done), `failed` (failed).

## Three commands

```bash
# Check once
python3 scripts/work.py status --workspace-id ws_abc123

# Check in batch
python3 scripts/work.py batch --workspace-ids ws_a ws_b ws_c

# Block until the result is ready
python3 scripts/work.py wait --workspace-id ws_abc123 --timeout 1200
```

## When you need it

Each capability script **automatically polls until a result is available** after submission by default, so under normal circumstances you won't need `work.py`. It's only needed in these three cases:

1. You used `--no-wait` to submit without waiting, and now want to come back and fetch the result
2. You submitted many tasks in batch and want to check all of their progress at once (`batch`)
3. Polling timed out — use the corresponding script's `query --workspace-id <id>`, or `wait` here

## A timeout does not mean failure

A polling timeout just means the client stopped waiting — **the task is still running on the server**. Do not resubmit it (this would incur duplicate charges); keep waiting on it using the `workspace_id`:

```bash
python3 scripts/work.py wait --workspace-id ws_abc123 --timeout 1800
```

Only when `status` is explicitly `failed` is it a genuine failure — only then should you consider resubmitting.

## Idempotency key

Most submission endpoints support `--idempotency-key`. When retrying after network jitter, pass the same key — the server will only create one task and won't charge twice. When submitting in batch, it's good practice to give each task a stable key.

## callback_id

`--callback-id` is **the caller's own tracking ID** — it is echoed back as-is, making it easy to match the result against your own business order number. It is not a webhook address — AdsTurbo does not push results by webhook yet; always poll with `work.py status` / `batch`.

---

# 任务状态 / Work Status

脚本：`scripts/work.py`

## 异步任务的生命周期

除少数同步接口（图片 `create`、数字人 `say`、广告复刻 `analyze`）外，其余能力都是异步的：

```
提交 → 拿到 workspace_id → 轮询状态 → 取 result_url
```

`status` 四个取值：`pending`（排队）、`processing`（生成中）、`completed`（完成）、`failed`（失败）。

## 三个命令

```bash
# 查一次
python3 scripts/work.py status --workspace-id ws_abc123

# 批量查
python3 scripts/work.py batch --workspace-ids ws_a ws_b ws_c

# 阻塞等到出结果
python3 scripts/work.py wait --workspace-id ws_abc123 --timeout 1200
```

## 什么时候需要它

各能力脚本默认**提交后自动轮询到出结果**，正常情况下用不到 `work.py`。以下三种情况才需要：

1. 用了 `--no-wait` 只提交不等待，之后回来取结果
2. 批量提交了很多任务，想一次性看全部进度（`batch`）
3. 轮询超时了——用对应脚本的 `query --workspace-id <id>`，或者这里的 `wait`

## 超时不等于失败

轮询超时只是客户端不等了，**任务还在服务端跑**。不要重新提交（会重复扣费），用 `workspace_id` 接着等：

```bash
python3 scripts/work.py wait --workspace-id ws_abc123 --timeout 1800
```

只有 `status` 明确是 `failed` 才是真失败，这时才考虑重新提交。

## 幂等键

多数提交接口支持 `--idempotency-key`。网络抖动重试时带上同一个 key，服务端只会建一个任务，不会重复扣费。批量提交时给每个任务一个稳定的 key 是好习惯。

## callback_id

`--callback-id` 是**调用方自己的追踪 ID**，会原样回传，方便把结果对回自己的业务单号。它不是 webhook 地址——目前 AdsTurbo 不支持 webhook 推送，结果一律通过 `work.py status` / `batch` 轮询获取。
