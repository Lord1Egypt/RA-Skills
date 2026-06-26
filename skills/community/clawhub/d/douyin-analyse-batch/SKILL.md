---
name: douyin-daily-report
description: 抖音每日自动热榜日报生成与邮件推送。当用户说"抖音日报"、"发送邮件报告"、"自动分析抖音"、"定时推送抖音"或需要"生成抖音视频分析报告"时使用此技能。自动获取热榜 TOP15 → OpenClaw LLM 分析 → Word 文档输出 → 邮件定时发送至指定收件人。本技能包含完整依赖（douyin-video-analysis、douyin-hot-trend、douyin-mcp-server），安装即用。
---

# 抖音每日热榜日报

全自动抖音视频分析邮件推送系统。每天定时（08:00、16:00）获取抖音热榜 TOP15，对每个视频调用 OpenClaw 内置模型（MiniMax-M2.7）生成结构化分析笔记，输出 Word 文档并邮件推送。

## 安装即用

本 skill 已包含所有依赖，无需单独安装其他 skills。安装后运行一键部署：

```bash
bash /root/.openclaw/workspace/skills/douyin-daily-report/scripts/setup_douyin_daily_report.sh
```

该脚本自动完成：

1. 创建 Python 虚拟环境（faster-whisper / yt-dlp / python-docx / requests）
2. 生成 `.env` 环境变量文件
3. 检查 TikHub API Token
4. 设置 Cron 定时任务（每天 08:00 和 16:00）

## 环境变量配置

编辑 `.env` 文件：

```env
SMTP_USER=your_email@qq.com
SMTP_PASS=QQ邮箱SMTP授权码
SMTP_HOST=smtp.qq.com
SMTP_PORT=587
DOUYIN_EMAIL_RECIPIENTS=
DOUYIN_DIGEST_LIMIT=15
```

TikHub Token 写入 `~/.openclaw/config.json`：

```json
{"tikhub_api_token": "tk_live_xxxxxxxx"}
```

## 手动运行

```bash
# 发送邮件
bash /root/.openclaw/workspace/skills/douyin-daily-report/scripts/cron_daily_digest_wrapper.sh

# 指定条数，不发邮件（测试用）
SMTP_USER=xxx SMTP_PASS=xxx DOUYIN_EMAIL_RECIPIENTS=xxx \
/usr/bin/python3 /root/.openclaw/workspace/skills/douyin-daily-report/scripts/run_daily_digest.py \
    --limit 15 --skip-transcribe --no-email
```

## 完整链路

```
TikHub 热榜 API
    ↓ fetch_hot_total_video_list
OpenClaw LLM（MiniMax-M2.7）
    ↓ title + tags → 分析笔记
MD 文件写入
    ↓
md_to_docx.py（python-docx）
    ↓
EmailMessage（RFC 5987 编码）
    ↓ SMTP → QQ 邮箱
只发 .docx 附件
```

## 输出内容

每条视频：播放量、点赞量、作者、链接、**LLM 分析笔记**（钩子、核心主张、论据支撑、批判性分析）

## 故障排查

- **邮件显示 .bin**：已修复，使用 EmailMessage RFC 5987 编码
- **LLM 分析失败**：确认 OpenClaw Gateway 运行中
- **TikHub 失败**：确认 `~/.openclaw/config.json` 中 `tikhub_api_token` 正确
- **日报少于15条**：TikHub 免费热榜每日返回数据量不固定

## 文件结构

```
douyin-daily-report/
├── SKILL.md
├── .env                              ← 环境变量（setup 脚本生成）
├── scripts/
│   ├── setup_douyin_daily_report.sh  ← 一键安装（含 venv + Cron）
│   ├── cron_daily_digest_wrapper.sh  ← Cron 入口
│   ├── run_daily_digest.py           ← 核心流水线
│   └── helpers/
│       ├── send_email.py              ← 邮件发送
│       └── md_to_docx.py             ← MD→Word
└── dependencies/                      ← 完整依赖 skills
    ├── douyin-video-analysis/
    ├── douyin-hot-trend/
    └── douyin-mcp-server/
```

## 卸载

```bash
# 删除 Cron
crontab -l | grep -v "douyin_daily_digest" | crontab -

# 删除虚拟环境和输出
rm -rf /tmp/douyin_transcribe
rm -rf ~/Documents/douyin_analysis

# 删除 skill 目录
rm -rf /root/.openclaw/workspace/skills/douyin-daily-report
```
