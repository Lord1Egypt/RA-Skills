# Phase 16 — Grounded Presentation Planning, Evidence Binding & Human Editorial Quality

> 中文名稱：**有根據的簡報規劃、證據綁定與人類編輯品質**
>
> 狀態：**COMPLETE / MERGED / BASELINE FROZEN**
>
> 產品定位：**Grounded enough to trust. Edited enough to present.**
>
> 中文定位：**內容有根據，呈現像人做的。**

本文件定義 Phase 16 的產品承諾、架構邊界、概念契約、子階段與驗收情境。Phase 16.1–16.5
均已實作、合併、通過整合 qualification，並以此文件記錄 baseline frozen 狀態。Phase 16
未建立公開 schema，也未改變 Phase 12–15 的既有行為。

## 1. North Star

Phase 16 同時追求兩個不可互相犧牲的承諾：

1. 簡報內容能追溯到證據。
2. 簡報的文字與視覺像經過熟練的人類簡報者有意識地編輯，而非機械式 AI 產出。

凍結的產品目標是：

> Every material factual claim derived from project sources must remain traceable
> from presentation planning through final deck generation to the original grounded
> source evidence, while AGY remains the sole semantic authority.

同時，每份簡報都應讀起來、看起來像經過熟練的人類簡報者刻意編輯。這是編輯品質目標，
不是對作者身分的判定。

## 2. Foundational Rule

```text
Evidence controls meaning. Editorial controls expression.
```

證據決定可以合理主張什麼；Human Editorial Quality 決定已核准意義如何被傳達。
編輯層可以改變措辭、節奏、標題、資訊密度與版面角色，但不得：

- 改變數值；
- 改變來源意義；
- 引入無支持的事實；
- 把 AGY synthesis 偽裝成來源直接陳述；
- 捏造引文或引用；
- 削弱或斷開 evidence binding。

任何編輯後內容都必須保持與編輯前的核准 claim 語意等價。若無法確定等價性，交回 AGY
審查，不得由 lint、renderer 或 worker 猜測。

## 3. Intended Pipeline

```text
Source
  → Acquisition / Ingestion
  → OCR / Extraction
  → Phase 12 Grounding
  → Evidence Binding
  → AGY Semantic Planning
  → Human Editorial Pass
  → Outline Approval
  → Style Approval
  → One Real Sample Approval
  → Full Deck
  → Final Traceability / Editorial QA
  → PPTX + Notes + Evidence
```

Human Editorial Pass 必須發生在語意與證據安全的規劃之後。它可以改善表達，但不得改變
事實意義。既有使用者核准流程維持 `Outline → Style → one real Sample → Full Deck`；
Phase 16 的內部嚴謹度不得增加一般使用者的工程噪音。

## 4. Authority Boundaries

### AGY

- 唯一 semantic authority 與 orchestrator；
- 解釋來源、規劃論點、決定 synthesis 與簡報敘事；
- 判斷 evidence 是否真正支持 claim；
- 審查 editorial rewrite 是否保留原意。

### OCR

- 只負責 extraction 與 evidence；
- 永遠不是語意權威；
- Phase 16 不新增 provider、不重設 OCR contract。

### Phase 12

- 維持 canonical source-grounding/reference system；
- 既有 source unit 與 locator 規則仍是唯一定位權威；
- Phase 16 只引用 Phase 12 grounded reference，不建立競爭 locator。

### Phase 16

- 把 grounded evidence 接到 presentation claim 與 plan；
- 執行 Human Editorial Quality review；
- 讓 provenance 延續到 slide、notes 與最終報告；
- 不取代 AGY 的語意判斷，也不回寫或重新定義 Phase 12。

### Slide / image workers

- 只執行已封閉的 slide instructions；
- 不決定 claim validity 或 evidence support；
- 不新增事實、不解除 blocker、不修改 evidence binding。

## 5. Content Origin Model

以下是 Phase 16 的內部概念契約，不是本階段發布的 public schema。

### `SOURCE_GROUNDED`

從專案來源證據衍生的 factual statement。每個 material claim 都需要 evidence binding，
並可沿 Phase 12 reference 追溯到 grounded source unit 與原始來源。

### `USER_PROVIDED`

