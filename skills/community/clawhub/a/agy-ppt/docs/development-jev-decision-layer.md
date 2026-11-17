# Jev 開發決策層

> 狀態：**ACTIVE — DEVELOPMENT-TIME ONLY**  
> 適用範圍：v0.6.0 Presentation Quality Hardening 與後續 repository engineering  
> 不屬於產品 runtime、CI 或 release authority

Codex 是 repository 的 Engineering Lead / Development Orchestrator。Jev 是 Codex 底下的
**Bounded Engineering Decision Engine**。產品 runtime authority 完全不變：

`User → AGY → Codex production worker → agy-ppt → PPTX`

Jev 不得出現在此 runtime chain；AGY 仍是 sole product orchestrator / semantic authority。

## 1. 決策階層

1. **DETERMINISTIC**：固定規則能可靠回答時，由 deterministic code 直接判斷。
2. **JEV**：bounded、repeated、typed/classifiable、semantically non-trivial 且會影響 engineering branch
   的判斷，預設交給 Jev。
3. **CODEX REASONING**：open-ended architecture、causal debugging、證據不足、新型 failure、Jev 結果
   衝突或 confidence 不足時，由 Codex 完整推理。

Jev 不重複回答已經固化成 deterministic rule 的問題。採用的判斷必須轉成 repository-owned code、
tests、fixtures、typed enums、compatibility matrix、regression expectation 或 documented contract。

## 2. Confidence 與 escalation

- `>= 0.85`：`HIGH_CONFIDENCE`；僅在與 deterministic evidence 一致時可採用。
- `0.65–0.84`：`REVIEW_REQUIRED`；Codex review 後才可分支實作。
- `< 0.65`：`ESCALATE`；Codex 執行完整 engineering reasoning。
- choice probability 前兩名差距小於 `0.15`，或結果互相矛盾：不論 nominal confidence，皆
  `ESCALATE`。

此 routing 已由 `dev_jev_decisions.py` 與 offline tests 固化。Jev service unavailable 時直接降級為
Codex reasoning；不得阻擋 runtime、CI 或 release validation。

## 3. Decision record

Meaningful Jev-assisted decision 必須留下 sanitized lightweight record，包含：

- `decision_id`
- task / question
- bounded answer schema
- evidence / fixture references
- Jev result 與 confidence
- Codex action
- escalated yes/no
- final engineering disposition
- repository capture（code/test/fixture/doc）

不得保存 API key、authorization header、credential、private input 或未清理的 live transcript。

## 4. Q1 — Live Worker Contract Wiring 實驗紀錄

2026-09-23 使用 repository-owned synthetic fixtures，透過 TypeSafe `jev-latest` 執行 9 個
independent Choice judgments。輸入未含 confidential material 或 credential；完整 raw service response
不進 repository。

| Decision ID | Schema / fixture | Jev result | Confidence | Codex disposition | Repository capture |
|---|---|---:|---:|---|---|
| Q1-JEV-001 | `COMPLETE/PARTIAL/UNSAFE` — complete worker job | COMPLETE | 0.99 | 採用；要求完整 manifest | `audit_worker_contract` + tests |
| Q1-JEV-002 | 同上 — contradictory native overlay job | UNSAFE | 0.94 | 採用；dispatch 前 fail closed | adapter parser + tests |
| Q1-JEV-003 | `CLEARLY_PROPAGATED/AMBIGUOUS/MISSING` — vague empty-area prompt | AMBIGUOUS | 0.96 | 採用；不接受含糊 exclusion | canonical prompt renderer + tests |
| Q1-JEV-004 | 同上 — explicit zone/exclusion/failure prompt | CLEARLY_PROPAGATED | 1.00 | 採用；固化 prompt tokens/manifest hash | prompt compliance rule + tests |
| Q1-JEV-005 | `LIVE_VERIFIED/PROXY_ONLY/INSUFFICIENT_EVIDENCE` — complete live record | LIVE_VERIFIED | 1.00 | 採用；要求 dispatch/job/thread/result/artifact identities | qualification classifier + tests |
| Q1-JEV-006 | 同上 — callback record | PROXY_ONLY | 1.00 | 採用；proxy 永不冒充 live | qualification classifier + tests |
| Q1-JEV-007 | 同上 — thread-only record | INSUFFICIENT_EVIDENCE | 1.00 | 採用；證據不足不得宣稱 live | qualification classifier + tests |
| Q1-JEV-008 | `RAW_PLATE/HYBRID_PREVIEW/AMBIGUOUS` — plate artifact | RAW_PLATE | 1.00 | 採用；raw plate 不得成為 sample fidelity 證明 | sample provenance + tests |
| Q1-JEV-009 | 同上 — manifest/render-hashed preview | HYBRID_PREVIEW | 1.00 | 採用；Hybrid Preview 必須顯式可證 | sample provenance + tests |

