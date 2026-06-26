# 完整安裝指南：從零開始部署 AI 老闆助理

> 本指南將帶你從全新的電腦環境，一步步部署完整的 AI 老闆助理系統。
> 預計完成時間：30-60 分鐘（取決於網路速度）

---

## 📋 系統需求

### 硬體需求
- **作業系統**：macOS 12+ / Windows 10+ / Linux (Ubuntu 20.04+)
- **記憶體**：至少 8GB RAM（建議 16GB）
- **硬碟空間**：至少 10GB 可用空間
- **網路**：穩定的網際網路連線

### 軟體需求
- **Node.js**：v18 或更新版本
- **npm**：v9 或更新版本
- **終端機**：Terminal (macOS/Linux) 或 PowerShell (Windows)

### 必備帳號
- **Google 帳號**：用於 Gmail、Calendar、Drive 整合
- **Telegram 帳號**：（可選）用於手機端操作
- **AI 模型 API Key**：Claude / GPT / Gemini（擇一）

---

## 第一部分：環境準備

### 步驟 1：安裝 Node.js

#### macOS（使用 Homebrew）
```bash
# 安裝 Homebrew（如果還沒有）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安裝 Node.js
brew install node

# 驗證安裝
node --version
npm --version
```

#### Windows
1. 下載安裝檔：https://nodejs.org/
2. 執行安裝檔，選擇 LTS 版本
3. 重新啟動終端機
4. 驗證：`node --version` 和 `npm --version`

#### Linux (Ubuntu/Debian)
```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# 驗證
node --version
npm --version
```

---

## 第二部分：安裝 Clawdbot

### 步驟 2：全域安裝 Clawdbot

```bash
npm install -g clawdbot
```

**驗證安裝**：
```bash
clawdbot --version
```

應該看到版本號，例如：`clawdbot version 1.x.x`

### 步驟 3：初始化 Clawdbot

```bash
# 建立 Clawdbot 工作目錄
mkdir -p ~/ai-boss-assistant
cd ~/ai-boss-assistant

# 初始化設定
clawdbot init
```

執行 `init` 時會詢問：
- **模型選擇**：選擇你的 AI 模型（Claude / GPT / Gemini）
- **API Key**：輸入你的 API Key
- **工作目錄**：確認使用當前目錄

### 步驟 4：下載 AI 老闆助理模板

**方法 A：從 GitHub 下載**（推薦）
```bash
# Clone 模板 repository
git clone https://github.com/YOUR-USERNAME/ai-boss-assistant-templates.git templates

# 或下載 ZIP 後解壓縮到 templates/ 資料夾
```

**方法 B：手動建立目錄結構**
```bash
mkdir -p templates/agent-persona
mkdir -p templates/老闆助理
mkdir -p templates/meta
mkdir -p templates/gog
mkdir -p templates/tasks
mkdir -p templates/setup
mkdir -p templates/security
mkdir -p templates/examples
mkdir -p templates/browser
mkdir -p templates/skills
mkdir -p templates/每日會報範例
```

然後將所有模板檔案複製到對應資料夾。

---

## 第三部分：設定 Google Workspace 整合

### 步驟 5：建立 Google OAuth 憑證

1. **前往 Google Cloud Console**
   - 網址：https://console.cloud.google.com/

2. **建立新專案**
   - 點擊「Select a project」→「New Project」
   - 專案名稱：`AI Boss Assistant`
   - 點擊「Create」

3. **啟用必要的 API**
   - 搜尋並啟用以下 API：
     - Gmail API
     - Google Calendar API
     - Google Drive API
     - Google Docs API
     - Google Sheets API

4. **建立 OAuth 2.0 憑證**
   - 左側選單：APIs & Services → Credentials
   - 點擊「Create Credentials」→「OAuth client ID」
   - Application type：「Desktop app」
   - Name：`AI Boss Assistant Client`
   - 點擊「Create」
   - **下載 JSON 檔案**（例如：`client_secret_xxx.json`）

### 步驟 6：安裝並設定 gog CLI

```bash
# macOS
brew install steipete/tap/gogcli

# Linux
npm install -g @steipete/gog

# Windows
npm install -g @steipete/gog
```

**配置憑證**：
```bash
# 建立 gog 設定目錄
mkdir -p "$HOME/Library/Application Support/gogcli"  # macOS
mkdir -p "$HOME/.config/gogcli"                       # Linux
mkdir -p "$env:APPDATA/gogcli"                        # Windows

# 將下載的憑證檔案移動到設定目錄
# macOS
mv ~/Downloads/client_secret_*.json "$HOME/Library/Application Support/gogcli/credentials.json"

# Linux
mv ~/Downloads/client_secret_*.json "$HOME/.config/gogcli/credentials.json"

# 告訴 gog 使用這個憑證
gog auth credentials "$HOME/Library/Application Support/gogcli/credentials.json"
```

