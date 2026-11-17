# 工具矩阵与选择规则

本 skill 遵循**最小步骤原则**：能用 curl 解决的不上 yt-dlp；能用 yt-dlp 解决的不上 aria2。选择优先级从下往上：**优先级数字小的先试**。

## 判定决策树

```
URL 拿到手
   |
   +-- 是 magnet:?xt=... ?
   |       --> kind=magnet，suggested_tool=none
   |           skill 不处理，报告用户用 BT 客户端
   |
   +-- URL 路径以 .torrent 结尾 ?
   |       --> kind=torrent，suggested_tool=curl
   |           只下种子文件本体（v0.2 决策 D8）
   |
   +-- host 是平台站（x.com / youtube.com / bilibili.tv / ...） ?
   |       --> kind=platform_video，suggested_tool=yt-dlp
   |
   +-- host 是网盘（pan.baidu.com / pan.quark.cn / ...） ?
   |       --> kind=cloud_drive，suggested_tool=none
   |           skill 不处理，报告用户手动转存（v0.2 决策 D10）
   |
   +-- URL 路径以文件扩展名结尾（.mp4/.pdf/.zip/...） ?
   |       --> kind=direct_file，suggested_tool=curl
   |
   +-- 都不匹配（unknown）
           --> kind=unknown，suggested_tool=curl
               先 curl -I 探 Content-Type，能识别就当 direct_file，
               否则问用户"这是什么类型的资源"
```

## 各工具能力边界

| 工具 | 处理对象 | 依赖 | 安装命令（示例） |
|------|---------|------|-----------------|
| `curl` | 任意 HTTP(S) 直链；不支持 magnet/BitTorrent；不支持平台视频解析；.torrent 文件本体（v0.2） | 系统自带 | 无需 |
| `yt-dlp` | 1744 个平台的视频/音频页面（YouTube, X, Bilibili, TikTok, Reddit, Vimeo, Dailymotion, Twitch 等） | Python 3.8+ | `uv tool install yt-dlp`（Windows/Linux/macOS 通用） |
| `aria2c` | BitTorrent 协议（`.torrent` 内容、`magnet:` URI）、HTTP 分块多线程 | C 二进制 | Windows: `winget install -e --id aria2.aria2`；Linux: `apt install aria2`；macOS: `brew install aria2` |

**v0.2 变化**：
- `.torrent` 文件从 aria2c 改为 curl（只下种子文件本体，不需要 BT 客户端）
- magnet 不再走任何下载工具（skill 只报告）
- aria2c 只在用户明确要下载 BT 内容时才需要

**其他候选（v0.1 未纳入，未来扩展）**：
- `uget` — 老派 curl 替代，Windows GUI 有历史，CLI 场景用不上。
- `axel` — 多线程直链下载，功能与 `aria2c -x` 重叠，无必要引入。
- `pywebhockey` 类脚本 — 特定站点破解，不进工具矩阵，遇到具体站点时按需处理。

## 工具缺失时的降级策略

| 场景 | 首选 | 若首选缺失，用户拒绝安装 |
|------|------|--------------------------|
| 平台视频 | yt-dlp | **无降级**（curl 抓不到平台视频流）；如实报告"需 yt-dlp" |
| 直链文件 | curl | **无降级**（curl 是最后兜底）；无 curl 则报错终止 |
| .torrent 文件本体 | curl | 无降级（curl 是最后兜底） |
| magnet | none | skill 不处理，报告用户用 BT 客户端 |
| cloud_drive | none | skill 不处理，报告用户手动转存 |

**关键点**：torrent/magnet 与平台视频**没有互相降级的可能**——它们需要不同的工具。skill 必须诚实报告"这个 URL 类型没有已装工具能处理"，而不是花哨地猜。

## 常见 URL 类型 → 工具对照

| URL 形态 | kind | tool |
|---------|------|------|
| `https://x.com/*/status/*/video/*` | platform_video | yt-dlp |
| `https://youtube.com/watch?v=*` | platform_video | yt-dlp |
| `https://youtu.be/*` | platform_video | yt-dlp |
| `https://b23.tv/*` | platform_video | yt-dlp |
| `https://*.mp4` / `*.mkv` / `*.webm` | direct_file | curl |
| `https://*.pdf` / `*.zip` / `*.tar.gz` | direct_file | curl |
| `https://*.torrent` | torrent | curl（只下种子文件） |
| `magnet:?xt=urn:btih:*` | magnet | none（skill 不处理） |
| `https://pan.baidu.com/s/*` | cloud_drive | none（skill 不处理） |
| `https://pan.quark.cn/s/*` | cloud_drive | none（skill 不处理） |
| `https://www.aliyundrive.com/s/*` | cloud_drive | none（skill 不处理） |
| `https://alfafile.net/file/*` / `https://nitroflare.com/view/*` | unknown | curl（但很可能进不了真下载页——见 `references/anti-bot.md`） |

## 代理参数速查（v0.2 新增）

| 工具 | 代理参数 |
|------|----------|
| curl | `--proxy <url>` 或 `-x` |
| yt-dlp | `--proxy <url>` |
| aria2c | `--http-proxy=<url>` / `--https-proxy=<url>` / `--all-proxy=socks5://...` |

**代理链解析**：跑 `python scripts/proxy_chain.py --json` 获取有序代理链，
按链顺序重试下载（先直连，失败才走代理）。**NO_PROXY 匹配的目标域名永远直连**。

## Windows 特殊约定

- `uv tool install <pkg>` 装到 `%LOCALAPPDATA%\\.local\\bin`（即 `~/.local/bin`）。
- **`scripts/check_tools.py` 自动扩展 PATH** 到 `%LOCALAPPDATA%\\.local\\bin`，所以用 check_tools 检查过的工具一定能找到。
- **每次 `terminal` 调用是新 shell**，直接用 `yt-dlp` 时仍需显式：
  ```bash
  export PATH="$HOME/.local/bin:$PATH" && yt-dlp --version
  ```
- `winget install -e --id aria2.aria2` 装完二进制在 `%LOCALAPPDATA%\\Microsoft\\WinGet\\Links\\`，PATH 里通常已有。
- **不要试图 `pip install yt-dlp`**：`pip` 不在 PATH，`uv tool install` 才是正确的安装方式。
- Windows 命令模板见 `references/commands-windows.md`。

## Linux / macOS 特殊约定

- Linux: `apt install aria2` 或 `dnf install aria2`；yt-dlp 用 `uv tool install` 或 `pipx install yt-dlp`。
- macOS: `brew install aria2 yt-dlp`（一条命令两个都装）。

## 何时向用户询问安装

**任何工具缺失时都要问，绝不静默安装。**询问内容包含：
1. 要装哪个工具（名字）
2. 为什么需要（这个 URL 类型没有别的替代）
3. 用哪个包管理器（本机探测：Windows → winget；Linux → apt/dnf；macOS → brew）
4. 大约多大（体积）
5. 一句"go"才能装

示例询问文案：
> 「这个链接需要 yt-dlp 才能下载（YouTube 页面直接 curl 拿不到视频流）。要用 uv 装吗？大约 3 MB，命令是 `uv tool install yt-dlp`。回复"go"我就装。」

## 何时不询问安装（v0.2 新增）

以下 kind 的 suggested_tool 是 `none`，**skill 不下载，不询问安装**：
- `magnet`：报告用户用 BT 客户端
- `cloud_drive`：报告用户手动转存
