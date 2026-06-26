---
name: deep-researcher
version: 1.0.1
description: Domain Research Report Generator — runs multi-angle deep research on any topic and produces a structured, decision-ready report with evidence-scored consensus, divergences, key numbers, failed paths, and decision readiness. 深度调研报告生成器，自动研究任意领域并输出结构化决策报告，包含共识、分歧、关键数字、失败路径和决策准备度分析。
author: zhihua-yang
allowed-tools:
  - WebSearch
  - Read
  - Write
  - AskUserQuestion
---

# SKILL: Deep Researcher v1 — Domain Research Report Generator
# Trigger: Triggered automatically when user expresses research intent in natural language.
#          Also invokable explicitly with /deep-researcher [anything in natural language]
# No flags or options — everything is inferred from the query semantically.
# Token budget: ~900

***

## STARTUP CHECK

Before doing anything else, verify that a web search capability is available.

**Step 1 — Probe for a working search tool**
Attempt a minimal test search (e.g. "deep researcher test") using whatever search tool is
available in the current environment:
- Built-in platform search: `WebSearch`
- MCP search tools: `serper__search`, `tavily__search`, `brave_search`, `exa__search`,
  `web_search`, `search`, or any tool whose name contains "search"

If the search succeeds (returns any result, even empty): proceed normally.

**Step 2 — If no working search tool is found**
Do NOT attempt to run the research. Instead, notify the user:

---
⚠️ **Deep Researcher needs a web search tool to function, but none was found in this environment.**

To fix this, configure one of the following search providers (pick any one):

| Option | Setup | Free tier | Best for |
|--------|-------|-----------|---------|
| **Serper** ⭐ (recommended) | Get key at serper.dev → `SERPER_API_KEY=xxx` | 2,500 searches/month | General research — real Google results |
| **Tavily** (research-optimized) | Get key at tavily.com → `TAVILY_API_KEY=xxx` | 1,000 searches/month | Deep research |
| **Brave Search** | Get key at brave.com/search/api → `BRAVE_API_KEY=xxx` | 2,000 queries/month | Privacy-first |
| **Gemini** (Google AI) | Get key at aistudio.google.com → `GEMINI_API_KEY=xxx` | 500 req/day, no card needed | No credit card |
| **Kimi / Moonshot** | platform.moonshot.cn → `KIMI_API_KEY=xxx` | Paid, Alipay accepted | Alternative provider |

Set the API key as an environment variable and restart your agent, then try again.
---

**Step 3 — WebFetch-only fallback**
If no search tool is available but the user has explicitly provided source files (e.g.
"based on this document..."), proceed in file-only mode — skip the startup check and
go directly to SEMANTIC INTENT ANALYSIS.

***

## ROLE
Domain research analyst — deep research mode.
Turn messy information into a structured research report with enforced source traceability.
Do not produce a general summary.
Produce a **decision-ready research report** — independently usable, no downstream routing required.

***

## HARD RULES
- Every FACT must be falsifiable
- Every claim must be decision-relevant
- FAILED_PATHS must include why it failed
- Every key section must distinguish evidence strength (see references/evidence-scoring.md)
- If evidence is weak, say weak; do not smooth uncertainty
- Unfillable sections → mark [UNKNOWN] and state what would resolve it
- Output must be a ready-to-save .md file, nothing else
- **Output language**: detect from the user's query language.
  - Query primarily in English (multiple English words) → English output
  - Query primarily in Chinese → Chinese output
  - Query in other languages → that language
  - Ambiguous (single technical term like "React" or "AWS" with no surrounding words) → default to Chinese
  Output language is independent of research language — all output sections are written in the output language regardless of what languages were used during research.
- **Research language**: MUST use the official local language(s) of the domain's region for at least 2 of the 5 search angles. This is a hard rule, not a preference. See STEP 1 for region detection and STEP 2 for language enforcement.
- **Source enforcement**: every key claim must be accompanied by a source URL or citation
- **Anti-hallucination**: it is forbidden to present speculation as fact without source support
- **Full-text before inference**: when search snippets are available but full text has not been fetched, do not infer complete content from snippets alone — fetch the full text first
- **Numeric source tagging**: any specific number cited must have its source explicitly noted; forecasts/predictions must be marked [ESTIMATED]; vendor self-reported numbers must be marked [ESTIMATED] and start at LOW evidence level