由使用者直接提供的事實或主張。可以使用，但 provenance 必須與文件來源區分；系統不得
暗示它來自 project source，也不得製造不存在的 citation。

### `AGY_SYNTHESIS`

由 AGY 產生的結論、解釋、建議、框架或綜合。它可以依賴一個或多個 grounded facts，
但不得冒充來源直接陳述。若 synthesis 含有新的 factual subclaim，該部分仍須依其真正
origin 個別治理。

## 6. Claim → Evidence Binding

概念關係固定為：

```text
Presentation
  → Slide
  → Claim
  → Evidence reference
  → Phase 12 grounded source unit
  → Original source
```

Phase 16 reference 應攜帶足以解析既有 Phase 12 grounding 的 identity，而不是複製 source
unit、建立第二套 locator 或把 OCR region 提升為語意權威。Evidence binding 必須在 slide
instructions 交給 generation worker 之前確定；worker 只能使用已核准的內容邊界。

## 7. Support Policy

```text
SOURCE_GROUNDED factual claim
  → evidence REQUIRED

USER_PROVIDED claim
  → allowed with user provenance

AGY_SYNTHESIS
  → allowed as analysis / synthesis
  → must not be represented as directly sourced fact

unsupported factual statement presented as source-derived
  → BLOCK or FLAG before final generation
```

此政策不禁止所有 unsourced language：轉場、標題式摘要、建議與清楚標示的 synthesis 可以
存在。真正禁止的是把缺少支持的 factual statement 表示為 source-derived。`BLOCK` 用於
明確越過事實邊界且無法安全繼續的情況；`FLAG` 用於需要 AGY 判斷 origin、materiality 或
支持充分性的情況。Phase 16 不加入 automatic internet fact-checking。

## 8. Final Traceability and Staleness

預設 visible slide 維持乾淨，不要求每頁堆疊 citation。初始架構把完整 traceability 放在
內部資料、speaker notes 或 project reporting 中，包含 claim provenance、evidence mapping
與 Phase 12 grounded references。未來若要顯示可見 citation，必須另行明確定義，並非
Phase 16 強制交付。

來源內容或 identity 的 digest 改變時：

```text
Source digest changes
  → evidence derived from that source becomes stale
  → dependent claims become stale
  → dependent slides require revalidation
```

失效應優先依 dependency graph 精準傳播。已知不依賴該來源的 slide 不應僅因任意來源變更
而整份失效。只有無法安全解析依賴時，才可 fail closed 並擴大 revalidation 範圍；不得把
「任何來源變更即整份 deck 失效」定為一般規則。

## 9. Human Editorial Quality

`Human Editorial Quality` 是專用 Phase 16 能力，其定義是：

```text
Editorial heuristics + AGY semantic review
```

目的在減少機械、重複、過度修飾的 AI-like presentation pattern，而不是偵測作者身分。
系統不得輸出 AI probability score，也不得建立 `AI_DETECTED` 或同義狀態。

### 9.1 Copy and presentation voice

Copy review 關注：

- 自然語言與適合口說的 presentation voice；
- headline quality；
- 重複措辭與 repeated rhetorical templates；
- 不必要的 corporate jargon；
- 過度整齊的 bullet pattern；
- 過長標題、抽象詞堆疊與機械式名詞化。

「打造、賦能、共贏、深化、核心價值、關鍵引擎、高效、一站式、全方位」是值得注意的
重複／語境 signal，不是禁詞。Lint 不得因單次出現便改寫或失敗。

系統要分辨寫來「讀」的內容與寫來「講」的內容。適合口頭呈現的 deck 應避免在 notes
機械重複「在這一頁」、「接下來我們來看」、「我們可以看到」、「透過這張圖」。

### 9.2 Headline Pass

Headline Pass 評估 slide title 是否過長、過度抽象、像報告章節標題、機械式名詞化，或
沒有明確觀點。它可以把 report-like heading 改成符合 audience 與 mode 的 presentation
headline，但不能為法律、法遵、技術、科學或 executive reporting 強迫加入廣告式標題。
精確度與場合適配優先於吸睛。

### 9.3 Speaker notes

Notes 可依 presentation mode 支援 opening thought、core point、example/explanation 與
transition，但不得強迫每頁使用相同結構。Editorial review 檢查重複 boilerplate、機械轉場
與不自然口語，同時保留事實、限定語與證據邊界。