統計：9 fixtures；9 high-confidence；0 review-required；0 low-confidence/escalated；0 unresolved。
Jev 判斷均先由 Codex 與 deterministic evidence 交叉檢查後才採用。

## 5. 權限與禁止事項

Jev 可以協助 bounded development classification，但不得決定：PR merge、CI pass、tag/release、
human presentation quality、evidence factual truth 或產品語意。`HUMAN_PRESENTATION_QUALITY` 仍只能由
human acceptance 通過；human rejection 一律覆蓋任何 automated classification。

Repository runtime 與 CI 對 Jev 的 dependency 為 **NONE**。TypeSafe credential 只存在於開發環境，
不得 commit。

## 6. Q2 — Layout & Typography Grammar 實驗紀錄

2026-09-23 以 5 頁 synthetic Hybrid PPTX 在實際 macOS Microsoft PowerPoint 輸出 PDF，Codex 先將
可觀察的 render evidence 整理為 structured state，再交由 TypeSafe `jev-latest` 執行 11 個
bounded Choice judgments。TypeSafe HTTP API 的 state 為 JSON/text；Jev 未直接收取 pixel image，
因此最終視覺根因仍由 Codex 根據 PowerPoint render 確認。Raw service response 不進 repository。

| Decision ID | Schema / fixture | Jev result | Confidence | Codex disposition | Repository capture |
|---|---|---:|---:|---|---|
| Q2-JEV-001 | visual defect — cover v1 | REFLOW | 0.99 | 採用；孤字換行是 dominant defect | mixed-CJK line estimator + tests |
| Q2-JEV-002 | `ACCEPT/WARNING/REPAIR/BLOCK` — cover v1 | REPAIR | 0.67 | REVIEW_REQUIRED；Codex 檢視實際 render 後確認 REPAIR | envelope line findings + fixture regression |
| Q2-JEV-003 | 同上 — repaired cover | ACCEPT | 0.85 | 採用；仍不等於 human acceptance | PowerPoint render evidence + tests |
| Q2-JEV-004 | visual defect — chart v1 | CHART | 1.00 | 採用；百分比格式與預設標題為根因 | explicit chart style + tests |
| Q2-JEV-005 | severity — chart v1 | BLOCK | 1.00 | 採用；12% 顯示為 1200% 屬 content-integrity block | exact chart data/format fixture |
| Q2-JEV-006 | severity — repaired chart | ACCEPT | 0.86 | 採用；12/14/18% 輸出已確認 | no title/grid/legend + labels/gap tests |
| Q2-JEV-007 | CJK outcome — three-card slide | GOOD | 1.00 | 採用為 representative positive fixture | grid/padding/hierarchy tests |
| Q2-JEV-008 | native decision — ordinary title | NATIVE_WITH_ENVELOPE | 0.98 | 採用；限定 2 lines / 48 chars / font range | production-plan envelope tests |
| Q2-JEV-009 | native decision — KPI | NATIVE_WITH_ENVELOPE | 0.99 | 採用；限定 1 line / 16 chars / prominent font | production-plan envelope tests |
| Q2-JEV-010 | native decision — artistic headline | LOCKED_REQUIRED | 0.99 | 採用；不用 native coverage 降級藝術字 | existing locked policy + regression |
| Q2-JEV-011 | native decision — mixed CJK display | LOCKED_PREFERRED | 0.81 | REVIEW_REQUIRED；Codex 依未知 client font risk 確認 | FONT_CRITICAL locked policy + regression |

統計：11 fixtures；9 high-confidence；2 review-required；0 low-confidence/escalated；0 unresolved。
兩個 review-required 案例均由 Codex 檢視實際 PowerPoint render 與 Phase 18 priority order 後完成處置。

Q2 的 deterministic capture 包含：10 × 5.625 inch canonical canvas、outer margins/columns/card gaps、
CJK/Latin native typography pairing、role-based hierarchy、mixed-script line estimation、editability-envelope findings、
cover crop、非預設 PowerPoint chart styling、以及只能由 exact-artifact human review 通過的
`HUMAN_PRESENTATION_QUALITY` contract。Jev runtime dependency 與 CI dependency 仍均為 **NONE**。

