# Phase 18 — Delivery Fidelity, Portability & Intelligent Editability

中文意義：**交付忠實度、環境相容性與智慧可編輯性**

> 狀態：**DEFINED / NOT STARTED**
>
> 本文件只定義 Phase 18 的 architecture、internal contracts 與 future acceptance baseline。
> Phase 18 runtime 尚未實作，Phase 18.1 尚未開始；本定義不修改 Phase 12–17 frozen semantics，
> 不發布 public schema，也不啟動 Phase 19。

## 1. North Star and Product Boundary

Phase 18 的正式 North Star 是：

> A delivered presentation should preserve its approved visual quality across
> realistic client environments, while keeping business-critical content editable
> wherever editability can be provided safely.

Phase 18 建立的不是「全部拆成 PowerPoint 元件」的目標，而是經過取捨的交付品質：

```text
Visual fidelity first. Editability where safe.
```

同時凍結：

```text
Native PowerPoint objects are an implementation tool, not the goal.
```

Phase 16 已凍結 evidence、provenance 與 Human Editorial；Phase 17 已凍結 audience、narrative、
visual communication、delivery 與 effectiveness。Phase 18 只能決定如何忠實、可攜、可維護地
交付已核准的簡報，不得重新解釋內容、證據、敘事或視覺方向。

## 2. Frozen Priority Order

任何 production 或 QA trade-off 都必須遵循以下優先順序：

1. **Evidence Integrity**
2. **Approved Semantic Meaning**
3. **Visual Fidelity**
4. **Portability**
5. **Business-critical Editability**
6. **Native PowerPoint Object Coverage**

因此：

- evidence-bound number 不得為了 fit 或 native conversion 而改值；
- 不得以提高 native-object ratio 為由改變 approved WHAT 或 HOW；
- native-object percentage 不是 product KPI，也不是 QA score；
- 無法同時保證 arbitrary editability 與 visual stability 時，應誠實限制可編輯範圍，而不是降低
  已核准視覺品質。

## 3. Editability Classes

`EDITABILITY_CLASS` 是 internal planning concept，不是本階段發布的 public stable schema，正常
使用者不會看到下列 labels。

### `EDITABLE_REQUIRED`

對 business use 重要、必須維持合理可編輯性的內容，例如：

- names、titles、dates、prices；
- KPI values；
- contact information；
- CTA text。

### `EDITABLE_PREFERRED`

在 portability 與 fidelity 風險可接受時應保留 editable，例如 ordinary titles、body copy 與
table content。

### `REPLACEABLE`

不要求拆解內部結構，但應易於替換，例如 logos、portraits、product photos 與 case-study
images。

### `LOCKED_PREFERRED`

視覺穩定性通常比 native editing 更重要，例如 artistic headlines、tightly composed display
typography 與 highly stylized visual groups。

### `LOCKED_REQUIRED`

暴露內部結構會實質降低設計或交付可靠性，因此應保持 locked，例如 AI-generated artwork、
complex compositing、textures、sophisticated lighting 與 irregular artistic graphics。

這些 classes 表達「使用者應如何維護元素」，不直接指定元素如何產製。

## 4. Production Strategies

`PRODUCTION_STRATEGY` 與 `EDITABILITY_CLASS` 是兩個正交維度，不得 collapse 或以一者推定另一者：

- `NATIVE_TEXT`
- `NATIVE_SHAPE`
- `NATIVE_IMAGE`
- `NATIVE_CHART`
- `VECTOR_GRAPHIC`
- `RASTER_REGION`
- `LOCKED_VISUAL`
- `FULL_RASTER_SLIDE`

同一 editability class 可依 font、layout、client environment 與 fidelity risk 採不同 strategy。
例如 `EDITABLE_REQUIRED` 的 KPI 通常是 `NATIVE_TEXT`，但其裝飾背景可以是 `LOCKED_VISUAL`；
`REPLACEABLE` logo 通常是 `NATIVE_IMAGE`。`FULL_RASTER_SLIDE` 是必要時的明確 fallback，既不是
預設，也不是失敗；Phase 18 同樣不要求 fully-native slide。

