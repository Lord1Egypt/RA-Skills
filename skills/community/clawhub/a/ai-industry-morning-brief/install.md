# AI 早报 Skill - 快速上手指南

## 一、这是什么？

自动生成 AI 大模型领域早报，每天早上 08:12 推送，包含：
- 📰 10 条精选资讯（每条 200-300 字详细总结 + 原文链接）
- 🎧 晓晓声音语音播报（Azure TTS）

## 二、安装步骤

### 1. 解压文件
```bash
# 把压缩包放到工作区
tar -xzf ai-daily-cn-20260429.tar.gz -C /root/.openclaw/workspace/skills/
```

### 2. 安装依赖
```bash
# 安装 TTS 工具（用于生成语音播报）
pip3 install edge-tts
```

### 3. 配置定时任务（可选）
```bash
# 编辑 crontab
crontab -e

# 添加以下内容（每天 08:12 自动推送）
12 8 * * * python3 /root/.openclaw/workspace/scripts/ai_morning_report_push.py >> /root/.openclaw/workspace/logs/ai_morning_report.log 2>&1
```

## 三、使用方法

### 方法 1：自动生成（推荐）
```bash
# 运行推送脚本（生成 + 验证 + 推送）
python3 /root/.openclaw/workspace/scripts/ai_morning_report_push.py
```

### 方法 2：手动生成
```bash
# 1. 生成早报
cd /root/.openclaw/workspace/skills/ai-daily-cn
python3 scripts/ai_daily.py --date 2026-04-29

# 2. 验证质量
python3 scripts/validate_report.py 2026-04-29

# 3. 查看生成的文件
cat output/AI-Daily-2026-04-29.md
```

### 方法 3：生成语音播报
```bash
# 生成晓晓声音的语音文件
edge-tts --voice zh-CN-XiaoxiaoNeural \
  --text "这里是播报内容..." \
  --write-media /root/.openclaw/workspace/output/AI-Daily-2026-04-29.mp3
```

## 四、输出说明

### 生成的文件
- **文字版**：`/root/.openclaw/workspace/skills/ai-daily-cn/output/AI-Daily-YYYY-MM-DD.md`
- **语音版**：`/root/.openclaw/workspace/output/AI-Daily-YYYY-MM-DD.mp3`
- **日志文件**：`/root/.openclaw/workspace/logs/ai_morning_report.log`

### 早报格式标准
✅ 每条新闻 200-300 字详细总结  
✅ 每条新闻附带原文链接  
✅ 约 10 条精选资讯  
✅ 只包含中文内容  
✅ Azure 晓晓声音播报  

## 五、常见问题

### Q1: 推送失败怎么办？
**检查日志：**
```bash
tail -50 /root/.openclaw/workspace/logs/ai_morning_report.log
```

**常见错误：**
- `not logged in` → 飞书授权过期，需要重新授权
- `edge-tts not found` → 运行 `pip3 install edge-tts`
- `RSS 抓取失败` → 网络问题，稍后重试

### Q2: 如何修改信息源？
编辑配置文件：
```bash
vim /root/.openclaw/workspace/skills/ai-daily-cn/config/sources.json
```

在 `rssFeeds.media` 数组中添加或修改 RSS 源。

### Q3: 如何修改推送时间？
编辑 crontab：
```bash
crontab -e
# 修改这一行的时间
12 8 * * * python3 /root/.openclaw/workspace/scripts/ai_morning_report_push.py
```

### Q4: 如何测试效果？
```bash
# 生成今天的早报
python3 /root/.openclaw/workspace/scripts/ai_morning_report_push.py

# 查看生成的文件
cat /root/.openclaw/workspace/skills/ai-daily-cn/output/AI-Daily-$(date +%Y-%m-%d).md
```

## 六、文件清单

```
ai-daily-cn/
├── config/
│   └── sources.json              # 信息源配置（8 个公众号）
├── scripts/
│   ├── ai_daily.py               # 核心生成脚本
│   ├── validate_report.py        # 质量验证脚本
│   └── generate.sh               # 入口脚本
├── README.md                     # 技术文档
└── ITERATION_SUMMARY.md          # 迭代历史记录
```

**推送脚本（单独）：**
- `/root/.openclaw/workspace/scripts/ai_morning_report_push.py`

## 七、技术支持

**文档位置：**
- 快速上手：`INSTALL.md`（本文档）
- 技术说明：`README.md`
- 迭代历史：`ITERATION_SUMMARY.md`

**日志查询：**
```bash
# 查看最近 50 行日志
tail -50 /root/.openclaw/workspace/logs/ai_morning_report.log

# 实时查看日志
tail -f /root/.openclaw/workspace/logs/ai_morning_report.log
```

---

**最后更新**：2026-04-29  
**版本**：v1.2.0（修复总结长度和语音问题）
