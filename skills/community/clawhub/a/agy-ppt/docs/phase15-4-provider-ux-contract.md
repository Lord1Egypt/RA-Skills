# Phase 15.4 OCR 提供者管理 UX 契約

本文件定義 Phase 15.4 的操作介面與設定治理。Phase 15.4 僅在已凍結的 Phase 15.1 `OCRProvider`、provider validation、resolution 與 fallback 契約之上提供管理 UX；不建立第二套 provider、evidence、model identity 或 fallback 系統。

## 1. 範圍與操作介面

Phase 15.4 使用 repository 現有的 Python／`argparse` 命令列慣例，提供內部 operator CLI：

```text
python3 skills/agy-ppt/scripts/manage_ocr_providers.py list
python3 skills/agy-ppt/scripts/manage_ocr_providers.py show
python3 skills/agy-ppt/scripts/manage_ocr_providers.py validate [--provider ID] [--language LANG ...]
python3 skills/agy-ppt/scripts/manage_ocr_providers.py set --scope project|user --provider ID [--allow-fallback|--no-allow-fallback]
python3 skills/agy-ppt/scripts/manage_ocr_providers.py unset --scope project|user
```

`list`、`show`、`validate`、`set` 與 `unset` 都是管理操作，不執行 OCR、不產生 `OCREvidence`、不下載模型，也不因錯誤啟動 provider fallback。輸出提供確定性 JSON，作為 operator／內部機器可讀輸出；OCR JSON schemas 仍維持 DEFERRED，此輸出不宣告為公開 frozen schema。

## 2. 設定層與解析

選擇優先序完全沿用 Phase 15.1：

1. 呼叫或 CLI 的 explicit override
2. project 設定
3. user/global 設定
4. 預設 `tesseract`

Phase 15.4 必須呼叫既有 `resolve_provider()`，不得複製解析規則。`show` 必須揭露 configured provider、effective provider、`selection_origin` 與有效 fallback 狀態。移除上層設定後自然顯露下一層，不把預設值寫入每份設定。

設定檔為最小 UTF-8 JSON object，僅允許：

```json
{"allow_fallback":false,"provider":"tesseract"}
```

欄位以排序 key、緊湊 JSON 與單一尾端換行寫出。`provider` 必須是 Phase 15.1 既有 provider ID；`allow_fallback` 必須是 boolean。未知／重複／型別錯誤欄位拒絕。專案設定預設位於 repository root 的 `.agy/ocr-provider.json`；user/global 設定預設位於 platform-neutral operator config root 下的 `agy-ppt/ocr-provider.json`，可由呼叫端以明確路徑注入。測試必須只使用暫存位置，禁止讀取開發者真實 home。

路徑是 operator state，不屬 canonical provenance，也不得出現在確定性 JSON。Project 路徑必須在已解析的 project root 內；user 路徑必須在已解析的 user config root 內。禁止 traversal 與 symlink target 寫入。

## 3. Provider discovery 與註冊邊界

`list` 僅列出呼叫端交付的受信任 frozen registry。每筆資料包含可由既有契約確定的 provider ID、contract availability、provider/engine version availability、capabilities、execution location、source privacy 與 default 狀態。排序固定依 provider ID。

註冊只允許應用程式受信任程式碼建立 `Mapping[str, OCRProvider]` 並注入管理層；provider ID 必須等於 registry key。設定檔不能指定 Python module、entry point、檔案路徑、shell command、URL 或任意載入器。Phase 15.4 不實作 cloud credential transport、動態 plugin protocol、遠端程式碼下載、PaddleOCR 或 Apple Vision adapter。

## 4. 驗證與診斷

`validate` 重用 Phase 15.1 `validate_provider()` 與 provider 自有的非 OCR runtime probe。驗證可以檢查：provider 存在、contract/capabilities、可執行環境、版本、支援版本、必要 model identity 與語言能力。Tesseract 可使用既有 version 與 traineddata discovery；不得呼叫 `recognize()`。

錯誤保留既有 machine code，包括 `OCR_PROVIDER_NOT_FOUND`、`OCR_PROVIDER_CONTRACT_INVALID`、`OCR_PROVIDER_CAPABILITY_MISSING`、`OCR_PROVIDER_VERSION_UNAVAILABLE`、`OCR_PROVIDER_VERSION_UNSUPPORTED`、`OCR_MODEL_CHANGED`、`OCR_MODEL_UNAVAILABLE` 與 `OCR_LANGUAGE_UNSUPPORTED`。人類訊息必須有界、穩定且不含任意 subprocess stderr、credential、環境 dump 或 host path。

## 5. Fallback UX

Fallback 預設為 `false`，只能由 operator 顯式設定為 `true`。有效設定必須清楚顯示 primary provider 與唯一 default fallback `tesseract`；不得建立 provider chain。管理操作本身不執行 fallback。實際 OCR 仍完全沿用 Phase 15.1：terminal failure 不 fallback，僅 eligible operational failure 在 `allow_fallback=true` 時最多 fallback 一次。

## 6. Secret policy

Phase 15.4 不建立 credential store。Project/user 設定不得包含 token、password、API key、credential value 或原始 secret environment variable。Provider 可由既有安全執行環境取得必要 secret；validation 只能回報 presence/capability，不能讀出或顯示值。Secret 不得出現在 list/show/validate、error、diagnostic、canonical serialization 或 `OCREvidence`。

## 7. 安全寫入

`set` 與 `unset` 必須在 replace 前完成 schema、provider 與路徑驗證。寫入採同目錄、權限受限的 temporary file，加上 flush/fsync 後以 atomic replace 完成；失敗不得留下部分設定。必須保存支援且未被變更的設定欄位，禁止 duplicate keys。`unset` 只移除 Phase 15.4 擁有的設定檔，並安全清理由它建立且已空的 `.agy` 目錄。

不得使用 `shell=True`、shell template、pickle、network discovery、任意 module import、hidden download 或 unrestricted diagnostics。

## 8. 階段邊界

Phase 15.4 不修改 Phase 15.1 provider execution/evidence/fallback 語意，也不修改 Phase 12/13、Phase 15.2 或 Phase 15.3 frozen baseline。Phase 15.5 grounding、Phase 15.6 live/release validation 與 OCR JSON schemas 均維持 DEFERRED／NOT STARTED。
