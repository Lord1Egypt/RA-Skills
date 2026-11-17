---
name: cn-browser-automation
description: 国内站点（小红书/淘宝/天猫/微信/微博/B站/12306/知乎/各类 SaaS 后台）的登录态浏览器自动化。当用户需要抓取或操作需要登录的国内网站、复用本机已登录 Chrome 的会话、带 cookie 导出数据，或提到"登录态""已登录浏览器""带账号抓取""复用我的 Chrome""不想重新登录"时使用。This skill should be used when the user wants to scrape or operate Chinese domestic websites that require authentication, reuse the locally logged-in Chrome session via CDP, or export data with login state preserved.
agent_created: true
---

# 国内站点登录态自动化 (cn-browser-automation)

## Overview

把"本机已经正常登录的 Chrome"借给 WorkBuddy 使用：通过 DevTools 远程调试端口接入那个**带登录态**的浏览器，再去抓取国内站点或操作后台，避免重复登录、绕过来之不易的会话。

与通用浏览器技能（browser-use / playwright / stagehand）的区别：**本 skill 默认复用用户的真实登录态**，专门解决国内站点"一上来就卡在登录页 / 被反爬拦"的痛点，并内置常见站点的选择器与反爬要点模板。

## When to use

- 用户要抓 / 操作需要登录的国内站点：小红书、淘宝/天猫、微信/公众号、微博、B站、12306、知乎、各类 SaaS 后台。
- 用户提到："登录态""已登录浏览器""带 cookie""复用我的 Chrome""不想重新登录""用我现在的账号抓"。
- 通用浏览器技能在目标站点卡在登录页时，由本 skill 接管。

## 核心思路：复用本机登录态（不要开干净浏览器）

让用户先在普通 Chrome 里正常登录目标站点，再让 WorkBuddy 接入那个浏览器：

1. 启动 Chrome 时打开远程调试端口并指定 `user-data-dir`（保存登录信息）。
2. 用 Playwright 的 `connect_over_cdp("http://127.0.0.1:9222")` 连接，**复用已有的浏览器上下文（含 cookie / 登录态）**。
3. 在该上下文里新建页面操作目标站点，会话天然生效。

启动方式与排错见 `references/setup.md`。

## Workflow

1. 确认本机 Chrome 已带远程调试端口运行；否则运行 `scripts/connect_chrome.py --launch` 帮用户启动（或参考 setup.md 手动启动）。
2. 运行脚本连接并打开目标页：
   `python scripts/connect_chrome.py <url> [--js "<提取JS>"] [--wait "<选择器或秒数>"] [--out <file.json>]`
3. 等待页面加载 / 登录态生效；必要时截图确认（脚本可加 `--screenshot` 后续扩展）。
4. 执行提取或操作（`page.evaluate` / 点击 / 填表），结果落盘为 json（再转 csv/xlsx）。
5. 站点特异性选择器与反爬要点见 `references/sites.md`。

## 站点模板索引（references/sites.md）

- ✅ 小红书：笔记列表 / 详情抓取、搜索页、登录态要点 —— 已固化 `scripts/xhs_scrape.py`
- ✅ 淘宝 / 天猫：商品页、搜索结果、反爬滑块 —— 已固化 `scripts/tb_scrape.py`（搜索页需登录态）
- ✅ B站：排行榜、视频信息 —— 已固化 `scripts/bili_scrape.py`（免登录）
- ⚠️ 微博、知乎：未登录被强反爬重定向，需登录态核验
- 微信 / 公众号：文章导出（强制登录）
- 12306：余票 / 订单（反爬强 + 实名，高风险）

> 注意：国内站点 DOM 与反爬策略经常变动，**模板中的选择器需在使用前实际核验**，不要假设长期有效。✅ 带 ✅ 的站点已由对应脚本实跑核验过。

## 反爬与合规红线

- 控制请求频率，加随机延时；尊重 robots 与站点 ToS。
- 登录态仅用于用户**自己的账号与已授权数据**，不得用于绕过付费 / 权限墙做违规抓取。
- 遇滑块 / 验证码：**优先让用户在浏览器里人工过一次**，再让脚本继续；**不要内置验证码破解逻辑**。

## Resources

### scripts/

- `connect_chrome.py`：通过 `connect_over_cdp` 连接本机已登录 Chrome，导航到目标页，可选执行 JS 提取数据并输出 json。支持 `--launch` 自动启动 Chrome。通用底层工具。
- `cn_browser.py`：公共模块。封装 `scrape(url, js, wait, port, launch, out_json, out_csv)`，复用 `connect_chrome.py` 的连接/启动逻辑，负责连接 → 导航 → 等待 → 提取 → 导出 JSON/CSV，供下列站点脚本调用，避免重复代码。
- `xhs_scrape.py`：小红书笔记列表一键抓取（探索页 / `--search 关键词`），列表 → JSON/CSV。✅ 选择器已实跑核验。
- `tb_scrape.py`：淘宝商品列表一键抓取（首页猜你喜欢 / `--search 关键词`），列表 → JSON/CSV。✅ 首页选择器已核验；搜索页需登录态才填充。
- `bili_scrape.py`：B站排行榜一键抓取（免登录，DOM 极稳定），列表 → JSON/CSV。✅ 选择器已实跑核验。

### references/

- `setup.md`：Chrome 远程调试启动方法、Playwright 安装（含受限网络下的腾讯镜像）、常见排错。
- `sites.md`：常见国内站点的选择器与反爬要点模板。
