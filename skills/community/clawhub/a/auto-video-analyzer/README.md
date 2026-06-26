# Auto Video Analyzer Skill

自动视频分析技能 - 一键提取视频帧并进行AI视觉分析 🔍🎬

**跨平台支持**: ✅ Windows | ✅ macOS | ✅ Linux

---

## 快速开始

### 1. 安装 FFmpeg (必需)

**Windows:**
```powershell
winget install Gyan.FFmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# CentOS/RHEL/Fedora
sudo yum install ffmpeg
```

### 2. 安装技能

```bash
# 从 ClawHub 安装
clawhub install auto-video-analyzer

# 或从 GitHub 直接安装
clawhub install shishenbaiye/auto-video-analyzer
```

### 3. 使用

```
分析视频 C:\Users\...\video.mp4
```

---

## 使用方法

当你想让我分析视频时，直接说：
```
分析视频 C:\Users\...\video.mp4
看一下这个视频：xxx.mp4，告诉我里面有什么
详细分析视频 D:\demo.mp4
Debug视频 E:\bug.mp4，角色为什么不移动
```

我会自动：
1. 检测你的操作系统 (Windows/macOS/Linux)
2. 下载对应平台的分析工具（首次使用，从 GitHub 自动拉取）
3. 智能提取关键帧
4. 分析每一帧内容
5. 给你完整报告

---

## 分析模式

| 模式 | 触发方式 | 用途 | 提取帧数 |
|------|---------|------|---------|
| **Scan** (默认) | "分析视频" | 快速了解视频整体内容 | ~8帧 |
| **Full** | "详细分析视频" | 深度分析，开头密集+中间采样 | ~16帧 |
| **Debug** | "Debug视频...问题" | 连续帧分析，用于排查问题 | 每秒2帧 |

---

## 工作流程

```
用户请求
    ↓
检测操作系统
    ↓
下载对应平台工具 (Windows: .ps1 / macOS/Linux: .sh)
    ↓
FFmpeg 提取关键帧
    ↓
AI 分析帧图片
    ↓
生成分析报告
    ↓
返回结果
```

---

## 示例

### 基础分析
```
你：分析视频 D:\recordings\gameplay.mp4
我：已提取8帧，这是三国SLG游戏，展示了战斗场景...
```

### Debug模式
```
你：Debug视频 D:\recordings\bug.mp4，为什么角色不移动
我：已提取连续帧，从第12帧开始角色位置没有变化，
    可能是动画状态机问题...
```

### 详细分析
```
你：详细分析视频 D:\recordings\demo.mp4
我：已提取16帧，完整分析UI布局、交互流程、视觉反馈...
```

---

## 项目结构

```
auto-video-analyzer/
├── SKILL.md                    # 技能定义（发布到 ClawHub）
├── README.md                   # 使用说明
└── tools/                      # 工具脚本（从 GitHub 下载）
    ├── auto-analyze-video.ps1  # Windows PowerShell 版本
    └── auto-analyze-video.sh   # macOS/Linux Bash 版本
```

---

## GitHub 仓库

- 🐙 **源码**: https://github.com/shishenbaiye/auto-video-analyzer
- 📦 **Releases**: https://github.com/shishenbaiye/auto-video-analyzer/releases
- 🐛 **Issues**: https://github.com/shishenbaiye/auto-video-analyzer/issues

---

## 注意事项

- ⚠️ 需要提前安装 FFmpeg
- 📁 视频文件会被临时复制到 `workspace/analysis/` 目录
- 🧹 分析完成后可以手动清理 `analysis/` 目录
- ⏱️ 大视频（>100MB）可能需要更长时间
- 💬 如果视频路径包含空格，不需要加引号

---

## License

MIT-0 · MIT No Attribution
