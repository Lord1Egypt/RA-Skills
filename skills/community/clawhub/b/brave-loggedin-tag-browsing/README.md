# brave-loggedin-tag-browsing

**自動化瀏覽器技能 - 使用已登入的 Brave 瀏覽器查看 X/Twitter、Facebook 用戶帖子**

## 📖 技能簡介

這個技能讓你能夠：
- ✅ **利用 Brave 瀏覽器的已登入狀態**存取 X/Twitter 或 Facebook 的完整內容
- ✅ **自動化提取**用戶的最新帖子（文字、時間、互動數據）
- ✅ **支援連接 OpenClaw 內建的 browser 工具**或啟動新的 Brave 實例
- ✅ **返回結構化 JSON 數據**，方便二次處理

## ⚠️ 平台支援（重要）

**目前版本僅支援以下平台：**
- `x` / `twitter` - X/Twitter（完整功能）
- `facebook` / `fb` - Facebook（基本功能）

**暫不支援的平台**（未來可能新增）：
- Instagram、LinkedIn、YouTube 等

如需其他平台，請開 Issue 或自行擴展 `PLATFORMS` 配置。

## 🎯 核心功能

| 功能 | 描述 |
|------|------|
| **登入狀態检测** | 自動檢查當前瀏覽器是否已登入目標平台，並提取登入帳號名稱 |
| **帖子提取** | 抓取指定用戶的最新 N 篇帖子，包含文字內容、發布時間 |
| **互動數據** | 可選提取轉推/喜歡/分享（X）或 留言/分享/讚數（FB） |
| **用戶資料** | 自動抓取用戶的姓名、bio、粉絲/追蹤數等基本資料 |
| **彈性連接** | 優先連接 OpenClaw browser 實例，次之啟動新 Brave 實例 |

## 📦 安裝位置

```
~/.openclaw/workspace/skills/brave-loggedin-tag-browsing/
├── index.js          # 主執行邏輯（Playwright + CDP）
├── cli.js            # CLI 包裝器
├── execute.js        # 備用執行入口
├── skill.json        # 技能元數據
├── package.json      # 依賴配置
└── README.md         # 本文件
```

## 🚀 使用方法

### 方式一：直接 CLI 執行

```bash
# 查看川普的最新 5 篇帖子（含互動數據）
node index.js realDonaldTrump x 5 true

# 查看馬斯克的最新 3 篇帖子（只看文字）
node index.js elonmusk x 3 false

# 查看 Mark Zuckerberg 的 Facebook 帖子
node index.js markzuckerberg facebook 3 true

# 使用 JSON 輸入（支援更多選項）
echo '{"username":"sama","platform":"x","maxPosts":10,"includeStats":true}' | node cli.js
```

### 方式二：OpenClaw sessions_spawn

```javascript
// 在 OpenClaw 會話中調用
const result = await sessions_spawn({
  runtime: "subagent",
  task: JSON.stringify({
    skill: "brave-loggedin-tag-browsing",
    params: {
      username: "realDonaldTrump",
      platform: "x",
      maxPosts: 5,
      includeStats: true
    }
  }),
  label: "social-browse-session"
});
```

### 方式三：自然語言觸發（與 find-skills 結合）

```
User: 幫我看一下川普最新的發言
→ find-skills 推薦此技能
→ 自動調用 brave-loggedin-tag-browsing
```

## 📥 輸入參數

| 參數 | 類型 | 必填 | 預設 | 說明 |
|------|------|------|------|------|
| `username` | string | ✅ | - | 社交平台帳號名稱（不需 `@` 符號） |
| `platform` | string | ❌ | `x` | 目標平台：`x`、`twitter` 或 `facebook`、`fb` |
| `maxPosts` | number | ❌ | 5 | 要抓取的最大帖子數（建議 ≤ 20） |
| `includeStats` | boolean | ❌ | true | 是否包含互動數據 |

## 📤 輸出格式

```json
{
  "username": "realDonaldTrump",
  "platform": "x",
  "loginStatus": "💰 錢錢AI (@MVenusean67544)",
  "profile": {
    "name": "Donald J. Trump",
    "handle": "@realDonaldTrump",
    "bio": "45th & 47th President of the United States of America 🇺🇸",
    "followers": "110.8M Followers",
    "verified": true
  },
  "posts": [
    {
      "time": "2026-03-02T16:20:05.000Z",
      "text": "【如果有文字內容】",
      "stats": {
        "replies": "37K",
        "retweets": "91K",
        "likes": "459K",
        "shares": "34K"
      }
    },
    {
      "time": "2026-02-28T07:44:23.000Z",
      "text": null,
      "stats": null
    }
  ],
  "metadata": {
    "maxPosts": 5,
    "includeStats": true,
    "timestamp": "2026-03-18T05:40:00.000Z",
    "connectionMode": "opencdl"
  }
}
```

**備註**：
- 如果帖子只有圖片/影片而無文字，`text` 為 `null`
- 若 `includeStats: false`，則 `stats` 欄位為 `null`
- `connectionMode` 顯示瀏覽器連接方式：`opencdl`（OpenClaw）、`cdp`（一般 Chrome）、`launch`（新啟動）

