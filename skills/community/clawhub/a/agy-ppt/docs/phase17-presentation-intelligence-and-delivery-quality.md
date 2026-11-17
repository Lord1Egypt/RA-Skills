# Phase 17 — Presentation Intelligence & Delivery Quality

中文意義：**簡報策略智能與實際呈現品質**

> 狀態：**COMPLETE / MERGED / BASELINE FROZEN**
>
> 本文件記錄已合併的 Phase 17 runtime、內部概念契約與驗收 baseline。Phase 17 未發布
> public schema，未改動 Phase 12–16 frozen contract；Phase 18 尚未開始。

## 1. Product Layering

產品能力依序建立三個不可互相取代的層次：

```text
Trust → Human Quality → Effectiveness
```

- **TRUST（Phase 16）**：source grounding、evidence binding、provenance 與 factual integrity。
- **HUMAN QUALITY（Phase 16）**：Human Editorial、自然語言、layout rhythm 與 information rhythm。
- **EFFECTIVENESS（Phase 17）**：audience-specific communication strategy、narrative progression、
  visual communication、timing 與 delivery readiness。

Phase 17 的正式 North Star 是：

> Every presentation should have a clear audience, purpose, desired outcome,
> narrative progression, slide-level intent, time budget, and delivery plan,
> while preserving all approved semantic meaning and Phase 16 evidence guarantees.

同時凍結以下產品原則：

> A good deck is not a collection of good slides. It is a sequence of intentional
> communication decisions made for a specific audience, purpose, and time limit.

## 2. Foundational Boundary and Authority

```text
Phase 16 controls credibility and expression.
Phase 17 controls communication strategy and delivery.
```

Phase 16 保持下列 frozen ownership：

- evidence、provenance 與 factual boundaries；
- editorial naturalness、headline/editorial quality；
- layout rhythm 與 information rhythm。

Phase 17 已實作並凍結：

- audience、purpose 與 desired outcome；
- narrative sequence、slide intent 與 slide takeaway；
- visual communication choice；
- time allocation 與 delivery readiness；
- presentation effectiveness QA。

Phase 17 不得弱化、覆寫或繞過 Phase 16。AGY 仍是唯一 semantic authority；worker 只執行
已核准的指令，不得自行決定 narrative meaning、evidence support 或 audience strategy。Phase 12
仍是 canonical grounding/reference authority，Phase 13 與 Phase 15 行為維持 frozen。

本階段的 QA finding 應是範圍明確、可獨立檢查的判斷，例如 `WEAK_CLOSE` 或
`TIMING_MISMATCH`，再由 deterministic policy 決定 warning、review 或既有 approval routing。
Typed finding 只限制介面，不等於真理，也不授權系統自行改動 approved WHAT/HOW。

## 3. Approval Workflow and User-facing Boundary

預設使用者流程維持不變：

```text
Request
  → Outline approval
  → Style approval
  → one real Sample approval
  → Full Deck
```

凍結：

```text
Internal presentation intelligence ≠ additional user approval gates.
```

不得預設新增 audience、strategy、narrative、timing 或 delivery approval。一般使用者也不應
看到 Presentation Brief 結構、narrative-role enum、slide-intent ID、QA state constant、timing
model internals、hierarchy classification 或 image-purpose enum。只有使用者明確要求、具體診斷
需要，或交付確實有幫助時，才以自然語言顯示必要資訊。

## 4. Semantic Change and Approval Safety

Phase 17 optimization 必須沿用既有 WHAT/HOW approval semantics。

可在不重開 outline 的安全 non-semantic 調整包括：

- speaker transition wording；
- delivery cues；
- timing annotations；
- 不改變 meaning 的 Notes cleanup。

下列屬 substantive WHAT change，必須回到 outline/content revision 並重新核准：

- 新增或移除 slide；
- 重排 substantive narrative；
- 改變 slide takeaway、substantive example、recommendation 或 factual claim；
- 改變任何已核准 WHAT。

若調整 materially 改變已核准 HOW，則依影響回到 style/sample approval。例：final QA 認為
Slide 3 與 Slide 4 應互換時，只能產生具體 improvement finding；不得直接 reorder。應將它
分類為 substantive content revision，返回既有 outline approval。Phase 17 永不以「改善」為由
靜默改變 meaning。

## 5. Phase 17.1 — Presentation Brief & Audience Contract

`Presentation Brief` 是 internal planning concept，不是本階段發布的 public stable schema。
它只保存對 communication decision 有用的 context：

