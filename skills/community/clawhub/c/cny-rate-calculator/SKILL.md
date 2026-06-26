---
name: cny-rate-calculator
version: 1.0.0
description: Auto-fetch Bank of Taiwan CNY exchange rates and calculate tiered pricing (base cost, 10K discount, 50K discount) using the Prairie Grasslands formula. REQUIRED: Channel configuration and Schedule setup must be completed before use. Supports Telegram, Discord, Slack, Signal, WhatsApp, iMessage, IRC, Google Chat, and webhooks.
---

# CNY Rate Calculator (大草原匯率計算器)

Automatically fetch Bank of Taiwan CNY exchange rates and calculate tiered pricing.

---

## 🤖 Agent 指引（自動執行規則）

> **以下規則 Agent 必須優先遵守，在任何使用者互動之前先執行檢查。**

### 規則一：Agent 啟動時 → 主動偵測並引導設定

Agent 每次啟動時，必須：

1. 讀取技能目錄下的 `config.json`
2. 檢查 `schedule.enabled` 是否為 `true`、`channels` 是否非空
3. 若任一條件不符（**未完成設定**），立即透過 OpenClaw 已啟用的頻道發送以下訊息：

```
🦞 大草原匯率計算器尚未完成設定

請選擇：
1. 快速設定
2. 自訂設定
```

4. 等待使用者回覆：
   - 回覆 `1` 或「快速設定」→ Agent 執行：
     ```
     python scripts/cny_rate.py --auto-setup
     ```
     自動套用基本設定（第一個已啟用頻道 + 預設排程：週一至週五 09:00–17:00 每小時），
     並回覆：「✅ 已套用基本設定，排程通知即將啟動。如需調整請輸入『設定匯率』。」
   - 回覆 `2` 或「自訂設定」→ Agent 在伺服器端執行：
     ```
     python scripts/cny_rate.py
     ```
     並回覆：「✅ 設定精靈已啟動，請依照終端提示完成設定。」

5. 設定精靈完成後自動將排程寫入 `~/.openclaw/cron/jobs.json`

### 規則二：排程觸發事件 → 執行匯率通知

當收到系統事件「執行人民幣匯率計算並發送通知」時：

1. 先確認 `config.json` 的 `schedule.enabled` 為 `true` 且 `channels` 非空
2. 若**已完成設定**，執行：
   ```
   python scripts/cny_rate.py --run
   ```
3. 若**尚未完成設定**，改為執行設定精靈（同規則一步驟 3）

### 規則三：觸發設定精靈的關鍵字

使用者輸入以下任一關鍵字時，執行 `python scripts/cny_rate.py`：

- `設定匯率`、`匯率設定`、`初始化`、`重新設定`
- `setup`、`configure`、`init`

---

## ⚠️ 使用前必須完成

**本技能會自動檢測系統中已配置的頻道，並引導您完成設定。**

### 🔍 自動檢測 + 交互式選擇 + 🧪 測試訊息

安裝後首次執行，技能會：
1. **自動掃描**您的 OpenClaw 配置
2. **列出可用頻道**讓您選擇
3. **自動保存**配置
4. **🧪 發送測試訊息**確認設定正確（就像印表機的測試頁！）

### 🧪 測試訊息流程

設定完成後，會詢問是否發送測試：

```
==================================================
🧪 設定完成！是否發送測試訊息？
==================================================

就像印表機安裝後列印測試頁一樣，
建議發送一次測試訊息確認設定正確。

發送測試訊息？(y/n): y

📤 發送測試訊息到 Telegram...
✅ 測試訊息發送成功！
```

**測試訊息內容：**
```
🦞 大草原匯率計算器 - 測試訊息

✅ 頻道設定：Telegram
✅ 排程設定：已啟用

這是一則測試訊息，確認設定正確。
正式匯率通知將依照排程時間發送。

測試時間：2025/03/16 12:00:00
```

### 1️⃣ 頻道設定（必需）
- 執行時自動檢測並提示選擇
- 或直接編輯 `config.json`
- 未設定頻道無法執行

### 2️⃣ 排程設定（必需）
- 編輯 `config.json` 設定發送時間
- 未設定排程無法執行

### 3️⃣ 🧪 測試訊息（建議）
- 設定完成後詢問是否發送測試
- 確認頻道設定正確
- 就像印表機的測試頁概念

