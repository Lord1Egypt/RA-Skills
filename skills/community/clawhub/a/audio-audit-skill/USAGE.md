# 音频内容审核 - 使用指南

## 快速开始

### 1. 环境准备

```bash
# Python 依赖
pip install requests

# 系统依赖
sudo apt install ffmpeg    # 视频音频提取

# 配置环境变量（添加到 ~/.bashrc 或 ~/.zshrc）
export SENSEAUDIO_API_KEY="你的 SenseAudio API 密钥"

source ~/.bashrc
```

> SenseAudio API 密钥在 https://senseaudio.cn 注册后获取。

### 2. 在 Claude Code 中使用

Skill 安装完成后，直接用自然语言对话即可：

**基础审核：**
```
帮我审核一下 ~/audio/podcast_ep01.mp3 有没有敏感内容
```

**深度审核（Claude 语义分析）：**
```
对 ~/videos/livestream.mp4 做深度内容审核
```

**批量审核：**
```
帮我审核 ~/media/ 目录下所有音视频文件
```

**自定义敏感词：**
```
检查 ~/audio/ad.mp3 里有没有虚假宣传，额外关注"包治百病,无效退款,秒杀全网"这些词
```

**多人场景定位：**
```
审核 ~/meeting.mp4，区分不同说话人，看谁说了不该说的
```

Claude 会自动运行脚本进行 ASR 转写和敏感词扫描，然后直接读取转写文本进行深度语义审核。

### 3. 手动命令行使用

```bash
# 基础审核（敏感词扫描）
python scripts/audio_audit.py ~/audio/podcast.mp3

# 说话人分离 + 情感分析
python scripts/audio_audit.py ~/meeting.mp4 --speaker --sentiment

# 自定义敏感词
python scripts/audio_audit.py ~/audio/ad.mp3 --keywords "包治百病,无效退款,限时秒杀"

# 批量审核目录下所有音视频
python scripts/audio_audit.py ~/media_folder/

# 指定输出目录
python scripts/audio_audit.py ~/videos/livestream.mp4 \
  --speaker \
  --sentiment \
  --keywords "自定义词1,自定义词2" \
  --model pro \
  --output ~/audit_reports/
```

## 审核能力说明

### 敏感词扫描（脚本自动完成）

内置多类别敏感词库，覆盖：政治敏感、暴力血腥、色情低俗、赌博诈骗、毒品相关、违禁广告。

也可通过 `--keywords` 添加自定义敏感词。

### 深度语义审核（Claude 完成）

脚本输出转写文本后，Claude 直接分析，可识别：
- 隐晦的擦边球内容
- 阴阳怪气/反讽表达
- 虚假宣传/夸大其词
- 隐私信息泄露
- 上下文组合后的违规含义

### 情感分析（`--sentiment`）

通过 ASR 情感识别检测异常情绪片段（如愤怒、恐惧），适用于客服质检、直播监控等场景。

## 输出文件

| 文件 | 说明 |
|------|------|
| `文件名_audit.json` | 结构化审核报告（JSON） |
| `文件名_audit.txt` | 人类可读的审核摘要 |
| `文件名_transcript.txt` | 完整语音转写文本 |

### 风险等级

| 等级 | 含义 | 建议 |
|------|------|------|
| `safe` | 安全 | 无需处理 |
| `low` | 低风险 | 建议人工复核 |
| `medium` | 中风险 | 需要人工审核 |
| `high` | 高风险 | 建议立即处理 |

## 常见问题

**Q: 报错 `积分不足`**
A: SenseAudio API 积分用完了，到 https://senseaudio.cn 充值或等待每日免费额度刷新。

**Q: 敏感词误报太多**
A: 敏感词扫描是粗粒度检测，让 Claude 分析转写文本可进行语义判断减少误报。

**Q: 想审核视频但不想处理语音？**
A: 本工具专门做语音内容审核。如需审核视频画面，需配合其他视觉审核工具。

**Q: 报错 `ffmpeg: command not found`**
A: 安装 ffmpeg：`sudo apt install ffmpeg`
