# 大綱、風格與樣張

預設互動式簡報流程必須依序通過三個使用者核准 gate：

```text
REQUEST
  -> OUTLINE_PENDING_APPROVAL
  -> STYLE_PENDING_APPROVAL
  -> SAMPLE_PENDING_APPROVAL
  -> FULL GENERATION
```

AGY 擁有流程與核准狀態；圖片 worker 只執行單頁 job，不能核准、跳過或推進 gate。

內部狀態名稱供實作、恢復與測試使用。正常使用者對話應以「確認大綱」、「確認視覺
方向」、「確認樣張」和「完成簡報」等自然語言呈現，不顯示 gate 編號、狀態常數、
狀態檔案或 worker dispatch 細節。

## 大綱

AGY 先建立 `outline.md`，至少包含：

- 簡報目的
- 受眾
- 頁數
- 每頁角色
- 每頁標題
- 核心訊息
- 必要資料／素材

AGY 此時只交付大綱供使用者確認。使用者要求修改時只更新規劃內容並再次請求核准；
不得先定稿風格、生成樣張或產生整套簡報。

## 視覺風格與文字密度

AGY 選擇一套統一 visual system，但不要求每頁使用完全相同 layout。

風格應涵蓋：

- 色彩
- 字型感
- 影像型別
- 留白密度
- 資訊密度與分區策略
- 圖表／卡片語言

只有已核准的大綱可以進入風格確認。AGY 以精簡、可判斷的方式呈現 visual direction、
typography、palette、density、影像處理與語氣，使用者核准後才可生成樣張。

## WHAT 與 HOW 的權責

`outline.md` 是簡報 **WHAT** 的權威來源：頁序、每頁目的、標題、敘事結構、核心訊息、
實例與事實主張。`deck_spec.json` 是 **HOW** 的視覺規格：方向、色彩、字體、留白、
版式語言、照片／插圖處理、圖像比例、卡片樣式及資訊密度的呈現方法。

deck spec 可包含供 renderer 使用、從核准大綱衍生的標題與重點，但這些欄位不是另一份
內容權威。風格產生或修訂不得藉此回寫、濃縮或改變核准大綱；若需短版顯示文字，應留在
衍生的 render 輸入層。

## 修訂語意

- **STYLE**：純視覺回饋只更新 HOW。大綱 revision 與核准保持有效；style、sample
  核准失效，重新確認風格後只生成一張新樣張。「金融雜誌風」、「淺色背景」、「照片
  大一點」、「視覺上少字」與「增加留白」均屬此類。
- **CONTENT**：頁序、頁數、標題含義、受眾、論點、實例、主題或 story arc 改變時，
  更新 WHAT 並撤銷 outline、style、sample 的相依核准，回到大綱確認。
- **MIXED**：同一則回饋同時包含內容與風格要求時，採 CONTENT 路徑，先重新確認大綱。

AGY 負責將使用者意圖分類成上述結構化類別；deterministic workflow 不做自然語言猜測。
純 STYLE 呼叫若夾帶 outline payload 必須拒絕，避免隱藏內容異動。

### 文字密度與排版原則

- **不設定固定字數上限**：AGY 不得單純因字數多而強制拆頁、刪除文字或縮寫權威文案（authoritative text）。文字內容完整性優先。
- **已驗證範圍**：Phase 8A 實測已驗證目前系統至少能穩定處理約 79～239 字／頁的高密度繁體中文內容（此為已驗證成功範圍，而非系統限制）。更高文字量依實際 Visual QA 判斷。
- **高文字量優先調整版型**：若文字量較高，優先採用雙欄、2×2、2×3、多區塊卡片、比較矩陣、Checklist、流程圖、階梯或 Framework 分區佈局，避免預設使用易壅塞的單欄長條列。
- **Regenerate 優先於拆頁**：若排版過密或字級不佳，先透過 `regenerate` 要求 Codex 採用更合適之高密度版型；僅在確定單頁無論如何無法清晰容納時才允許拆頁。

## 樣張

在大量生圖前，先準備一個有代表性的 slide job，交給 Codex。預設穩定選擇大綱中
第一張非 cover/title 的內容頁；若沒有非封面頁則選第一頁。使用者可明確指定另一頁。

樣張用來驗證：

- 字是否可讀
- 資訊密度與版面佈局是否合理
- 視覺風格是否正確
- 圖文比例是否符合預期
- required asset 是否能被正確保留

樣張必須走實際單頁生成路徑，每次 sample attempt 只生成一張；不得先生成整套後只顯示
其中一張。最終是否接受樣張由 AGY／使用者決定，不由 Codex 決定。樣張生成失敗時
維持 `SAMPLE_PENDING_APPROVAL`，不得開始完整生成。

## 核准失效與恢復

- 大綱變更：`outline`、`style`、`sample` 的相依核准失效，從大綱重新確認。
- 風格變更：`style` 與 `sample` 核准失效，必須確認風格並重新生成一張樣張。
- 樣張變更：`sample` 維持未核准，直到修訂後的單張樣張再次通過。
- 完整生成失敗：保留仍屬目前 revision 的核准；只有失敗顯示規劃必須變更時才使相依 gate 失效。

`project_state.json` 的 gate metadata 保存 outline/style revision fingerprint 與樣張相依
revision。恢復 session 時只有與目前 deck plan 相符的核准可以重用，其他 deck 或舊 revision
的核准一律無效。完整生成的必要條件是：

```text
outline_approved == true
AND style_approved == true
AND sample_approved == true
```

完整簡報沿用已核准樣張的 typography、palette、spacing、visual language、image treatment
與元件樣式；每頁可以採用不同結構，但不得在核准後無聲改換整套設計方向。

## 對話與 QA 呈現

風格確認只摘要 HOW，不重新列出整份投影片內容。樣張回覆提供真實樣張並簡短詢問版面、
色調與文字密度；沒有實際警示時不附冗長 Visual QA 報告。完成回覆優先提供 PPTX 與必要
預覽。

使用者可見的 QA 結論只描述實際完成的檢查。不得把「已檢查可讀性」擴張為「完全無
擁擠」，也不得在沒有對應 deterministic 證據時宣稱「逐字完全無錯」或「百分之百正確」。
