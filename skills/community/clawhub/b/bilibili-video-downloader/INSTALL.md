# 安装指南

## 系统要求

- **操作系统**: Windows 10/11, macOS 10.15+, Ubuntu 20.04+
- **Python**: 3.8 或更高版本
- **磁盘空间**: 至少 100MB 可用空间（用于存放脚本和依赖）
- **网络**: 需要连接互联网下载视频

## 安装步骤

### 1. 安装 Python

#### Windows
```powershell
winget install Python.Python.3.12
```

或从 [Python官网](https://www.python.org/downloads/) 下载安装包

#### macOS
```bash
brew install python
```

或从 [Python官网](https://www.python.org/downloads/) 下载安装包

#### Linux
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### 2. 安装 yt-dlp

```bash
# Windows
pip install yt-dlp

# macOS / Linux
pip3 install yt-dlp
```

### 3. 安装 ffmpeg

#### Windows
```powershell
winget install Gyan.FFmpeg
```

#### macOS
```bash
brew install ffmpeg
```

#### Linux
```bash
sudo apt install ffmpeg
```

### 4. 验证安装

```bash
# 检查 Python
python --version

# 检查 yt-dlp
yt-dlp --version

# 检查 ffmpeg
ffmpeg -version
```

## 配置 Cookies（可选）

如需下载大会员专享或高清视频，配置 cookies：

### 方法 1：使用浏览器扩展

1. 安装 "Get cookies.txt" 浏览器扩展
2. 登录 Bilibili
3. 点击扩展图标，导出 cookies
4. 将文件保存为 `cookies.txt` 放在脚本目录

### 方法 2：使用 BBDown（高级）

```bash
# 安装 BBDown
# 从 https://github.com/nilaoda/BBDown/releases 下载

# 登录
BBDown login
```

## 常见问题

### Q: 提示 "yt-dlp 不是内部或外部命令"

A: Python 的 Scripts 目录未添加到 PATH。解决方法：

```powershell
# Windows - 添加到 PATH
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";" + (python -c "import site; print(site.USER_BASE)") + "\Scripts", "User")
```

### Q: 下载的视频没有声音

A: 未安装 ffmpeg 或 ffmpeg 未正确配置。请重新安装 ffmpeg 并确保其在 PATH 中。

### Q: 无法下载高清视频

A: 部分高清视频需要登录。请配置 cookies.txt 文件。

### Q: 提示 "Unable to extract"

A: B站页面结构可能已更新。尝试更新 yt-dlp：

```bash
pip install -U yt-dlp
```

## 卸载

直接删除 Skill 目录即可：

```bash
# Windows
Remove-Item -Recurse -Force "C:\Path\To\bilibili-video-downloader"

# macOS / Linux
rm -rf /path/to/bilibili-video-downloader
```

依赖（Python、yt-dlp、ffmpeg）不会自动卸载，如需卸载请单独操作。