## ⚙️ 技術實現

### 依賴庫
- **playwright**：chromium 模組（需安裝）
- **Node.js**：v18+（支援ES模組）

### 安裝依賴

```bash
cd ~/.openclaw/workspace/skills/brave-loggedin-tag-browsing
npm install
# Playwright 會自動安裝所需瀏覽器
npx playwright install chromium
```

### 連接策略

1. **優先連接 OpenClaw browser 實例**（CDP 端口 18800）
   - 利用 OpenClaw 已啟動的 Brave（通常已登入 X/FB）
   - 最快速，無需重啟瀏覽器

2. **嘗試連接通用 Chrome CDP**（端口 9222）
   - 連接手動啟用的 Chrome/Chromium
   - 需提前開啟：`brave-browser --remote-debugging-port=9222`

3. **啟動新的 Brave 實例**
   - 使用持久化 userDataDir（保留登入狀態）
   - 執行路徑：`/usr/bin/brave-browser`
   - 首次啟動會稍慢，但後續會記住登入狀態

### 平台選擇器對應表

| 平台 | 帖子容器 | 文字選擇器 | 時間選擇器 | 登入狀態按鈕 |
|------|----------|------------|------------|--------------|
| X/Twitter | `article[data-testid="tweet"]` | `div[data-testid="tweetText"]` | `time[datetime]` | `button[data-testid="accountButton"]` |
| Facebook | `div[role="article"], div[data-pagelet^="TimelineFeedUnit_"]` | `[data-ad-preview], [data-testid="post_message"], .x1lliihq` | `time, abbr[title], span[data-utime]` | `button[aria-label*="個人檔案"], a[href*="/settings"]` |

## 🔧 故障排除

### 問題：連接 OpenClaw Brave 失敗
**原因**：OpenClaw browser 工具未啟動  
**解決**：
```bash
# 在 OpenClaw 中先行啟動瀏覽器
/browser start
```

### 問題：提示安裝 Playwright 瀏覽器
**錯誤**：`Error: Browser executable not found`  
**解決**：
```bash
npx playwright install chromium
```

### 問題：登入狀態顯示「未檢測到」
**原因**：Brave 未登入目標平台或會話過期  
**解決**：
1. 手動開啟 Brave，登入 X 或 Facebook 帳號
2. 保持瀏覽器開啟，重新執行技能
3. 或刪除 `~/.config/google-chrome/Default/Cookies` 重新登入

### 問題：提取不到帖子
**原因**：頁面載入不夠或選擇器變更  
**解決**：
- 增加等待時間：修改 `page.waitForTimeout(3000)` 為更長時間
- 檢查平台是否更新了 DOM 結構（可提交 Issue）

## 💡 使用場景範例

### 1. 政治人物動態監控
```bash
node index.js realDonaldTrump x 10 true > trump_tweets.json
node index.js JoeBiden x 10 true > biden_tweets.json
```
應用：比較兩位候選人的發言傾向，進行情感分析

### 2. 科技領袖言論收集
```bash
node index.js elonmusk x 20 true > musk_tweets.json
node index.js sama x 20 true > altman_tweets.json
node index.js markzuckerberg facebook 10 true > zuck_posts.json
```
應用：追蹤 AI 最新趨勢，市場影響力分析

### 3. 即時新聞源
```bash
# 設定 cron job 每小時執行一次
0 * * * * node index.js CNN x 5 true >> news_feed.jsonl
```

### 4. 投資決策輔助
```bash
# 監控可能影響股價的關鍵人物
node index.js realDonaldTrump x 3 false | jq '.posts[].text' | grep -i 'china'
```

## 🔒 安全與隱私

⚠️ **重要提醒**：
- 此技能會**連接已登入的瀏覽器**，請確保該瀏覽器的會話安全
- 提取的數據包含公開 IPO 內容，遵守各平台的使用條款
- 請勿用於非法監控、騷擾或商業爬蟲（違反 ToS）
- 建議僅用於個人研究、新聞追蹤、公開數據分析

## 📊 效能指標

| 指標 | 數值 |
|------|------|
| 首次執行時間 | 8-12 秒（需啟動瀏覽器）|
| 後續執行時間 | 3-5 秒（連接現有實例）|
| 記憶體使用 | ~150MB（Playwright + 瀏覽器）|
| CPU 使用 | 低（等待頁面載入時）|
| 最大帖子數 | 建議 20 篇（太多會變慢）|

## 📝 版本歷史

- **v2.0.0** (2026-03-18) - 新增 Facebook 支援，優化選擇器
- **v1.0.0** (2026-03-18) - 初始版本，僅支援 X/Twitter

## 🤝 貢獻

歡迎提交 Issue 或 Pull Request 改善此技能：

- 新增更多平台支援（Instagram、LinkedIn、YouTube）
- 改進選擇器穩定性
- 增加圖片/影片 URL 提取
- 提供圖表化輸出選項

---

**Made with ❤️ by Shuttle AI**  
**發布於 ClawHub：brave-loggedin-tag-browsing (ID: k975x4rgk1aeqgg7d11jch7xz58325fg)**