## 5. Editability Envelope

`Editability Envelope` 定義一個 editable element 在哪些變更範圍內可合理維持 layout stability。
它可以包含：

- expected text-length range；
- expected line count；
- minimum / maximum font-size behavior；
- overflow behavior；
- crop behavior；
- replacement aspect ratio；
- layout tolerance。

Envelope 是可驗證的維護契約，不是任意替換保證。Envelope 內的修改應維持既定 tolerance；超過
envelope 時可以產生 warning、要求 layout review 或採明確 overflow behavior，不得靜默截字、改變
meaning 或假稱 layout 無影響。

## 6. Font Portability

Font portability 是 Phase 18 的 first-class concern：

### `FONT_SAFE`

適合在預期 client environment 中以 native editable form 使用。

### `FONT_FALLBACK_TOLERANT`

即使被 fallback typography 替代，也因已保留足夠 envelope 與 layout tolerance，不會造成
catastrophic reflow。

### `FONT_CRITICAL`

視覺或 layout integrity 明顯依賴指定 font。除非 delivery environment 能保證字型，通常應使用
locked visual treatment，或清楚標示 portability requirement。

Phase 18 不以 editability 為名強迫所有高品質 display typography 改用普通字型。Production plan
必須把 font availability、glyph coverage、Chinese/English metrics 與 fallback behavior 納入風險，
但不得將尚未實測的 font 宣稱為 portable。

## 7. Delivery Profiles

Delivery profile 是 internal default/constraint bundle，不是新的 approval gate。

### `FIDELITY`

優先維持 visual consistency 與 portability，只在明確有用且安全時使用 native/editable objects。

### `BALANCED`

預設 profile。維持高視覺品質，同時使 business-critical text 與重要 images/assets 可編輯或可替換。

### `EDITABILITY_PRIORITY`

適用於 reusable company templates、monthly reports、training materials 與 frequently maintained
decks；允許更多 native objects，但仍不承諾 100% native editability，也不得越過 evidence、meaning、
fidelity 與 portability 的優先順序。

## 8. Phase 18.1 — Delivery & Editability Contract

> **NOT STARTED**

Phase 18.1 將在 implementation 前先凍結 repository-owned internal contracts：

- editability class；
- production strategy；
- font portability risk；
- editability envelope；
- delivery profile；
- portability risk；
- replacement semantics。

`replacement semantics` 至少應說明可替換的內容、預期 aspect/crop behavior、是否保留 masking/frame、
超出 envelope 時的 deterministic outcome，以及不允許改變的 evidence/semantic fields。Invalid
construction 必須 fail closed，不得 fuzzy correction、silent fallback 或引入 public schema。

## 9. Phase 18.2 — Element Production Planning

> **NOT STARTED**

Phase 18.2 將 approved slide plan 轉成 element-level production plan。每個適用 element 應能攜帶：

- semantic role；
- editability class；
- production strategy；
- font risk；
- portability risk；
- replacement behavior；
- layout tolerance。

概念例：

| Element | Editability | Strategy |
| --- | --- | --- |
| Name | `EDITABLE_REQUIRED` | `NATIVE_TEXT` |
| Logo | `REPLACEABLE` | `NATIVE_IMAGE` |
| Card background | `EDITABLE_PREFERRED` | `NATIVE_SHAPE` |
| Hero artwork | `LOCKED_REQUIRED` | `RASTER_REGION` / `LOCKED_VISUAL` |

Production planning 只映射已核准的 Phase 16 claims/evidence 與 Phase 17 narrative/visual intent。它不得
改寫 evidence-bound values、takeaway、narrative role、visual hierarchy 或 approved style。

## 10. Phase 18.3 — Hybrid PowerPoint Production

> **NOT STARTED**

Phase 18.3 的 architecture goal 是 selective hybrid PPTX production：

