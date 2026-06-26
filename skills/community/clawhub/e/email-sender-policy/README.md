# Email Sender Policy Skill

自動應用郵件發送標準政策，確保所有外發郵件符合格式規範。

## 🎯 **核心功能**

1. **標題 UTF-8 Base64 編碼**（RFC 2047）
   - 避免亂碼，支援所有郵件客戶端
   - 自動處理中文字、特殊符號

2. **Markdown 表格轉清單**
   - 輸入表格自動轉為項目符號清單
   - 保持閱讀流暢性

3. **RFC 822 標準格式**
   - 正確的郵件頭部與分隔
   - 使用 `\r\n` 行分隔符

4. **Gmail API 整合**
   - 使用 Maton API Gateway
   - 自動選擇當前登入連接
   - 多收件人支援

## 📦 **安裝**

```bash
cd ~/.openclaw/workspace/skills
clawhub link email-sender-policy  # 本地連結
# 或
clawhub install email-sender-policy  # 從 ClawHub 安裝（未來）
```

## ⚙️ **配置**

### 環境變數
```bash
export MATON_API_KEY="your-api-key"
```

### Gmail 授權
1. 登入 Maton: https://maton.ai/settings
2. 複製 API Key
3. 建立 Google Mail 連接：https://ctrl.maton.ai/connections
4. 選擇 `google-mail` 應用並完成 OAuth

## 🚀 **使用方法**

### CLI 直接使用
```bash
# 基本發信
email-sender-policy --to "user@example.com" --subject "報告" --body "內容..."

# 多收件人
email-sender-policy -t "a@x.com,b@x.com" -s "會議通知" -b "會議時間..."

# 從檔案讀取（表格自動轉換）
email-sender-policy -t "team@company.com" -s "週報" -f "weekly.md"

# 測試模式（驗證格式，不發送）
email-sender-policy -t "test@x.com" -s "測試" -b "內容" --test
```

### 作為 Subagent 呼叫
```javascript
// 在其他技能中嵌入此政策
const result = await sessions_spawn({
  runtime: "subagent",
  label: "email_sender",
  task: `
    email-sender-policy send
      --to "${recipient}"
      --subject "${subject}"
      --body "${content}"
  `
});
```

## 🔄 **表格轉換規則**

### 輸入示例
```markdown
# 銷售報告

| 產品 | 銷量 | 成長率 |
|------|------|--------|
| AI助手 | 150 | +25% |
| 自動化工具 | 89 | +12% |
```

### 輸出結果
```
# 銷售報告

• AI助手：銷量 150，成長率 +25%
• 自動化工具：銷量 89，成長率 +12%
```

**轉換邏輯**：
- 移除分隔線（`|---|`）
- 每行資料轉為項目符號開頭
- 多欄位合併為單一句子

## 📧 **RFC 2047 編碼示例**

### 原始標題
```
【重要】本週行銷會議延期通知
```

### 編碼後
```
=?utf-8?b?4ouG5a657NGW5Lik5Iqx5YGa5qCh5ou86ZKf?=
```

所有郵件客戶端（Gmail、Outlook、Apple Mail）皆能正確顯示。

## 🧪 **測試**

```bash
# 1. 驗證 RFC 822 格式（不發送）
email-sender-policy --to "test@example.com" --subject "測試標題" --body "內容" --test

# 2. 檢查政策轉換
echo "| A | B |\n|---|---|\n| 1 | 2 |" | email-sender-policy --format-only

# 3. 完整發送測試
email-sender-policy -t "yourself@example.com" -s "Policy Test" -b "Hello world" --test
```

## 📊 **政策對照表**

| 政策名稱 | 舊方式 | 新方式（此 skill） |
|---------|--------|-------------------|
| 標題編碼 | 無編碼 → 亂碼 | UTF-8 Base64 → 正常 |
| 表格格式 | 原樣發送 → 排版錯亂 | 轉清單 → 易讀 |
| 電子報排版 | 手動製作 → 不統一 | 自動裝飾 → 專業 |
| 行分隔符 | `\n` 可能出問題 | `\r\n` 符合 RFC 822 |
| 連接選擇 | 手動指定 | 自動使用當前登入 |

---

## 📧 **電子報格式（v2.0 新增）**

### 使用方式

```bash
# 基本電子報（自動添加頭尾）
email-sender-policy -t "subscriber@example.com" \
  -s "本週 AI 新聞摘要" \
  -f "content_with_tables.md" \
  --newsletter \
  --title "🤖 AI 新聞週報｜2026年3月"
```

### 輸出格式

📧 **電子報標題**
發行日期：2026年3月17日
編輯：Shuttle AI 蝦蝦 🦐

---

（內容，已轉換表格為清單）

---

感謝您的閱讀！如有任何問題，請回信告知。

### 自訂選項

```javascript
// 可調整的參數（修改 formatAsNewsletter function）
{
  title: '自訂標題',
  issueDate: '2026年3月17日',   // 預設：今日日期
  editor: '你的名字',           // 預設：Shuttle AI 蝦蝦 🦐
  footer: '自訂結尾語',         // 預設：感謝語
  includeHeader: true,
  includeFooter: true
}
```

## 🔗 **整合範例**

### marketing-drafter + email-sender-policy
```javascript
// 1. 產生 Email 文案
const draft = await marketing_drafter.generate({
  type: 'email',
  audience: 'B2B founders',
  topic: 'AI automation trends'
});

// 2. 套用政策發送
await sessions_spawn({
  runtime: 'subagent',
  label: 'email_policy',
  task: `
    email-sender-policy send
      --to "prospect@company.com"
      --subject "${draft.subject}"
      --body "${draft.content}"
  `
});
```

## 🐛 **已知問題**

| 問題 | 狀態 | 備註 |
|------|------|------|
| HTML 郵件不支援 | ❌ | 僅限純文字 |
| 附件上傳 | ❌ | 待開發 v1.1 |
| 其他郵件服務 | ❌ | 僅 Gmail via Maton |

## 🗺️ **未來藍圖**

- [ ] HTML 模板支援
- [ ] 附件上傳
- [ ] Outlook/Exchange 支援
- [ ] 郵件追蹤（開啟率、CTR）
- [ ] 模板庫管理
- [ ] GDPR 合規退訂

## 📖 **API 參考**

### `send` 命令
```bash
email-sender-policy send [options]
```

**參數**：
- `--to, -t` (必要)：收件人，多個用逗號分隔
- `--subject, -s` (必要)：郵件標題
- `--body, -b`：郵件內容（或使用 `--file`）
- `--file, -f`：從檔案讀取內容
- `--cc`：副本
- `--bcc`：密件副本
- `--test`：測試模式

### ` convert` 命令
```bash
email-sender-policy convert --input table.md --output list.txt
```
僅執行表格轉換，不發送。

## 📄 **授權**

MIT License - 可自由使用、修改、商業用途。

## 🙏 **致謝**

- Maton.ai - OAuth 與 API Gateway
- RFC 2047 / RFC 822 標準
- OpenClaw 生態系統

---

**版本**：1.0.0  
**發布日期**：2026-03-17  
**維護者**：Shuttle AI
