---
name: airdrop-monitor-cn
description: 空投任务与公告监控助手。监控项目公告页/文档页的内容变化，提取截止时间线索，识别高风险关键词与可疑链接，输出可执行的每日行动清单。用于把“刷空投”变成可重复的监控流程（本地运行 + 可选计费）。
---

# Airdrop Monitor CN (实战版)

## 1) 准备配置

创建监控配置（可直接复制 `config.example.json`）：

```json
{
  "projects": [
    {
      "name": "ExampleProject",
      "sources": [
        {"name": "Official Announcement", "url": "https://example.com/announcements"},
        {"name": "Docs", "url": "https://example.com/docs"}
      ]
    }
  ]
}
```

## 2) 本地运行（无计费）

```bash
cd skills/airdrop-monitor-cn
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py --config config.example.json
```

输出内容包含：
- 变化来源（哪些页面内容变了）
- 截止时间线索（自动从文本中提取）
- 风险提示（助记词/私钥/可疑链接）
- 今日 Top 动作（可直接执行）

## 3) 启用 SkillPay 计费（可选）

```bash
export SKILL_BILLING_API_KEY="sk_xxx"
export SKILL_ID="39bf8448-ceba-4764-8f73-b58ed00e4f57"
export SKILL_PRICE_USDT="0.001"   # 可选：每次调用扣费
python app.py --config config.example.json --channel discord --raw-user-id 123456
```

余额不足时返回 `payment_url`，用户充值后重试。

快速自检：

```bash
python verify_billing.py --user-id discord_123456 --amount 0.001
```

## 4) 定时执行（建议）

每 15 分钟跑一次（示例）：

```bash
*/15 * * * * cd /path/to/skills/airdrop-monitor-cn && /path/to/.venv/bin/python app.py --config config.prod.json >> monitor.log 2>&1
```

## 5) 风险边界

- 不承诺收益
- 不提供投资建议
- 不索要私钥或助记词
