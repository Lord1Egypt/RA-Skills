# 英语口语练习

帮助用户练习英语口语的 AI 技能。通过语音或文字与用户进行英语对话，提供即时反馈和改进建议。

## 功能

### 对话训练
- 用户发送英文语音或文字
- AI 识别内容并给出回复（语音 + 文字）
- 提供口语分析：正确表达、改进建议、补充词汇

### 每日推送（可选）
- 每天定时推送 5 条日常英语短语
- 包含翻译和用法说明
- 帮助积累日常表达

## 快速开始

### 1. 安装

将整个文件夹复制到 OpenClaw 的 skills 目录。

### 2. 配置

```bash
cd english-speaking-practice
cp config.example.json config.json
```

编辑 `config.json`，填写必要配置：

```json
{
  "user": {
    "name": "你的名字",
    "learningGoal": "日常英语口语对话"
  },
  "api": {
    "url": "https://your-api.com/v1/chat/completions",
    "apiKey": "your-api-key",
    "model": "your-model"
  },
  "push": {
    "enabled": false,
    "channel": "feishu",
    "targetUserId": "your-user-id"
  }
}
```

### 3. 启用每日推送（可选）

配置 cron 任务，每天 10:00 自动推送：

```bash
crontab -e
# 添加以下行
0 10 * * * cd /path/to/english-speaking-practice && python3 scripts/daily-english-push.py
```

## 使用方式

### 对话训练
用户发送英文语音或文字，AI 会：
1. 识别语音（语音消息）
2. 翻译并分析口语
3. 用语音回复（TTS）
4. 发送文字补充分析

### 每日推送
每天 10:00 自动收到 5 条英语短语推送。

## 数据存储

学习数据保存在 `practice-data/` 目录，按月份存储为 JSON 文件。

## 目录结构

```
english-speaking-practice/
├── SKILL.md                    # 技能说明
├── CONFIG.md                   # 配置指南
├── config.example.json         # 配置模板
├── config.json                 # 运行时配置
├── practice-data/              # 学习数据
└── scripts/
    ├── update-english-data.py  # 数据管理
    ├── daily-english-push.py   # 每日推送
    └── monthly-english-summary.sh
```

## 更多详情

- 完整技能说明：[SKILL.md](SKILL.md)
- 配置详解：[CONFIG.md](CONFIG.md)