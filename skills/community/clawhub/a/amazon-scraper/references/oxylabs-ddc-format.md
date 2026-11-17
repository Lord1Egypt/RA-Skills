# Oxylabs DDC — 工作格式与故障排查

## 结论（2026-07-02 实测 + 官方文档）

**Oxylabs DDC 配爬虫，必须用入口域名 `ddc.oxylabs.io` + 端口，不要直接打 "Assigned IP"。**

| 形式 | 结果 |
|---|---|
| `http://user-XXX:pass@ddc.oxylabs.io:8001` | ✅ 官方推荐格式，代理层通（前提：目标站没被 Oxylabs 标 restricted） |
| `http://user-XXX:pass@45.73.183.199:8001` | ❌ 直连 IP。VPS 上 `socket.connect()` 直接 `No route to host`（45.x.x.x 段路由不通） |

每个 user 关联的 "Assigned IP" 在 Oxylabs dashboard 的 `My Products → Dedicated Datacenter Proxies → Proxy list` 里能看到。**那个 IP 是 Oxylabs 帮你分配的出口 IP，不是入口**。文档原文：

> "Please note that you will use ports for making requests with your IPs, meaning you will not directly access your IPs."

> "Entry point: The gateway to connect to your proxies — this value never changes and is always `ddc.oxylabs.io`."

## ⚠️ 关于"用 DDC 爬 Amazon"本身

**DDC（datacenter 代理）对 Amazon 大规模爬取基本不可用。** 不管用域名还是直连 IP，Amazon 都会：

- 整段 datacenter ASN 范围（AS14061 / AS204957 / AS8100 / AS6079 等）标为高风险
- 返回 "Sorry! Something went wrong!" 软拦截页面（totalProducts: 0，HTTP 200，伪装成正常）
- 偶尔能跑通 1-2 个请求（stealth 模式 + 时机），**不可重复**

`proxies.json` 配置 100% 正确 ≠ 拿到数据。**剩下的不是配置问题，是 Amazon 反爬针对 datacenter 段的问题**。

**对 Amazon 真正可用的方案**（按成本升序）：

1. **Oxylabs ISP Proxies** — 入口 `isn.oxylabs.io` 或 `pr.oxylabs.io:8001`，住宅 ISP 段 IP，Amazon 不拦。**2026-07-02 实测跑通 cable management Top 100**。
2. **Oxylabs Web Scraper API** — 不是代理，是 HTTP POST API，Oxylabs 自己爬好你拿 JSON。`https://realtime.oxylabs.io/v1/queries` + `source: "amazon_search"`。无爬虫代码，$1.50/1K 请求。
3. **其他 ISP 池** — Smartproxy / IPIDEA / Bright Data ISP 套餐。

## 故障排查命令

单独验证代理还活着（**先确认代理本身通**，再考虑目标站拦不拦）：

```bash
# 用 curl 测（注意：用 HTTP 不是 HTTPS，否则 urllib3 会误诊协议）
curl -x ddc.oxylabs.io:8001 -U "user-XXX:password" http://ip.oxylabs.io/location

# 用 python requests 测
python3 -c "
import requests
p = {'http': 'http://user-XXX:pass@ddc.oxylabs.io:8001',
     'https': 'http://user-XXX:pass@ddc.oxylabs.io:8001'}
r = requests.get('https://ip.oxylabs.io/location', proxies=p, timeout=20)
print(r.status_code, r.text[:200])
"
```

返回 200 + JSON（如 `{"ip":"205.188.202.202","country":"US",...}`）= 代理层通了。
返回 503 = Oxylabs 主动拒（看 response code 速查表）。
返回 `No route to host` = **你直接打了直连 IP**（45.x.x.x 段），改回 `ddc.oxylabs.io` 域名。

## Oxylabs Response Code 速查

| Code | 含义 | 怎么修 |
|------|------|--------|
| 400 | 请求格式错 | 检查 URL 格式 |
| 403 | **restricted target** | 目标站（如 amazon.com）在此产品黑名单。换 ISP Proxies 或 Web Scraper API |
| 404 | 域名解析不到 | 域名错或资源下架 |
| 407 | 凭证错 / 没白名单 | 检查 user/pass，或在 dashboard 加白名单出口 IP |
| 429 | 并发超限 | 降速或买更多带宽 |
| 503 | 目标 DNS 失败 | 目标站从代理侧不可达。先直连目标确认它活着 |
| 504 | 代理超时（60s） | 目标慢，重试或加超时 |

## 历史教训

**之前（2026-07-01）这个文件写的是反的**："用直连 IP，不要用域名"。那次"成功"是 1 次侥幸（stealth 模式 + Amazon 当时没识别），不是配置正确。

**2026-07-02 复测**：
- 直连 IP `45.73.183.199:8001` → `OSError: [Errno 113] No route to host`（VPS 路由层）
- 域名 `ddc.oxylabs.io:8001` → 503（按官方 response code 表 = 目标 DNS 失败，**不是格式问题**，是 Amazon 在 Oxylabs 黑名单）

下次遇到"代理挂了"先分两类：
1. 代理层通不通？→ 跑 `curl -x ddc.oxylabs.io:8001 ... http://ip.oxylabs.io/location` 验证
2. 代理通了之后目标让不让爬？→ 看返回页是 "Sorry! Something went wrong!" 还是真数据
