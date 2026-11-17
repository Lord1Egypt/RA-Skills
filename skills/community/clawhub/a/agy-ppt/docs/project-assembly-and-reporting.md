# 專案組裝與回報

## 專案基本結構

```text
<PPT專案>/
├── origin_image/
│   ├── slide_01.png
│   ├── slide_02.png
│   └── ...
├── prompts/
├── outline.md
├── speech.md
├── deck_spec.json
├── slide_jobs.json
├── slide_run_state.json
└── <name>.pptx
```

## 組裝

若上游既有 `scripts/assemble_ppt.py` 可正常工作，AGY 可以直接執行。

若需要修改任何 assembly behavior，AGY 可明確指派 Codex Production Engineering Worker 或 Kiro；worker 只負責工程實作並回報 AGY。

## 最終驗證

AGY 至少檢查：

- 頁數正確
- slide 順序正確
- 圖片都存在
- 無缺頁
- speaker notes 對應正確
- PPTX 可開啟
- 輸出路徑清楚

## 回報

最終由 AGY 回報：

- PPTX 路徑
- 投影片圖片目錄
- 是否有 blocker / workaround
- 是否有 engineering worker 修改過的工程專案，以及使用的 worker
