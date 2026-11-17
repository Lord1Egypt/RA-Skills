# URL 探测器（detect.py）

`scripts/detect.py` 是本 skill 的核心探测器：给定一个 URL，返回 JSON 描述 URL 类型、建议工具、目标文件名和验证命令。

## 契约

**输入**：`--url <url>`（必填）

**输出（stdout）**：JSON，字段：

| 字段 | 类型 | 含义 |
|------|------|------|
| `url` | str | 原样回传 |
| `host` | str | 域名（`urlparse().hostname`），可能为空（如 `magnet:`） |
| `kind` | str | `platform_video` / `direct_file` / `torrent` / `magnet` / `cloud_drive` / `unknown` |
| `suggested_tool` | str | `yt-dlp` / `curl` / `none` |
| `dest_name` | str\|null | 建议的目标文件名（含扩展名），caller 决定最终路径。cloud_drive/magnet 为 null |
| `verify_cmd` | str\|null | 验证命令模板（含 `<file>` 占位符）。cloud_drive/magnet 为 null |
| `install_hint` | dict | 建议工具缺失时的安装提示，可能为空 `{}` |
| `user_action` | str\|null | skill 不处理时给用户的行动指引（v0.2 新增） |
| `reason` | str\|null | 为什么这样建议（v0.2 新增） |

**退出码**：0（除 --help/参数错误外永不非零——错误信息走 JSON）

## 判定优先级（从上到下短路）

1. URI scheme 是 `magnet:` → `kind=magnet`，`suggested_tool=none`
2. 路径以 `.torrent` 结尾 → `kind=torrent`，`suggested_tool=curl`（只下种子文件本体）
3. host 在 `PLATFORM_SITES` 白名单里 → `kind=platform_video`，`suggested_tool=yt-dlp`
4. host 在 `CLOUD_DRIVE_SITES` 白名单里 → `kind=cloud_drive`，`suggested_tool=none`
5. 路径有扩展名且是视频/音频/图片/归档/文档 → `kind=direct_file`，`suggested_tool=curl`
6. 都不匹配 → `kind=unknown`，`suggested_tool=curl`（caller 用 `curl -I` 探测）

## 平台站白名单（PLATFORM_SITES）

当前覆盖：`youtube.com`, `youtubekids.com`, `youtu.be`, `music.youtube.com`, `twitter.com`, `x.com`, `bilibili.com`, `b23.tv`, `tiktok.com`, `vm.tiktok.com`, `vimeo.com`, `dailymotion.com`, `douyin.com`, `weibo.com`, `redditmedia.com`, `reddit.com`, `twitch.tv`

**新增站点**：在 `scripts/detect.py` 顶部 `PLATFORM_SITES` 字典加一行，值统一 `"yt-dlp"`。

## 网盘站白名单（CLOUD_DRIVE_SITES，v0.2 新增）

识别但不下载。当前覆盖 10 个 host：

| Provider | Hosts |
|----------|-------|
| 百度网盘 | `pan.baidu.com`, `yun.baidu.com` |
| 夸克网盘 | `pan.quark.cn` |
| 阿里云盘 | `www.aliyundrive.com`, `www.alipan.com` |
| 115 网盘 | `115.com`, `115cdn.com` |
| 天翼云盘 | `cloud.189.cn` |
| 腾讯微云 | `wl.123pan.com` |
| 百度文库 | `wenku.baidu.com` |

**新增网盘**：在 `scripts/detect.py` 顶部 `CLOUD_DRIVE_SITES` 字典加一行，值统一为 provider 中文名。

## 文件名生成规则

- **平台视频**：`<host>_<id>.<ext>`，id 从 URL 提取
  - YouTube `?v=<id>` → `www_youtube_com_<id>.mp4`
  - X/Twitter `/status/<id>/video/*` → `x_com_<id>.mp4`
  - youtu.be 短链 `/youtu.be/<id>` → `youtube_<id>.mp4`
- **直链文件**：直接取路径末段（URL decode `%20` → 空格），经 `sanitize_filename` 净化
- **magnet**：从 `dn=` 参数取（URL decode），经 `sanitize_filename` 净化
- **cloud_drive**：`dest_name=null`（不下载，无需文件名）

**v0.2 新增**：所有文件名都过 `sanitize_filename()` 净化（防路径穿越 / shell 注入）：
- 路径分隔符 `/` 和 `\` 替换为 `_`
- `..` 路径穿越拒绝
- 控制字符（0x00-0x1F, 0x7F）strip
- shell 元字符（`` ` $ & | ; < > ( ) { } [ ] * ? " ' \ ``）替换为 `_`
- 长度截断 200 字符
- 空字符串 fallback 为 `download`

## 验证命令模板

- 媒体文件（视频/音频）→ `ffprobe`
- 归档/文档/图片/其他 → `file`
- magnet / cloud_drive → `verify_cmd=null`（不下载，无需验证）

`<file>` 占位符在 SKILL.md 的 Phase 4 被 caller 替换为真实绝对路径。

## 反例：不做网络请求

探测器**不发送任何 HTTP 请求**。原因：
1. 有些站点的 Referer/User-Agent 会泄露用户身份，探测即触发反爬。
2. `curl -I` 对某些 CDN 会返回 `302 → challenge page`，把简单直链误判为 unknown。
3. 用户可能希望"探测 + 询问"是一次轻量对话，而不是偷偷去访问目标服务器。

**如果 caller 需要对 unknown URL 做进一步网络判定**，由 caller 决定（例如 curl -I 看 Content-Type），detect.py 只返回元数据不代替决策。

## 测试

`evals/test_detect.py` 覆盖 28 个用例：
- 每个 kind 至少 1 个 URL（platform_video 6 个 / direct_file 4 个 / torrent 1 / magnet 2 / cloud_drive 11 / unknown 2）
- YouTube `?v=` 与 youtu.be 短链的 id 提取
- X/Twitter status id 提取
- magnet `dn=` 参数解析 + user_action / reason 字段
- cloud_drive 所有 10 个 host
- 路径无扩展名但 host 是 .com/.org 的 unknown 兜底
- dest_name 路径穿越 / shell 注入净化
