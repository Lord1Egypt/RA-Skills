# CDP Fallback 爬取策略

## 问题场景

批量爬取 Amazon 详情页时（`--asins` 模式），Docker 代理方案在以下情况会被 Amazon 软拦截：
- 总并发 ≥ 15（5 容器 × concurrency 3）
- 单代理端口并发 ≥ 3
- 短时间内同 IP 大量请求

软拦截表现：`status: SUCCESS` 但 `title/brand/seller/bsr` 全部 null，页面未渲染。

## 解决方案：Chrome CDP 直连

**核心思路**：绕过 Docker 代理，用 VPS 本地 Chrome 浏览器（CDP 协议）逐个串行爬取，配合 2-4 秒随机延迟。

**实测结果（2026-07-04）**：
- Docker 代理方案：75 个失败 ASIN，成功率 0%（全部被拦）
- CDP 直连方案：75 个失败 ASIN，**成功率 100%**（0 失败）
- 耗时：75 个 ASIN × ~5 秒/个 = 约 6 分钟

## 前置条件

1. Chrome 已启动并监听 CDP：

```bash
export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x24 &>/dev/null &
/opt/google/chrome/chrome --disable-gpu --no-first-run \
  --no-default-browser-check \
  --remote-debugging-port=9222 \
  --remote-debugging-address=127.0.0.1 \
  --user-data-dir="$HOME/.cache/amazon-scraper-chrome" \
  "https://www.amazon.com"
```

> ### ⚠️ 不要加 `--remote-allow-origins=*`
>
> CDP **没有任何认证机制**：谁能连上 9222，谁就完全控制这个浏览器 —— 读 cookie、以登录用户身份下单、改收货地址、导出 session。本方案的前提恰恰是这个 Chrome 带着真实 Amazon 登录态，所以它的调试口就等于账号凭证。
>
> - `--remote-allow-origins=*` 关掉了 WebSocket 的 Origin 校验，于是**你在这个浏览器里打开的任意网页**都能连上 9222 接管它。只在确实遇到 Origin 报错时，针对具体来源写白名单，不要用 `*`。
> - 必须显式 `--remote-debugging-address=127.0.0.1`。绑到 `0.0.0.0` 的 VPS 等于开了一个公网无密码浏览器后门；即使绑回环，也要确认没有端口转发或 docker 规则把它暴露出去（`ss -lntp | grep 9222` 自查）。
> - 不要用 `--no-sandbox`。VPS 上常以 root 跑 Chrome，关掉沙箱意味着一个渲染器漏洞就能拿到 root。需要在容器里跑就改用非 root 用户 + `--user-ns` 之类的方案。
> - profile 不要放 `/tmp`（全局可写，其他本地用户可读你的 cookie）。放 `$HOME/.cache/...` 并保持 `chmod 700`。
> - 用完把这个 Chrome 关掉，别长期挂着一个带登录态的调试口。

本目录的两个 CDP 脚本都会**自己新开一个标签页**并在结束时关掉，不会劫持你正在用的标签页。

2. Python 依赖：
```bash
pip install websocket-client
```

## 使用方法

```bash
# 方式1：直接传 ASIN 列表
python3 ~/.openclaw/skills/amazon-scraper/scripts/cdp_fallback_scrape.py \
  --asins "B07XXX,B08YYY,B09ZZZ" \
  --output cdp_results.json

# 方式2：从 JSON 文件读 ASIN 列表
python3 ~/.openclaw/skills/amazon-scraper/scripts/cdp_fallback_scrape.py \
  --asin-file failed_asins.json \
  --output cdp_results.json
```

## 完整工作流：Docker 批量 + CDP 补漏

```bash
# Step 1: Docker 批量爬取（快但有失败）
# 每个容器一个独立出口端口。没有 N 个不同出口就不要开 N 个容器。
# 凭证从环境变量取，不要写进命令行（会进 shell history 和 ps 输出）。
read -rsp 'proxy user: ' PROXY_USER; echo
read -rsp 'proxy pass: ' PROXY_PASS; echo

for i in 0 1 2 3 4; do
  PORT=$((8001 + i))
  AMAZON_PROXIES="http://${PROXY_USER}:${PROXY_PASS}@isp.oxylabs.io:${PORT}" \
  docker run --rm -v ~/scrapes:/data \
    -e AMAZON_PROXIES \
    amazon-scraper node assets/amazon_handler.js \
    --asins "$BATCH_$i" --concurrency 2 \
    --output "batch_${i}.json" &
done
wait

# Step 2: 找出失败的 ASIN（title/brand 全 null）
python3 -c "
import json
failed = []
for i in range(5):
    d = json.load(open(f'batch_{i}.json'))
    for p in d.get('products', []):
        if not (p.get('title') or p.get('brand')):
            failed.append(p['asin'])
json.dump(failed, open('failed_asins.json', 'w'))
print(f'{len(failed)} failed ASINs')
"

# Step 3: CDP 补漏（串行，100% 成功率）
python3 ~/.openclaw/skills/amazon-scraper/scripts/cdp_fallback_scrape.py \
  --asin-file failed_asins.json \
  --output cdp_results.json

# Step 4: 合并所有结果
python3 -c "
import json
all_details = {}
for i in range(5):
    d = json.load(open(f'batch_{i}.json'))
    for p in d.get('products', []):
        if p.get('title') or p.get('brand'):
            all_details[p['asin']] = p
for p in json.load(open('cdp_results.json')):
    if p.get('title') or p.get('brand'):
        all_details[p['asin']] = p
json.dump(list(all_details.values()), open('merged_details.json', 'w'), ensure_ascii=False, indent=2)
print(f'Merged: {len(all_details)} ASINs with full data')
"
```

## 为什么 CDP 方案不会被拦截

1. **真实浏览器指纹**：Chrome 150 的真实 User-Agent、Canvas、WebGL 指纹，比 playwright-extra stealth 更难检测
2. **VPS 本地 IP**：不走代理，用 VPS 的数据中心 IP 直连。虽然 Amazon 对 datacenter IP 有风控，但**单 IP 低频串行请求（每 3-5 秒一个）不会触发**
3. **已登录态**：Chrome profile 可能有 Amazon 登录 cookie（如果之前登录过），进一步降低风控。

   ⚠️ 这条是双刃剑，而且代价不对称：带登录态抓取会把抓取行为直接绑到一个真实账号上。被判定为自动化访问时，封的是这个买家账号（连带历史订单、Prime、礼品卡余额），如果它和卖家账号有关联信息，还可能牵连卖家账号。详情页（`/dp/`）匿名可见，**不需要登录态就能抓，就不要用登录态抓**。只有评论页这种必须登录的场景才值得权衡，并且应该用一个专用的、与主业务无关的账号。
4. **CDP 协议**：通过 Chrome DevTools Protocol 控制真实浏览器，不是 headless 模式

## 注意事项

- **串行慢但稳**：每个 ASIN 约 5 秒（3 秒页面加载 + 2-4 秒随机延迟），100 个 ASIN 约 8-10 分钟
- **不要并发**：CDP 方案的核心优势就是串行低频，并发会破坏这个优势
- **Chrome 需保持运行**：脚本运行期间不要关闭 Chrome 或断开 Xvfb
- **进度保存**：每 10 个 ASIN 自动保存一次结果到 output 文件
- **适用范围**：仅适用于详情页（`/dp/ASIN`），搜索页/BSR 页仍用 Docker 方案
