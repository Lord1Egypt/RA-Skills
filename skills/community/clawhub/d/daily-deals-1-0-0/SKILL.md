# 每日神价推送

自动聚合全网优惠，每日定时推送精简报告。

## 功能

1. **定时推送**: 每日 8:00/20:00 自动发送
2. **全网聚合**: 淘宝/京东/拼多多/什么值得买
3. **智能筛选**: 只推送真正的神价（折扣>30%）
4. **分类整理**: 数码/服饰/家居/食品
5. **利润测算**: 附带套利空间计算

## 安装

```bash
# 安装依赖
cd ~/.openclaw/skills/daily-deals-1.0.0
npm install

# 配置推送渠道（微信/钉钉/飞书）
cp config/config.example.json config/config.json
# 编辑 config.json 填写你的 webhook
```

## 使用

### 手动运行
```bash
# 生成今日神价报告
node scripts/generate-report.js

# 推送到配置好的渠道
node scripts/push-report.js
```

### 定时任务（推荐）
```bash
# 添加到 cron，每日 8:00 和 20:00 推送
0 8,20 * * * cd ~/.openclaw/skills/daily-deals-1.0.0 && node scripts/daily-push.js
```

### 自定义配置

编辑 `config/config.json`:
```json
{
  "categories": ["digital", "clothing", "home", "food"],
  "minDiscount": 0.3,
  "platforms": ["jd", "taobao", "pdd", "smzdm"],
  "pushChannels": ["wechat", "dingtalk"],
  "webhooks": {
    "wechat": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx",
    "dingtalk": "https://oapi.dingtalk.com/robot/send?access_token=xxx"
  }
}
```

## 输出示例

```
📦 每日神价日报 2026-03-24

🔥 今日 TOP10 神价

【数码】
1. iPhone 17 128G - ¥4,429（日常¥5,999）
   平台：京东 | 折扣：74折 | 省¥1,570
   套利空间：拼多多售价¥4,999，毛利¥570

2. RTX 5060Ti 8G - ¥2,899（日常¥3,699）
   平台：京东 | 折扣：78折 | 省¥800

【服饰】
3. 优衣库羽绒服 - ¥199（日常¥599）
   平台：天猫 | 折扣：33折 | 省¥400

📊 今日统计：
- 监控商品：5000+
- 神价数量：47
- 平均折扣：65折
- 最大折扣：25折

💡 套利建议：
今日数码类价差较大，建议关注 iPhone/显卡
```

## 数据来源

- 什么值得买（SMZDM）
- 京东百亿补贴
- 淘宝特价版
- 拼多多百亿补贴

## 技术栈

- Stealth Scraper（反爬虫抓取）
- Node.js
- Cron（定时任务）

## 作者

Created by OpenClaw
