# 国内网络配置方案

NotebookLM 服务在大陆**不可直连**，必须解决网络问题才能用本 Skill。

## 三套方案选一

| 方案 | 难度 | 成本 | 稳定性 | 适合 |
|---|---|---|---|---|
| **A. 系统代理** | 🟢 低 | 视代理而定 | 🟡 看代理 | 已有梯子的用户 |
| **B. 海外服务器** | 🟡 中 | $5+/月 | 🟢 高 | 长期重度使用 |
| **C. 本地 Playwright + 浏览器代理插件** | 🟢 低 | 0 | 🟡 | 偶尔用一次 |

---

## 方案 A：系统代理（最常用）

假设代理监听 `127.0.0.1:7890`：

```bash
# 加到 ~/.zshrc
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
export all_proxy=socks5://127.0.0.1:7890

# Playwright 也走代理
export HTTPS_PROXY=$https_proxy
```

```bash
source ~/.zshrc
```

验证：

```bash
curl -I https://www.google.com  # 200 OK 即通
curl -I https://notebooklm.google.com  # 200 OK 即通
```

> ⚠️ 代理节点务必用美/日/新加坡等 NotebookLM 已开放区域，**不要选香港**（部分账号在港 IP 下会被风控）。

---

## 方案 B：海外服务器（长期方案）

把整个 WorkBuddy 部署到海外 VPS（DigitalOcean / Linode / 腾讯云海外节点），本地通过 SSH 远程访问。

适合：每天处理多篇付费文章、大量小宇宙播客转写的重度用户。

---

## 方案 C：浏览器代理插件兜底

如果你只想偶尔用一次，不想配系统代理：

1. Chrome 装 SwitchyOmega
2. 仅对 `*.google.com` `*.googleusercontent.com` 走代理
3. 让 Playwright 复用系统 Chrome：

```python
# 上游脚本里改启动方式
playwright.chromium.launch_persistent_context(
    user_data_dir="~/Library/Application Support/Google/Chrome",
    channel="chrome",  # 用系统 Chrome 而非内置 chromium
    headless=False
)
```

---

## 付费墙抓取的网络选择

抓微信公众号、知识星球、财新等**国内**站点时：
- ❌ **关闭代理** 或代理走"国内站点直连规则"
- 否则会被反爬识别为海外异常流量

抓 NYT / WSJ / FT / Economist 等**海外**站点时：
- ✅ **开启代理** 走美/欧节点
- archive.today 在国内常打不开，可走 archive.org 备份

本 Skill 在工作流中会**自动判断**目标域名归属，并提示是否需要切换代理。

---

## 排错

| 现象 | 原因 | 解决 |
|---|---|---|
| `Connection refused` | 代理未启动 | 启动 Clash/V2Ray |
| `407 Proxy Authentication` | 代理需要鉴权 | `http_proxy=http://user:pass@host:port` |
| NotebookLM 一直转圈 | Cookie 过期 | 重新跑 `notebooklm login` |
| 抓微信公众号一直 403 | 代理把国内流量也劫持了 | 设置 PAC 规则放行 mp.weixin.qq.com |
