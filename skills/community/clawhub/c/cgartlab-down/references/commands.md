# 下载命令配方

所有命令都假设 caller 已经：
1. 用 `clarify` 或对话确定了**保存路径 `<dest>`**（绝对路径）
2. 用 `scripts/detect.py` 拿到了 `<kind>` / `<suggested_tool>` / `<dest_name>`
3. 用 `scripts/check_tools.py` 确认工具可用
4. 用户批准了必要的工具安装（如有）

**代理兜底**：如果直连失败，用 `python scripts/proxy_chain.py --json` 拿代理链，
在命令后加 `--proxy <url>` 重试。详见 `references/tool-matrix.md` 的"代理参数速查"。

## 平台视频（platform_video → yt-dlp）

```bash
export PATH="$HOME/.local/bin:$PATH"  # Windows 上必须，uv tool install 装在这里
yt-dlp --no-playlist -f "mp4/best" \
       -o "<dest>/<dest_name>.%(ext)s" \
       "<url>"
```

关键点：
- **`--no-playlist` 不可省**：X/Twitter 的多视频 post 不带此参数会把整条 post 的所有视频都拉下来。
- **`-f "mp4/best"`**：选 mp4 容器里最好的档位。X/Twitter 上的 `http-*` 格式（muxed audio+video）优先于 `hls-*`（video-only）。
- **`%(ext)s` 必须保留**：让 yt-dlp 选真实容器（有时是 webm/mkv），写死 `.mp4` 会炸。

**如果下载完 ffprobe 显示只有 video 没有 audio**：重新跑一次 `yt-dlp -F "<url>"` 列出格式，选显式的 `http-*` id 而不是 `hls-*`：
```bash
yt-dlp -f "http-<best_id>" -o "<dest>/<dest_name>.%(ext)s" "<url>"
```

## 直链文件（direct_file → curl）

```bash
curl -L --fail \
     --retry 3 --retry-delay 2 \
     --progress-bar \
     -o "<dest>/<dest_name>" \
     "<url>"
```

关键点：
- `-L` 跟随重定向（大多数 CDN 会 302 一次）
- `--fail` HTTP 错误时退出非零（否则 404 页也会被保存成文件）
- `--retry 3` 三次重试（网络抖动很常见）
- `--progress-bar` 一行进度条（无进度输出更清晰，`--progress-bar` 会覆盖默认）

## Torrent 文件本体（torrent → curl）

**v0.2 决策**：只下载 `.torrent` 文件本体（几 KB 到几 MB 的小文本文件），
用户手动用 BT 客户端打开下载内容。不需要 aria2c。

```bash
curl -L --fail \
     --retry 3 --retry-delay 2 \
     --progress-bar \
     -o "<dest>/<dest_name>" \
     "<url>"
```

关键点：
- 命令与 `direct_file` 一致，`.torrent` 文件就是普通 HTTP 文件
- 下载完成后回复：`"下载完成 <dest>/<name>.torrent。如需下载内容，用 qBittorrent 等 BT 客户端打开此文件。"`

## Magnet 链接（magnet → none，skill 不处理）

skill 不处理 magnet。回复模板：

```
「这是 magnet 链接，需要 BT 客户端解析。请复制到：
  - Windows: qBittorrent / Transmission
  - macOS:   Transmission / qBittorrent
  - Linux:   qBittorrent / Transmission / Deluge
  或者告诉我是否有 .torrent 文件直链，我可以下载 .torrent 本体。」
```

## 网盘链接（cloud_drive → none，skill 不处理）

skill 不处理网盘。回复模板：

```
「这个链接是 {provider}，skill 不处理网盘内容。
  请把链接转存到你的网盘账号，需要其他帮助就说。」
```

## 验证命令

### 媒体文件（.mp4/.mkv/.mp3/.m4a/...）

```bash
ffprobe -v error \
        -show_entries format=duration,size,bit_rate \
        -show_entries stream=codec_type,codec_name,width,height,r_frame_rate \
        -of default=nw=1 \
        "<file>"
```

期望输出（视频）：
```
codec_name=h264
codec_type=video
width=1920
height=1080
r_frame_rate=30/1
codec_name=aac
codec_type=audio
duration=365.123
size=12345678
bit_rate=270000
```

### 其他文件

```bash
file "<file>"
sha256sum "<file>"   # 或 sha1sum，Windows 用 certutil -hashfile
```

## 回复模板

### 下载成功

```
✅ 下载完成，验证通过：h264 1920×1080 + AAC，6:05，12.3 MB
（该 URL 类型是 <kind>，用 <tool> 下载）

MEDIA:<absolute path>

📁 保存位置：<dest>/<dest_name>
```

Windows 上 MEDIA: 路径必须**双反斜杠或正斜杠**：`D:\\Download\\file.mp4` 或 `D:/Download/file.mp4`。

### magnet / cloud_drive 不下载

```
📎 这是 {magnet|{provider}} 链接，skill 不处理。

{user_action}

如需其他帮助就说。
```
