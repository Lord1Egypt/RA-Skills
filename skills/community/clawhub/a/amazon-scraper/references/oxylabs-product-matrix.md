# Oxylabs 代理产品矩阵 — 哪个产品对应哪个入口域名

## 速查表

| Oxylabs 产品 | 入口域名 | Amazon 可用? | 适用场景 | 备注 |
|---|---|---|---|---|
| **Datacenter Proxies** (DC) | `dc.oxylabs.io` | ❌ | 大流量、低成本、对反爬不严 | 与 DDC 不同产品 |
| **Dedicated Datacenter Proxies** (DDC) | `ddc.oxylabs.io` | ❌ | 个人独享 IP、对反爬不严 | 文档说"你不会直接访问 IP" |
| **ISP Proxies** ⭐ | `isn.oxylabs.io` 或 `pr.oxylabs.io` | ✅ **推荐** | Amazon 爬取、电商 | 住宅 ISP 段，Amazon 不拦 |
| **Dedicated ISP Proxies** | `pr.oxylabs.io` | ✅ | 长期项目、高频爬 Amazon | 比 ISP 更稳定更贵 |
| **Residential Proxies** | `pr.oxylabs.io` | ✅ | 任何目标站、轮换 IP | 按 GB 流量计费 |
| **Mobile Proxies** | `mob.oxylabs.io` | ✅ | 反爬最严目标 | 4G/5G 移动 IP，最难被识别 |
| **Web Scraper API** (非代理) | `https://realtime.oxylabs.io/v1/queries` | ✅ | 不写爬虫代码，HTTP POST 拿 JSON | $1.50/1K 请求起 |

## `proxies.json` 模板

### ISP Proxies（Amazon 推荐）
```json
{
  "proxies": [
    "http://user-XXX:pass@isn.oxylabs.io:8001",
    "http://user-XXX:pass@isn.oxylabs.io:8002",
    "http://user-XXX:pass@isn.oxylabs.io:8003"
  ]
}
```

### DDC（用 `ddc.oxylabs.io` 域名）
```json
{
  "proxies": [
    "http://user-XXX:pass@ddc.oxylabs.io:8001",
    "http://user-XXX:pass@ddc.oxylabs.io:8002",
    "http://user-XXX:pass@ddc.oxylabs.io:8003"
  ]
}
```

⚠️ **不要把 dashboard 上的 "Assigned IP" 当入口用**（如 `45.73.183.199:8001`）。VPS 上直连会 `No route to host`。

### Web Scraper API（不走代理）
不是 `proxies.json` 配的，是**直接发 HTTP POST**：
```bash
curl 'https://realtime.oxylabs.io/v1/queries' \
  -u "API_USER:API_PASS" \
  -H "Content-Type: application/json" \
  -d '{"source":"amazon_search","query":"cable management","parse":true}'
```
返回完整 JSON（含 title/price/asin/bsr/...），无爬虫代码。

## 判断"该买哪个"的决策

| 你的情况 | 买什么 |
|---|---|
| 一次爬 100-1000 个 Amazon 产品 | ISP Proxies 最低套餐 |
| 每天/每周跑 Amazon 监控 | Dedicated ISP Proxies |
| 完全不写代码，只想要数据 | Web Scraper API |
| 爬非 Amazon 站（普通电商/新闻） | Residential Proxies |
| 预算紧 + 目标站反爬弱 | Datacenter Proxies |
| 反爬最严（机票/Sneaker/抢购） | Mobile Proxies |

## 切换代理的最小动作

1. 改 `~/.openclaw/skills/amazon-scraper/config/proxies.json`（按上面模板）
2. 直接 `docker run` 即可（**不需要重新 build 镜像** — `proxies.json` 是运行时读取）

⚠️ 反例：改 `assets/amazon_handler.js` 后才需要 `docker build -t amazon-scraper .` 重新 build。

## 凭证安全

`proxies.json` 里的 user/pass 是**明文凭证**。打包 skill 发给别人前先参考 `sharing-checklist.md`（先问真实/占位/空数组 三选一）。
