# chatgpt-ads-landing

ChatGPT Ads 纯静态落地页。一个仓库放多个客户页面，每页一个子目录；零依赖、无服务端。
每个页面打成一个 zip，上传到支持静态站点托管的平台，一页一个站点。

## 命令

```bash
pnpm dev      # 构建 + 本地预览 http://localhost:4123/ ,改文件自动重建
pnpm build    # pages/ → dist/
pnpm check    # 上线体检,有 ❌ 退出码 1(不可上线)
pnpm package my-page          # 构建 + 体检 + 打 zip → out/my-page-<时间>.zip
pnpm package my-page --force  # 体检不过也打包(仅首次部署拿访问地址用)
```

## 目录

```
shared/geo.js             访客国家 + cookie 同意状态(build 内联进 <head>,先于 Pixel)
shared/lp.js              公共运行时:CTA / 页脚链接地理分流、参数透传、Pixel 事件、cookie 横幅
pages/<slug>/
  index.html              页面正文(静态 HTML,关 JS 也完整可读)
  page.json               访问地址 url、Pixel ID、国家→站点、CTA → 目标/事件、页脚链接、consent
  assets/                 样式、图片、页面专属 JS(page.js)
scripts/build.js          构建:替换 token、注入 Pixel 与 LP_CONFIG、生成站点根的 robots/sitemap
scripts/package.js        打包上传用 zip(去掉 __MACOSX / 隐藏文件)
scripts/check.js          体检
scripts/dev.js            本地预览
```

## index.html 里可用的 token

| token | 替换为 |
|---|---|
| `{{PAGE_URL}}` | page.json 的 `url`,站点根地址(canonical、og:image 用) |
| `{{cta:<name>}}` | 该 CTA 的无 JS 兜底地址:固定国家站,或 geo CTA 的 fallback |
| `{{link:<name>}}` | page.json `links.<name>.fallback`;配 `data-link="<name>"`,JS 按国家改写(不带 UTM、不发事件) |

CTA 写法:`<a data-cta="hero" href="{{cta:hero}}">…</a>`。Pixel 安装代码、`<noscript>` Image Tag、`lp.js` 由 build 自动注入,页面里不要手写。

## 硬约束(OpenAI Ads 审核)

- **页面本身绝不跳转**。OAI-AdsBot 必须直接拿到完整 HTML;地理分流只改写 CTA 的 href。
- **正文写死在 HTML 里**,JS 只做增强(tab、分流、埋点)。
- robots.txt 放行 OAI-AdsBot(必需)和 OAI-SearchBot。托管站点**不能开加密访问**,否则 AdsBot 抓不到。
- JSON-LD 与可见文案逐字一致(check 会核对 FAQPage)。

## 地理分流

`page.json` 里 `"dest": "geo"` 的 CTA:浏览器时区(`Intl` 时区 → 国家,能区分美/加)→ 浏览器语言地区 → `routing.fallback`。
`"dest": "US"` 之类为固定国家站。所有 CTA 都追加 `routing.forwardKeys` 里的页面参数(oppref、utm_*)以及 `lp_cta`、`v`。
`routing.ipLookup: true` 时,lp.js 再查访客 IP 国家(Cloudflare `cdn-cgi/trace`,失败换 `api.country.is`,各 2 秒超时;
不带 cookie / referrer、不落本地存储)。IP 国家在 `routing.sites` 里才覆盖时区结果,否则保留时区判断;页面先按时区写好 href,
IP 结果回来再改,不阻塞加载。cookie 横幅仍按时区判断(必须在 Pixel init 前决定,等不了异步查询)。
本地模拟其他国家:Chrome DevTools → 传感器(Sensors)→ 位置选城市(会同时改时区);测 IP 分流需挂对应国家的代理/VPN。

## OpenAI Measurement Pixel

按官方文档接入:`<head>` 内官方 `oaiq` 安装代码 + `page_viewed`；CTA 点击发自定义事件
`oaiq("measure","custom",{type:"custom"},{custom_event_name})`;关 JS 时由 `<noscript>` Image Tag 兜底 `page_viewed`。
`page.json` 的 `pixelId` 为空时不安装 Pixel(check 会拦)。

- https://developers.openai.com/ads/measurement-pixel
- https://developers.openai.com/ads/image-tag
- https://help.openai.com/en/articles/20001243-advertiser-guidance-for-allowing-openai-web-crawlers

## 新增一个落地页

1. `cp -R ../starter-page pages/<slug>`,改 `page.json`(Pixel、站点、CTA;url 先留占位)。
2. 重写 `index.html` 正文与 JSON-LD,替换 `assets/` 图片(单张 < 800KB)。
3. `pnpm dev` 预览,然后按下面「发布」走。

## 发布(托管平台)

平台规则(实测 + 前端代码 `src/pages/Symphony/WebsiteDeployment/`):
- 一个站点一个子域名 `https://<子域名>.<平台域名>/`,`/` 和无扩展名路径都返回「主入口文件」;
  子目录的 `xxx/` **不会**解析到 `xxx/index.html`,所以一页一个站点,index.html 必须在 zip 根。
- 只收白名单扩展名(html/css/js/json/图片/字体/txt/xml…),其他静默跳过;解压后 ≤ 50MB。check 会校验。
- 托管在腾讯云 EdgeOne + COS,海外可访问;OAI-AdsBot UA 实测 200。

**首次上线**(访问地址要部署后才知道):
1. `pnpm package <slug> --force` → 平台「新建部署」上传 zip,主入口 `index.html`,**不加密**。
2. 把平台给的访问地址填进 `page.json` 的 `url`,补齐 Pixel ID 等占位。
3. `pnpm package <slug>`(必须全绿)→ 该站点「部署新版本」上传。之后投放用这个地址。

**后续改版**:改代码 → `pnpm package <slug>` → 「部署新版本」。平台保留 3 个历史版本,可一键回滚。

## Cookie 同意(page.json `consent`)

`consent.countries` 里的国家(目前只有 GB,英国 PECR 要求广告/统计 cookie 事先同意)才弹横幅,国家判断与地理分流相同。
按官方文档在 `oaiq("init")` 之前调用 `oaiq("consent", false)`;Pixel 不会补发被拦的事件,所以 lp.js 先暂存事件,
访客点 Accept 后 `oaiq("consent", true)` 并补发 `page_viewed` 与暂存事件,点 Decline 则丢弃。选择存在 localStorage
`lp_measurement_consent`,页脚 `[data-consent-settings]` 可重新打开横幅。关 JS 时无法判断国家,`<noscript>` Image Tag 仍会发 `page_viewed`。
