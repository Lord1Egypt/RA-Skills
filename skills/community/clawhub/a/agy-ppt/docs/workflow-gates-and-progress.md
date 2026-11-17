# Workflow Gates 與進度控制

## Gate 1：需求與輸入

確認：

- source material
- audience
- goal
- page count
- required assets
- forbidden changes

## Gate 2：大綱

AGY 建立 `outline.md`。

原則：
- 文字內容完整性優先，**不設定固定字數上限**。不得單純因字數多而強制拆頁、刪字或縮寫。
- 若特定頁面資訊量較大，在規劃階段即應預先考量雙欄、2×2、2×3、卡片矩陣、流程或 Checklist 等結構化版型。
- 必須把大綱交給使用者核准；未核准前不得進入風格、樣張或完整生圖。

## Gate 3：視覺方向

AGY 定義 style system。

只有大綱核准後才能進入此 gate。AGY 必須讓使用者確認 style system；未核准前不得
生成樣張或完整簡報。風格異動會使既有樣張核准失效。

## Gate 4：圖片 backend 可用性

確認 Codex `$imagegen` / built-in `image_gen` 可用。

不可用時：

```text
IMAGE_BACKEND_UNAVAILABLE
```

## Gate 5：樣張

大綱與風格核准後，生成第一張適合的非封面內容頁（或使用者指定頁）作為代表性樣張，
AGY QA 並交由使用者核准。每次只生成一張真實 slide，不得預先生成整套。

## Gate 6：批次生成

只有目前 outline/style/sample 三個 gate 均已核准時，AGY 才建立其餘 jobs 並逐頁派 Codex。
任何大綱修改會使三者回到待確認；任何風格修改會使 style/sample 回到待確認；樣張修改
後 sample 維持待確認。

## Gate 7：整套 QA（Visual QA）

檢查：

- **文字正確性**：逐字核對權威文案（authoritative text），繁體字形正確無錯字、無漏字、無多字、無簡體字、無亂碼。
- **排版與可讀性**：字級清楚可讀、無裁切、無重疊、長句換行合理、保留足夠留白。
- **文字密度判定原則**：
  - 不以硬性字數門檻（如 240 / 300 字）判定失敗；Phase 8A 已實證系統至少可穩定處理約 79～239 字／頁（已驗證成功範圍）。
  - 只要文字精確、排版清楚、閱讀動線舒適，即可判定 `qa_passed`。不得僅因「文字很多」判失敗。
- **Regenerate 優先於拆頁**：若排版太擠或間距不佳，先由 AGY 判定 `qa_failed -> ready -> regenerate` 要求 Codex 調整版型。僅在單頁確定無法清晰容納時才允許拆頁。
- **資料完整性與風格**：事實無誤、required assets 完整保留、整份簡報風格嚴格一致。


## Gate 8：組裝

執行既有 assembly script。

## 工程插入點

任何 gate 遇到「需要修改 executable code」：

```text
目前 phase 暫停
 -> AGY 建立 engineering task
 -> Kiro
 -> 回 AGY
 -> 驗收後恢復原 phase
```
