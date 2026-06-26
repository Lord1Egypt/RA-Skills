# 🎬 B站视频转录专家

**专业处理B站视频字幕问题，支持语音转文字、字幕下载、内容分析、热门评论获取**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.1.0-brightgreen)]()

## ✨ 特性

### 🎯 核心功能
- **智能字幕处理**：自动按优先级获取（CC 字幕 → AI 字幕 → 音频转录 → 视频下载）
- **语音转文字**：使用 Whisper / Vosk 模型进行高精度语音识别
- **💬 热门评论获取**：自动提取视频评论区精华信息
- **Cookie 安全存储**：多路径冗余存储 + immutable 写保护
- **扫码登录**：支持 B 站扫码登录，自动管理 Cookie
- **国内镜像支持**：自动使用国内镜像源，解决网络问题
- **批量处理**：支持批量处理多个 B 站视频

### 🆕 v2.1.0 新增
- **热门评论获取**：自动获取按点赞排序的热门评论及回复
- **评论输出**：Markdown/JSON 格式均包含评论区信息
- **非关键路径**：评论获取失败不影响主流程

## 🚀 快速开始

### 安装

```bash
# 1. 从 ClawHub 安装（推荐）
clawhub install bilibili-video-transcriber

# 2. 或从 GitHub 克隆
git clone https://github.com/adolescen-he/bilibili-video-transcriber.git
cd bilibili-video-transcriber
pip install -r requirements.txt
```

### 扫码登录（推荐）

```bash
# 扫码登录，自动保存 Cookie
bilibili-transcribe --login
```

### 基本使用

```bash
# 处理单个视频（自动获取字幕 + 评论）
bilibili-transcribe BV1txQGByERW

# 指定 Cookie 文件
bilibili-transcribe BV1txQGByERW --cookie ~/.bilibili_cookie.txt

# 批量处理
bilibili-transcribe --batch bv_list.txt
```

## 📖 详细文档

### 命令行参数

```bash
# 查看完整帮助
bilibili-transcribe --help

# 处理视频
bilibili-transcribe <BV号> [选项]

# 常用选项
--model <base|small|medium>    # 选择模型（默认: base）
--format <txt|json|markdown>   # 输出格式（默认: txt）
--output <目录>                # 输出目录（默认: ./bilibili_transcripts）
--keep-audio                   # 保留音频文件
--verbose                      # 详细输出
--debug                        # 调试模式
```

### Python API

```python
from bilibili_transcriber import BilibiliTranscriber

# 初始化
transcriber = BilibiliTranscriber()

# 处理视频（自动获取字幕 + 热门评论）
result = transcriber.process(bvid="BV1txQGByERW")

if result.success:
    print(f"✅ 处理成功: {result.video_info.title}")
    print(f"📄 转录文件: {result.transcript_path}")
    
    # 评论信息
    if result.comments:
        for c in result.comments[:3]:
            print(f"💬 [{c.user}] {c.message[:60]}")
```

## 💬 评论获取功能详解

处理视频时自动获取**按点赞排序的热门评论**：

### 特性
- 最多获取 30 条热评
- 每条热评可获取 3 条回复
- 按点赞数排序（B 站 `OrderType.LIKE`）
- 非关键路径，获取失败不影响主流程

### 输出示例

**Markdown 格式：**
```markdown
## 💬 热门评论

### 👍 5 · 磊哥聊AI
实现步骤：
1.升级爱马仕：hermes update
2.打开控制台：hermes dashboard
3.打开网关：hermes gateway

### 👍 2 · 章鱼柔
这更像是一个后台管理系统，不是用户的使用界面
```

**CLI 输出：**
```
💬 评论: 获取 5 条热评 + 2 条回复
热门评论（前3条）:
  👍5 [磊哥聊AI] 实现步骤：1.升级爱马仕：hermes update 2.打开控制台...
  👍2 [章鱼柔] 这更像是一个后台管理系统
```

## 🔧 Cookie 安全机制

```
存储路径（3重冗余）:
  1. 技能目录: .bilibili_cookie ← immutable 保护
  2. 用户目录: ~/.bilibili_cookie_storage
  3. 配置目录: ~/.config/bilibili_transcriber/cookie

运行引用: ~/.bilibili_cookie.txt（600权限）

失效时: → 自动检测 → 生成二维码 → 通过飞书发送 → 用户扫码 → 自动保存
```

## 📊 智能处理优先级

```
【步骤 1】获取 CC 字幕（1-3 秒）✅ 有字幕直接完成
    ↓ 失败
【步骤 2】获取 AI 字幕（1-3 秒）✅ 有 AI 字幕直接完成
    ↓ 失败
【步骤 3】下载音频并转录（30-120 秒）✅ 无需下载视频
    ↓ 失败
【步骤 4】下载视频并提取音频（60-300 秒）✅ 最后选择

额外：获取热门评论（1-3 秒）💬 自动进行，不影响主流程
```

## ⚙️ 配置

配置文件位置：`~/.config/bilibili_transcriber/config.yaml`

```yaml
# Cookie 配置
cookie:
  auto_refresh: true
  refresh_interval: 86400  # 24 小时
  redundant_storage: true   # 启用冗余存储

# 模型配置
model:
  engine: "whisper"    # whisper / vosk
  device: null         # 自动选择

# 评论配置（v2.1.0 新增）
comment:
  enabled: true          # 是否获取评论
  max_count: 30          # 最多获取多少条热评
  max_replies: 3         # 每条热评最多获取多少条回复
```

## 📊 输出格式

### Markdown 格式（推荐）
包含评论区信息、视频信息、全部转录内容。

### JSON 格式
包含 `video_info`、`transcript`、`comments` 数组、`metadata`。

### 文本格式
纯时间戳 + 文本，适合进一步处理。

## 🔍 故障排除

### Cookie 相关问题
```bash
# 检查 Cookie 状态
bilibili-transcribe --check-cookie

# 扫码登录
bilibili-transcribe --login
```

### 评论获取失败
评论获取是非关键步骤，不影响字幕处理。常见原因：
- 视频评论被关闭
- 网络问题
- API 限流

## 🏗️ 项目结构

```
bilibili-video-transcriber/
├── bilibili_transcriber.py    # 核心处理模块（字幕 + 评论）
├── cookie_manager.py          # Cookie 安全存储管理
├── cli.py                     # 命令行接口
├── config.yaml                # 配置文件
├── setup.py                   # 安装脚本
├── requirements.txt           # 依赖列表
├── README.md                  # 说明文档
├── SKILL.md                   # 技能文档
├── package.json               # 包配置
└── examples/                  # 示例文件
```

## 📄 许可证

MIT License

## 🙏 致谢

- [bilibili-api](https://github.com/Nemo2011/bilibili-api) - B 站 API 封装
- [faster-whisper](https://github.com/guillaumekln/faster-whisper) - 快速 Whisper 实现
- [Vosk](https://github.com/alphacep/vosk-api) - 离线语音识别
- [OpenAI Whisper](https://github.com/openai/whisper) - 语音识别模型

## 📞 支持

- **GitHub Issues**: https://github.com/adolescen-he/bilibili-video-transcriber/issues
- **ClawHub**: https://clawhub.ai/skills/bilibili-video-transcriber

---

**基于实际经验开发，专门解决 B 站字幕系统各种问题，稳定可靠！** 🎬💬
