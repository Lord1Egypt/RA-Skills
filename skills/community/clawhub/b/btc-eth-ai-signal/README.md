# 🤖 BTC/ETH AI Trader

AI 驱动的加密货币交易分析系统。自动分析 BTC 和 ETH 行情，基于技术指标生成开仓建议，推送至飞书 / Telegram / Discord / 企业微信。

**数据源：** CoinEx API（国内直连，无需翻墙）

---

## 功能

- BTC/ETH 实时行情（价格、涨跌、24h区间）
- AI 技术分析：RSI / MACD / MA / 布林带 / ATR / 成交量
- 开仓建议：入场区间、目标价、止损位、盈亏比
- 多平台推送：飞书 / Telegram / Discord / 企业微信
- 每30分钟自动推送分析报告

## 安装

编辑 config.json，按需配置推送渠道：

**飞书：** 飞书开放平台创建应用 → App ID / Secret → 发布后获取 OpenID
**Telegram：** 注册 BotFather 创建 Bot → 获取 token 和 chat_id
**Discord：** 频道设置→ 整合 → Webhook → 复制 URL
**企业微信：** 群聊 → 添加机器人 → 复制 Webhook URL

只配其中一个也行，其他留空即可。

## 使用

```bash
python3 scripts/advise.py    # 查看分析报告
python3 scripts/push.py      # 推送到已配置的平台

# 定时推送
*/30 * * * * cd /path/to && PYTHONPATH=. python3 scripts/push.py
```

## 风险提示

本系统仅供分析参考，不构成投资建议。