## 10. `PRESENTATION_MODE`

`PRESENTATION_MODE` 是內部 planning concept，本階段不發布 schema。初始概念 modes：

- `PITCH`
- `EXECUTIVE`
- `TRAINING`
- `SALES`
- `REPORT`
- `TECHNICAL`
- `KEYNOTE`
- `EDUCATIONAL`

Mode 調節 editorial behavior，而不是改變證據規則。例如：

- `EXECUTIVE`：直接、精簡、data/evidence forward、節制修辭；
- `SALES`：較口語、容易記憶、以 benefit 與 context 組織；
- `TECHNICAL`：容許必要術語、精確度優先、可提高 evidence density；
- `KEYNOTE`：較強視覺節奏、適度低密度、重視 narrative pacing。

Human Editorial layer 不得把一種通用「自然語氣」套用到所有簡報。

## 11. Visual Human Editorial Quality

視覺目標是：

```text
Same design system, different intentional slide roles.
```

它不是 random layout，也不是每頁重複同一 template。`Layout Rhythm` 可使用下列內部
slide-role concepts（本階段不發布 schema）：

- `HERO`
- `STANDARD`
- `DENSE`
- `LIGHT`
- `DATA`
- `QUOTE`
- `CASE`
- `PROCESS`
- `COMPARISON`

一份 deck 可以有意識地安排 Cover → Hero → Case → Data → Comparison → Quote → Process
→ CTA，同時維持 typography、palette、spacing、visual language 與 imagery treatment。

`Information Rhythm` 則規劃頁面密度的刻意變化。連續 `DENSE → DENSE → DENSE → DENSE`
可能值得 review，但不構成任意 hard limit。內容完整性與 presentation mode 仍然優先。

## 12. Editorial Lint and Bounded Repair

Deterministic editorial lint 可以產生下列 signals：

- repeated phrase count；
- repeated layout family，包含多頁連續 3-card pattern；
- 多數頁面使用相同 image position；
- 多數頁面 bullet count 完全相同；
- long headline warning；
- excessive average sentence length；
- repeated transition phrases；
- uniform information density；
- repeated structural templates。

這些 signal 是 warnings，不是無條件 validation failure。概念狀態可使用
`EDITORIAL_REVIEW_RECOMMENDED`；不得使用 `AI_DETECTED`。AGY 可以根據 lint 執行最多
**一次自動 editorial repair pass**，並重新確認 meaning/evidence integrity。禁止無上限的
lint → rewrite loop；剩餘 warnings 可保留供內部 review。

可能的內部 `Editorial QA` report 包含：

- Copy repetition
- Headline quality
- Layout rhythm
- Information rhythm
- Speaker-note naturalness
- Evidence integrity
- Unsupported factual claims

概念狀態可為 `PASS`、`WARNING`、`REVIEW_REQUIRED`。一般使用者預設看不到完整報告。

## 13. User-facing UX Boundary

一般使用者仍只經歷：

```text
Outline → approve → Style → approve → one Sample → approve → Full Deck
```

預設不顯示 evidence IDs、source unit IDs、locator structures、editorial lint internals、internal
schemas、stale dependency graphs 或 state-machine constants。只有使用者明確要求、真實診斷
需要，或交付用途確實有幫助時，才以自然語言揭露必要資訊。

## 14. Frozen Subphase Plan

下列五個子階段均已分別通過 implementation scope、contract review、deterministic tests、
exact CI 與 repository governance，並在合併後成為 frozen Phase 16 baseline。

### Phase 16.1 — Claim & Evidence Contract

**COMPLETE / MERGED / BASELINE FROZEN**（PR #43；squash merge
`b501ab2111a51f2a5980c7136fd4fb14a18320c9`）。定義並實作 claim、content origin、evidence
binding、support status、Phase 12 reference、provenance boundary 與 unsupported-claim behavior。

### Phase 16.2 — Grounded Outline Planning

**COMPLETE / MERGED / BASELINE FROZEN**（PR #44；squash merge
`a179709c2a34bad664539bc976f489c15e1f1085`）。

連接 grounded sources → AGY semantic planning → evidence-aware outline。每個 source-derived
slide plan 應知道支持它的 grounded units；user-facing outline 維持乾淨。

