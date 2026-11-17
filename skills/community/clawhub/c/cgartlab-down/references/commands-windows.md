# Windows PowerShell 命令模板

本文件是 `references/commands.md`（POSIX/bash）的 Windows 版本。
所有命令都用 **PowerShell 语法**，**`curl.exe`**（Windows 10+ 自带，不是 PowerShell 的 `Invoke-WebRequest` alias）。

## 前置约定

- **`curl.exe` 而非 `curl`**：PowerShell 里 `curl` 是 `Invoke-WebRequest` 的 alias，行为完全不同。
  显式用 `curl.exe` 才是 Windows 10+ 自带的 GNU curl。
- **`&` 调用外部程序**：PowerShell 里 `& "C:\path\with space\yt-dlp.exe" args` 才能调用带空格路径的可执行文件。
- **`%USERPROFILE%\.local\bin`** 而非 `$HOME/.local/bin`：`uv tool install` 默认装到 `%LOCALAPPDATA%\.local\bin`（即 `C:\Users\<user>\.local\bin`）。
- **`%TEMP%`** 而非 `/tmp`：Windows 临时目录。
- **`%USERPROFILE%`** = `C:\Users\<user>`。

## 平台视频（platform_video → yt-dlp）

```powershell
$env:PATH = "$env:LOCALAPPDATA\.local\bin;$env:PATH"   # uv tool install 装在这里
& yt-dlp --no-playlist -f "mp4/best" `
    -o "<dest>\<dest_name>.%(ext)s" `
    "<url>"
```

或一行式（推荐用于脚本）：

```powershell
$env:PATH = "$env:LOCALAPPDATA\.local\bin;$env:PATH"; & yt-dlp --no-playlist -f "mp4/best" -o "<dest>\<dest_name>.%(ext)s" "<url>"
```

关键点：
- **`&` 调用外部程序**不可省：不带 `&` 会被 PowerShell 当成内置 cmdlet 查找失败。
- **反引号 `` ` ``** 是 PowerShell 的行续符（bash 是 `\`）。
- **`%(ext)s` 必须保留**：让 yt-dlp 选真实容器（有时是 webm/mkv）。
- **`--no-playlist` 不可省**：X/Twitter 的多视频 post 不带此参数会把整条 post 的所有视频都拉下来。

## 直链文件（direct_file → curl）

```powershell
& curl.exe -L --fail `
     --retry 3 --retry-delay 2 `
     --progress-bar `
     -o "<dest>\<dest_name>" `
     "<url>"
```

或一行式：

```powershell
& curl.exe -L --fail --retry 3 --retry-delay 2 --progress-bar -o "<dest>\<dest_name>" "<url>"
```

关键点：
- **`curl.exe`** 而非 `curl`：PowerShell 里 `curl` 是 `Invoke-WebRequest` 的 alias。
- **`&` 调用外部程序**。
- 路径用**反斜杠** `\`，但 shell 里**双反斜杠**转义（或正斜杠 `/` 也行）。

## Torrent 文件本体（torrent → curl）

```powershell
& curl.exe -L --fail `
     --retry 3 --retry-delay 2 `
     --progress-bar `
     -o "<dest>\<dest_name>" `
     "<url>"
```

命令与 `direct_file` 完全一致，`.torrent` 文件就是普通 HTTP 文件。
用户手动用 qBittorrent 打开下载内容。

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

```powershell
& ffprobe -v error `
    -show_entries format=duration,size,bit_rate `
    -show_entries stream=codec_type,codec_name,width,height,r_frame_rate `
    -of default=nw=1 `
    "<file>"
```

### 其他文件

```powershell
Get-Item "<file>" | Format-List Name,Length,LastWriteTime

# SHA256 校验和
certutil -hashfile "<file>" SHA256
```

或者用 Python（跨平台通用）：
```powershell
python -c "import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "<file>"
```

## 回复模板

### 下载成功

```
✅ 下载完成，验证通过：h264 1920×1080 + AAC，6:05，12.3 MB
（该 URL 类型是 <kind>，用 <tool> 下载）

MEDIA:D:\Download\file.mp4

📁 保存位置：D:\Download\file.mp4
```

Windows 上 MEDIA: 路径用**单反斜杠**或**正斜杠**均可：`D:\Download\file.mp4` 或 `D:/Download/file.mp4`。

### magnet / cloud_drive 不下载

```
📎 这是 {magnet|{provider}} 链接，skill 不处理。

{user_action}

如需其他帮助就说。
```

## Windows 代理配置

**永久设置环境变量**（当前用户）：
```powershell
[Environment]::SetEnvironmentVariable("HTTPS_PROXY", "http://127.0.0.1:7897", "User")
[Environment]::SetEnvironmentVariable("HTTP_PROXY",  "http://127.0.0.1:7897", "User")
[Environment]::SetEnvironmentVariable("NO_PROXY",    "localhost,127.0.0.1,::1,sensenova.cn", "User")
```

**当前 shell 临时设置**（PowerShell）：
```powershell
$env:HTTPS_PROXY = "http://127.0.0.1:7897"
$env:HTTP_PROXY  = "http://127.0.0.1:7897"
$env:NO_PROXY    = "localhost,127.0.0.1,::1,sensenova.cn"
```

**当前 shell 临时设置**（cmd.exe）：
```cmd
set HTTPS_PROXY=http://127.0.0.1:7897
set HTTP_PROXY=http://127.0.0.1:7897
set NO_PROXY=localhost,127.0.0.1,::1,sensenova.cn
```

**代理工具默认监听**：
- Clash 默认 7890（HTTP + SOCKS）
- Hermes 建议 7897（自建代理）

设置后 curl.exe / yt-dlp / aria2c 都会自动尊重这些环境变量。

## 常见坑

- **PowerShell 里 `curl` 是 `Invoke-WebRequest` 的 alias**：行为完全不同，必须用 `curl.exe`。
- **PowerShell 里 `&` 调用外部程序**：`& yt-dlp ...` 而非 `yt-dlp ...`（当 yt-dlp 路径有空格时必需）。
- **行续符是反引号 `` ` ``**：bash 是 `\`。
- **`$env:NAME`** 是 PowerShell 的环境变量语法（不是 `$NAME`）。
- **`%USERPROFILE%`** 是 cmd.exe 的语法，PowerShell 用 `$env:USERPROFILE`。
- **Windows 路径分隔符**：`\`，但 shell 命令里也可以用 `/`（POSIX 风格，curl.exe 支持）。
- **`python` vs `python3`**：Windows 通常只有 `python`（不是 `python3`）。SKILL.md 已适配。
