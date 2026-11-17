---
name: down
description: 'Analyze a URL and download it with minimal steps.'
version: 0.2.0
author: cgartlab, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [download, yt-dlp, aria2, curl, magnet, torrent, cloud-drive]
    related_skills: [file-download, blocked-page-recovery]
---

# Down — 万能下载 skill

分析任何 URL，用最少的步骤把它落到本地。**只使用当前环境已装工具**，任何安装动作必须先询问用户批准。

## 何时使用

- 用户扔一个 URL 过来，语义是"下载/保存/我要这个文件"。
- 用户明确说 "下载"、"存下来"、"拉过来"、"down this"、"get this" 等。

## 何时不用

- 用户只是要看网页内容 → `web_extract`。
- 用户只是要看视频但不用保存 → 直接给链接。
- 用户要求生成文件（不是下载外部）→ 走对应工具。
- 用户扔的是中文标题（"星际穿越 4K"）而不是 URL → 请用户先搜好链接再扔回来。skill 不搜索资源。

## 能力边界（v0.2）

skill 只做文件下载，不越界：

**能做的**：
- ✓ 下载直链文件（HTTP/HTTPS → curl）
- ✓ 下载平台视频（YouTube / X / Bilibili / TikTok / Douyin / ... → yt-dlp）
- ✓ 下载 .torrent 文件本体（→ curl）
- ✓ 识别网盘链接但不下载（→ 用户手动转存）

**不做的**：
- ✗ 搜索资源（"星际穿越 4K" 类模糊标题 → 请用户自己搜好链接）
- ✗ 从 magnet 拉内容（需要 BT 客户端，skill 只报告）
- ✗ 从网盘下载内容（需要账号登录，用户自己转存）
- ✗ 破解反爬站点（JS 挑战、Cloudflare turnstile 等）

## 触发方式

用户消息里出现 URL（且语义是下载/保存），即自动激活本 skill。**不需要用户显式说"用 down"**。

## URL 到手后的第一件事：确定保存路径

**路径优先级（从上到下，先命中先赢）：**

1. **用户在这次消息里明确说了路径** → 直接用（如"下载到 D:\Movies"）。
2. **用户环境里有本机偏好** → 用偏好的路径。具体来源：
   - Hermes memory 里明确的"用户本机下载偏好"（如 `D:\Download`）
   - 或 skill 配置（未来 v0.2 支持 `~/.downrc`）
   - 或环境变量 `DOWN_DEFAULT_DIR`
3. **都没有** → 默认保存到**临时目录**（`$TMPDIR` 或 `~/.cache/down/<session-id>/`）。

**不询问**——三种情况都是确定性的，不需要 `clarify` 阻塞用户。用户想改路径，直接说就行。

**设计要点**：skill 本身**不硬编码任何默认路径**（不写死 D:\Download 也不写死 /tmp），它只提供"临时目录"这个通用的最终兜底。本机偏好由 agent 的 memory / config 决定，属于用户环境层，不属于 skill 逻辑。

## 三条不可让渡的规则

1. **不静默安装**：任何工具（yt-dlp / aria2 / 其他）缺失时，先向用户展示"要装什么、用哪个包管理器、大约多大"，等一句"go"再动手。绝不默认 `uv tool install` 或 `winget install`。
2. **只用最小步骤**：能用 `curl` 解决的不上 yt-dlp；能用 yt-dlp 解决的不上 aria2。工具选择规则见 `references/tool-matrix.md`。
3. **验证才算完成**：下载成功后必须 `ffprobe`（媒体）或 `sha256sum`（其他）核验，把真实数字写进回复；不能仅凭退出码声称成功。

## 工作流