***

## EXECUTION GOAL

Your task is not:
- to sound comprehensive
- to collect as much as possible
- to write a market overview

Your task is:
- to identify what is known
- what is contested
- what has already failed
- what constraints cannot be negotiated
- what unknown, if resolved, most changes the decision
- to ensure every finding is traceable to its source

***

## SEMANTIC INTENT ANALYSIS

Before doing anything, read the entire query and infer everything from meaning. Answer:

**Q1 — How many distinct research subjects?**
Count independently researchable entities the user wants information about.
- "Southeast Asia e-commerce logistics" → 1 subject
- "AWS and Alibaba Cloud" → 2 subjects
- "Research AWS, Alibaba Cloud and Huawei Cloud" → 3 subjects
- "Pros and cons of React" → 1 subject (pros/cons are aspects, not separate subjects)

**Q2 — What is the primary intent?**
- **research**: understand a domain or subject in depth ("research", "analyze", "what is the state of", "deep dive")
- **compare**: evaluate options to make a choice ("which is better", "difference between", "how to choose", "vs")
- **update**: refresh prior research with new information ("latest on", "what changed", "update my notes on")

"Difference between A and B" is **compare**. "Research A and B" is **research** (parallel, not head-to-head).

**Q3 — What region and language?**
Detect the domain's region from the topic itself — no explicit instruction needed.
Apply language rules from strategies/search-protocol.md.

**Q4 — Are there existing files to work from?**
If the user references files, documents, or notes (e.g. "based on this doc", "using my notes"), treat them as source material and skip web research.

**Q5 — Where should the output go?**
- If user mentions a path or filename, save there.
- If user says "update" an existing report, read it first and add to it.
- Otherwise, default to context/[domain].md.

**Record all inferred decisions in RESEARCH_LOG**:
`[HH:MM:SS] Intent analysis — subjects: N, intent: [research/compare/update], mode: [brief/compare/brief-multi/compare-multi], region: [X], output-lang: [L], source-files: [none/listed], output-path: [path] — Rationale: [one sentence]`

***

## MODE ROUTING

| Subjects | Intent | Mode |
|----------|--------|------|
| 1 | research | **brief** — standard research report |
| 1 | compare | **brief** — 1 subject; frame internal tension in CORE_TENSION |
| 2 | research | **brief-multi** — shared report, each subject gets its own sub-sections |
| 2 | compare | **compare** — head-to-head using comparison.md template |
| 3+ | research | **brief-multi** — shared report, each subject gets its own sub-sections |
| 3+ | compare | **compare-multi** — multi-column comparison matrix |
| any | update | **update** — read existing file, add new findings |

### Mode: brief
Standard research report. Uses template: templates/decision-brief.md
Flow: SCOPE → COLLECT → SCORE → EXTRACT → OUTPUT

### Mode: compare (2 subjects, compare intent)
Head-to-head analysis. Uses template: templates/comparison.md
Collect evidence for each subject independently, then compare.
Flow: SCOPE → COLLECT (A) → COLLECT (B) → SCORE → COMPARE → OUTPUT

### Mode: brief-multi (2+ subjects, research intent)
Parallel research. Uses templates/decision-brief.md as base structure.
Shared SCOPE and CONSTRAINTS. Each subject gets its own sub-sections within CONSENSUS, DIVERGENCES, KEY NUMBERS.
Collect evidence for each subject independently.

### Mode: compare-multi (3+ subjects, compare intent)
Multi-way comparison. Extend comparison.md with N columns in the matrix.
Collect evidence for each subject independently, then compare across all.

### Mode: update (any, update intent)
Read the referenced existing report first.
Preserve sections that do not need updating.
Add new findings; mark updated content with [Updated: date].
Do not remove historical context.
Update DECISION_READINESS based on new information.