---

## 設定流程

### Step 0: 自動檢測（安裝後自動執行）

安裝後執行技能，會自動檢測您的 OpenClaw 配置：

```
==================================================
🔍 檢測到以下可用頻道:
==================================================

  1. Telegram
     狀態: 已啟用
     備註: 需要 Chat ID

  2. Discord
     狀態: 已啟用
     備註: 需要 Webhook URL

  3. Console (僅終端輸出，不發送)
  4. 取消設定

請選擇要使用的頻道 (1-4): 1

已選擇: Telegram
請輸入 Telegram Chat ID: 6462528054

✅ 已保存頻道配置: telegram
```

### Step 1: 頻道設定（先完成）

根據自動檢測結果，編輯 `config.json`：

```json
{
  "channels": [
    { "type": "telegram", "target": "YOUR_CHAT_ID" }
  ]
}
```

**支援頻道：**

| 頻道 | type | target | 環境變數 |
|------|------|--------|---------|
| Telegram | `telegram` | Chat ID | `TELEGRAM_BOT_TOKEN` |
| Discord | `discord` | Webhook URL | 無 |
| Slack | `slack` | Webhook URL | 無 |
| Signal | `signal` | 電話號碼 | `OPENCLAW_GATEWAY_TOKEN` |
| WhatsApp | `whatsapp` | 電話號碼 | `OPENCLAW_GATEWAY_TOKEN` |
| iMessage | `imessage` | 聯絡人名稱 | `OPENCLAW_GATEWAY_TOKEN` |
| IRC | `irc` | 頻道名稱 | `OPENCLAW_GATEWAY_TOKEN` |
| Google Chat | `googlechat` | Webhook URL | 無 |
| Webhook | `webhook` | 自訂 URL | 無 |

### Step 2: 排程設定（後完成）

編輯 `config.json`：

```json
{
  "schedule": {
    "enabled": true,
    "days_of_week": [1, 2, 3, 4, 5],
    "start_time": "09:00",
    "end_time": "17:00",
    "interval_hours": 1,
    "schedule_times": ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"],
    "description": "週一至週五 09:00-17:00 每小時",
    "cron": "0 9-17 * * 1-5"
  }
}
```

**排程欄位說明：**

| 欄位 | 說明 | 範例 |
|------|------|------|
| `enabled` | 啟用排程 | `true` |
| `days_of_week` | 執行日期（0=日, 6=六） | `[1,2,3,4,5]` |
| `start_time` | 開始時間 | `"09:00"` |
| `end_time` | 結束時間 | `"17:00"` |
| `interval_hours` | 間隔小時 | `1`, `2`, `3`, `4` |
| `schedule_times` | 執行時間列表 | `["09:00", "10:00"]` |
| `description` | 描述 | 自由填寫 |
| `cron` | Cron 表達式 | `0 9-17 * * 1-5` |

### Step 3: 🧪 測試訊息（建議）

設定完成後執行：

```bash
python scripts/cny_rate.py
```

配置驗證通過後會詢問：
```
🧪 設定完成！是否發送測試訊息？
就像印表機安裝後列印測試頁一樣...

發送測試訊息？(y/n): y
```

---

## 完整配置範例

```json
{
  "formula": {
    "deltas": [0.05, 0.03, 0.015],
    "labels": ["基礎成本", "滿萬優惠", "五萬優惠"]
  },
  "source": {
    "name": "Bank of Taiwan",
    "url": "https://rate.bot.com.tw/xrt"
  },
  "channels": [
    { "type": "telegram", "target": "123456789" },
    { "type": "discord",  "target": "https://discord.com/api/webhooks/..." }
  ],
  "schedule": {
    "enabled": true,
    "days_of_week": [1, 2, 3, 4, 5],
    "start_time": "09:00",
    "end_time": "17:00",
    "interval_hours": 1,
    "schedule_times": ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"],
    "description": "週一至週五 09:00-17:00 每小時",
    "cron": "0 9-17 * * 1-5"
  }
}
```

---

## 排程部署

### Windows 工作排程器
- 程式：`python`
- 參數：`scripts/cny_rate.py`
- 觸發：依照 config.json 中的排程設定

