---
name: brave-loggedin-tag-browsing
description: |
  使用 Brave 瀏覽器（已登入狀態）瀏覽 X/Twitter、Facebook 用戶頁面並提取最新帖子。
  自動化社交媒體監控，支援登入狀態檢查、帖子提取、互動數據抓取。
version: "2.0.0"
author: Shuttle AI
tags: ["browser", "social-media", "x", "twitter", "facebook", "brave", "logged-in", "multi-platform"]
mode: subagent
triggers:
  - browse social media
  - view x tweets
  - view facebook posts
  - check social media
---

# brave-loggedin-tag-browsing

**自動化瀏覽器技能 - 使用已登入的 Brave 瀏覽器查看 X/Twitter、Facebook 用戶帖子**

## ⚠️ 平台支援

**目前僅支援：**
- `x` / `twitter` - X/Twitter（完整功能）
- `facebook` / `fb` - Facebook（基本功能）

**暫不支援**：Instagram、LinkedIn、YouTube 等

## 🎯 核心功能

- **登入狀態检测**：自動檢查瀏覽器是否已登入目標平台
- **帖子提取**：抓取最新 N 篇帖子（文字、時間）
- **互動數據**：可選提取轉推/喜歡/分享 或 留言/分享/讚數
- **用戶資料**：抓取姓名、bio、粉絲/追蹤數
- **彈性連接**：優先連接 OpenClaw browser 實例

## 📥 輸入參數

| 參數 | 類型 | 必填 | 預設 | 說明 |
|------|------|------|------|------|
| `username` | string | ✅ | - | 帳號名稱（不需 `@`） |
| `platform` | string | ❌ | `x` | `x`、`twitter`、`facebook`、`fb` |
| `maxPosts` | number | ❌ | 5 | 最大帖子數（建議 ≤ 20） |
| `includeStats` | boolean | ❌ | true | 是否包含互動數據 |

## 🚀 使用方式

### CLI
```bash
node index.js realDonaldTrump x 5 true
node index.js markzuckerberg facebook 3 false
```

### OpenClaw (sessions_spawn)
```javascript
await sessions_spawn({
  runtime: "subagent",
  task: JSON.stringify({
    skill: "brave-loggedin-tag-browsing",
    params: { username: "elonmusk", platform: "x", maxPosts: 5, includeStats: true }
  })
});
```

## 📤 輸出格式

```json
{
  "username": "realDonaldTrump",
  "platform": "x",
  "loginStatus": "💰 錢錢AI (@MVenusean67544)",
  "profile": { "name": "...", "bio": "...", "followers": "110.8M" },
  "posts": [
    { "time": "2026-03-02T16:20:05.000Z", "text": "...", "stats": { "likes": "459K" } }
  ],
  "metadata": { "maxPosts": 5, "timestamp": "...", "connectionMode": "opencdl" }
}
```

## ⚙️ 技術實現

- **依賴**：playwright（chromium）
- **連接策略**：
  1. OpenClaw CDP (port 18800)
  2. Chrome CDP (port 9222)
  3. 啟動新 Brave 實例（userDataDir）

## 🔧 故障排除

| 問題 | 解決方案 |
|------|----------|
| 連接 OpenClaw Brave 失敗 | 先執行 `/browser start` |
| 提示安裝瀏覽器 | `npx playwright install chromium` |
| 未檢測到登入 | 在 Brave 中手動登入目標平台 |
| 提取不到帖子 | 增加等待時間或檢查 DOM 選擇器 |

## 📊 效能指標

- 首次執行：8-12 秒
- 後續執行：3-5 秒
- 記憶體：~150MB
- 建議 maxPosts ≤ 20

## 📝 License

CC BY-NC 4.0
