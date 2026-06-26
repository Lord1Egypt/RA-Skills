---
name: email-sender-policy
description: |
  郵件發送政策管理員，自動應用寄信規則：
  - 標題 UTF-8 Base64 編碼（RFC 2047）
  - Markdown 表格轉換為清單格式
  - 使用當前登入的 Gmail 連接
  - 支援多收件人
version: "2.0.1"
author: Shuttle AI
tags: ["email", "policy", "formatting"]
mode: subagent
triggers:
  - send email
  - 寄信
  - 發送郵件
  - email formatting
---

# Email Sender Policy Skill

自動應用郵件發送標準政策，確保所有外發郵件符合格式規範。

## 📜 **核心政策**

### 1. 標題編碼Policy
- ✅ **強制使用 UTF-8 Base64 編碼**（RFC 2047 格式）
- ✅ 格式：`=?utf-8?b?{base64_encoded_title}?=`
- ✅ 避免亂碼，確保所有郵件客戶端正確顯示

### 2. 內容格式Policy
- ✅ **Markdown 表格一律轉為清單格式**
  - 表頭列 `| 欄位1 | 欄位2 |` → 轉為項目符號`.`開頭
  - 分隔列 `|-----|-----|` → 移除
  - 數據列 `| 內容1 | 內容2 |` → 轉為 `  • 內容2` 層級
- ✅ **保持純文字優先**，不嵌入複雜格式
- ✅ 使用 `\r\n` 作為 RFC 822 行分隔符

### 3. 寄件人Policy
- ✅ **使用當前登入的 Gmail 連接**
- ✅ 不自定義寄件人（除非另有授權）
- ✅ 從 Maton API Gateway 的 OAuth 會話取得有效連接

### 4. 多收件人Policy
- ✅ **支援多收件人同時寄送**
- ✅ 格式：`To: user1@example.com, user2@example.com`
- ✅ 個別追蹤 Message ID

---

## 🛠 **使用方法**

### 基本發信
```bash
email-sender-policy send \
  --to "recipient@example.com" \
  --subject "你的主題" \
  --body "郵件內容（支援清單、項目符號）"
```

### 多收件人
```bash
email-sender-policy send \
  --to "user1@example.com, user2@example.com" \
  --subject "團隊通知" \
  --body "內容..."
```

### 檔案 Macedonia
```bash
email-sender-policy send \
  --to "recipient@example.com" \
  --subject "報告" \
  --file "path/to/document.md"  # 自動轉換表格為清單
```

---

## 🔄 **內部工作流程**

```
1. 接收參數（to, subject, body）
2. 預處理：
   • 檢查 MATON_API_KEY 環境變數
   • 載入當前有效的 Gmail 連接
   • 轉換 Markdown 表格 → 清單（如需要）
3. 建置 RFC 822 郵件：
   • From: me (使用當前連接)
   • To: [收件人列表]
   • Subject: UTF-8 Base64 編碼
   • Content-Type: text/plain; charset=UTF-8
   • Content-Transfer-Encoding: 8bit
4. Gmail API 發送：
   • POST https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages/send
   • Headers: Authorization: Bearer $MATON_API_KEY
   • Body: { "raw": base64url(message) }
5. 回傳結果：
   • Message ID
   • 發送狀態
```

---

## 📊 **表格轉換規則示例**

### 輸入（Markdown 表格）
```markdown
| 景點 | 特色 | 預算 |
|------|------|------|
| DDP屋頂 | 免费 | KRW 0 |
| 樂天塔 | 高空步道 | KRW 27,000 |
```

### 輸出（清單格式）
```
• DDP屋頂：免费
• 樂天塔：高空步道 + KRW 27,000
```

**轉換邏輯**：
- 每行資料轉為 `• [第一欄]：[第二欄]（[第三欄]）`
- 合併多欄位為單一行人閱讀句子
- 移除表格邊界字符（|、-）

---

## 🧩 **與其他技能整合**

此 skill 可作為底層政策被其他技能調用：