### Linux/macOS Cron
```bash
# 編輯 crontab
crontab -e

# 加入排程（範例：週一至週五 9-17點每小時）
0 9-17 * * 1-5 cd /path/to/skill && python scripts/cny_rate.py
```

### OpenClaw Cron
```json
{
  "cny-rate-check": {
    "schedule": "0 9-17 * * 1-5",
    "command": "python scripts/cny_rate.py",
    "cwd": "/path/to/cny-rate-calculator"
  }
}
```

---

## 計算公式

| 檔位 | 計算方式 | 預設標籤 |
|------|---------|---------|
| 中間價 | (買入 + 賣出) / 2 | - |
| 基礎成本 | 中間價 + 0.05 | 基礎成本 |
| 滿萬優惠 | 中間價 + 0.03 | 滿萬優惠 |
| 五萬優惠 | 中間價 + 0.015 | 五萬優惠 |

---

## 資料來源

- **台灣銀行牌告匯率**: https://rate.bot.com.tw/xrt
- **大草原計算機參考**: https://78lion.com/CNY.html

---

## 環境變數

| 變數 | 適用頻道 | 說明 |
|------|---------|------|
| `TELEGRAM_BOT_TOKEN` | Telegram | Bot 憑證 |
| `OPENCLAW_GATEWAY_TOKEN` | Signal, WhatsApp, iMessage, IRC | Gateway 憑證 |
| `OPENCLAW_GATEWAY_URL` | Signal, WhatsApp, iMessage, IRC | Gateway 網址 |

---

## 頻道管理（對話指令）

安裝完成後，可直接透過已設定的頻道（如 Telegram）與 agent 互動管理通知頻道清單。

| 關鍵字 | 功能 |
|--------|------|
| `加入頻道` | 查看可加入的頻道並選擇加入 |
| `移除頻道` | 從通知清單移除指定頻道 |
| `頻道設定` | 查看目前所有通知頻道狀態 |

---

### 觸發一：使用者主動輸入關鍵字

當使用者傳送 `加入頻道`、`移除頻道` 或 `頻道設定` 時：

1. 執行 `python scripts/cny_rate.py --list-channels` 取得 JSON：
   - `configured`：目前通知清單中的頻道
   - `available`：OpenClaw 已啟用但尚未加入的頻道

2. **加入頻道** → 展示 `available` 編號清單，詢問選哪個：
   ```
   可加入的頻道：
   1. Discord
   2. Slack
   回覆編號或名稱選擇，回覆「取消」退出
   ```

3. **移除頻道** → 展示 `configured` 編號清單，詢問選哪個

4. **頻道設定** → 同時展示兩份清單，詢問要加入還是移除

---

### 觸發二：回覆新頻道偵測通知

排程執行偵測到新頻道時，會發送以下格式的通知：

```
📡 偵測到新啟用頻道

以下頻道可加入匯率通知清單：
1. Discord
2. Slack

回覆頻道名稱或編號即可加入
（例：Discord 或 1）
回覆「略過」忽略此提示
```

當使用者回覆**編號**（如 `1`）或**頻道名稱**（如 `Discord`）時：

1. 對照通知中的清單確認選擇的頻道類型
2. 詢問該頻道需要的目標值：

   | 頻道 | 詢問內容 |
   |------|---------|
   | Telegram | 請提供 Chat ID（純數字） |
   | Discord / Slack / Google Chat | 請提供 Webhook URL |
   | Signal / WhatsApp | 請提供目標電話號碼 |
   | iMessage | 請提供聯絡人名稱 |
   | IRC | 請提供頻道名稱 |

3. 收到目標值後執行：
   ```
   python scripts/cny_rate.py --add-channel <type> <target>
   ```
4. 回覆確認結果，並告知下次排程將發送到新頻道

使用者回覆 `略過` 則不執行任何操作，回覆確認已略過。

---

### 自動偵測通知

排程執行時若偵測到 OpenClaw 有新啟用的頻道（尚未加入通知清單），自動透過現有頻道發送上述格式的提醒訊息。

---

## 檔案結構

```
cny-rate-calculator/
├── SKILL.md              # 本說明文件
├── config.json           # ⚠️ 必須設定（頻道+排程）
└── scripts/
    ├── cny_rate.py       # 主程式（含自動檢測+測試訊息）
    ├── run.bat           # Windows 啟動
    └── run.sh            # Linux/macOS 啟動
```
