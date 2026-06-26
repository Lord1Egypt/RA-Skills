# FB Ads Copywriter Pro

**Facebook 廣告文案專家 - 生成 6 個高轉化率廣告版本，包含 A/B 測試建議和受眾分析**

## 🚀 快速開始

### 安裝

```bash
# 使用 ClawHub 安裝
clawhub install fb-ads-copywriter-pro

# 或手動安裝
git clone https://github.com/vic-ai/fb-ads-copywriter-pro.git
cd fb-ads-copywriter-pro
pip install -r requirements.txt
```

### 配置

```bash
# 設置環境變量
export GLM_API_KEY="your-glm-api-key"
export RESEND_API_KEY="your-resend-api-key"  # 可選
export TELEGRAM_BOT_TOKEN="your-telegram-token"  # 可選
export TELEGRAM_CHAT_ID="your-chat-id"  # 可選
```

### 使用

```bash
# 生成廣告文案
python scripts/copy-generator.py generate \
  --product "維 C 亮白精華素" \
  --audience "25-45 歲女性" \
  --budget "5000-8000 HKD/月"

# 使用問卷數據
python scripts/copy-generator.py generate \
  --questionnaire memory/questionnaire-sub_123456.md

# 發送通知
python scripts/copy-generator.py send \
  --email client@example.com \
  --telegram
```

## 📋 功能特點

- ✅ 6 個廣告風格生成（FOMO/社交證明/權威/痛點/促銷/故事）
- ✅ A/B 測試建議（3 個測試組合）
- ✅ 目標受眾分析（3 個細分群組）
- ✅ 投放策略建議（預算分配 + KPI 目標）
- ✅ 粵語口語化創作
- ✅ 符合 Facebook 廣告政策
- ✅ Email 交付功能
- ✅ Telegram 通知功能

## 📚 文檔

詳細使用說明請查看 [SKILL.md](SKILL.md)

## 💰 定價

| 版本 | 價格 | 功能 |
|------|------|------|
| 基礎版 | $29 | 6 個廣告版本，基礎 A/B 測試 |
| 專業版 | $99 | 無限生成，進階 A/B 測試，受眾分析 |
| 企業版 | $299 | 定制語氣，批量生成，API 訪問 |

## 📞 支持

- Email: support@vic-ai.com
- Telegram: @vicaimonitor_bot
- 網站：https://platform-cyan-zeta.vercel.app

## 📜 許可證

MIT License
