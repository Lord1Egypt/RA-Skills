---
name: douyin-transcribe-fast
description: |
  抖音视频快速转文字（优化版）。用户发抖音链接，自动提取文案。
  特点：本地 Whisper 转录，无需 API Key，零成本，高隐私。
  触发词：抖音、转文字、提取文案、视频转录
---

# 抖音视频快速转文字（优化版）🎬➡️📝

本地 Whisper 转录，无需 API Key，零成本，高隐私。

---

## 前置依赖检查

使用前确保以下工具已安装：

### 1. Python 3.8+
```bash
python --version
```

### 2. FFmpeg（音频处理）
```bash
ffmpeg -version
```
未安装？Windows: `winget install Gyan.FFmpeg`

### 3. OpenAI Whisper（本地转录）
```bash
pip install openai-whisper
```

---

## 使用方式

### 方式 1：抖音链接

用户发送抖音链接，如：
> 2.89 03/17 zTl:/ n@d.nq 真正赚钱的人到底怎么用 AI？ https://v.douyin.com/D4SVbwCEY6g/

**执行步骤：**

#### 步骤 1：解析视频信息
使用 douyin-mcp 获取视频下载链接：
```bash
mcporter call douyin-mcp.parse_douyin_video_info share_link="<抖音链接>"
```

#### 步骤 2：下载视频（仅音频流）
```bash
ffmpeg -i "<视频URL>" -vn -acodec pcm_s16le -ar 16000 -ac 1 "audio.wav" -y
```

#### 步骤 3：本地 Whisper 转录
```bash
whisper "audio.wav" --model tiny --language Chinese --output_format txt
```

> 💡 **优化提示**：
> - 使用 `tiny` 模型最快（适合短视频）
> - 使用 `base` 模型平衡速度和质量
> - 使用 `small` 模型质量最好（适合长视频）

#### 步骤 4：返回结果
读取生成的 txt 文件，返回给用户。

---

### 方式 2：本地视频文件

用户发送视频文件，直接执行步骤 3-4。

---

## 优化策略

### 🚀 速度优化

| 策略 | 效果 | 适用场景 |
|------|------|----------|
| 只下载音频流 | 减少 90% 下载时间 | 所有视频 |
| 使用 tiny 模型 | CPU 转录 1-2 分钟 | 短视频 (<3分钟) |
| 使用 base 模型 | CPU 转录 3-5 分钟 | 中等视频 (3-10分钟) |
| 跳过视频下载 | 直接提取音频 URL | 网页版抖音 |

### 💰 成本优化

- **零 API 费用**：本地 Whisper 完全免费
- **零网络依赖**：不需要 Groq/OpenAI API
- **隐私保护**：视频/音频不离开本地机器

### 🛡️ 稳定性优化

- **不依赖浏览器**：避免抖音反爬和登录问题
- **不依赖第三方 API**：避免 API 限制和费用
- **离线可用**：安装后无需网络即可转录

---

## 完整工作流程

```
用户发送抖音链接
    ↓
提取 modal_id / 视频 URL（通过 douyin-mcp）
    ↓
下载音频流（ffmpeg，~1-5MB）
    ↓
本地 Whisper 转录（tiny/base/small 模型）
    ↓
返回中文文案
```

**总耗时**：
- 短视频（<3分钟）：2-3 分钟
- 中等视频（3-10分钟）：5-8 分钟
- 长视频（>10分钟）：10-15 分钟

---

## 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| douyin-mcp 返回 403 | API Key 无效 | 检查 `~/.cursor/mcp.json` 配置 |
| ffmpeg 未找到 | 未安装或不在 PATH | 安装 ffmpeg 并添加到环境变量 |
| whisper 未找到 | 未安装 | 运行 `pip install openai-whisper` |
| 转录质量差 | 模型太小或音频不清 | 改用 base/small 模型 |
| 转录速度慢 | CPU 性能不足 | 使用 tiny 模型或升级硬件 |

---

## 模型选择建议

| 模型 | 速度 | 质量 | 显存/内存 | 推荐场景 |
|------|------|------|-----------|----------|
| tiny | ⚡ 最快 | ⭐⭐ | ~1GB | 短视频、快速预览 |
| base | 🚀 快 | ⭐⭐⭐ | ~1GB | 日常使用 |
| small | 🚗 中等 | ⭐⭐⭐⭐ | ~2GB | 高质量需求 |
| medium | 🐢 慢 | ⭐⭐⭐⭐⭐ | ~5GB | 专业用途 |

---

## 配置示例

### Windows PowerShell 环境变量
```powershell
$env:PATH = "C:\Users\<用户名>\AppData\Local\Programs\Python\Python311\Scripts;" +
            "C:\ffmpeg\bin;" +
            $env:PATH
```

### 快速转录命令
```powershell
# 下载音频
ffmpeg -i "<视频URL>" -vn -acodec pcm_s16le -ar 16000 -ac 1 "audio.wav" -y

# 转录（tiny 模型，最快）
whisper "audio.wav" --model tiny --language Chinese --output_format txt

# 转录（base 模型，平衡）
whisper "audio.wav" --model base --language Chinese --output_format txt
```

---

## 与原版 skill 对比

| 特性 | douyin-transcribe | douyin-transcribe-fast（本版） |
|------|-------------------|-------------------------------|
| 依赖 | Groq API Key | 无需 API Key |
| 费用 | 免费（Groq） | 完全免费 |
| 隐私 | 音频上传到 Groq | 完全本地 |
| 速度 | 3-5 秒 | 2-15 分钟（取决于视频长度） |
| 网络要求 | 需要网络 | 安装后离线可用 |
| 准确度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐（small模型） |
| 适用场景 | 快速转录、大量视频 | 隐私敏感、离线环境、零成本 |

---

## 最佳实践

1. **短视频（<3分钟）**：直接用 tiny 模型，2分钟出结果
2. **中等视频（3-10分钟）**：用 base 模型，平衡速度和质量
3. **长视频（>10分钟）**：用 small 模型，或分段处理
4. **批量处理**：先下载所有音频，再批量转录
5. **质量优先**：对重要视频使用 small 模型，日常用 base

---

## 技术栈

- **douyin-mcp**：获取视频信息
- **ffmpeg**：音频提取和处理
- **OpenAI Whisper**：本地语音识别
- **Python**：运行环境

---

*优化版 Skill，让抖音文案提取更简单、更私密、更经济。*