- audience；
- purpose；
- desired audience outcome；
- 既有 `PRESENTATION_MODE`；
- presentation context；
- duration / time budget；
- audience knowledge level；
- relevant constraints。

### 5.1 Desired audience outcome

一份簡報可同時有多個 outcome，但每個 outcome 必須保留其不同用途：

- `KNOW`：觀眾應知道什麼；
- `UNDERSTAND`：觀眾應理解什麼；
- `REMEMBER`：什麼應留下記憶；
- `DECIDE`：應支援哪個決策；
- `ACT`：觀眾應採取什麼行動。

例如 BNI presentation 可以讓觀眾 KNOW 哪些商業情境與產險有關、REMEMBER 三個轉介紹
trigger，並在 trigger 出現時 ACT、轉介紹講者。

### 5.2 Audience inference and agency

AGY 可以從明確 request 安全推定顯而易見的場合，例如「董事會 15 分鐘 review」或
「新進人員 training」。缺乏必要 context 時，應保留 unknown、採取保守預設，或在確實影響
結果時向使用者詢問；不得捏造 audience attributes。

禁止推斷或建立：

- political preference、religion、health、sexual orientation 或 ethnicity；
- income assumptions；
- sensitive demographic profiles；
- personality manipulation 或 psychological vulnerability profiles。

不得進行 audience surveillance、emotion recognition 或針對推定弱點最佳化說服策略。

### 5.3 Reuse Phase 16 presentation modes

Phase 17 必須重用 Phase 16 既有概念 modes，不建立 competing system：

- `PITCH`
- `EXECUTIVE`
- `TRAINING`
- `SALES`
- `REPORT`
- `TECHNICAL`
- `KEYNOTE`
- `EDUCATIONAL`

Phase 17 消費這些 mode semantics 以調整 narrative、visual form、timing 與 delivery；mode 不得
改變證據規則，也不是本階段發布的 public schema。

## 6. Phase 17.2 — Narrative Architecture & Slide Intent

Deck 必須先有 intentional narrative progression，不能只把個別好 slide 拼在一起。內部
narrative architecture 概念包括：

- deck thesis 與 narrative arc；
- slide narrative role；
- slide intent、slide takeaway 與 slide job-to-be-done；
- opening strategy、closing strategy；
- slide-to-slide transitions。

### 6.1 Narrative roles

初始 conceptual roles 為：

- `OPEN`
- `CONTEXT`
- `PROBLEM`
- `QUESTION`
- `INSIGHT`
- `EVIDENCE`
- `CASE`
- `CONTRAST`
- `EXPLANATION`
- `RECOMMENDATION`
- `DECISION`
- `ACTION`
- `CLOSE`

這些是 internal planning vocabulary，不是 stable public schema。

### 6.2 Narrative role is not visual role

凍結：

```text
Narrative role ≠ visual role.
```

Phase 17 narrative role 說明一頁的 communication purpose。Phase 16 的 `HERO`、`DATA`、
`CASE`、`PROCESS`、`COMPARISON` 等 visual roles 說明視覺／資訊 treatment。兩者正交，不能
collapse。例如 narrative role 可以是 `EVIDENCE`，visual role 同時是 `DATA`。

### 6.3 Slide intent, takeaway, and job-to-be-done

每個 material slide 概念上必須回答三個不同問題：

1. **Intent — Why does this slide exist?** 例如建立 urgency、重構 misconception、證明 claim、
   解釋 mechanism、比較 choice、呈現 case、enable decision 或 drive action。
2. **Takeaway — If the audience remembers one thing, what should it be?** Takeaway 通常應是
   communication idea，而非僅有 topic label；所有生成仍受 Phase 16 evidence integrity 約束。
3. **Job-to-be-done — What must this slide accomplish in the sequence?** 它描述完成條件，例如
   「讓決策者理解延遲的 material risk，才能進入 option comparison」。

沒有 meaningful job 的 slide 可被標記 redundant，但核准後不得自動刪除。

弱 topic label `合作產業` 可以在 evidence-safe 前提下規劃為較明確 takeaway，例如：
`產險最好的轉介紹機會，常出現在企業正在發生變化的時候。` 這種改寫不得增加 unsupported
fact，也不得把 AGY synthesis 假裝成 sourced fact。

### 6.4 Narrative continuity signals

Future QA 應定義具體 deterministic 或 AGY semantic findings：