### Phase 16.3 — Slide-Level Evidence Binding

**COMPLETE / MERGED / BASELINE FROZEN**（PR #45；squash merge
`4fa009a02c695c351077ec6334774f5f64621c37`）。

連接 slide → content section/material claim → grounded evidence。Evidence 必須在 generation
worker 收到指令前固定；worker 永不判斷 support。

### Phase 16.4 — Human Editorial & Presentation Rhythm

**COMPLETE / MERGED / BASELINE FROZEN**（PR #46；squash merge
`b0427f6ff037f9e61dea36989c3b19d006b733fc`）。

實作 copy naturalness、headline quality、presentation voice、repetition lint、speaker-note
naturalness、layout rhythm、information rhythm、editorial warnings 與 bounded repair，且不得
改變 evidence meaning。

### Phase 16.5 — Final Deck Traceability & QA

**COMPLETE / MERGED / BASELINE FROZEN**（PR #47；squash merge
`76171a41ebb95118ba93585715c21e419c4218de`）。

把 evidence/provenance 延續到 final slide plan、PPTX、Notes 與 project reporting，驗證
support coverage、unsupported factual claims、stale evidence、provenance 與 editorial QA，
完成後才可依治理流程凍結 Phase 16 baseline。

## 15. Acceptance E2E

Phase 16 integrated qualification 已覆蓋：

1. searchable-text PDF；
2. scanned OCR PDF；
3. image OCR；
4. mixed PDF；
5. multi-source presentation；
6. user-provided factual statements；
7. AGY synthesis；
8. unsupported factual claim；
9. source changes after outline approval；
10. source changes after sample approval；
11. repetitive AI-like copy；
12. repetitive layout structure；
13. speaker notes with mechanical phrasing；
14. audience-dependent presentation modes。

Canonical E2E proof 已證明：

```text
Original PDF
  → extraction / OCR
  → Phase 12 source unit
  → AGY claim
  → evidence-aware outline
  → slide claim
  → Human Editorial Pass
  → final slide
  → PPTX Notes
  → trace back to original PDF page
```

驗收必須同時檢查 evidence integrity 與 editorial quality；後者不得以犧牲前者換取。

合併後 qualification 結果：Phase 16 focused/integrated 75/75 PASS、Phase 12 65/65 PASS、
Phase 13 206/206 PASS、Phase 15 198/198 PASS、presentation workflow 27/27 PASS、installation
2/2 PASS、recovery 10/10 PASS、full unittest discovery 976/976 PASS。Frozen guard、repository
hygiene/security 與 README parity/links 均 PASS。

## 16. Non-goals

Phase 16 明確不包含：

- 新 OCR providers；
- OCR redesign；
- 新 public OCR schemas；
- Phase 12 locator changes；
- Phase 13 ingestion redesign；
- Phase 15 contract changes；
- vector database requirement；
- RAG platform rewrite；
- automatic internet fact-checking；
- arbitrary AI detector 或 AI probability score；
- image-generation architecture redesign；
- presentation approval workflow redesign；
- citation beautification engine 作為必要交付；
- visible citation clutter by default。

OCR schemas 維持 deferred。未來任何新增 schema 都必須由其實作子階段另行定義與審查，
不得從本概念文件推定為已承諾 public contract。

## 17. Principles Carried Forward

- AGY 是唯一 semantic authority。
- OCR 只負責 extraction/evidence。
- Phase 12 是 canonical grounding/reference authority。
- Evidence determines factual boundaries。
- Human Editorial 可以改 expression，不可改 meaning。
- Workers 執行，不判斷 evidence support。
- Default user UX 保持簡單。
- Internal rigor 不構成 user-facing engineering noise 的理由。

## 18. Related Frozen Architecture

- [Source grounding](source-grounding.md)：Phase 12 canonical grounding/reference。
- [Source ingestion](source-ingestion.md)：Phase 13 ingestion boundary。
- [Phase 15 OCR architecture](phase15-ocr-architecture.md)：OCR extraction/evidence 與 frozen baseline。
- [Outline, style, and sample workflow](outline-style-and-sample.md)：v0.4.2 使用者核准流程。
- [Architecture and design rationale](architecture-and-design-rationale.md)：AGY 與 worker authority。