```
[URL 到手]
   |
Phase 1 — 探测（scripts/detect.py --url "<url>"）
   |  JSON 出：kind / dest_name / suggested_tool / verify_cmd
   |           user_action / reason（v0.2 新增）
   |
   ├── kind=cloud_drive → 报告网盘，不下载（见"网盘链接处理"）
   ├── kind=magnet     → 报告客户端处理，不下载（见"Magnet 链接处理"）
   └── kind=platform_video/direct_file/torrent/unknown → 继续
   |
Phase 2 — 工具检查（scripts/check_tools.py --json）
   |  ├─ available → 直接执行
   |  └─ 缺失 → 询问用户是否安装（不装则如实报告）
   |
Phase 2.5 — 代理兜底（scripts/proxy_chain.py --json）
   |  直连失败 → 按链顺序重试（见"代理兜底"）
   |
Phase 3.0 — 文件名冲突检查
   |  如果 <dest>/<name> 已存在 → 追加序号 foo.mp4 → foo (1).mp4
   |
Phase 3 — 执行下载（curl / yt-dlp）
   |  输出到 Phase 0 确定的路径
   |
Phase 4 — 验证
   |  跑 verify_cmd（ffprobe / file / sha256sum）
   |  失败 → 报告失败原因（不重下、不编造）
   |
Phase 5 — 回复用户
        MEDIA:<绝对路径> + 规格摘要 + 保存路径
```

## Phase 1 — 探测

跑 `python scripts/detect.py --url "<url>"`（Windows）或 `python3 scripts/detect.py --url "<url>"`（POSIX）。返回 JSON：

```json
{
  "url": "https://...",
  "kind": "platform_video | direct_file | torrent | magnet | cloud_drive | unknown",
  "host": "youtube.com",
  "suggested_tool": "yt-dlp | curl | none",
  "dest_name": "some-title.mp4",
  "verify_cmd": "ffprobe -v error -show_entries ...",
  "install_hint": { "name": "yt-dlp", "install_by_platform": { "windows": "uv tool install yt-dlp", "linux": "...", "macos": "..." }, "size_mb": 3, "license": "Unlicense" },
  "user_action": "（v0.2 新增：skill 不处理时的用户指引，或 null）",
  "reason": "（v0.2 新增：为什么这样建议，或 null）"
}
```

**kind 分类**（6 种，见 `references/detectors.md`）：
- `platform_video`：YouTube / X / Bilibili / TikTok / Douyin 等平台视频 → yt-dlp
- `direct_file`：直链文件（.mp4 / .pdf / .zip / ...） → curl
- `torrent`：.torrent 文件 URL → **curl**（只下种子文件本体，见 v0.2 决策 D8）
- `magnet`：magnet:?xt=... → **none**（skill 不处理，见"Magnet 链接处理"）
- `cloud_drive`：网盘链接（百度/夸克/阿里/115/天翼/微云/文库） → **none**（见"网盘链接处理"）
- `unknown`：无法识别，先 curl -I 探测

**判定规则**（host 白名单 + URL 特征匹配）见 `references/detectors.md`。

## Phase 2 — 工具检查

跑 `python scripts/check_tools.py --json` 一次性检查所有工具：

```json
{
  "platform": "windows",
  "tools": {
    "curl":   {"available": true,  "path": "...", "version": "8.4.0"},
    "yt-dlp": {"available": true,  "path": "...", "version": "2024.09.06"},
    "aria2c": {"available": false, "path": null,  "install_hint": {"windows": "winget install -e --id aria2.aria2", ...}}
  },
  "missing": ["aria2c"],
  "verdict": "partial"
}
```

**检查完按建议工具决定**：
- `curl` 缺失 → 报错，本 skill 无法工作（curl 是最后兜底）。
- `yt-dlp` 缺失 → 提示"要装 yt-dlp 吗？`uv tool install yt-dlp`（Python 包，~3 MB）"。
- `aria2c` 缺失 → 提示"要装 aria2 吗？`winget install -e --id aria2.aria2`（~4 MB）"。**注意**：v0.2 后 torrent/magnet 都不走 aria2c 了，只有用户明确要下 BT 内容时才需要。
- 用户拒绝安装 → 如实报告"此 URL 类型需要 <tool>，无法处理"。

**Windows 上**：check_tools.py 会自动扩展 PATH 到 `%LOCALAPPDATA%\.local\bin`，解决 SKILL.md 里已知的"uv 装的工具找不到"的坑。

## Phase 2.5 — 代理兜底

**默认行为**：先直连，失败才走代理。**绝不默认代理所有请求。**