- topic jump；
- duplicated slide purpose／redundant narrative role；
- missing logical bridge／narrative gap；
- premature conclusion；
- unexplained recommendation；
- unresolved problem；
- weak transition；
- closing 未連回 desired outcome。

這些是 communication-quality findings，不得壓成假精確的總分。

### 6.5 Opening intelligence

Opening strategy 必須依 mode 與 context 選擇，不強迫每份 deck 使用故事或 agenda：

- `SALES` / networking：relevant question、recognizable situation、concise problem、memorable claim；
- `EXECUTIVE`：conclusion first、material risk、decision context；
- `TECHNICAL`：problem/failure mode、system constraint、architecture question；
- `TRAINING`：learning objective、capability outcome；
- `KEYNOTE`：narrative tension、memorable insight、strong visual premise。

### 6.6 Closing intelligence

Closing 必須回應 desired audience outcome：

- `ACT`：clear next step；
- `DECIDE`：specific decision requested；
- `REMEMBER`：memorable synthesis；
- training：participants 現在能做什麼。

不得把每份 deck 預設結束為 `Thank you` 或 `感謝聆聽`；只有場合適合時才可使用。

## 7. Phase 17.3 — Visual Communication Intelligence

本子階段不 redesign renderer，也不取代 Phase 16 Layout Rhythm：

```text
Phase 16 Layout Rhythm prevents mechanical visual repetition.
Phase 17 Visual Communication asks whether the selected form serves the message.
```

### 7.1 Information form and message matching

可評估的 internal forms 包括 statement、image-led message、comparison、matrix、table、timeline、
process、flow、chart、data callout、case study、quote、before/after 與 decision options。

典型 matching 原則：

- comparison → side-by-side、matrix 或 table；
- ordered time → timeline、sequence，或資料合適時使用 line chart；
- single core idea → statement + relevant visual；
- process → flow/process representation；
- data trend → appropriate chart。

Simple text 較清楚時不得強迫 visual complexity；也不要求每頁都使用圖片。

### 7.2 Visual hierarchy

概念 hierarchy 為 `PRIMARY`、`SECONDARY`、`SUPPORTING`。最具視覺支配力的 element 通常
應對應 slide takeaway。若 intended PRIMARY 是 `18%`，但 decorative icon 明顯主導畫面，
可以產生 hierarchy mismatch warning。本架構不要求 pixel-perfect computer-vision scoring。

### 7.3 Image purpose and relevance

Image purpose 可概念性區分為：

- `CONTEXT`
- `EVIDENCE`
- `EXAMPLE`
- `EMOTION`
- `IDENTITY`
- `DECORATION`

Decorative image 合法，stock photo 也不被禁止；但幾乎所有圖片都只是 generic decoration 時，
可依 slide takeaway、audience、narrative role 與 mode 產生 relevance warning。

### 7.4 Data storytelling

Phase 16 確保 data evidence-safe；Phase 17 規劃 data 如何推進 narrative：

```text
Fact → Context → Comparison → Meaning → Decision relevance
```

`Meaning` 與 `Decision relevance` 若由 AGY 產生，仍必須維持 AGY synthesis provenance；不得
被重分類為 source-grounded fact。

## 8. Phase 17.4 — Delivery & Rehearsal Intelligence

目標是讓 deck 在使用者的實際場合中可講、可控時、可排練。

### 8.1 Time budget and Output Honesty

使用者提供 duration 時，系統應建立 internal time budget。分配必須依 narrative weight，
不得只做 `duration / slide count`。例如 5-minute deck 可以讓 case、central insight 與 action
取得比 cover 或 transition 更多時間。

Timing QA 應以 speaker content 與可說明的 pacing assumptions 估計 delivery duration，並與
requested duration 比較。若內容明顯需要 10+ 分鐘，就不得宣稱「5-minute deck ready」。
Material overrun 或 undershoot 應產生 specific warning 或 correction requirement。這是
**Output Honesty** 原則；估計值不得偽裝成保證。

### 8.2 Speaker Notes effectiveness

Phase 16 確保 Notes 不機械、不重複；Phase 17 使 Notes 真正支援 delivery。依 slide 需要可包含：

- opening cue；
- core message；
- supporting evidence/example；
- emphasis；
- transition；
- optional timing guidance。

不得強迫每頁使用同一 Notes template。User-facing Notes 維持自然 prose，machine traceability
仍遵守 Phase 16 的結構與可讀性邊界。

### 8.3 Transition intelligence