## 7. Q3 — Editorial / Content Quality Hardening 實驗紀錄

2026-09-24 使用 17 個 repository-owned synthetic copy／narrative fixtures，透過 TypeSafe
`jev-latest` 執行 bounded Choice judgments。Jev 只分類 expression、specificity、slide-quality 與
narrative alignment；不判定來源真實性、不生成 evidence，也不改寫文案。Raw service response 不進
repository。

| Decision ID | Schema / fixture | Jev result | Confidence | Codex disposition | Repository capture |
|---|---|---:|---:|---|---|
| Q3-JEV-001 | headline — `核心績效指標` | LABEL_ONLY | 1.00 | 採用為 topic-label fixture | headline shape tests |
| Q3-JEV-002 | supported renewal headline | ASSERTION_SUPPORTED | 0.94 | 採用；support 仍由 Phase 16 驗證 | evidence-preservation test |
| Q3-JEV-003 | same assertion without evidence | ASSERTION_UNSUPPORTED | 0.99 | 採用為 fail-closed fixture | evidence-integrity block test |
| Q3-JEV-004 | interrogative headline | QUESTION | 0.98 | 採用 | headline shape tests |
| Q3-JEV-005 | decision headline | DECISION_FRAME | 0.96 | 採用 | headline shape tests |
| Q3-JEV-006 | concrete next action | DECISION_FRAME | 0.59 | ESCALATE；Codex 依 imperative function 定為 ACTION_FRAME | action-role alignment test |
| Q3-JEV-007–011 | generic/slogan/specific/actionable/evidence-poor copy | expected bounded labels | 0.97–1.00 | 採用；不轉成關鍵字 blacklist | contextual generic-copy tests |
| Q3-JEV-012 | schema-fill slide | REPAIR | 0.95 | 採用 | deterministic preflight finding |
| Q3-JEV-013 | specific evidence slide | PASS | 0.96 | 採用 | positive evidence fixture |
| Q3-JEV-014 | unsupported numeric slide | BLOCK | 0.99 | 採用；由 Phase 16 validator 執行 | factual-drift regression |
| Q3-JEV-015–016 | aligned / misaligned role-copy pairs | ALIGNED / MISALIGNED | 0.98 / 1.00 | 採用 | narrative-copy alignment tests |
| Q3-JEV-017 | case body with label-only title | PARTIALLY_ALIGNED | 0.27 | ESCALATE；Codex 確認 body 合理但 headline 需 review | review-not-block regression |

統計：17 fixtures；15 high-confidence；0 review-required；2 low-confidence/escalated；0 unresolved。
兩個低信心結果都由 Codex 依完整 narrative context 處置，並固化成 deterministic regression。

Q3 的 repository capture 是 additive `presentation_content_quality.py` preflight、Phase 16 evidence
validation reuse、mode-aware density、role-copy alignment、worker semantic-preservation prompt，以及既有
content-revision approval boundary。它不自動改寫 approved meaning，也不建立 runtime Jev dependency。
Jev runtime dependency 與 CI dependency 仍均為 **NONE**。

## 8. Q4 — Visual Qualification 實驗紀錄

2026-09-24 使用 12 個 synthetic exact-render observation fixtures，透過 TypeSafe `jev-latest`
執行 18 個 bounded Choice judgments。Jev 分類 issue、severity、Plate → Hybrid degradation、
Hybrid → client drift 與 native-vs-locked action；不直接通過 human quality，也不決定 release。

