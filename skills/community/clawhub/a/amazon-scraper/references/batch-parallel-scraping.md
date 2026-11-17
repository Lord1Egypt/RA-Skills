# Batch Parallel Scraping Pattern

**当前不适用。** 活代理只有 1 条（出口 IP 和端口见你本地的 `config/proxies.json`，不要写进文档）。代码把并发卡成 `min(请求值, 任务数, proxies.length)`，所以 `--concurrency 5` 仍是 1。`-e AMAZON_PROXIES` 在 `proxies.json` 非空时不生效。下面的 5 容器 × Oxylabs 8001–8005 是旧方案，现在执行会让 5 个浏览器打同一个 IP。

大批量在只有 1 条 IP 时：一个容器，`--asins`，`--output` 必须配 `-v 宿主机目录:/data`，超过约 10 分钟改后台。先用 `http://api.ipify.org` 确认出口 IP 等于你配置的代理 host，再跑亚马逊。裸 curl 拿到 500/202 不算爬虫失败，以 handler 的 JSON 为准。

旧方案（要有 5 个不同出口才能用，且必须挂载覆盖 `/app/config/proxies.json`，不能靠环境变量）：

Safe high-throughput detail page scraping using multiple Docker containers with dedicated proxy ports.

## Problem
Single container `--asins "100_asins" --concurrency 5` is slow (~20 min for 100 ASINs). But naive parallelism (5 containers × concurrency 5 = 25 total concurrent requests) causes ISP proxy soft-blocks — 76% of ASINs return all-null data.

## Safe Pattern: 5 Containers × 2-3 Concurrency

```bash
PROXY_USER="user-XXX"
PROXY_PASS="XXX"

# Split 100 ASINs into 5 batches of 20
# Each batch → its own Docker container with a dedicated proxy port

for i in 0 1 2 3 4; do
  PORT=$((8001 + i))
  BATCH="<20 ASINs comma-separated>"
  docker run --rm -v ~/scrapes:/data \
    -e AMAZON_PROXIES="http://${PROXY_USER}:${PROXY_PASS}@isp.oxylabs.io:${PORT}" \
    amazon-scraper node assets/amazon_handler.js \
    --asins "$BATCH" --concurrency 2 \
    --output "batch_${i}.json" \
    > "batch_${i}.log" 2>&1 &
done
wait
```

## Key Parameters

| Parameter | Safe Value | Risk Value | Notes |
|---|---|---|---|
| Containers | 5 | >8 | One per proxy port (8001-8005) |
| Concurrency per container | 2-3 | ≥5 | Each proxy port handles 2-3 concurrent connections |
| Total concurrent | 10-15 | ≥25 | >15 triggers Amazon soft-blocks on ISP proxies |
| ASINs per batch | 20 | >30 | Bigger batches = longer single-container runtime |

## Performance

| Mode | 100 ASINs | Success Rate |
|---|---|---|
| Single container, concurrency 5 | ~20 min | ~90% |
| 5 containers × concurrency 3 | ~5 min | ~25% (too aggressive) |
| 5 containers × concurrency 2 | ~5-7 min | ~25% (still aggressive on retry) |
| 5 containers × concurrency 2, then retry failed with concurrency 1 | ~10 min | ~50% cumulative |

## Retry Strategy for Failed ASINs

After the first pass, collect ASINs that returned all-null (proxy soft-blocked), then retry with lower concurrency:

```python
# Collect failed ASINs
for p in all_products:
    if not (p.get('title') or p.get('brand')):
        failed_asins.append(p['asin'])
```

Retry with `--concurrency 1` or `--concurrency 2` on the same 5-container pattern. Typical improvement: +10-15% success on retry.

## Merging Results

After all batches + retries complete, merge by ASIN — prefer rows with actual data (title/brand not null):

```python
detail_map = {}
for prefix in ['batch_', 'retry_']:
    for i in range(5):
        d = json.load(open(f'{prefix}{i}.json'))
        for p in d['products']:
            if p.get('title') or p.get('brand'):  # has real data
                detail_map[p['asin']] = p
```

## When This Pattern is Needed
- 100+ ASIN detail pages needed (monopoly analysis, competitive research)
- Time constraint (user wants results in <10 min, not 20+)
- Search page data already collected (just need brand/seller/bsr/bullets/details)

## When to Use Single Container Instead
- <30 ASINs (single container concurrency 3-5 is fine)
- No time pressure
- Want maximum success rate per ASIN