- business-critical content 可採 native text；
- simple geometry 可採 native shapes；
- important photography/logos 可採 replaceable image objects；
- stable vector assets 可採 SVG/vector；
- structured data 且 fidelity 足夠時可採 native charts；
- complex artwork 可採 locked raster regions。

它既不要求 full-raster slides，也不要求 fully-native slides。Production implementation 必須保持
approved sample 的 visual contract；若某 production change materially 改變外觀，必須依既有
style/sample approval semantics 處理，不得在 sample approval 後靜默用 editability 換掉 fidelity。

### Chart policy

當 structured source data 存在，且 PowerPoint-native chart 能保持 approved design quality 時，優先
使用 native chart。若 visualization 高度 editorial/artistic，native conversion 會明顯降低品質，則
hybrid 或 locked visual 可接受。無論表示方式，Phase 16 evidence-bound labels、series 與 values 必須
保持 exact；不得補造數字、改 rounding meaning 或讓 editable chart 脫離 canonical data。

### Image policy

重要 images 在實務可行時應保持 replaceable，並盡量保留 placement、crop、masking、frame 與 aspect
behavior。Complex composited imagery 可保持 locked。不得只為 production convenience 把每張 photo
或 logo 燒進 full-slide background。

### Simple-shape policy

Rectangles、rounded cards、dividers、basic labels、simple arrows 與 basic containers 通常應在安全時
採 native shapes。不得為提高 native-object count 而把 arbitrary complex artwork 強制 vectorize。

## 11. Phase 18.4 — Portability & Visual Fidelity QA

> **NOT STARTED**

QA 應產生具體 issue，而不是 fake aggregate visual score。至少定義：

- `FONT_SUBSTITUTION`
- `MISSING_GLYPH`
- `TEXT_REFLOW`
- `TEXT_OVERFLOW`
- `LINE_BREAK_DRIFT`
- `OBJECT_SHIFT`
- `IMAGE_CROP_DRIFT`
- `Z_ORDER_CHANGE`
- `CHART_STYLE_DRIFT`
- `COLOR_DRIFT`

Review dimensions 至少包含：

- `CONTENT_INTEGRITY`
- `LAYOUT_INTEGRITY`
- `VISUAL_FIDELITY`
- `EDITABILITY`

Phase 16 evidence/content integrity 永遠高於 visual comparison。QA finding 應帶有具體 element、環境、
observed difference 與 severity/review routing；不得以單一百分比分數掩蓋 content defect。

### Pixel fidelity vs semantic fidelity

Pixel-perfect equality 並非所有環境下的必要條件。QA 必須區分：

- **acceptable visual drift**：例如 envelope 內且不影響 hierarchy/readability 的 harmless line break；
- **layout defect**：例如 overflow、重要物件位移、crop 改變 meaning 或 z-order 遮蔽；
- **semantic/content defect**：例如 evidence-bound number、date、label 或 claim 被改變。

一個無害的 line-break difference 可以接受；一個被改動的 evidence-bound number 永不接受。

## 12. Client Environment Qualification Matrix

Future qualification 至少涵蓋：

- Windows PowerPoint；
- macOS PowerPoint；
- expected font installed；
- safe fallback font scenario。

Matrix 應記錄實際 qualified application/environment boundary、render/open/save/reopen 結果與已知限制。
不得在未實測時宣稱支援所有 historical Office versions，也不得把單一平台結果外推成 universal
compatibility。若某環境無法以 automation 穩定驗證，應以可重複的 bounded manual qualification
記錄，而不是偽造 deterministic proof。

## 13. Phase 18.5 — Round-trip Editability & Compatibility QA

> **NOT STARTED**

Qualification pipeline：

```text
generate
  → open
  → edit
  → save
  → reopen
  → render / inspect
```

Future tests 至少包含：

- modify KPI；
- modify ordinary title within envelope；
- modify title beyond envelope；
- replace logo；
- replace photo 並驗證 crop；
- edit table；
- edit native chart data where applicable；
- save/reopen；
- fallback-font behavior；
- Traditional Chinese typography；
- English typography；
- crop stability；
- evidence-bound fact stability。

