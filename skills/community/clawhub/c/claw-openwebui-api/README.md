# Claw\_OpenWebUI\_API

**版本：** v1.0.3  
**更新日期：** 2026-03-15

## 📚 API 資料來源

本專案的 API 端點資訊來自 Open WebUI 官方文檔：

* **官方文檔：** https://docs.openwebui.com/
* **API 端點參考：** https://docs.openwebui.com/reference/api-endpoints/

\---

## 🎯 技能介紹

**Claw\_OpenWebUI\_API** 是一個讓 OpenClaw 可以透過 API 操作 Open WebUI 的技能。

### 主要功能：

1. **🤖 聊天互動** - 透過 API 發送對話請求到 Open WebUI
2. **📦 模型管理** - 列出所有可用模型
3. **📚 RAG 知識庫** - 上傳文件到知識庫、對話時引用知識庫
4. **🔌 API 整合** - 完整支援 Open WebUI REST API

\---

## ⚠️ 重要：API Key 設定教學

### 步驟 1：產生 API Key

1. 登入 Open WebUI (http://localhost:3000)
2. 點擊左下角 **設定 (Settings)**
3. 點擊 **帳戶 (Account)**
4. 產生 API Key

### 步驟 2：設定環境變數

```bash
export OPENWEBUI\_API\_KEY="您的JWT\_Token"
💻 使用方式

### 環境變數設定

```bash
export OPENWEBUI\_URL="http://127.0.0.1:3000"  # 或 http://open-webui IP:3000
export OPENWEBUI\_API\_KEY="your-jwt-token"
```

### 指令列表

|指令|功能|
|-|-|
|`./claw-openwebui.sh ping`|測試連線|
|`./claw-openwebui.sh models`|列出可用模型|
|`./claw-openwebui.sh list-knowledge`|列出知識庫|
|`./claw-openwebui.sh upload-rag <檔案> <知識庫名稱>`|上傳檔案到知識庫|
|`./claw-openwebui.sh upload <檔案>`|只上傳檔案（不上傳到知識庫）|
|`./claw-openwebui.sh chat <模型> <訊息>`|發送聊天|
|`./claw-openwebui.sh files`|列出已上傳檔案|

### OpenClaw 自然語法（安裝技能後）

```
小蝦，上傳 note.txt 到知識庫 test3
小蝦，列出知識庫
```

\---

## 📖 上傳檔案到知識庫 - 完整流程

### 步驟 1：確認知識庫名稱

```bash
./claw-openwebui.sh list-knowledge
```

輸出：

```
📚 知識庫列表：
  • test3 (ID: XXXXXXXXXXXXX)
  • test2 (ID: AAAAAAAAAAAA)
```

### 步驟 2：上傳檔案到知識庫

```bash
./claw-openwebui.sh upload-rag /path/to/file.txt test3
```

**注意：**

* 必須指定知識庫名稱（不可省略）
* API 會根據 JWT Token 自動過濾使用者有權限的知識庫
* 如果知識庫名稱不存在，會顯示錯誤訊息

\---

## ❓ 常見問題

### Q: 為什麼要指定知識庫名稱？

A: 因為每個使用者的知識庫權限不同，API 會根據 JWT Token 自動過濾可存取的知識庫。

### Q: 如何知道有哪些知識庫？

A: 使用 `./claw-openwebui.sh list-knowledge` 指令列出。

### Q: 知識庫名稱不存在會怎樣？

A: 會顯示錯誤訊息，列出可用的知識庫名稱。

### Q: 需要認證嗎？

A: 是的，需要從 Open WebUI 取得 API Token。

\---

## 🔧 環境變數

|變數|說明|預設值|
|-|-|-|
|OPENWEBUI\_URL|Open WebUI URL|http://127.0.0.1:3000|
|OPENWEBUI\_API\_KEY|JWT Token|(必填)|

> ⚠️ \*\*注意：\*\* 如果 Open WebUI 不是運行在本機，請將 IP 改成對應的區網 IP

\---

**License:** MIT  
**Author:** kuanlin.huang

