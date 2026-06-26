# bilibili-transcriber

B站视频转文字摘要工具。贴个链接，自动完成下载、转录、摘要，全程本地处理。

## 功能特点

- **官方字幕优先**：自动检测B站CC字幕（含AI字幕），有字幕直接用，秒级完成
- **Whisper 本地兜底**：无字幕时自动下载音频，使用 faster-whisper 本地转录，不依赖任何外部转录服务
- **智能模型选择**：根据视频时长、内容类型、系统内存自动选择最优 whisper 模型
- **流式内存处理**：小文件直接在内存中处理，跳过磁盘 I/O
- **模型单例缓存**：首次加载后常驻内存，批量处理多个视频时只加载一次模型
- **国内模型加速**：集成 ModelScope / HF-Mirror，国内下载 whisper 模型无需翻墙
- **结构化输出**：生成带时间戳的转录文本和 Markdown 格式摘要

## 使用方式

直接告诉 AI agent 一个B站视频链接即可，例如：

```
帮我摘要这个视频 https://www.bilibili.com/video/BV1xxxxxx
```

支持的输入格式：
- 完整 URL：`https://www.bilibili.com/video/BV1xxxxxx`
- BV 号：`BV1xxxxxx`
- 短链接：`https://b23.tv/xxxxxx`

## 依赖安装

```bash
pip install faster-whisper yt-dlp
```

ffmpeg 需要单独安装：
- Windows: `winget install ffmpeg`
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

云端转写还需要：`pip install dashscope requests`

## API Key 配置（云端转写）

本技能支持两种转录方式，**无 API Key 也能用**——会自动回退到本地 faster-whisper 转录。如果你想使用速度更快、方言更准的云端转写（阿里云 Paraformer），需要配置 API Key：

**1. 申请 Key**

前往 [阿里云百炼控制台](https://bailian.console.aliyun.com/) 注册并创建 API Key（即 DashScope Key），新用户有免费额度。

**2. 设置环境变量**

Windows (PowerShell)：
```powershell
[System.Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "sk-你的key", "User")
```

Windows (CMD)：
```cmd
setx DASHSCOPE_API_KEY "sk-你的key"
```

macOS / Linux：
```bash
echo 'export DASHSCOPE_API_KEY=sk-你的key' >> ~/.bashrc
source ~/.bashrc
```

**3. 优先级**

技能会按以下顺序查找 Key：`DASHSCOPE_API_KEY` → `OPENAI_API_KEY`（兼容百炼的 OpenAI 兼容接口）。两个都没设置时，自动使用本地 faster-whisper，无需联网。

## 处理流程

```
输入URL → 解析BV号 → 获取视频信息 → 检查官方字幕
                                          ├─ 有字幕 → 直接使用 → 生成摘要
                                          └─ 无字幕 → 下载音频 → whisper转录 → 生成摘要
```

## 模型选择参考

| 模型 | 速度 | 精度 | 内存占用 | 适用场景 |
|------|------|------|----------|----------|
| tiny | 最快 | 一般 | ~400MB | 短视频、快速预览 |
| base | 快 | 较好 | ~600MB | 中等时长、日常使用 |
| small | 中等 | 好 | ~1GB | 长视频、技术内容（默认） |
| medium | 较慢 | 很好 | ~1.5GB | 专业内容、多语言混合 |
| large | 最慢 | 最佳 | ~2.5GB | 最高质量需求 |

## 许可证

MIT License
