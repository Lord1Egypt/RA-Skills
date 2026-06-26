---
name: auto-video-analyzer
description: "自动分析视频内容，提取关键帧进行AI视觉分析。支持 Windows、macOS 和 Linux。首次使用自动从GitHub下载对应平台的工具脚本。"
metadata:
  version: "1.0.0"
  author: "shishenbaiye"
  requires:
    - ffmpeg
  platforms:
    - windows
    - macos
    - linux
---

# Auto Video Analyzer

自动分析视频内容，提取关键帧进行AI视觉分析。

## 触发条件

当用户消息包含以下模式时自动调用：

| 模式 | 关键词 | 示例 |
|------|--------|------|
| Scan | "分析视频", "看一下视频", "说说视频内容" | "分析视频 C:\\video.mp4" |
| Full | "详细分析视频", "深度分析视频" | "详细分析视频 D:\\demo.mp4" |
| Debug | "Debug视频", "排查视频", "视频问题" | "Debug视频，为什么角色不动" |

## 工作原理

1. **检查/下载工具脚本** - 首次使用自动从 GitHub 拉取对应平台版本
2. **提取视频关键帧** - 使用 FFmpeg 智能采样
3. **AI 视觉分析** - 分析帧图片内容
4. **生成分析报告** - 输出结构化分析结果

## 使用方式

### 前提条件

**安装 FFmpeg** (必需):

**Windows:**
```powershell
winget install Gyan.FFmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install ffmpeg
```

**Linux (CentOS/RHEL):**
```bash
sudo yum install ffmpeg
```

### 自动工作流

当用户说：
> "分析一下 /Users/xxx/Videos/demo.mp4"

AI 自动执行：
1. 检测操作系统类型
2. 检查对应平台的工具脚本是否存在
3. 不存在则从 GitHub 下载
   - Windows: `auto-analyze-video.ps1`
   - macOS/Linux: `auto-analyze-video.sh`
4. 执行脚本提取视频帧
5. 分析帧图片内容
6. 返回分析报告

## 技术依赖

- **FFmpeg**: 视频信息读取和帧提取
- **PowerShell** (Windows) 或 **Bash** (macOS/Linux)
- **AI Vision**: 图像分析能力

## 工具下载

脚本托管于 GitHub:
- 仓库: https://github.com/shishenbaiye/auto-video-analyzer
- 工具目录: https://github.com/shishenbaiye/auto-video-analyzer/tree/main/tools

包含：
- `auto-analyze-video.ps1` - Windows PowerShell 版本
- `auto-analyze-video.sh` - macOS/Linux Bash 版本

首次使用时 AI 会自动检测平台并下载对应版本。

## 平台自动检测逻辑

AI 助手首次使用时执行以下逻辑：

```powershell
# 展开路径
$toolsDir = $executionContext.InvokeCommand.ExpandString("$env:USERPROFILE/.openclaw/workspace/tools")

# 检测平台
$isWindows = $IsWindows -or ($env:OS -eq "Windows_NT") -or ($PSVersionTable.Platform -eq "Win32NT")

if ($isWindows) {
    $scriptName = "auto-analyze-video.ps1"
    $scriptPath = Join-Path $toolsDir $scriptName
} else {
    $scriptName = "auto-analyze-video.sh"
    $scriptPath = Join-Path $toolsDir $scriptName
}

$scriptUrl = "https://raw.githubusercontent.com/shishenbaiye/auto-video-analyzer/main/tools/$scriptName"

# 检查并下载
if (-not (Test-Path $scriptPath)) {
    New-Item -ItemType Directory -Force -Path $toolsDir | Out-Null
    Invoke-WebRequest -Uri $scriptUrl -OutFile $scriptPath -UseBasicParsing
    
    # Linux/macOS 需要添加执行权限
    if (-not $isWindows) {
        chmod +x $scriptPath
    }
    
    Write-Host "✅ 工具已下载: $scriptPath"
}
```

## 安装本技能

```bash
# 从 ClawHub 安装
clawhub install auto-video-analyzer

# 或从 GitHub 直接安装
clawhub install shishenbaiye/auto-video-analyzer
```

## 更新日志

### v1.0.0
- 基础视频分析功能
- 支持 Windows PowerShell 版本
- 支持 macOS/Linux Bash 版本
- 自动检测平台并下载对应工具