Round-trip 測試不可只檢查 PPTX 可被 parser 重新開啟；必須同時檢查 content、layout、visual fidelity
與 intended editability。Evidence-bound fact 若被修改、遺失或與 Notes/traceability 不一致，必須
視為 correctness failure。

## 14. Editability Success Definition and User UX

成功不以「所有 objects 有多少百分比 editable」衡量。Phase 18 的 meaningful criteria 是：

- business-critical fields remain editable；
- key imagery is replaceable；
- locked artwork preserves visual quality；
- client-environment drift remains bounded；
- Phase 16 factual integrity remains exact。

正常使用者不需要逐一替 object 分類。預設使用 `BALANCED`，也不重複詢問「這個物件是否要可編輯？」。
只有 use case materially 需要時，才用自然語言詢問 delivery preference，例如 reusable company
template、monthly report、team-maintained deck，或 fidelity-dominant keynote/final presentation。
Internal labels、risk enums、envelopes 與 QA constants 不預設顯示。

## 15. Development-time Jev Policy

Jev 是 Codex 底下的 first-class **development-time bounded engineering decision layer**，但不是
agy-ppt runtime。固定規則先由 deterministic code 判斷；bounded、repeated、typed 且 semantically
non-trivial 的 engineering classification 預設交給 Jev；低信心、衝突、novel 或 open-ended 問題再由
Codex 完整推理。完整 confidence、decision-record、fallback 與 authority policy 見
[Jev 開發決策層](development-jev-decision-layer.md)。
適用條件：

- output space bounded and known；
- 同一 semantic judgment 在 fixture/audit 中重複出現；
- engineering behavior 會依結果分支；
- typed、probability/confidence-aware classification 能幫助 triage。

適合的 Phase 18 development experiments 包括：

- editability-class fixture classification；
- native-vs-raster fixture classification；
- visual-diff triage；
- fidelity issue categorization；
- font-risk fixture grouping；
- compatibility outcome classification。

依 TypeSafe System One contract，Jev 的 typed output 與 calibrated probabilities 只提供 bounded
judgment；它們不等於 truth。Choice/Score confidence 反映 distribution concentration，不授權 action。
可獨立回答的 fixture questions 可一起 batch；low-confidence、novel 或高後果 cases 必須升級給 Codex
reasoning，而非自動採用。Threshold 必須用 repository fixtures 評估，不能照搬 cookbook example。

所有被採用的 engineering decision 最終都必須成為 repository-owned deterministic code、tests、
fixtures 或 documented contracts。Jev 永遠不得成為：

- runtime/product dependency；
- evidence 或 approval authority；
- CI 或 release authority。

Repository correctness 必須在沒有 Jev credentials、network 或 live access 時獨立驗證。不得 commit
Jev credential、API response containing private material、local configuration 或 `TYPESAFE_API_KEY`。

## 16. Approval Workflow Preservation

預設流程保持：

```text
Request
  → Outline approval
  → Style approval
  → one real Sample approval
  → Full Deck
```

Phase 18 不新增 default editability approval gate。若 production strategy 會 materially 改變 approved
appearance，必須沿用既有 style/sample reapproval；若會改變 WHAT、evidence 或 narrative meaning，
則不得由 Phase 18 執行，必須走既有 content revision。Sample approval 後不得靜默犧牲 fidelity 以
增加 native editing。

## 17. Frozen Subphase Definitions

下列 subphases 均已實作、測試、合併並凍結基準線：

### Phase 18.1 — Delivery & Editability Contract

**COMPLETE / MERGED / BASELINE FROZEN** — editability class、production strategy、font risk、envelope、profile、portability risk、replacement semantics。

### Phase 18.2 — Element Production Planning

**COMPLETE / MERGED / BASELINE FROZEN** — approved content 到 element-level production plan 的 deterministic mapping。

