# fomo.family 前端结构与数据源（2026-08-09 逆向）

## 路由与链接格式
- 前端 = Remix SPA，路由表在 `manifest-*.js`（`"id":"routes/..."` 条目，含 path + module 文件）
- 代币页路由：`routes/token` → path `tokens/:chain/:tokenAddress`（挂在 `layouts/authenticated` 下=需登录；未登录访问会跳回首页，这是正常认证行为不是 404）
- chain-slug 映射（来自 `chains-BqIg7KZZ.js` 的 te 表，id 为 viem chain id）：
  | slug | chain | id |
  |---|---|---|
  | solana | Solana | 1399811149 |
  | base | Base | 8453 |
  | monad | Monad | 143 |
  | bnb | BNB Smart Chain | 56 |
  | ethereum | Ethereum | 1 |
  | hyperliquid | Hyperliquid | 1337 |
  | robinhood | Robinhood Chain | 4663 |
- ⚠️ URL 第一段是 **chain** 不是代币名——`tokens/robinhood/0x...` = Robinhood Chain 上的代币，不是"robinhood 代币"

## API（prod-api.fomo.family）
- base：`https://prod-api.fomo.family`（前端 `fomoFetch-D5cT03NM.js` 硬编码）
- 已知端点：`/proxy/trendingTokens`、`/proxy/mostHeld`、`/proxy/graduatedTokens`、`/proxy/cryptoTokens`、`/proxy/verifiedTokens`、`/proxy/tokenDetails`、`/proxy/filterTokens`、`/tokenAllowList/detailed`
- 前端 query-key 集合：`trending` / `graduated` / `pre-graduated` / `most-held` / `crypto-tokens` / `verified`
- 访问约束：Cloudflare bot 防护 + Privy 登录态（JWT）。数据中心 IP 直连 → "Attention Required" 封锁页；未登录页面上下文 fetch → Failed to fetch。用户在自己浏览器登录后可访问（FOMO App 本身就用这些端点）

## 逆向配方（对任何 Remix SPA 可复用）
1. 首页 HTML → 收集 `/assets/*.js`（modulepreload 列表）
2. 下载 `manifest-*.js` → `grep -oE '"id":"routes/[^"]*"'` 拿路由表，再取目标路由条目的 module + imports
3. 下载关键模块：chains 配置、fetch 封装、URL 工具
4. grep API base：`"https://[a-z0-9.-]*"` 模式；grep 端点：`"/proxy/..."`、`"/[a-z]+/..."` 模式
5. CSP header 的 `connect-src` 也会泄露允许的 API 域名（*.prod-edge.fomo.family 等）

## 实测结论
- 链接 `https://fomo.family/tokens/solana/{mint}?r={邀请码}` 格式正确（trending.py 已内置）
- 服务器无法直连 API → FOMO 实时榜数据走钱包交易解析管道（trending.py），不用等官方 API
