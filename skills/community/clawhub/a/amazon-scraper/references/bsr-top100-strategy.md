# Amazon BSR Top 100 抓取策略

## 核心限制（必读）

**`/gp/bestsellers/` URL 只能拿到 2 页 = 60 个产品。** Amazon 官方限制。`?pg=3` 会返回 "Page Not Found"。

这意味着：
- 拿 Top 30 ✅ 直接 `/gp/bestsellers/{category}`
- 拿 Top 50/60 ✅ `/gp/bestsellers/{category} --pages 2`
- **拿 Top 100 ❌ 单个 BSR URL 不行**

## 三种 Top 100 策略

### 策略 A：搜索页替代（最快、推荐）⭐

```bash
docker run --rm -v /tmp/top100:/data amazon-scraper \
  node assets/amazon_handler.js \
  "https://www.amazon.com/s?k=cable+management" \
  --pages 5 \
  --output /data/cm.json
```

- 一次调用，~3 分钟
- 5 页 = 100+ 个产品（去重后约 60-80 个独立 ASIN）
- **数据是搜索算法排序的，不是 BSR 严格排名**（混了广告位）
- 对"市场分析"够用

**适合**：快速拿数据做品类分析、价格带分析、视觉调研。

### 策略 B：多子类目 BSR 合并

BSR 父类目下钻到 5 个子类目，每个拿 Top 30 = 150 个产品：

```python
# 主类目 electronics 没有子节点
# 子类目节点 ID（在 URL 里能看到）
subcats = [
    "electronics/172541",      # Audio & Video
    "electronics/281407",      # Computers & Accessories
    "electronics/2407745011",  # Wearable Technology
    "electronics/13896617011", # Computer & Accessories
    "electronics/3024167031",  # Cell Phones
]
# 拼 URL: https://www.amazon.com/gp/bestsellers/{subcat}
```

每个子 BSR 限 2 页 = 30 个。**5 × 30 = 150，去重 ~120 个**。

**适合**：要做严格的"畅销榜"分析（不被广告位污染）。

### 策略 C：单 session 串行（最稳但最慢）

把 BSR Top 30 拿到 ASIN，逐个爬详情，3 个代理并发：

```bash
# /tmp/top100.sh
while read asin; do
  docker run --rm amazon-scraper node assets/amazon_handler.js \
    "https://www.amazon.com/dp/${asin}" \
    --output "/tmp/details/${asin}.json" 2>/dev/null
  sleep 3
done < /tmp/asins.txt
```

**耗时**：30 个 ASIN × 15-25 秒 = 7-12 分钟（单容器，1 代理）

**适合**：要拿详情做品牌/BSR/详情页分析。

## 提速方案

| 方案 | 速度 | 限制 |
|---|---|---|
| 单容器 `--pages 5` | 1x | skill 本身 |
| 多 Docker 容器并发 | Nx（N=容器数） | 需 N 个不同代理 |
| 改 handler.js 加并发 | 内部可控 | 需重新 build 镜像 |

**多容器并发的现实约束**：你的代理数 = 最大并发数。
- 3 个 DDC IP → 最多 3 个并发 → 3x 提速
- 5 个 ISP 端口 → 最多 5 个并发 → 5x 提速

skill 自带轮询：handler 内部已支持 1 个容器内多代理轮询 + 故障切换，无需额外配置。

## 速度与限流

- 单个 session：~30 秒/页（含 15 秒冷启动 + 3-5 秒 waitFor）
- Amazon 限流：30-60 请求/小时/同一 IP 是安全线，超了会触发 503
- 跑 Top 100 一次消耗约 5-10 个"请求单位"

## 输出文件路径

⚠️ **坑**：`--output` 是**容器内路径**。要保存到主机必须挂载卷：

```bash
# 错：文件在容器里
docker run --rm amazon-scraper node .../amazon_handler.js "URL" --output /tmp/x.json

# 对：挂载 /data
docker run --rm -v /tmp/results:/data amazon-scraper node .../amazon_handler.js \
  "URL" --output /data/x.json
# 文件在主机的 /tmp/results/x.json
```

代码里 `--output` 的路径会拼到 `/data/` 前缀下。
