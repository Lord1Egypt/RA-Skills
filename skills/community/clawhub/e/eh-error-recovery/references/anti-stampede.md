# Pattern 5.7: Anti-Stampede Retry Asymmetry

## Problem

API 返回 529（overloaded）时，如果所有请求都重试，会放大过载——本来就忙不过来，重试让请求量翻倍。

## Claude Code 的做法

前台查询（用户直接发起的对话）遇 529 会重试（最多 3 次，honors retry-after header）。后台查询（session summary、YOLO classifier、background compaction）遇 529 **立即放弃**，不重试。

这是刻意的不对称：后台任务丢失可以容忍（summary 下次再生成），但后台重试会在系统最脆弱的时候增加负载。

## 对 Hook 设计的启示

Async hook（`"async": true`）在本质上是后台任务。应用同样的 anti-stampede 原则：

1. **Async hook 失败不重试** — hook 脚本 exit 1 就算了，不要在脚本内部加 retry loop
2. **Async hook 超时要短** — 系统过载时 async hook 排队会加剧延迟。设 5-10 秒超时，超时就放弃
3. **Sync hook 可以重试但要谨慎** — sync hook 阻塞 agent 主循环，重试成本更高。最多重试 1 次

```bash
# async hook 的模板：快速失败，不重试
INPUT=$(cat)
# ... 处理逻辑 ...
RESULT=$(curl -s --max-time 5 "$URL" 2>/dev/null) || exit 0  # 超时或失败就静默退出
```

## 与 Pattern 5.1 Rate Limit Recovery 的区别

| | 5.1 Rate Limit Recovery | 5.7 Anti-Stampede |
|---|---|---|
| 场景 | 429 限速（单用户被限） | 529 过载（服务端全局过载） |
| 策略 | 等待后重试（honors retry-after） | 后台不重试，前台有限重试 |
| 原因 | 429 是暂时的，等一下就好 | 529 时重试会雪上加霜 |

## Source

Claude Code 源码 `withRetry.ts`（823 行），`FOREGROUND_529_RETRY_SOURCES` 白名单。