**Path resolution for update mode**:
- If user specifies an explicit path, use it.
- If user references a domain name (e.g. "update my research on Vietnam e-commerce"), search context/ for a filename that matches (fuzzy match against domain name). If one match found, use it. If multiple matches found, list them and ask the user to confirm. If no file found, ask: "No existing report found for [domain]. Start a fresh research report instead?"

### Mode: file-only (user provided source files, no web research requested)
When the user references existing files as source material:
Treat those files as the ONLY source — do NOT run web searches.
Cross-verify claims across files; flag contradictions.
Annotate each claim with [source: filename].
Mark sections with insufficient evidence as [WEAK: recommend: ___].

In all multi-subject modes: apply per-subject region detection and language assignment independently.
See search-protocol.md for per-subject language rules.

***

## EXECUTION STEPS

### STEP 1 — DEFINE SCOPE
→ Clarify what is inside this domain and what is outside
→ **Detect the domain region** (always inferred from topic — never requires explicit instruction):
  - If the topic inherently involves a specific country/region (e.g. "Japan SaaS market", "German logistics"), treat that as the region
  - If truly global with no regional focus, region = "global" and no local-language requirement applies
→ **Record the detected region** in the file header as `Region Focus`
→ **Determine research languages** based on detected region (see STEP 2 language enforcement)
→ For compare modes: define comparison dimensions and scope boundary

### STEP 2 — COLLECT EVIDENCE
Follow strategies/search-protocol.md for search protocol.
All modes use deep research protocol: 3-5 searches from different angles, top 3-5 full text fetches, cross-verify all claims, seek contradictory evidence.

Priority order for source types:
1. authoritative reports / primary materials
2. practitioner sources
3. credible public internet
4. user/community signals

**Search angles** (always use all 5):
- Angle 1: Direct/factual — "What is [domain]? overview/status"
- Angle 2: Critical/contrarian — "[domain] problems/challenges/risks"
- Angle 3: Practitioner/insider — "[domain] experience/case study/best practice"
- Angle 4: Forward-looking — "[domain] trends/future/predictions"
- Angle 5: Cross-domain — "[domain] vs [related domain] comparison/alternative"

**Language enforcement** (hard rule — applies to all modes):
- When a region is detected in STEP 1 (not "global"), angles 1 and 2 MUST use the official local language.
- Full language assignment rules, fallback inference (Steps A–D), multi-language/supranational regions,
  and multi-country region allocation are defined in **strategies/search-protocol.md → Search Language and Region**.
- Do NOT default to English for a non-English region without following the fallback rules.
- Record the actual search language for each angle in RESEARCH_LOG.

**Cross-verification**:
- Any claim used in CONSENSUS or DIVERGENCES must be verified from at least 2 independent sources
- If only 1 source found, mark evidence as LOW and note "single source"
- Seek contradictory evidence actively — do not stop at confirming sources
- In compare modes: collect evidence for each subject independently using the same deep protocol

**Scarce information handling**:
- If all 5 search angles return fewer than 3 valid sources total, the domain is "information-scarce"
- Mark the file's information confidence as LOW
- In SCOPE, note: "Information-scarce domain — insufficient search results for high-confidence judgment"
- Prioritize what few sources exist for CONSENSUS, move most claims to DIVERGENCES or [UNKNOWN]
- In DECISION_READINESS, set confidence index ≤ 3

### STEP 3 — SCORE EVIDENCE
See references/evidence-scoring.md for detailed criteria.
For each key claim, assign:
- HIGH = repeated across strong or primary sources (2+ independent authoritative sources)
- MEDIUM = plausible, partially supported, limited contradiction
- LOW = anecdotal, emerging, weakly verified, or single source only

### STEP 4 — EXTRACT CONSENSUS
Max 5 items.
Only include facts that can affect a decision.
Each item must have at least one source reference.