Transition 應連接 Slide N takeaway 與 Slide N+1 intent，而不是機械地寫「下一頁」。例如：

> 剛剛我們知道哪些產業最容易合作；接下來真正重要的是，客戶出現什麼訊號時，夥伴應該想到你？

並非每個 transition 都必須說出口；QA 應判斷 continuity 需要，而不是增加固定 boilerplate。

### 8.4 Rehearsal cues

Optional lightweight cues 可包含 pause、ask audience、emphasize number、skip reading table、
keep case under 30 seconds。它們不得變成 teleprompter control language，也不得把工程 marker
預設暴露給使用者。

## 9. Phase 17.5 — Final Presentation Effectiveness QA

Effectiveness review 與 Phase 16 evidence QA、Phase 16 editorial QA、visual/render correctness QA
不同，但必須將它們視為不可繞過的 prerequisites。Internal report 可包含：

- audience fit；
- purpose alignment；
- desired-outcome clarity；
- narrative continuity；
- slide intent clarity；
- redundancy；
- opening effectiveness；
- closing/action clarity；
- timing fit；
- visual hierarchy；
- image relevance；
- data-story alignment；
- transition quality；
- delivery readiness；
- Phase 16 evidence integrity；
- Phase 16 editorial integrity。

Conceptual statuses 限於 `PASS`、`WARNING`、`REVIEW_REQUIRED` 等具體 routing state。禁止產生
presentation score 92/100、quality percentage、engagement probability、persuasion score 或
AI-generated score。概率或 confidence 即使未來作為某個窄判斷的 internal signal，也不能被
解讀為整份 deck 的品質、真實性或自動修改權限。

### 9.1 Specific findings

- **Redundancy**：多頁執行相同 narrative job。
- **Narrative gap**：problem/claim 直接跳到 recommendation，缺少必要 bridge。
- **Weak slide intent**：無法說明 slide 為何存在。
- **Weak takeaway**：只有 topic，沒有 meaningful point。
- **Timing mismatch**：estimated delivery materially over/undershoots duration。
- **Image irrelevance**：visual 不支持 slide purpose。
- **Hierarchy mismatch**：dominant visual 與 intended primary message 衝突。
- **Weak close**：未解決 `ACT`、`DECIDE` 或其他 desired outcome。
- **Weak opening**：未以符合 mode 的方式建立 relevance/context。

Finding 必須保存可檢查的 category、scope、affected slides 與 reason；不得只給一個 aggregate
score。Deterministic rule、AGY semantic review、missing context、render observation 與 Phase 16
integrity failure 應保持可區分，避免 fuzzy fallback 或 silent correction。

## 10. Safe Repair and Escalation Policy

Runtime 必須先分類 proposed repair：

```text
non-semantic delivery cleanup
  → may apply within existing approval state

substantive WHAT change
  → content revision
  → outline reapproval

material HOW change
  → style/sample reapproval as appropriate

Phase 16 integrity risk
  → block; never trade evidence for effectiveness
```

Effectiveness QA 不得把 warning 當成任意 mutation license，也不得以低 confidence 或單一
heuristic 自動做高影響變更。剩餘 findings 可保留為 `WARNING` 或 `REVIEW_REQUIRED`；一般
使用者只接收自然、必要、可行動的說明。

## 11. Frozen Subphase Definitions

所有子階段皆為 **COMPLETE / MERGED / BASELINE FROZEN**：

### Phase 17.1 — Presentation Brief & Audience Contract

**COMPLETE / MERGED / BASELINE FROZEN**（#51）

Audience、Purpose、Desired outcome、Context、Duration、Knowledge level、Mode、Constraints。

### Phase 17.2 — Narrative Architecture & Slide Intent

**COMPLETE / MERGED / BASELINE FROZEN**（#52）

Deck thesis、Narrative arc、Narrative roles、Slide intent、Slide takeaway、Slide job-to-be-done、
Opening、Closing、Transitions。

### Phase 17.3 — Visual Communication Intelligence

**COMPLETE / MERGED / BASELINE FROZEN**（#53）

Information form、Visual hierarchy、Image purpose/relevance、Data storytelling、
Chart/message alignment。

### Phase 17.4 — Delivery & Rehearsal Intelligence

**COMPLETE / MERGED / BASELINE FROZEN**（#54）

Time budget、Speaker pacing、Delivery Notes、Transitions、Rehearsal cues、Duration validation。

### Phase 17.5 — Final Presentation Effectiveness QA