**触发条件**（curl exit code 白名单）：
- 6 (couldn't resolve host)
- 7 (couldn't connect to host)
- 28 (operation timeout)
- 35, 51, 52, 53, 60 (SSL/TLS 相关)
- 91, 92, 99, 104, 105 (连接被重置 / 协议错误)

**不重试**：HTTP 4xx/5xx、认证错误、内容校验失败——服务器明确拒绝，代理救不了。

**代理链解析**：
```bash
python scripts/proxy_chain.py --json
```

按输出 chain 顺序逐条重试，第一条成功即停。

**NO_PROXY 强制规则**：目标域名匹配 `NO_PROXY` 环境变量时**禁用代理**，即使代理链里有可用项。
例：`https://api.sensenova.cn/...` 永远直连，不走任何代理。

**三工具的代理参数**：

| 工具 | 代理参数 |
|------|----------|
| curl | `--proxy <url>` 或 `-x` |
| yt-dlp | `--proxy <url>` |
| aria2c | `--http-proxy=<url>` / `--https-proxy=<url>` / `--all-proxy=socks5://...` |

**重试流程**（agent 手写，无脚本）：

```python
RETRYABLE = {6, 7, 28, 35, 51, 52, 53, 60, 91, 92, 99, 104, 105}
for proxy in chain:
    if domain_in_noproxy(target): break
    cmd = base_cmd + ("" if proxy.type == "direct" else f" --proxy {proxy.proxy}")
    result = run(cmd)
    if result.exit_code not in RETRYABLE: break
```

**报告**：
- 成功：告知"用了 <proxy source> 完成下载"。
- 全部失败：告知"直连和 3 个代理都失败，错误码 <最后一次 exit code>"。

## Phase 3.0 — 文件名冲突检查

下载前检查 `<dest>/<dest_name>` 是否已存在：

- **已存在** → 追加序号：`foo.mp4` → `foo (1).mp4` → `foo (2).mp4`
- **达到 100 个同前缀** → 拒绝并报告（防误删保护）
- **不存在** → 直接用原名

不覆盖、不删除旧文件——用户想覆盖就说一声。

## Phase 3 — 执行下载

按 kind 走不同配方，完整命令见 `references/commands.md`。摘要：

| kind | 命令骨架 |
|------|---------|
| platform_video | `yt-dlp --no-playlist -f "mp4/best" -o "<dest>/<name>.%(ext)s" "<url>"` |
| direct_file | `curl -L --fail -o "<dest>/<name>" "<url>"` |
| torrent | `curl -L --fail -o "<dest>/<name>.torrent" "<url>"` |
| unknown | 先 `curl -I` 看 Content-Type，能识别就当 direct_file，否则问用户 |

**kind=magnet 和 cloud_drive 不进 Phase 3**——见下面"网盘链接处理"和"Magnet 链接处理"。

## Phase 4 — 验证

- 媒体（.mp4/.mkv/.mp3/.m4a）：`ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_type,codec_name,width,height -of default=nw=1 "<file>"`。
- 归档（.rar/.zip/.7z）：`7z t "<file>"` 或 `unrar t "<file>"`（若装了）。
- 其他：`file "<file>"` + `sha256sum "<file>"`。

**验证失败 ≠ 下载失败**。如实报告（如"文件已下载 5 MB 但 ffprobe 报 invalid data"），别自己再下一遍。

## Phase 5 — 回复

回复结构（三行）：
1. `MEDIA:<绝对原生路径>`（单独一行，Windows 用 `D:\...`，POSIX 用绝对路径）。
2. 规格：codec、WxH、duration、size（用真实数字）。
3. 保存路径确认 + 一句工具选择说明（"用 curl 直下，无需 yt-dlp"）。

## Pitfalls（已知坑，来自实战）

- **`yt-dlp` 遇到 x.com 必须带 `--no-playlist`**：不带会把整条 post 的多视频都拉下来。
- **X 上选 `http-*` 格式，不要 `hls-*`**：hls 通常 video-only，需要再合并 audio，多一步。
- **不要预设登录**：Twitter/YouTube 的 yt-dlp extractor 自带 guest token，未登录就能跑；只有 extractor 报 auth 错误才去折腾 cookies。
- **输出模板保留扩展名**：`-o "...%(ext)s"` 让下载器选真实容器；写死 `.mp4` 会在遇到 webm/mkv 时炸。
- **Windows 上 `python -c "..."` 会吃掉反引号**（当命令替换执行）：所有复杂命令写到 .py 文件后 `python xxx.py` 执行，不要用 `-c` 或 heredoc。
- **Windows 上 `curl` 输出到 `/tmp`** 实际落到 `C:\Users\<user>\AppData\Local\Temp\`（MSYS 转换）：验证/后续访问要用真实路径。
- **Nitroflare 硬墙**：`RandHash2` JS 挑战 CLI 无法绕过 → 如实报告过不去，不要耗时间硬试。
- **Alfafile 免费流**：需要 JS 渲染 30 秒倒计时 + captcha，curl 拿不到直链 → 同上。
- **`uv tool install` 装的二进制在 `~/.local/bin`**：每次 `terminal` 调用是新 shell，必须显式 `export PATH="$HOME/.local/bin:$PATH"` 才能找到。

## 网盘链接处理（kind=cloud_drive）

识别到 `kind=cloud_drive` 时，**不下载、不尝试、不询问**，直接报告：

```
「这个链接是 {provider}，skill 不处理网盘内容。
  请把链接转存到你的网盘账号，需要其他帮助就说。」
```

**覆盖的网盘**（detect.py 的 `CLOUD_DRIVE_SITES` 白名单，10 个 host）：

| Provider | Hosts |
|----------|-------|
| 百度网盘 | `pan.baidu.com`, `yun.baidu.com` |
| 夸克网盘 | `pan.quark.cn` |
| 阿里云盘 | `www.aliyundrive.com`, `www.alipan.com` |
| 115 网盘 | `115.com`, `115cdn.com` |
| 天翼云盘 | `cloud.189.cn` |
| 腾讯微云 | `wl.123pan.com` |
| 百度文库 | `wenku.baidu.com` |

**为什么不下载**：
- 每个网盘 API 都不同，稳定性不可能保证
- 每个网盘都要 cookie / 登录态，违反"不静默认证"红线
- 用户明确说"给我链接就好"——信任用户自己的工具

## Magnet 链接处理（kind=magnet）

magnet 是元数据 URI，不是文件下载。skill 只报告，不处理：

```
「这是 magnet 链接，需要 BT 客户端解析。请复制到：
  - Windows: qBittorrent / Transmission
  - macOS:   Transmission / qBittorrent
  - Linux:   qBittorrent / Transmission / Deluge
  或者告诉我是否有 .torrent 文件直链，我可以下载 .torrent 本体。」
```

**为什么不处理**：
- magnet 需要 BT 客户端 + DHT 网络 + tracker 解析
- skill 定位是"文件下载"，不是"BT 内容下载"
- 用户手动下内容是明确偏好（决策 D9）

## 平台视频失败应对

yt-dlp 报错时**不要盲目重试**。按症状查：

| 症状 | 应对 |
|------|------|
| `No video formats found` | 升级到最新版 yt-dlp（`uv tool upgrade yt-dlp`） |
| `Sign in to confirm you're not a bot` | YouTube 反爬，等 24h 或换 IP |
| `HTTP Error 429: Too Many Requests` | 触发速率限制，等 5-10 分钟 |
| Extractor 报错（具体平台） | 检查 https://github.com/yt-dlp/yt-dlp/issues 是否有已知问题 |
| 网络超时 / 连接失败 | 尝试代理链（Phase 2.5） |

**不要**：反复重试同一命令。失败一次后升级工具或换代理。

## 与旧 skill `file-download` 的关系

`file-download` 是老版本，硬编码 `D:\Download`、假设 yt-dlp 存在。**本 skill 是它的正式替代**：
- 保存路径**三级优先级**：用户显式指定 → 环境偏好（memory/config）→ 临时目录兜底。skill 不硬编码任何默认路径。
- 工具安装强制询问（不再默认 `uv tool install`）。
- 覆盖 torrent/magnet（file-download 不覆盖）。
- 保留 file-download 的所有 X/Twitter 最佳实践。

用户显式加载本 skill 后，新下载请求应走 down，不走 file-download。

## Verification

- 文件物理存在于目标路径，size > 0，文件名描述性。
- ffprobe/file/sha256sum 输出与文件大小一致。
- `MEDIA:` 路径指向同一个文件。
- 工具安装动作前有过一次用户批准（除非用户显式说"你决定"）。