| Fixture / schema | Jev result | Confidence | Codex disposition | Repository capture |
|---|---:|---:|---|---|
| harmless one-line wrap — severity / issue | ACCEPT / REFLOW | 0.92 / 0.99 | 採用 | bounded-drift tests |
| evidence number changed — severity | BLOCK | 1.00 | 採用；semantic integrity 優先 | content-change block rule |
| clipped core title — issue / severity | OVERFLOW / BLOCK | 1.00 / 0.32 | ESCALATE；Codex 依 core content obscured 判定 BLOCK | core-obscured rule |
| 0.03-inch harmless shift | ACCEPT | 0.98 | 採用 | bounded-drift test |
| crop removes subject — issue / severity | CROP / REPAIR | 1.00 / 0.44 | ESCALATE；非 evidence image 可修復，判定 REPAIR | crop repair test |
| chart obscures headline — issue / severity | Z_ORDER / BLOCK | 1.00 / 0.99 | 採用 | core-overlap block test |
| default chart degradation — issue / severity | CHART / REPAIR | 1.00 / 0.97 | 採用 | chart repair test |
| slight brand-family color drift | ACCEPT | 0.77 | REVIEW_REQUIRED；Codex 確認 contrast/hierarchy 未變 | bounded-color test |
| decorative icon displaces KPI hierarchy | HIERARCHY / BLOCK | 1.00 / 0.57 | ESCALATE；approved quality floor 優先 | hierarchy-floor block rule |
| Plate → weak native reconstruction | MATERIAL_DEGRADATION | 0.98 | 採用 | stage-loss localization test |
| Hybrid → harmless client wrap | MINOR_DRIFT | 0.70 | REVIEW_REQUIRED；Codex 確認無 overflow／meaning change | actual-client localization test |
| font-critical artistic headline | LOCK | 1.00 | 採用；fidelity 優先於 native coverage | production fallback policy |

統計：18 judgments；13 high-confidence；2 review-required；3 low-confidence/escalated；0 unresolved。
所有 review／escalation 均由 Codex 依 Phase 18 priority、exact observation 與 approved Sample floor
完成處置。採用結果已固化為 `presentation_visual_qualification.py`、exact hash/provenance chain、
stage-loss localization、deterministic disposition rules 與 offline tests。Automated result 永遠不會把
`HUMAN_PRESENTATION_QUALITY` 設成 PASS。Jev runtime dependency 與 CI dependency 仍均為 **NONE**。

同日另以 5 頁 synthetic Hybrid deck 執行 macOS Microsoft PowerPoint `ACTUAL_CLIENT` export。
一張 Hybrid Sample 與 final deck 對應頁的 144-DPI PowerPoint render 完全相同（相同 PNG SHA-256），
因此沒有 Sample → final representation degradation。PowerPoint 在 export 時另加上 tenant/client policy
標示「限閱」；原始 PPTX OOXML 不含該字串，故記為 external-client policy marking，不能冒充 renderer
輸出，也不能由 repository 靜默移除。這項 actual-client observation 仍交由 exact-artifact human review
決定是否可接受。

## 9. Q4 — Presentation Density Repair 實驗紀錄

2026-09-27 對人類已審查的四頁 exact live-Codex regression artifact 執行 8 個 bounded
Choice judgments。輸入只包含 exact render SHA、可重現的結構觀察與 deterministic supporting
signals；Jev 未取得 credential、商業資料或 product-runtime access。

| Fixture | Composition density | Visual anchor | Confidence / routing | Codex disposition |
|---|---|---|---|---|
| regression slide 1 — cover | `UNDERFILLED` | `WEAK` | 0.99 high / 0.50 escalate | 採用 density；anchor 由人類 BLOCK 與 exact render 裁決 |
| regression slide 2 — KPI/chart | `BALANCED` | `STRONG` | 0.99 high / 0.75 review | 採用為 balanced-density reference |
| regression slide 3 — image/right column | `UNDERFILLED` | `STRONG` | 0.99 high / 0.83 review | 主圖 anchor 強，但右欄缺少 structured takeaways，仍 underfilled |
| regression slide 4 — CTA | `UNDERFILLED` | `WEAK` | 0.98 high / 0.65 review | 採用；單一句子不能取代三段 action flow |

這組結果證明 hero image、occupied envelope 或 empty-area ratio 都不能單獨決定 composition
density。Repository capture 為 `CompositionDensity`、`VisualAnchor`、typed supporting signals、
role-aware review triggers，以及四頁 regression tests。這些 deterministic signals 只提示 review，
不計算 aesthetic score，也不會把 `HUMAN_PRESENTATION_QUALITY` 設成 PASS。

Jev runtime dependency 與 CI dependency 仍均為 **NONE**。

同一輪修復後，另對四頁 exact PowerPoint renders 重跑相同 schema。Slide 1–4 的 density
均為 `BALANCED`（0.62 / 1.00 / 0.98 / 0.84），anchor 均為 `STRONG`
（0.92 / 0.86 / 0.99 / 0.92）。Slide 1 density 依 low-confidence policy 升級至 Codex
exact-render review；Slide 4 density 依 medium-confidence policy 經 Codex review。兩者都只取得
「可交付人類重新審查」的 engineering disposition，沒有取代人類 presentation-quality gate。

## 10. Q4 — Dense Visual Style Profile 實驗紀錄