### 步驟 7：授權 Google 帳號

```bash
# 為主要帳號授權（開啟所有服務）
gog auth add your-email@gmail.com --services gmail,calendar,drive,docs,sheets

# 如果有多個帳號，重複上述指令
gog auth add work-email@company.com --services gmail,calendar,drive,docs,sheets
```

執行後會開啟瀏覽器，要求你登入 Google 並授權。

**驗證授權**：
```bash
gog auth list
```

應該看到你的帳號列表及已授權的服務。

---

## 第四部分：設定 Clawdbot Gateway

### 步驟 8：配置 Gateway

```bash
# 啟動 Gateway 設定精靈
clawdbot gateway configure
```

會詢問：
1. **API Key**：確認你的 AI 模型 API Key
2. **預設模型**：例如 `claude-sonnet-4` 或 `gpt-4`
3. **工作目錄**：確認為 `~/ai-boss-assistant`
4. **啟用的通道**：
   - 選擇 `telegram`（推薦，方便手機操作）
   - 或選擇 `web`（純網頁版）

### 步驟 9：設定 Telegram Bot（可選但推薦）

如果選擇 Telegram 通道：

1. **建立 Telegram Bot**
   - 在 Telegram 搜尋 `@BotFather`
   - 發送 `/newbot`
   - 設定 Bot 名稱（例如：`My AI Boss Assistant`）
   - 設定 Bot username（例如：`my_ai_boss_bot`）
   - **複製 Bot Token**（格式：`123456789:ABCdefGHIjklMNOpqrsTUVwxyz`）

2. **配置 Telegram Token**
   ```bash
   clawdbot gateway config set telegram.botToken "YOUR_BOT_TOKEN"
   ```

3. **啟動 Gateway**
   ```bash
   clawdbot gateway start
   ```

4. **連接你的 Bot**
   - 在 Telegram 搜尋你的 Bot username
   - 發送 `/start`
   - Bot 會回應並建立連線

---

## 第五部分：套用 AI 老闆助理模板

### 步驟 10：載入核心人設

在 Telegram（或 Web UI）中發送以下訊息：

```
請依序閱讀以下檔案，學習成為我的 AI 老闆助理：

第一階段（基礎人設）：
1. templates/agent-persona/PERSONA.md
2. templates/agent-persona/COMMUNICATION.md
3. templates/agent-persona/WORKFLOW.md
4. templates/agent-persona/RULES.md

第二階段（專業定位）：
5. templates/老闆助理/AI 老闆助理產品白皮書.md
6. templates/老闆助理/AI 老闆助理MVP功能表.md

第三階段（工具掌握）：
7. templates/meta/Clawdbot 技能與工具總覽.md
8. templates/gog/gog 安裝與使用教學.md

讀完後告訴我你準備好了。
```

AI 會逐一讀取這些檔案並學習。

### 步驟 11：完成前置訪談

AI 學習完畢後，會主動向你詢問：

**基本資訊**：
- 你希望我怎麼稱呼你？
- 你的工作性質是什麼？
- 你最常用哪些 Google 帳號？

**工作偏好**：
- 你希望每天幾點收到行程提醒？
- 你希望我主動做哪些事？哪些一定要先問？
- 你偏好的溝通風格？

**生活習慣**：
- 有哪些固定的生活事件？
- 有哪些重要日期需要提醒？

**任務優先級**：
- 什麼類型的任務最重要？
- 什麼情況算「緊急」？

根據你的回答，AI 會建立個人化設定。

### 步驟 12：測試基礎功能

完成訪談後，測試以下功能：

**測試 1：行程管理**
```
幫我排明天下午 2 點與客戶的視訊會議
```

AI 會詢問：
- 用哪個帳號？
- 要不要加 Google Meet 連結？
- 會議主題是什麼？

**測試 2：郵件草稿**
```
幫我寫一封信給客戶，主題是「合作提案」
```

**測試 3：檔案查詢**
```
幫我找 Drive 裡最近的報價單
```

**測試 4：每日提醒**
```
設定每天早上 8 點提醒我今日行程
```

---

## 第六部分：進階設定

### 步驟 13：設定每日自動提醒（Heartbeat）

編輯 `HEARTBEAT.md`：

```bash
cd ~/ai-boss-assistant
nano HEARTBEAT.md
```

加入以下內容：
```markdown
# 每日自動檢查項目

## 早上 8:00
- [ ] 檢查今日行程
- [ ] 檢查未讀郵件（重要的）

## 下午 6:00
- [ ] 整理今日完成事項
- [ ] 提醒明日重要行程
```

