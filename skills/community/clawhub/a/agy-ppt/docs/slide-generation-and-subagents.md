# 投影片生成與 Worker

上游原本可把一頁交給一個 subagent；本 fork 將這個概念固定化為 Codex image worker。

## 一頁一個 job

每個 Codex invocation 原則上只處理一張投影片。

輸入：

```text
slide_<NN>.json
```

輸出：

```text
slide_<NN>.png
```

## Job 必須足夠封閉

AGY 應在 job 裡提供：

- slide id
- headline
- body content
- hierarchy
- visual intent
- required assets
- forbidden changes
- style reference

Codex 不應依靠「整份簡報上下文猜測」來決定內容。

## QA 分工與文字密度原則

### 分工邊界
- **Codex**：renderer-level 檢查（圖檔生成、基礎渲染）。不得擅自修改、縮減、改寫文案或刪減條列。
- **AGY**：最終 content + visual QA 擁有者。

### 文字密度與 Visual QA 判定規則
1. **不設固定字數上限**：AGY 不得僅因文字量超過某門檻就擅自拆頁、刪字或縮寫。權威文本（authoritative text）的完整性優先。
2. **實證範圍**：Phase 8A 實測已驗證目前系統至少能穩定處理約 79～239 字／頁的高密度繁體中文內容（此為已驗證成功範圍，而非硬性上限）。不建立硬性 240 / 300 字門檻，更高文字量依實際 Visual QA 判斷。
3. **QA 通過條件**：只要生成後符合：
   - authoritative text 完整且文字完全正確
   - 字級清楚可讀、無裁切、無重疊
   - 換行合理、層級清楚
   - 版面具備合理留白、閱讀舒適
   即可判定 `qa_passed`。不得因為「文字很多」本身判定失敗。
4. **高文字量版型適配**：單頁字數較多時，AGY 應引導採用雙欄、2×2、2×3、多區塊卡片、比較矩陣、Checklist、流程圖、階梯或 Framework 分區佈局，避免預設使用單欄長條列。
5. **Regenerate 優先於拆頁**：若排版太擠、字級過小或間距不足，先由 AGY 判定 `generated -> qa_failed -> ready -> regenerate` 要求 Codex 採用更合適之高密度版型。只有當 AGY 判斷單頁在維持完整文字與可讀性前提下確實無法合理容納時，才允許拆頁。

