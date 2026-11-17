# 抖音评论接口 / 签名 参考（踩坑点）

本技能提供两条路径：纯 Python 签名（零浏览器、零 node）与无头浏览器游客态（免登录）。
纯 HTTP 路径依赖三块纯 Python 代码：`scripts/sign`（a_bogus 签名 + SM3 + 指纹）、
`scripts/mstoken.py`（mssdk 真 msToken 换发）、`scripts/fetch_comments.py`（采集 CLI）。
无头浏览器路径见 `scripts/browser_fetch.py`（依赖 playwright，可选安装）。

## 1. 两个评论端点

| 端点 | aid | 说明 |
|------|-----|------|
| 创作者中心 `creator.douyin.com/web/api/third_party/aweme/api/comment/read/aweme/v1/web/comment/list/select/` | **2906** | **默认、已验证可用**。账号域隔离：必须用**该视频本人账号**的 cookie。 |
| 公开 `www.douyin.com/aweme/v1/web/comment/list/` | **6383** | 实验性。自 ~2026-08-20 起对非真实浏览器静默空体，多半返回空，仅供试探。 |

**关键结论**：`a_bogus` 签名器内嵌的 `aid` 必须与端点一致，否则网关判 `status_code:5 参数不合法`。
- creator 端点 → `ABogusPureSigner(aid=2906)`
- public 端点 → `ABogusPureSigner(aid=6383)`

## 2. a_bogus 是「对有序 query 串」算的签名

`a_bogus` 本质是对「不含 a_bogus 的有序 query 串」做 SM3 派生的签名。因此：

1. **参数插入顺序 = 签名的一部分**：构造 params 字典必须逐位稳定，且与签名串完全一致。
   本技能固定顺序见 `fetch_comments.py::fetch_raw`：
   `device_platform → aid → app_id → channel_id → aweme_id → cursor → count → sort_options
   → screen_width/height → browser_* → engine_* → os_* → cpu_core_num → device_memory
   → platform → downlink → effective_type → round_trip_time → webid/verifyFp/fp → msToken`
2. **签名时机**：先放 `webid/verifyFp/fp/msToken`，再对「不含 a_bogus 的 query」算 `a_bogus`，最后把 `a_bogus` 追加进 params。
3. **指纹同源**：params 里的 `screen_width/height/browser_*` 必须取自与签名器**同一个 `get_profile()`**，否则参数值与签名内嵌指纹不一致 → 校验失败。
4. **避免二次编码**：用 `_splice_url()` 自己拼 query（`urllib.parse.quote` 每个 value），把含 `a_bogus` 的完整 URL 直接交给 httpx，**不要**传 `params=dict` 让 httpx 重新编码（可能破坏与签名串的一致性）。
5. `s_v_web_id` 取自 cookie，填入 params 的 `verifyFp` / `fp`（`auth.cookie['s_v_web_id']`）。

## 3. msToken：向官方「要」，不碰运气

- 用 mssdk 端点 `https://mssdk.bytedance.com/web/common?ms_appid=6383` POST 一段 RC4 加密指纹，
  响应头 `x-ms-token` 下发**真** token（开源同构实现见 `mstoken.py`）。
- 600s 进程内缓存，避免高频触发风控。换发失败返回空串，调用方降级为假随机串（但抖音边缘可能直接丢请求）。

## 4. Cookie 怎么拿

登录 `https://creator.douyin.com/`，打开浏览器开发者工具 → Network → 任意请求 → 复制 Request Headers 里的 `Cookie` 整串。
该 cookie 必须属于**目标视频的发布账号**。

## 5. 风险控制与失效处理

- `a_bogus` 是逆向算法，抖音改签名即失效 → 表现为 `status_code!=0` / 空响应体。此时纯 HTTP 路线不可用，需等算法更新或改用浏览器方案。
- 空 comments 但 `has_more=0` 是**合法结果**，不要当失败。
- 跨账号（cookie 非本人）→ `status_code:5`，换本人 cookie。

## 6. 输出字段（扁平化后）

`cid, parent_cid, text, user_id, nickname, digg_count, reply_count, ip_label, create_time, aweme_id`
二级回复以 `parent_cid` 关联顶层评论，单独成行。

## 7. 无头浏览器方案（免登录，--browser）

纯 HTTP 公开接口被加固空体后，这条路径用来"免登录也能抓到评论"。思路：**启动真实 Chromium
以游客身份打开视频页，抖音前端自己算好 a_bogus/msToken 并带完整指纹去调评论接口，我们只拦截
它的 `comment/list` 网络响应把数据捞出来**。签名、指纹、风控全交给浏览器，脚本零参与。

### 实测要点（2026-08-28，已验证可用）
1. **游客态能抓到真实评论**：零 cookie 打开 `https://www.douyin.com/video/<aweme_id>`，
   拦截到的 `comment/list` 响应 `status_code=0`、返回真实评论（非空体）。这证明纯 HTTP 的空体是
   "环境指纹风控"，真实浏览器补上了这块拼图。
2. **评论接口 host 是 `www-hj.douyin.com` / `www.douyin.com`**（边缘节点），不是 `creator.douyin.com`。
   拦截过滤条件用 `/comment/list/` 子串即可命中。
3. **`response.json()` 静默吞数据**：Playwright 的 `response.json()` 在非标准 Content-Type/压缩时
   会抛异常被 `except` 吞掉，导致整页评论丢失。务必用 `response.text()` + `json.loads()`。
4. **翻页是「无限滚动」而非按钮**：把 `.parent-route-container`（或 `.route-scroll-container`）+
   `.comment-mainContent` 与 `window` **同时**滚到底，才触发下一页 `comment/list`（cursor 0→5→10…）。
   单滚容器不会触发翻页。不要用"点击加载更多"按钮——合成点击会把 cursor 拉回 0 重抓第 1 页，
   Playwright 真实点击在嵌套滚动容器里又易超时。
5. **抖音游客评论墙**：滚到第 3 页左右（前 ~14-20 条）后抖音不再加载更多（页面显示
   "请先登录后发表评论"）。要抓全部评论仍需本人 cookie + 创作者接口。一次一个作品、只需部分样本时
   浏览器方案足够。
6. **反 headless 检测**：`launch` 加 `--disable-blink-features=AutomationControlled`；`add_init_script`
   覆盖 `navigator.webdriver = undefined`；UA/视口/locale/时区设成桌面中文环境。
7. **等待策略**：页面有持续轮询/长连接，`wait_until="networkidle"` 永不触发 → 用 `domcontentloaded`
   + 固定 `wait_for_timeout` 等初始评论。

### 启动参数（参考 browser_fetch.py）
```python
p.chromium.launch(headless=True, args=[
    "--disable-blink-features=AutomationControlled",
    "--no-sandbox", "--disable-dev-shm-usage"])
ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
```