2026-09-27 因人類將目標明確修正為 `DENSE / CARD_HIGH / IMAGE_RICH`，對新的四頁 exact
PowerPoint renders 執行 20 個 bounded Choice judgments。每個 fixture 都包含 exact render SHA、
slide role、清理過的可觀察版面描述與 deterministic supporting signals；Jev 未直接接觸 product
runtime、credential 或 private source。

| Fixture | Style match | Density | Card structure | Image usage | Hierarchy |
|---|---|---|---|---|---|
| slide 1 — cover hero | `MATCH` (0.83, review) | `ON_TARGET` (0.98) | `ON_TARGET` (0.98) | `ON_TARGET` (0.99) | `STRONG` (0.97) |
| slide 2 — KPI/chart evidence | `PARTIAL_MATCH` (0.58, escalate) | `ON_TARGET` (0.94) | `ON_TARGET` (0.88) | `ON_TARGET` (0.92) | `STRONG` (0.91) |
| slide 3 — image cluster/insights | `MATCH` (0.99) | `ON_TARGET` (0.99) | `ON_TARGET` (1.00) | `ON_TARGET` (1.00) | `STRONG` (1.00) |
| slide 4 — contextual action flow | `MATCH` (0.92) | `ON_TARGET` (0.92) | `ON_TARGET` (0.97) | `ON_TARGET` (0.98) | `STRONG` (0.91) |

Slide 1 的 medium-confidence style result 經 Codex exact-render review 後採用。Slide 2 的低信心
style result 升級至 Codex：該頁沒有照片，但原生 chart 是符合 analytic role 的 primary informative
visual；同一判斷中 density、cards、image/chart usage 與 hierarchy 均為 high-confidence positive，且
approved grammar 明定不是每頁都必須含照片，因此最終 engineering disposition 為 deck-level match，
不增加裝飾性 stock image。

Stable capture 是 opt-in `PresentationStyleProfile`、`LayoutDensity`、`CardDensity`、`ImageDensity`、
typed card roles、role-aware layout-selection policy 與 regression tests。Default profile 保持
`BALANCED / MEDIUM / MEDIUM`，不會把所有 agy-ppt 使用者強制改成 dense。這些結果只支持送交人類
重新審查，不會把 `HUMAN_PRESENTATION_QUALITY` 設成 PASS。Jev runtime dependency 與 CI
dependency 仍均為 **NONE**。

## 11. Q4 — Effective Density Repair 實驗紀錄

2026-09-28 因人類確認 dense direction 正確、但要求 semantic density 追上 visual density，對四頁
exact PowerPoint renders 執行 12 個 bounded Choice judgments。新 schema 為
`CARD_INFORMATION_DEPTH`、`IMAGE_VARIETY` 與 `SEMANTIC_DENSITY`；輸入只包含 exact render SHA、
slide role、sanitized observation 與 deterministic supporting signals。

| Fixture | Card information depth | Image variety | Semantic density | Codex disposition |
|---|---|---|---|---|
| slide 1 — approved cover | `LABEL_ONLY` (0.97) | `DISTINCT_INFORMATIONAL` (0.97) | `BALANCED` (0.29, escalate) | 人類已明確 PASS；category tags 是 cover labels，不套用 content-card depth 要求 |
| slide 2 — KPI/chart evidence | `SUPPORTING` (0.85) | `DISTINCT_INFORMATIONAL` (0.99) | `HIGH` (0.88) | 採用；三張既有 cards 各有 operational supporting layer |
| slide 3 — distinct image roles | `SUPPORTING` (0.99) | `DISTINCT_INFORMATIONAL` (0.98) | `HIGH` (0.82, review) | exact-render review 後採用；三張圖片不是同圖裁切，且分別承擔情境、排序、聚焦 |
| slide 4 — action flow | `SUPPORTING` (1.00) | `DISTINCT_INFORMATIONAL` (1.00) | `HIGH` (0.66, review) | exact-render review 後採用；卡片數不變，每一步均有 concise operational detail |

Stable repository capture 是 typed effective-density enums、card-depth counts、image-role counts、
role-aware review prompts 與 regression tests。規則不以 card/image 數量推導 semantic quality，也不把
cover 的 category tags 當成內容卡缺陷。重複裁切、decorative-only image 與 content slide 缺少
supporting layer 都會觸發 deterministic review finding；最終美學與 presentation-quality gate 仍只由
exact-artifact human review 決定。Jev runtime dependency 與 CI dependency 仍均為 **NONE**。
