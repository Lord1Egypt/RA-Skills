# 用户画像

将画像保存到当前工作目录的 `.arti-opportunity-radar/profile.json`。先告知用户并取得确认。不要保存到 Skill 目录。

## Schema

```json
{
  "version": 1,
  "locale": "zh-CN",
  "timezone": "Asia/Shanghai",
  "markets": ["CN", "HK", "US"],
  "holdings": [
    {
      "symbol": "NASDAQ:NVDA",
      "name": "英伟达",
      "position_weight": null
    }
  ],
  "watchlist": [
    {
      "symbol": "HKEX:00700",
      "name": "腾讯控股"
    }
  ],
  "themes": ["AI 基础设施", "半导体"],
  "portfolio_source": {
    "type": "manual",
    "connector": null,
    "last_synced_at": null
  },
  "sources": {
    "discovery": ["readhub", "aihot", "poche"],
    "custom": [],
    "verification": ["official_filings", "company_ir"]
  },
  "reports": {
    "morning_enabled": false,
    "evening_enabled": false,
    "max_items": 10
  },
  "updated_at": "2026-07-23T00:00:00+08:00"
}
```

## 规则

- 使用带交易所的规范代码，避免 `0005`、`5.HK` 等歧义。
- 港股统一为五位数字，例如 `HKEX:00700`。
- A 股使用 `SSE:600519` 或 `SZSE:000001`。
- 美股优先使用 `NASDAQ:NVDA`、`NYSE:BABA` 等交易所代码。
- 公司同时在多个市场上市时保留候选项并向用户确认，例如台积电 `TWSE:2330` 与 `NYSE:TSM`；确认前不要写入画像。
- `holdings` 与 `watchlist` 不重复；持仓优先。
- `position_weight` 默认 `null`，不主动询问。
- `verification` 至少保留 `official_filings` 和 `company_ir`。
- 修改时保留用户未要求变更的字段，并更新 `updated_at`。
- 腾讯自选股只在连接器已存在且用户授权后同步；不要保存登录凭证。