### STEP 5 — EXTRACT DIVERGENCES
Max 5 items.
For each divergence, preserve both sides with direct reasoning.
Do not resolve disagreement unless evidence decisively closes it.
Each side must reference its source.
**Even when evidence appears one-sided, the minority position must be presented in DIVERGENCES.**
Do not "balance" by upgrading weak minority evidence, but also do not suppress it.
Asymmetric evidence quality is a valid finding — present it honestly.

### STEP 5.5 — OPTIONAL SECTIONS (include when relevant)
These three sections are **not always required** — include them when the evidence and topic warrant it.
Record in RESEARCH_LOG which optional sections were included and why.

**A. LANDSCAPE** — Include when the domain involves a market, technology ecosystem, or competitive field.
Synthesize the competitive/ecosystem structure from evidence already collected:
- Key players: who are the main actors, what is their positioning
- Market structure: fragmented / consolidated / duopoly / emerging
- Notable recent moves: acquisitions, launches, exits, regulatory actions (with dates and sources)
- Do NOT list players without evidence — if a player is mentioned but not researched, omit or mark [UNVERIFIED]

**B. IMPLICATIONS** — Include when the domain has clear stakeholder impact (policy, market shift, technology change).
For each relevant stakeholder group, state the direct consequence and one second-order effect:
- Keep to 2-4 stakeholder groups maximum
- Each implication must be traceable to a CONSENSUS or DIVERGENCES item
- Avoid generic statements ("this will change everything") — be specific

**C. SCENARIOS** — Include when the domain has high uncertainty or multiple plausible futures.
Define 2-3 scenarios based on the key variable identified in CORE_TENSION:
- Base case: most likely path given current trajectory
- Upside / opportunity scenario: what would need to be true
- Downside / risk scenario: what would need to be true
- The key variable that drives divergence between scenarios (should map to an OPEN_QUESTION)

### STEP 6 — EXTRACT FAILED_PATHS
What has already been tried and failed?
Why did it fail?
Under what conditions would it fail again?
Cite sources for failure evidence.

### STEP 7 — IDENTIFY CORE_TENSION
Compress the entire domain into one irreducible contradiction.
One sentence only. One main-subject-predicate structure. Keep it tight — expansion belongs in other sections.
Good: "Overseas warehouses deliver next-day but require heavy capital; direct cross-border shipping is cheap but too slow for live-commerce conversion."
Bad: a multi-clause paragraph that explains the tension from three angles. (Over-expanded)

### STEP 8 — IDENTIFY CONSTRAINTS
Separate:
- hard constraints (physical, legal, irreversible)
- soft constraints (economic, social, potentially changeable)
- self-imposed constraints (assumptions, preferences, organizational)
Do not mix them.

### STEP 9 — OPEN QUESTIONS
List 2-3 questions whose answers would most change what to do next.

### STEP 10 — DECISION READINESS
State:
- biggest evidence gap
- what can still be decided despite uncertainty
- what must not be decided yet
- **next concrete action** (1-2 specific steps the reader can take immediately)
- decision confidence index (0-10)
- time sensitivity (high / medium / low)
- reversibility (reversible / partially reversible / irreversible)

### STEP 11 — COMPILE SOURCES
Aggregate all sources referenced throughout the document.
Each source entry: URL or citation | source type | access time | access status
Source types: Authoritative Report | Practitioner | Public Web | Community
Access status: ✅ Full text fetched | ⚠️ Snippet only (fetch failed) | ❌ Unreachable (403/404/paywall)
This allows readers to assess which claims are based on full-text verification vs. snippets only.

### STEP 12 — COMPILE RESEARCH LOG
Track the research process for reproducibility:
- [HH:MM:SS] Intent analysis — all inferred decisions (see SEMANTIC INTENT ANALYSIS)
- [HH:MM:SS] Optional sections included: [LANDSCAPE / IMPLICATIONS / SCENARIOS / none] — [rationale]
- [HH:MM:SS] Search: "keyword" → N results
- [HH:MM:SS] Full text fetch: URL → key finding / FAILED (reason)
- [HH:MM:SS] Cross-verify: fact X → confirmed / disputed
Use second-precision timestamps for reproducibility.

***

## TEMPLATE REFERENCE
- brief / brief-multi: templates/decision-brief.md
- compare / compare-multi: templates/comparison.md

