\---

name: Claw\_OpenWebUI\_API
slug: claw-openwebui-api
author: kuanlin.huang
version: 1.0.3
description: |
整合 Open WebUI RAG 知識庫 API，讓 OpenClaw 能自動上傳文件和查詢知識庫。
triggers:

* "openwebui"
* "rag"
* "知識庫"
* "上傳文件"
* "搜尋知識庫"
metadata:
openclaw:
emoji: "🦞"
requires:
env: \["OPENWEBUI\_URL", "OPENWEBUI\_API\_KEY"]
bins: \["python3", "requests"]
install:

  * id: pip
kind: pip
package: requests
label: Install requests library

\---

# Claw\_OpenWebUI\_API

讓 OpenClaw 調用 Open WebUI 的 RAG 知識庫 API。

## 功能

* 📤 上傳文件到知識庫
* 🔍 搜尋知識庫
* 💬 對話時自動引用知識庫
* 📊 列出知識庫內容

## 前置需求

1. Open WebUI 已安裝並運行
2. 已建立知識庫
3. 取得 API Token

## 安裝

```bash
# 安裝技能
git clone https://github.com/你的帳號/Claw\\\_OpenWebUI\\\_API.git \\\~/.openclaw/workspace/skills/Claw\\\_OpenWebUI\\\_API
```

## 設定

### 環境變數（必須設定）

```bash
# 必需設定環境變數
export OPENWEBUI\\\_URL="http://你的伺服器IP:3000"
export OPENWEBUI\\\_API\\\_KEY="你的API\\\_Token"
```

### 取得 API Token

1. 登入 Open WebUI
2. 進入設定 → 帳號
3. 產生 API Token

### 或設定檔

編輯 `\\\~/.openclaw/openclaw.json`：

```json
{
  "skills": {
    "Claw\\\_OpenWebUI\\\_API": {
      "url": "http://192.168.0.176:3000",
      "api\\\_key": "your\\\_api\\\_token"
    }
  }
}
```

## 使用方式

### 🚀 OpenClaw 指令（自然語法）

安裝技能後，可以直接用自然語法呼叫：

```
# 設定環境變數（只需設定一次）
小蝦，設定 OPENWEBUI\\\_URL 為 http://127.0.0.1:3000
小蝦，設定 OPENWEBUI\\\_API\\\_KEY 為 your-jwt-token

# 上傳檔案到知識庫
小蝦，上傳 note.txt 到知識庫 test3
小蝦，把 report.pdf 上傳到知識庫 mydocs

# 列出知識庫
小蝦，列出所有知識庫
小蝦，有哪些知識庫？

# 查詢檔案
小蝦，查詢上傳的檔案列表

# 對話（自動引用知識庫）
小蝦，用 Qwen3-4B 問關於 test3 的內容
```

### 📝 Bash 指令（直接執行）

```bash
# 設定環境變數
export OPENWEBUI\\\_URL="http://127.0.0.1:3000"
export OPENWEBUI\\\_API\\\_KEY="your-jwt-token"

# 列出知識庫
\\\~/.openclaw/workspace/skills/Claw\\\_OpenWebUI\\\_API/claw-openwebui.sh list-knowledge

# 上傳檔案到知識庫（需指定知識庫名稱）
\\\~/.openclaw/workspace/skills/Claw\\\_OpenWebUI\\\_API/claw-openwebui.sh upload-rag /path/to/file.txt test3

# 發送聊天
\\\~/.openclaw/workspace/skills/Claw\\\_OpenWebUI\\\_API/claw-openwebui.sh chat "Qwen3-4B-Instruct-2507-4bit" "你好"
```

### 📜 Python 指令（可選）

```bash
# 上傳 PDF 文件
python3 \\\~/.openclaw/workspace/skills/Claw\\\_OpenWebUI\\\_API/scripts/upload.py --file /path/to/document.pdf

# 上傳多個文件
python3 \\\~/.openclaw/workspace/skills/Claw\\\_OpenWebUI\\\_API/scripts/upload.py --file file1.pdf --file file2.docx
```

### 搜尋知識庫

```bash
python3 \\\~/.openclaw/workspace/skills/Claw\\\_OpenWebUI\\\_API/scripts/search.py --query "關於 OpenClaw 的設定"
```

### 對話（知識庫增強）

```bash
python3 \\\~/.openclaw/workspace/skills/Claw\\\_OpenWebUI\\\_API/scripts/chat.py --message "如何安裝 OpenClaw?"
```

## API 端點

|方法|端點|功能|
|-|-|-|
|GET|/api/v1/models|列出模型|
|POST|/api/v1/files/upload|上傳檔案|
|GET|/api/v1/files|列出已上傳檔案|
|POST|/api/v1/rag|搜尋知識庫|

## 架構

```
Claw\\\_OpenWebUI\\\_API/
├── SKILL.md
├── scripts/
│   ├── upload.py      # 上傳文件
│   ├── search.py      # 搜尋知識庫
│   ├── chat.py        # 對話+知識庫
│   └── list\\\_files.py  # 列出檔案
└── README.md
```

## 範例

### Python 程式碼

```python
import requests

OPENWEBUI\\\_URL = "http://192.168.0.176:3000"
API\\\_KEY = "your\\\_token"

headers = {
    "Authorization": f"Bearer {API\\\_KEY}"
}

# 搜尋知識庫
def search\\\_knowledge(query):
    response = requests.post(
        f"{OPENWEBUI\\\_URL}/api/v1/rag",
        headers=headers,
        json={"query": query}
    )
    return response.json()

# 上傳檔案
def upload\\\_file(file\\\_path):
    with open(file\\\_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            f"{OPENWEBUI\\\_URL}/api/v1/files/upload",
            headers=headers,
            files=files
        )
    return response.json()
```

## 常見問題

### Q: 需要認證嗎？

A: 是的，需要從 Open WebUI 取得 API Token

### Q: 支援哪些檔案格式？

A: PDF、Word、Excel、PPT、TXT、Markdown 等

### Q: 如何取得 API Token？

A: 登入 Open WebUI → 設定 → 帳號 → API Token

## 授權

MIT License

\---

*Author:* kuanlin.huang
*Version: 1.0.3*

