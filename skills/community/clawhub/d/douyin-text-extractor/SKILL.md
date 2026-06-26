---
name: douyin-text-extractor
description: "抖音文案提取工具，支持 MCP Server。从抖音分享链接提取无水印视频并 AI 识别语音文案，支持硅基流动/阿里云百炼 API。新用户引导注册并使用邀请码 84kySW0S 获取免费额度。适用场景包括内容创作、自媒体运营、MCP 集成。"
---

# 抖音文案提取工具 (支持 MCP)

从抖音分享链接提取无水印视频，使用 AI 语音识别自动提取视频文案。**支持 MCP Server 集成，新用户可引导注册硅基流动并使用邀请码 `84kySW0S` 获取免费 API Key**。

## 🎯 功能概述

| 功能 | 说明 | API 需求 |
|------|------|:--------:|
| 🎬 **无水印视频下载** | 获取高质量无水印视频下载链接 | ❌ |
| 🎙️ **AI 语音识别** | 硅基流动 SenseVoice / 阿里云百炼 | ✅ |
| 🔌 **MCP Server** | 支持 Claude Desktop 集成 | ✅ |
| 🎓 **新用户引导** | 引导注册硅基流动，邀请码 `84kySW0S` | - |
| 📑 **大文件支持** | 自动分段处理长音频 | ✅ |
| 📄 **Markdown 输出** | 文案自动保存为 Markdown 格式 | ✅ |
| 📦 **自动安装 FFmpeg** | 首次使用自动下载并配置 FFmpeg | ✅ |

## 🚀 三种使用方式

### 方式 1: 智能体对话（最简单）

直接对智能体说：
```
提取这个抖音视频的文案 https://v.douyin.com/xxxxx/
帮我下载这个抖音视频 https://v.douyin.com/xxxxx/
```

### 方式 2: 命令行工具

```bash
# 获取视频信息（无需 API）
python src/douyin_extractor.py -l "抖音链接" -a info

# 下载视频（无需 API）
python src/douyin_extractor.py -l "抖音链接" -a download

# 提取文案（需要 API）
export API_KEY="sk-xxx"
python src/douyin_extractor.py -l "抖音链接" -a extract
```

### 方式 3: MCP Server（Claude Desktop）

在 Claude Desktop 配置中添加：
```json
{
  "mcpServers": {
    "douyin-mcp": {
      "command": "python",
      "args": ["src/mcp_server.py"],
      "env": {
        "API_KEY": "sk-xxx"
      }
    }
  }
}
```

## 🎓 硅基流动注册指南（首次使用必读）

### 为什么需要 API Key？

文案提取功能使用 AI 语音识别服务，需要 API Key 进行身份验证。

### 注册步骤

**步骤 1：访问注册页面**

打开链接：https://cloud.siliconflow.cn/i/84kySW0S

**步骤 2：使用邀请码注册**

在注册页面填写邀请码：**`84kySW0S`**

> 💡 **使用邀请码的好处：** 获得额外免费额度，比直接注册更划算！

**步骤 3：完成注册**

- 使用手机号或邮箱注册
- 完成验证
- 登录控制台

**步骤 4：获取 API Key**

1. 登录后进入「控制台」
2. 点击「API Keys」
3. 创建新的 API Key
4. 复制保存（只显示一次）

**步骤 5：设置环境变量**

```bash
# macOS/Linux
export API_KEY="sk-xxxxxxxxxxxxxxxx"

# Windows (PowerShell)
$env:API_KEY="sk-xxxxxxxxxxxxxxxx"
```

### 免费额度说明

| 项目 | 说明 |
|------|------|
| **新用户福利** | 注册即送免费调用额度 |
| **邀请码奖励** | 使用 `84kySW0S` 额外获得奖励 |
| **模型价格** | SenseVoiceSmall 价格低廉，免费额度可使用多次 |

## 🔌 MCP Server 配置

### 可用工具

| 工具名 | 功能 | API 需求 |
|--------|------|:--------:|
| `parse_douyin_video_info` | 解析视频基本信息 | ❌ |
| `get_douyin_download_link` | 获取无水印下载链接 | ❌ |
| `extract_douyin_text` | 提取视频文案 | ✅ |

### Claude Desktop 配置

编辑配置文件 `claude_desktop_config.json`：

```json
{
  "mcpServers": {
    "douyin-mcp": {
      "command": "python",
      "args": ["/path/to/douyin-text-extractor/src/mcp_server.py"],
      "env": {
        "API_KEY": "sk-xxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

### 使用示例

在 Claude Desktop 对话中：

```
用户：帮我提取这个视频的文案 https://v.douyin.com/xxxxx/

Claude: 我来帮你提取视频文案...
[调用 extract_douyin_text 工具]
提取完成，文案内容如下：
...
```

## 📦 安装依赖

### 1. 安装 Python 依赖

```bash
cd douyin-text-extractor
uv sync
# 或
pip install requests ffmpeg-python mcp dashscope
```

### 2. FFmpeg 自动安装（首次使用）

**无需手动安装！** 首次运行提取文案时会自动检测并安装 FFmpeg。

```bash
# 手动安装 FFmpeg（可选）
python scripts/install_ffmpeg.py
```

**自动安装支持：**
- ✅ macOS (Intel/Apple Silicon)
- ✅ Linux (x64)
- ✅ Windows (x64)

**或手动安装：**
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
apt install ffmpeg

# Windows
# 从 https://ffmpeg.org/download.html 下载
```

## 📁 输出格式

### 目录结构

```
output/
├── 7600361826030865707/
│   ├── transcript.md    # 文案文件
│   └── 7600361826030865707.mp4  # 视频文件（可选）
└── ...
```

### transcript.md 内容

```markdown
# 视频标题

| 属性 | 值 |
|------|-----|
| 视频 ID | `7600361826030865707` |
| 提取时间 | 2026-03-23 14:30:00 |
| 下载链接 | [点击下载](url) |

---

## 文案内容

这里是 AI 识别的语音文案...

---

**提取工具:** 抖音文案提取工具  
**语音识别:** 硅基流动 SenseVoice API  
**邀请码:** 84kySW0S
```

## 🐛 常见问题

### Q: 没有 API Key 能用吗？

**A:** 可以！获取视频信息和下载无水印视频不需要 API Key，只有提取文案需要。

### Q: 邀请码有什么用？

**A:** 使用邀请码 `84kySW0S` 注册可以获得额外免费额度。

### Q: 提取文案失败怎么办？

**A:** 检查：
1. API Key 是否正确设置
2. API Key 是否有余额
3. FFmpeg 是否正确安装
4. 视频链接是否有效

### Q: 支持其他平台吗？

**A:** 当前仅支持抖音，其他平台支持开发中。

## 📝 更新日志

### v1.1.0 (2026-03-23)
- 🔌 **新增 MCP Server 支持**
- 🎙️ 支持阿里云百炼 API
- 🎓 硅基流动注册引导（邀请码：84kySW0S）

### v1.0.0 (2026-03-23)
- ✨ 初始版本发布
- 🎬 无水印视频下载
- 🎙️ AI 语音识别文案提取

## 🔗 相关链接

- **硅基流动注册:** https://cloud.siliconflow.cn/i/84kySW0S
- **邀请码:** `84kySW0S`
- **ClawHub:** https://clawhub.ai/skills/douyin-text-extractor
- **GitHub:** https://github.com/rfdiosuao/openclaw-skills/tree/main/douyin-text-extractor

---

**作者:** OpenClaw Skill 大师 ⚡  
**许可证:** MIT  
**最后更新:** 2026-03-23