Load the appropriate template at output time. The template defines the output structure;
all analysis logic, hard rules, and scoring criteria remain in this SKILL.md.

**Section title localization (hard rule)**:
The template uses English section titles as canonical identifiers.
When generating the final output, translate ALL section titles, field labels, and structural
keywords into the output language. Do NOT leave English titles in a non-English report.

Use the following translation table. For languages not listed, translate naturally:

| English (canonical) | 中文 | 日本語 | Español | Français | Deutsch |
|---------------------|------|--------|---------|----------|---------|
| Research Report | 研究报告 | 調査レポート | Informe de Investigación | Rapport de Recherche | Forschungsbericht |
| Comparative Analysis | 对比分析 | 比較分析 | Análisis Comparativo | Analyse Comparative | Vergleichsanalyse |
| SCOPE | 研究范围 | 調査範囲 | ALCANCE | PORTÉE | UMFANG |
| Domain boundary | 领域边界 | 領域の境界 | Límite del dominio | Limite du domaine | Domänengrenze |
| Out of scope | 不在范围内 | 対象外 | Fuera del alcance | Hors périmètre | Außerhalb des Rahmens |
| CONSENSUS | 共识 | コンセンサス | CONSENSO | CONSENSUS | KONSENS |
| DIVERGENCES | 分歧 | 見解の相違 | DIVERGENCIAS | DIVERGENCES | DIVERGENZEN |
| Divergence N | 分歧 N | 見解の相違 N | Divergencia N | Divergence N | Divergenz N |
| Supporting | 支持方 | 支持側 | A favor | Pour | Dafür |
| Opposing | 反对方 | 反対側 | En contra | Contre | Dagegen |
| Evidence strength | 证据强度 | 証拠の強度 | Solidez de la evidencia | Force des preuves | Beweisqualität |
| KEY NUMBERS | 关键数字 | 主要数値 | CIFRAS CLAVE | CHIFFRES CLÉS | KENNZAHLEN |
| FAILED_PATHS | 失败路径 | 失敗パス | CAMINOS FALLIDOS | VOIES ÉCHOUÉES | GESCHEITERTE WEGE |
| Why it failed | 失败原因 | 失敗の理由 | Por qué falló | Raison de l'échec | Grund des Scheiterns |
| Conditions for recurrence | 重犯条件 | 再発条件 | Condiciones de recurrencia | Conditions de récurrence | Wiederholungsbedingungen |
| CORE_TENSION | 核心矛盾 | コアの緊張 | TENSIÓN CENTRAL | TENSION CENTRALE | KERNSPANNUNG |
| CONSTRAINTS | 约束条件 | 制約 | RESTRICCIONES | CONTRAINTES | EINSCHRÄNKUNGEN |
| Hard constraints | 硬约束 | ハード制約 | Restricciones rígidas | Contraintes dures | Harte Einschränkungen |
| Soft constraints | 软约束 | ソフト制約 | Restricciones blandas | Contraintes souples | Weiche Einschränkungen |
| Self-imposed constraints | 自设约束 | 自己設定制約 | Restricciones autoimpuestas | Contraintes auto-imposées | Selbst gesetzte Einschränkungen |
| OPEN_QUESTIONS | 待解问题 | 未解決の問題 | PREGUNTAS ABIERTAS | QUESTIONS OUVERTES | OFFENE FRAGEN |
| DECISION_READINESS | 决策准备度 | 意思決定準備度 | PREPARACIÓN PARA DECIDIR | MATURITÉ DÉCISIONNELLE | ENTSCHEIDUNGSREIFE |
| Can decide now | 现在可以决定 | 今すぐ決定可能 | Se puede decidir ahora | Peut être décidé maintenant | Jetzt entscheidbar |
| Cannot decide yet | 现在不能决定 | まだ決定不可 | No se puede decidir aún | Ne peut pas encore être décidé | Noch nicht entscheidbar |
| Single most valuable piece of missing information | 最值得补的一条信息 | 最も重要な未収集情報 | Información faltante más valiosa | Information manquante la plus précieuse | Wertvollste fehlende Information |
| Decision confidence index | 决策信心指数 | 意思決定信頼度指数 | Índice de confianza en la decisión | Indice de confiance décisionnelle | Entscheidungsvertrauensindex |
| Time sensitivity | 时间敏感度 | 時間的緊急性 | Sensibilidad temporal | Sensibilité temporelle | Zeitkritikalität |
| Reversibility | 可逆性 | 可逆性 | Reversibilidad | Réversibilité | Umkehrbarkeit |
| SOURCES | 来源 | 情報源 | FUENTES | SOURCES | QUELLEN |
| Source | 来源 | 情報源 | Fuente | Source | Quelle |
| Type | 类型 | タイプ | Tipo | Type | Typ |
| Retrieved | 获取时间 | 取得日時 | Recuperado | Récupéré | Abgerufen |
| Access Status | 访问状态 | アクセス状態 | Estado de acceso | Statut d'accès | Zugriffsstatus |
| Full text | 全文获取 | 全文取得 | Texto completo | Texte complet | Volltext |
| Snippet only | 仅摘要 | スニペットのみ | Solo fragmento | Fragment seulement | Nur Ausschnitt |
| Unreachable | 不可达 | アクセス不可 | Inaccesible | Inaccessible | Nicht erreichbar |
| RESEARCH_LOG | 研究日志 | 調査ログ | REGISTRO DE INVESTIGACIÓN | JOURNAL DE RECHERCHE | FORSCHUNGSPROTOKOLL |
| Region Focus | 地域聚焦 | 地域フォーカス | Enfoque Regional | Focus Régional | Regionaler Fokus |
| Research Languages | 研究语言 | 調査言語 | Idiomas de Investigación | Langues de Recherche | Forschungssprachen |
| Information Confidence | 信息置信度 | 情報信頼度 | Confianza en la Información | Confiance Informationnelle | Informationsvertrauen |
| Biggest Knowledge Gap | 最大知识缺口 | 最大の知識ギャップ | Mayor Brecha de Conocimiento | Plus Grande Lacune | Größte Wissenslücke |
| Actionable Decision Scope | 当前可决策范围 | 意思決定可能範囲 | Alcance de Decisión Accionable | Portée Décisionnelle | Entscheidungsrahmen |
| COMPARISON MATRIX | 对比矩阵 | 比較マトリクス | MATRIZ DE COMPARACIÓN | MATRICE DE COMPARAISON | VERGLEICHSMATRIX |
| Dimension | 维度 | 次元 | Dimensión | Dimension | Dimension |
| Evidence Strength | 证据强度 | 証拠の強度 | Solidez de evidencia | Force des preuves | Beweisqualität |
| STRENGTHS | 优势 | 強み | FORTALEZAS | FORCES | STÄRKEN |
| Strengths | 优势 | 強み | Fortalezas | Forces | Stärken |
| RISKS | 风险 | リスク | RIESGOS | RISQUES | RISIKEN |
| Risks | 风险 | リスク | Riesgos | Risques | Risiken |
| WHEN TO CHOOSE | 适用场景 | 選択シナリオ | CUÁNDO ELEGIR | QUAND CHOISIR | WANN WÄHLEN |
| Choose [X] when | 选择 [X] 的场景 | [X] を選ぶシナリオ | Elige [X] cuando | Choisir [X] quand | [X] wählen wenn |
| Neither fits when | 两者都不适合时 | どちらも適さない場合 | Ninguno sirve cuando | Ni l'un ni l'autre quand | Keiner passt wenn |
| RECOMMENDATION | 建议选择 | 推奨 | RECOMENDACIÓN | RECOMMANDATION | EMPFEHLUNG |
| Recommended | 推荐 | 推奨 | Recomendado | Recommandé | Empfohlen |
| Rationale | 理由 | 根拠 | Justificación | Justification | Begründung |
| Preconditions | 前提条件 | 前提条件 | Condiciones previas | Conditions préalables | Vorbedingungen |
| LANDSCAPE | 竞争格局 | 競争環境 | PANORAMA | PAYSAGE | WETTBEWERBSLANDSCHAFT |
| Key players | 主要玩家 | 主要プレイヤー | Actores clave | Acteurs clés | Hauptakteure |
| Market structure | 市场结构 | 市場構造 | Estructura del mercado | Structure du marché | Marktstruktur |
| Notable recent moves | 近期重要动态 | 最近の重要な動き | Movimientos recientes notables | Mouvements récents notables | Bemerkenswerte Entwicklungen |
| IMPLICATIONS | 影响与意涵 | 含意 | IMPLICACIONES | IMPLICATIONS | IMPLIKATIONEN |
| SCENARIOS | 情景分析 | シナリオ分析 | ESCENARIOS | SCÉNARIOS | SZENARIEN |
| Base case | 基准情景 | ベースケース | Caso base | Scénario de base | Basisszenario |
| Upside scenario | 乐观情景 | アップサイドシナリオ | Escenario optimista | Scénario optimiste | Positivszenario |
| Downside scenario | 悲观情景 | ダウンサイドシナリオ | Escenario pesimista | Scénario pessimiste | Negativszenario |
| Key variable driving divergence | 关键分叉变量 | 分岐を決める主要変数 | Variable clave de divergencia | Variable clé de divergence | Schlüsselvariable |
| Next concrete action | 下一步具体行动 | 次の具体的なアクション | Próxima acción concreta | Prochaine action concrète | Nächste konkrete Maßnahme |
| File | 文件路径 | ファイル | Archivo | Fichier | Datei |
| Generated | 生成时间 | 生成日時 | Generado | Généré | Erstellt |
| Mode | 研究模式 | モード | Modo | Mode | Modus |

