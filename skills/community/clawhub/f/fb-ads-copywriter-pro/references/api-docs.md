# FB Ads Copywriter Pro - API 文檔

## GLM-4-Flash API

### 端點

```
POST https://open.bigmodel.cn/api/paas/v4/chat/completions
```

### 請求頭

```json
{
  "Authorization": "Bearer YOUR_API_KEY",
  "Content-Type": "application/json"
}
```

### 請求體

```json
{
  "model": "glm-4-flash",
  "messages": [
    {
      "role": "system",
      "content": "你係一個專業的 Facebook 廣告文案專家，擅長粵語文案創作。"
    },
    {
      "role": "user",
      "content": "請為維 C 精華生成一個 FOMO 風格的廣告文案..."
    }
  ],
  "temperature": 0.7,
  "max_tokens": 2000
}
```

### 響應

```json
{
  "choices": [
    {
      "message": {
        "content": "{JSON 格式的廣告文案}"
      }
    }
  ]
}
```

## Resend Email API

### 端點

```
POST https://api.resend.com/emails
```

### 請求頭

```json
{
  "Authorization": "Bearer YOUR_RESEND_API_KEY",
  "Content-Type": "application/json"
}
```

### 請求體

```json
{
  "from": "Vic AI Company <onboarding@resend.dev>",
  "to": ["client@example.com"],
  "subject": "您嘅廣告文案已準備好！",
  "html": "<html>...</html>"
}
```

## Telegram Bot API

### 發送消息

```
POST https://api.telegram.org/bot{BOT_TOKEN}/sendMessage
```

### 請求體

```json
{
  "chat_id": "YOUR_TELEGRAM_CHAT_ID" // 從環境變量 TELEGRAM_CHAT_ID 獲取,
  "text": "消息內容",
  "parse_mode": "HTML"
}
```

## 錯誤處理

### GLM API 錯誤碼

| 錯誤碼 | 說明 | 解決方法 |
|--------|------|----------|
| 401 | 未授權 | 檢查 API Key |
| 429 | 請求過多 | 等待後重試 |
| 500 | 服務器錯誤 | 稍後重試 |

### Resend API 錯誤碼

| 錯誤碼 | 說明 | 解決方法 |
|--------|------|----------|
| 403 | 禁止訪問 | 驗證域名 |
| 422 | 參數錯誤 | 檢查請求格式 |
| 429 | 請求過多 | 等待後重試 |

## 限額

### GLM-4-Flash

- **免費版：** 100 次/日
- **付費版：** 無限制
- **速率限制：** 10 次/秒

### Resend

- **免費版：** 100 封/日
- **付費版：** 3,000 封/月 起
- **速率限制：** 視計劃而定

### Telegram Bot

- **免費：** 無限制
- **速率限制：** 30 次/秒

## 最佳實踐

1. **錯誤重試：** 實現指數退避重試機制
2. **緩存：** 緩存常用文案模板
3. **日誌：** 記錄所有 API 調用
4. **監控：** 監控 API 使用量和錯誤率
5. **降級：** API 失敗時使用本地模板