**COMPLETE / MERGED / BASELINE FROZEN**（#55）

Audience fit、Narrative effectiveness、Redundancy、Timing、Visual communication、
Delivery readiness、Phase 16 integrity。

Phase 17.1–17.5 已依序通過 focused tests、full regression、exact CI、squash merge 與
post-merge validation，形成 frozen implementation baseline。

## 12. Acceptance E2E

Phase 17 deterministic integrated qualification 已通過以下 14 個 scenarios（14/14 PASS）：

1. **5-minute BNI networking deck**：referral-oriented outcome、少量 memorable points、
   conversational delivery、actionable close、realistic timing。
2. **15-minute executive review**：conclusion/decision-forward、restrained rhetoric、
   evidence/data prioritization、clear decision/action。
3. **30-minute training deck**：learning progression、examples、recap、適當 practice/application、
   realistic allocation。
4. **Technical presentation**：precision、architecture/failure-mode progression、術語保留、
   不強迫簡化、適當 evidence density。
5. **Same evidence, different audiences**：相同來源產生 `EXECUTIVE`、`SALES`、以及
   `TRAINING` 或 `TECHNICAL` deck；facts/evidence identity 穩定，但 narrative、takeaways、
   emphasis、visual form、Notes 與 timing 合理不同。
6. **Overlong 5-minute deck**：timing QA 明確指出 mismatch，不得 falsely claim fit。
7. **Redundant deck**：duplicate narrative jobs 產生 specific redundancy warning。
8. **Narrative gap**：problem → solution 缺少 support bridge 時被偵測。
9. **Generic stock-photo deck**：多數 imagery 為 generic decoration 時產生 relevance warning，
   但不禁止 decoration。
10. **Poor visual hierarchy**：supporting decoration 壓過 primary message 時產生 warning。
11. **Weak close**：outcome 為 `ACT`/`DECIDE` 卻以 generic Thank You 結束時產生 finding。
12. **Source/evidence stability**：Phase 17 optimization 保留 Phase 16 claim/evidence identity。
13. **Post-approval structural improvement**：reorder/add/remove suggestion 不靜默 mutation，
    而是回到既有 approval workflow。
14. **Delivery Notes**：Notes/transitions 可實際使用，且不重複、不機械。

Acceptance 必須檢查具體 outcome 與 application behavior，而非只檢查 internal prediction。

## 13. Security and User Agency

Phase 17 可以最佳化 clarity、relevance、structure、pacing 與 comprehension，但不得利用推定的
psychological vulnerability。使用者保有 narrative、approval 與 delivery 決定權。Audience
context 的取得、保存與使用必須符合最小必要原則；不得以更有效說服為由擴張 surveillance、
sensitive inference 或 manipulation。

## 14. Product Positioning

Phase 16：

> 內容有根據，呈現像人做的。

Phase 17 在內部產品 positioning 加上：

> 而且真的講得動。

Potential combined positioning：

> 內容有根據。呈現像人做的。而且真的講得動。

Phase 17 runtime 與 qualification 完成後，README 已採用同等精簡的 bilingual positioning，
未將 README 擴張為架構規格。

## 15. Non-goals

Phase 17 明確不包含：

- Phase 16 evidence redesign；
- source-grounding redesign；
- OCR changes 或 public OCR schema；
- renderer rewrite 或 image-generation architecture rewrite；
- automatic audience surveillance；
- sensitive-personality inference、sensitive demographic profiling 或 psychographic manipulation；
- emotion recognition 或 eye-tracking requirement；
- fake engagement probability、fake persuasion probability 或 presentation quality score；
- AI authorship detector；
- automatic slide-count inflation；
- default extra approval stages；
- web research redesign；
- Phase 18 implementation。

## 16. Governance and Related Architecture

- Phase 12–16 runtime contracts 維持 frozen；本文件不得被解讀為修改權。
- OCR schemas 維持 **DEFERRED**。
- Phase 17.1–17.5 的 contracts、tests 與 exact CI 分別由 #51–#55 完成並合併。
- Phase 17 未加入 provider、API credential 或 public schema，也未啟動 Phase 18。

Related documents：

- [Phase 16 grounded presentation and editorial quality](phase16-grounded-presentation-and-editorial-quality.md)
- [Outline, style, and sample workflow](outline-style-and-sample.md)
- [Architecture and design rationale](architecture-and-design-rationale.md)
- [Source grounding](source-grounding.md)
- [Phase 15 OCR architecture](phase15-ocr-architecture.md)
