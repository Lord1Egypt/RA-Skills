# 每日神价推送 v2.0

双数据源版本：什么值得买 + 识货网

## 数据源

| 数据源 | 优势 | 数据类型 |
|--------|------|----------|
| **什么值得买** | 京东/拼多多/天猫聚合 | 平台优惠价 |
| **识货网** | 品牌正品 + 付款人数 | 价格热度参考 |

## 使用流程

### 1. 抓取数据

```bash
# 抓取什么值得买
browser(action="open", targetUrl="https://faxian.smzdm.com/h3s183t0f0c0p1/")
browser(action="snapshot", refs="aria")
# 保存 snapshot 到 assets/smzdm-snapshot.txt

# 抓取识货网
browser(action="open", targetUrl="https://www.shihuo.cn/")
browser(action="snapshot", refs="aria")
# 保存 snapshot 到 assets/shihuo-snapshot.txt
```

### 2. 生成并推送

```bash
cd ~/.openclaw/skills/daily-deals-1.0.0
node scripts/daily-push.js
```

### 3. 定时任务（推荐）

```bash
crontab -e
# 每日 8:00 和 20:00 推送
0 8,20 * * * /home/gaof/.openclaw/workspace/skills/daily-push-cron.sh
```

## 输出示例

```
🔥 每日神价日报 2026-03-26 星期四

📊 数据来源：什么值得买 + 识货网

【什么值得买】📦
1. 酷态科 10 号电能棒 10000 毫安 120W 快充
   💰 119 元 | 🛒 拼多多
   🔗 https://www.smzdm.com/p/170981835/

【识货网】👟
1. 苹果 iPhone17 Pro Max 5G 手机
   💰 ¥9399 | 🏷️ 1.72w 人付款
   🔗 https://www.shihuo.cn/page/pcGoodsDetail?goodsId=7929864

📊 今日统计：
- 什么值得买：5 个
- 识货网：10 个
- 总计：15 个神价
```

## 文件结构

```
daily-deals-1.0.0/
├── scripts/
│   ├── daily-push.js       # 主程序（双数据源）
│   ├── generate-report.js  # 报告生成器
│   ├── push-report.js      # 推送程序
│   └── parse-smzdm.py      # 什么值得买解析器
├── assets/
│   ├── smzdm-snapshot.txt  # 什么值得买 snapshot
│   ├── shihuo-snapshot.txt # 识货网 snapshot
│   └── daily-report.txt    # 生成的报告
└── config/
    └── config.json         # 配置文件
```

## 注意事项

1. **snapshot 文件**：需要先通过 browser 工具抓取并保存
2. **飞书配置**：在 config.json 中填写 appId/appSecret/receiveId
3. **数据更新**：建议每次推送前重新抓取 snapshot

## 作者

Created by OpenClaw
