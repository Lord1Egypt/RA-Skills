# 反爬与硬墙站点

有些站点即使工具齐备也**无法通过 CLI 下载**。这些是硬墙，需要如实报告而不是耗时间硬试。识别到这些站点时，skill 应该：
1. 说明"这个站点有反爬，CLI 拿不到直链"
2. 给出可能的替代路径（登录手动点、找同源镜像、放弃）
3. **不**尝试用 headless 浏览器破解（Hermes 环境一般无法可靠跑 JS 挑战）

## Nitroflare（及同类 Rapidgator 生态）

**特征**：URL 形如 `https://nitroflare.com/view/<FILE_ID>/<NAME>`

**硬墙**：页面底部有 `RandHash2` JS 挑战脚本，浏览器端计算哈希后再 AJAX POST 到 `ajax/randHash.php` 换取真实下载凭证。CLI 无法计算 → 永远进不了免费下载页。

**页面特征字段**（可 grep 快速识别）：
- `downloadLocked` 隐藏字段
- `Slow Download` 按钮 + `180s` ticket waiting
- 明确写着 "Reduced download speed (max. 20 kb/s)"

**报告文案示例**：
> 这个文件在 Nitroflare 上，站点的 `RandHash2` JS 挑战挡住了所有非浏览器请求。CLI 拿不到真实下载链接。
>
> 可选方案：
> 1. 用浏览器手动点慢速下载（每份 ~20 kb/s，速度极慢）
> 2. 找同源镜像（其他网盘）
> 3. 放弃这个源，直接买官方（如果有）

## Alfafile

**特征**：URL 形如 `https://alfafile.net/file/<SHORT_ID>`

**硬墙**：慢速下载按钮走 AJAX：
1. GET `/download/start_timer/<id>` → 返回 `{"timer":"30","redirect_url":"/file/<id>/captcha"}`
2. 前端 JS 计时 30 秒
3. 自动跳 `/file/<id>/captcha` 完成人机验证
4. 拿到真实直链

CLI 用 curl 拿不到这个流程的中间态（`/captcha` 用 XHR 头 + 前置 session 访问才返回真数据，直接 GET 拿到的是 404）。

**页面特征字段**（可 grep 识别）：
- `slow_download_btn` + `data-href="/download/start_timer/..."`
- `Download restriction: 1 file per 120 minutes`

## CGPersia 类资源站

**特征**：WordPress 博客，文章里贴网盘直链（Rapidgator / Alfafile / Nitroflare 组合）

**特点**：
- **不是**站点本身反爬，而是**上游网盘**反爬
- 站点可能给多个网盘做备份（"Rapidgator + Alfafile + Nitroflare"），每个都可能有不同的通过率
- 通常**没有密码保护**（文章里没写密码 = 无密码）——用 `grep password` 在页面 HTML 里找，只命中网站登录框的 `name="password"` 就说明无密码

**报告文案**：
> 这个资源在 CGPersia 上，本身没问题，但引用的 Nitroflare/Alfafile 直链有 JS 反爬。
>
> 已确认：RAR 文件本身**无密码**（页面 grep 结果）。
>
> 可选：
> 1. 你手动在浏览器里点慢速下载（每份 ~2 小时）
> 2. 找其他镜像源

## 需要登录的站点

**特征**：URL 打开就跳 `/login` 或显示"Please log in to view this page"

**处理方式**：
1. 检查 vault：如果用户有登录保存，用 `browser_vault_fill` 自动填
2. 如果没有：如实报告"这个资源需要登录"，不要尝试猜测密码或爬 cookie
3. 让用户决定是否手动登录后再来

## 需要付费的站点

**特征**：URL 打开是购买页（"Buy for $X"）

**处理方式**：如实报告，不尝试破解。如果用户想要"绕过付费墙"——拒绝，礼貌说明。

## 通用识别原则

CLI 拿不到直链时，**先做静态分析再决定**：
1. `curl -sL <url> -o /tmp/page.html`
2. `grep -iE 'captcha|login|paywall|randhash|js challenge|blocked' /tmp/page.html`
3. 命中 → 判定为硬墙，走"如实报告"路径
4. 不命中 → 尝试走完整下载流程

**避免的做法**：
- 花大量时间调 User-Agent 或 headers 试图"绕过"
- 启动 headless 浏览器去破解 JS 挑战（Hermes 环境不可靠，且可能违反站点 ToS）
- 反复重试同一条硬墙链（每次都会失败，浪费时间）
