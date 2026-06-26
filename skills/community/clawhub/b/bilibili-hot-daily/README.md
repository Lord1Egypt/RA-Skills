# 🔥 B站热点日报 - Bilibili Hot Daily

> 自动抓取哔哩哔哩热门视频排行榜，支持AI摘要生成和多渠道推送

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ClawHub](https://img.shields.io/badge/ClawHub-Available-brightgreen)](https://clawhub.ai)

## ✨ 功能特性

- 📊 自动抓取 B站热门视频 Top 20
- 🤖 AI 智能分类摘要（科技/娱乐/生活/游戏等）
- 📱 多渠道推送（Telegram/微信/邮件）
- ⏰ 定时执行（每日自动更新）
- 📈 数据统计（播放量/点赞/投币/收藏）

## 🚀 快速开始

### 安装

```bash
npx clawhub@latest install bilibili-hot-daily
```

### 使用

```bash
# 获取今日热门 Top 10
python3 fetch_hot.py --top 10

# 获取完整 Top 20
python3 fetch_hot.py --top 20

# 生成摘要并导出
python3 fetch_hot.py --summary --output hot.json
```

## 📊 输出示例

```
#1 脑袋要坏掉惹:p
   👤 樱庭芥子 | 📂 宅舞
   👁 512.3万 | 👍 60.7万 | 🪙 16.3万 | ⭐ 27.8万
   🔗 https://b23.tv/BV1fYQSBeE8f
```

## 💰 定价

- **免费版**：每日 Top 10，基础数据
- **Pro版（49元）**：Top 20 + AI摘要 + 多渠道推送

## 📄 许可证

MIT License - 小天🦞