儲存後，AI 會在指定時間自動執行這些檢查。

### 步驟 14：安裝額外技能（可選）

```bash
# 安裝瀏覽器自動化
npm install -g agent-browser
npx playwright install

# 安裝 Notion 整合（如果需要）
npm install -g @notionhq/client

# 安裝 Slack 整合（如果需要）
npm install -g @slack/web-api
```

### 步驟 15：備份與版本控制

```bash
cd ~/ai-boss-assistant

# 初始化 Git（保護你的設定）
git init
git add .
git commit -m "Initial AI Boss Assistant setup"

# 建立 .gitignore（避免上傳敏感資訊）
cat > .gitignore << EOF
*.json
*.log
.env
credentials/
tokens/
memory/*.md
EOF
```

---

## 第七部分：日常使用

### 常用指令範例

**行程管理**：
- 「幫我排下週一早上 10 點的會議」
- 「今天有什麼行程？」
- 「把明天的會議改到下午 3 點」

**郵件處理**：
- 「幫我寫信給 client@example.com，主題是...」
- 「有什麼重要的未讀郵件嗎？」
- 「幫我寄這份報告給...」

**文件管理**：
- 「幫我找 Drive 裡的某某檔案」
- 「把這份文件轉成 PDF」
- 「分享這個檔案給...」

**任務追蹤**：
- 「記下：明天要跟進客戶報價」
- 「今天要做什麼？」
- 「標記這個任務完成」

---

## 🔧 故障排除

### 問題 1：Gateway 無法啟動

**症狀**：`clawdbot gateway start` 報錯

**解決方案**：
```bash
# 檢查 Gateway 狀態
clawdbot gateway status

# 停止舊的 Gateway
clawdbot gateway stop

# 清除設定後重新啟動
clawdbot gateway restart
```

### 問題 2：gog 授權失敗

**症狀**：`gog auth add` 時瀏覽器沒有開啟

**解決方案**：
```bash
# 確認憑證檔案位置
gog auth credentials --path

# 手動指定憑證檔案
gog auth credentials /path/to/credentials.json

# 重新授權
gog auth add your-email@gmail.com --services gmail,calendar
```

### 問題 3：AI 回應緩慢或無回應

**可能原因**：
- API Key 額度用完
- 網路連線問題
- Gateway 沒有正常運行

**解決方案**：
```bash
# 檢查 Gateway 日誌
clawdbot gateway logs

# 檢查 API Key 額度（到對應平台查看）
# 重啟 Gateway
clawdbot gateway restart
```

### 問題 4：Telegram Bot 無法連線

**解決方案**：
```bash
# 檢查 Bot Token 設定
clawdbot gateway config get telegram.botToken

# 重新設定
clawdbot gateway config set telegram.botToken "YOUR_BOT_TOKEN"

# 重啟 Gateway
clawdbot gateway restart
```

---

## 📚 下一步

### 學習資源
- **完整文件**：`templates/` 資料夾內所有 `.md` 檔案
- **範例對話**：`templates/examples/對話範例.md`
- **進階功能**：`templates/老闆助理/AI 老闆助理產品白皮書.md`

### 客製化
- 修改 `PERSONA.md` 調整 AI 個性
- 編輯 `HEARTBEAT.md` 設定自動任務
- 更新 `USER.md` 記錄你的偏好

### 擴展功能
- 整合 Notion 資料庫
- 整合 Slack 工作區
- 設定 Browser Automation 自動化網頁操作
- 加入財務報表整合

---

## ✅ 安裝完成檢查清單

完成以下項目代表安裝成功：

- [ ] Node.js 與 npm 已安裝
- [ ] Clawdbot 已全域安裝
- [ ] Google OAuth 憑證已設定
- [ ] gog CLI 已安裝並授權
- [ ] Gateway 已啟動並可連線
- [ ] Telegram Bot 已連線（如使用）
- [ ] AI 已讀取所有模板檔案
- [ ] 完成前置訪談
- [ ] 成功測試基礎功能（行程、郵件、檔案）
- [ ] 設定每日自動提醒

---

## 🎉 恭喜！

你已經成功部署 AI 老闆助理系統！

現在你可以：
- 用自然語言管理行程
- 讓 AI 幫你寫信
- 自動整理文件
- 每天收到智慧提醒

享受你的 AI 助理帶來的效率提升！

---

## 📞 技術支援

如有問題，請參考：
- **文件庫**：所有 templates 內的教學文件
- **故障排除**：本文件第七部分
- **社群支援**：[你的支援管道]
- **專業服務**：[你的聯絡方式]

---

*版本：v1.0 | 更新日期：2026-02-02*