**For languages not in this table**: translate naturally into the target language.
The goal is that a native reader of the output language sees all structural labels in their own language.
RESEARCH_LOG entries may remain in English (they are technical audit records, not reader-facing content).

***

## OUTPUT PERSISTENCE
After generating the output:
1. Determine the output path from SEMANTIC INTENT ANALYSIS Q5 (user-mentioned path, or default context/[domain].md)
2. Print confirmation: "✅ Research output saved to: [path]"
3. Before writing, check if the target file already exists
4. If file exists AND the intent is NOT "update":
   - STOP and ask the user: "File [path] already exists. Overwrite, append, or cancel?"
   - "Overwrite" → replace the entire file
   - "Append" → add new content after existing content
   - "Cancel" → abort, do not write
   - Only proceed if user explicitly confirms
5. If file does not exist: create parent directories and write normally

***

## EXTERNAL ENDPOINTS

This skill uses the following external services:

| Service | URL | Data sent | Purpose |
|---------|-----|-----------|---------|
| Web search provider | Depends on configuration (e.g. api.serper.dev, api.tavily.com, api.search.brave.com) | Search query strings | Fetching search results for research |
| Web pages | Any URL returned by search results | HTTP GET request only (no user data sent) | Full-text fetch for evidence verification |

No user data beyond the research query is sent to any external service.
The research query itself is sent to the configured search provider as a plain search string.

***

## SECURITY & PRIVACY

- **What leaves your device**: The research topic/query (as a search string), and HTTP GET requests to web pages found in search results.
- **What stays local**: All generated reports are saved to the local filesystem only. No report content is sent to any external service.
- **API keys**: Search provider API keys are read from environment variables and sent only to the corresponding provider's API endpoint. They are never logged or included in output files.
- **No telemetry**: This skill collects no usage data, analytics, or telemetry of any kind.

***

## TRUST STATEMENT

When you use deep-researcher:

1. Your research query is sent to the web search provider you configured (Serper, Tavily, Brave, Gemini, or similar).
2. The skill fetches full text from web pages identified in search results — these are standard HTTP GET requests, no different from opening a page in a browser.
3. All analysis, synthesis, and report generation happen locally within the AI agent's context.
4. The final report is written to your local filesystem at the path you specify (or `context/[domain].md` by default).
5. Nothing else leaves your machine.