```javascript
// marketing-drafter 產生內容後，自動應用政策發送
const email = await email_sender_policy({
  to: ["customer@example.com"],
  subject: " your report",
  body: generated_content  //自動處理表格編碼
});
```

---

## ⚙️ **配置**

### 環境變數
| 變數 | 說明 | 強制性 |
|------|------|--------|
| `MATON_API_KEY` | Maton API 金鑰 | ✅ 必須 |
| `EMAIL_DEFAULT_FROM` | 預設寄件人（可選） | ❌ 可選 |

### 連接管理
- 使用 `https://ctrl.maton.ai/connections` 管理 OAuth 連接
- 自動選擇 `status=ACTIVE` 的 `google-mail` 連接
- 支援多個連接切換（未來擴展）

---

## 🎯 ** triggers 說明**

當用戶出現以下意圖時自動觸發：
- "幫我寄信"、"send email"
- "寄給..."、"發送郵件"
- "調整標題編碼"、"避免亂碼"
- "表格轉清單"、"格式轉換"

---

## 📝 **SKILL 规范檢查清單**

- ✅ `name` 符合小寫+連字符
- ✅ `description` 完整說明
- ✅ `version` 語義化版本
- ✅ `triggers` 觸發關鍵字
- ✅ `mode: subagent` 子代理執行
- ✅ `tags` 標記正確
- ✅ 符合 AgentSkills v1.1 規範

---

## 🚀 **安装與發布**

```bash
# 開發中測試
cd ~/.openclaw/workspace/skills
clawhub link email-sender-policy  # symbolic link

# 發布到 ClawHub
clawhub publish
```

---

## 📖 **範例 Usage**

### 案例 A：行銷電子報
```bash
email-sender-policy send \
  --to "subscriber@example.com" \
  --subject "本週新內容｜產品更新與行銷技巧" \
  --body "📧 電子報內容...
  
  本周新功能：
  • 功能1：...
  • 功能2：...
  
  ⭐ 行銷建議：..."
```

### 案例 B：含表格的報告
```markdown
# 銷售報告

| 產品 | 銷量 | 成長率 |
|------|------|--------|
| AI助手 | 150 | +25% |
| 自動化工具 | 89 | +12% |
```

→ 自動轉換為：
```
# 銷售報告

• AI助手：銷量 150，成長率 +25%
• 自動化工具：銷量 89，成長率 +12%
```

---

## 🐛 **已知限制**

- ❌ 僅支援純文字內容，不支援 HTML
- ❌ 附件功能待實現（未來版本）
- ❌ 僅支援 Gmail 連接（未來擴展其他服務）
- ⚠️ 需先完成 Maton OAuth 授權

---

## 🔮 **未來藍圖**

- [ ] 支援 HTML 郵件模板
- [ ] 附件上傳功能
- [ ] 多服務支援（Outlook、SendGrid）
- [ ] 郵件模板庫
- [ ] 發送統計追蹤
- [ ] 退訂管理（GDPR 合規）

## 📈 **版本歷史**

### v2.0.1 (2026-03-17)
- ✅ **修復參數別名問題**：新增 `--bodyFile` 別名，與 `--file` 功能相同
- ✅ **提升易用性**：支援不同命名字串，減少使用錯誤

### v2.0.0 (2026-03-17)
- ✅ **新增電子報格式排版**：自動添加頭尾裝飾、分隔線
- ✅ **表格轉換優化**：支援三欄位以上合併
- ✅ **CLI 參數增強**：`--newsletter`、`--title` 參數
- ✅ **完全重寫與文件更新**

### v1.0.0 (2026-03-16)
- ✅ 初始版本
- ✅ UTF-8 Base64 標題編碼（RFC 2047）
- ✅ Markdown 表格轉清單
- ✅ RFC 822 標準郵件構建
- ✅ Gmail API 整合（Maton Gateway）

---

**維護者**：Shuttle AI
**許可證**：MIT
**ClawHub ID**：k97cc6x99pbra5535jb0eb2269832z2v
