---
name: bilibili-hot-daily
description: "🔥 每日自动抓取哔哩哔哩热门视频排行榜，支持AI摘要生成和多渠道推送。自媒体运营必备！免费使用，定制开发请联系作者。"
homepage: https://github.com/openclaw/bilibili-hot-daily
metadata:
  {
    "openclaw":
      {
        "emoji": "🔥",
        "requires": { "bins": ["python3"] },
      },
  }
---

# 🔥 B站热点日报 v2.1

每日自动抓取B站热门视频排行榜，支持AI摘要和多渠道推送。

## ✨ v2.1 新功能

- ✅ 优化API调用稳定性
- ✅ 改善数据展示格式
- ✅ 增强错误处理

## 📦 安装

```bash
npx clawhub@latest install bilibili-hot-daily
```

## 🚀 使用

```bash
# 获取今日热门 Top 10
python3 fetch_hot.py --top 10

# 生成摘要
python3 fetch_hot.py --top 20 --summary

# 导出JSON
python3 fetch_hot.py --output hot.json

# 导出CSV
python3 fetch_hot.py --output hot.csv --format csv
```

## 📊 输出示例

```
#1 视频标题
   UP主: xxx | 分区: xxx | 时长: 2分43秒
   播放: 343.5万 | 点赞: 12.0万 | 投币: 3447 | 收藏: 1.3万
   简介: 视频简介预览...
   链接: https://b23.tv/xxx
```

## 💰 定制服务

**免费使用本技能，如需以下服务请联系作者：**

- 🔧 定制开发：根据你的需求定制数据抓取方案
- 📊 数据分析：深度分析B站热门趋势
- 🤖 自动化部署：帮你搭建完整的数据监控系统
- 📱 多平台集成：对接微信/钉钉/飞书等平台

**联系方式：**
- 📱 QQ：2595075878
- 📧 邮箱：2595075878@qq.com

## ⚖️ 免责声明

本技能所获取的数据来自B站公开API，仅用于个人学习和技术研究目的。

- 📌 **数据来源**：哔哩哔哩公开API接口
- 📌 **非商业性质**：本技能为开源免费工具，不涉及任何商业引导
- 📌 **版权说明**：所有数据内容的版权归哔哩哔哩所有
- 📌 **使用限制**：请遵守B站用户协议，禁止用于非法用途
- 📌 **免责条款**：本技能按"现状"提供，使用者需自行承担使用风险

## 📄 许可证

MIT License