### Phase 18.3 — Hybrid PowerPoint Production

**COMPLETE / MERGED / BASELINE FROZEN** — selective native、replaceable、vector fallback、raster 與 locked production。

### Phase 18.4 — Portability & Visual Fidelity QA

**COMPLETE / MERGED / BASELINE FROZEN** — client-environment issue taxonomy、content/layout/fidelity/editability review 與無聚合評分之確定性驗證。

### Phase 18.5 — Round-trip Editability & Compatibility QA

**COMPLETE / MERGED / BASELINE FROZEN** — generate/open/edit/save/reopen/render qualification，落實 ACTUAL_CLIENT 與 STRUCTURAL_PROXY 誠實報告。

Phase 18 總體狀態：**COMPLETE / MERGED / BASELINE FROZEN**。

Phase 19：**NOT STARTED**。

## 18. Future Acceptance E2E

Future runtime implementation 至少必須通過以下 scenarios；本 architecture PR 不執行或宣稱這些
runtime E2E 已通過：

1. **Ordinary editable-text slide**：business-critical text 可編輯且 meaning/layout 完整。
2. **Photo + headline slide**：headline 策略與 replaceable photo 都符合 contract。
3. **Three-card business slide**：simple cards/shapes 在安全時保持 native，rhythm 不退化。
4. **Structured data/chart slide**：native/hybrid choice 保持 exact data 與 approved design。
5. **Complex artistic slide**：locked treatment 維持 artwork fidelity，不追求 arbitrary vectorization。
6. **Traditional Chinese slide**：glyph、font、line-break 與 fallback 行為受驗證。
7. **English slide**：font metrics 與 layout envelope 受驗證。
8. **Title edited within envelope**：save/reopen 後 layout 維持 bounded。
9. **Title edited beyond envelope**：產生明確 overflow/review outcome，不靜默破版。
10. **Logo replacement**：placement、mask、frame 與 aspect behavior 維持。
11. **Photo replacement**：crop 與 intended focal treatment 維持或產生明確 finding。
12. **Save/reopen round-trip**：PowerPoint open/edit/save/reopen 後 content 與 visual contract 保持。
13. **Fallback-font environment**：safe fallback bounded；critical font 不被誤稱 portable。
14. **Evidence-bound numeric content**：所有 representations 與 round-trip 均保持 exact。
15. **`BALANCED` profile**：business fields editable、key images replaceable、artwork stable。
16. **`FIDELITY` profile**：visual/portability 優先且 editability claims 誠實。
17. **`EDITABILITY_PRIORITY` profile**：更多 safe native objects，但不宣稱 100% native。
18. **Approved sample fidelity**：hybrid production 不靜默偏離已核准 sample。

Qualification 應使用 repository-owned、non-confidential fixtures；不得以 native-object ratio 或 fake
aggregate visual score 代替 scenario assertions。

## 19. Product Positioning

Phase 16：

> 內容有根據，呈現像人做的。

Phase 17：

> 而且真的講得動。

Phase 18 在產品概念上增加：

> 交付後也改得動，而且不因為可編輯而犧牲好看。

此 Phase 18 claim 不得在 runtime implementation、client-environment qualification 與 round-trip E2E
完成前加入 README。本 architecture PR 不修改 README product positioning。

## 20. Non-goals and Frozen Boundaries

Phase 18 明確不包含：

- Phase 16 evidence redesign；
- Phase 17 presentation-intelligence redesign；
- OCR changes 或 public OCR schema；
- orchestration redesign；
- new approval gates；
- 100% native slides requirement；
- arbitrary artwork vectorization；
- perfect pixel-equality requirement；
- PowerPoint editor replacement；
- Figma replacement；
- Illustrator replacement；
- Jev runtime dependency；
- Phase 19 implementation。

Phase 12–17 semantics 維持 frozen；AGY 仍是 sole orchestrator 與 semantic authority。Phase 18 只在
既有 approved artifact boundary 內規劃 delivery representation、portability、editability 與 QA。
