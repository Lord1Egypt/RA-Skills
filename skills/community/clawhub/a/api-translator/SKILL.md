---
name: api-translator
slug: api-translator
version: 1.1.0
description: |
  將 API 文檔翻譯成繁體中文。輸入 API 文檔網址，輸出翻譯後的 API 說明。
metadata:
  openclaw:
    emoji: "📝"
    triggers:
      - 翻譯 API
      - API 文件
      - api translator
---

# API 文件翻譯助手

將 API 文檔翻譯成繁體中文（使用 LLM）。

## 使用方法

當用戶要求翻譯 API 文檔時：

1. 使用 `web_fetch` 工具抓取 API 文檔內容
2. 將內容發送給 LLM 翻譯
3. 輸出翻譯結果

## 翻譯 Prompt 模板

```
請將以下 API 文檔翻譯成繁體中文（台灣用語），保持 Markdown 格式和程式碼不變，只翻譯說明文字：

[API 文檔內容]
```

## 翻譯要求

- 保持 Markdown 格式
- 保持程式碼不變
- 只翻譯說明文字
- 使用台灣用語：
  - 軟體 → 軟體
  - 網路 → 網路
  - 數據 → 資料
  - 請求 → 請求
  - 響應 → 回應
  - 錯誤 → 錯誤
  - 認證 → 驗證
  - 授權 → 授權
  - 終端 → 端點

## 增強功能 (v1.1.0)

### 支援格式
- HTML 網頁 (自動提取內容)
- JSON API 回應
- Markdown 文件

### 翻譯選項
| 參數 | 說明 |
|------|------|
| --format | 輸出格式 (markdown/json/txt) |
| --preserve-code | 是否保留程式碼 (預設 true) |
| --taiwan | 使用台灣用語 (預設 true) |

### 批次翻譯
支援多個 URL 批次翻譯：
```
翻譯以下 API 文檔：
- https://example.com/api/v1/docs
- https://example.com/api/v2/docs
```

## 範例

**輸入：** 用戶給你 https://platform.openai.com/docs/api-reference/introduction

**輸出：** 翻譯後的繁體中文 API 文檔

---

*本技能由 OpenClaw 團隊開發*
