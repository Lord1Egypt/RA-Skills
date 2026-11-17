# Verification details (v1.10)

> **30 秒导航**：五态判定完整阈值与检查明细——先看判定语义节，再按标识符（DOI/PMID/arXiv/URL）查对应检查；开关语义含 --cn/--proxy/--review-kit/--doctor。

> **30 秒入口**：何时读我——想弄懂某个判定为什么是 partial/invalid、或要配 --judge-url/--nli-url 等进阶旗标时。最短路径：先看「五态判定」表 + `--explain N`（CLI 直接人话解释单条，v3.12）再决定要不要深读本篇。回 [INDEX.md](INDEX.md)。


Full semantics of every check `verify_refs.py` performs. SKILL.md keeps the
short version; this file is the complete reference.

## Cross-check rules by identifier

- **DOI** (v1.4+): DOI.org content negotiation returns the registered CSL
  metadata. Title similarity < 0.50 → `invalid` ("real DOI, wrong paper" —
  fabricated or mis-cited); 0.50–0.82 → `partial` (human review); ≥ 0.82 →
  consistent. Year difference ≥ 2 adds a warning note. A DOI the registry has
  never heard of (404) → `invalid`, never `unreachable`.
- **PMID**: NCBI E-utilities esummary. PubMed's own web pages return 2xx even
  for nonexistent PMIDs, so only the API actually catches fabrications.
- **DOI ↔ PMID cross-check** (v1.6): when both keys are present, the PMID's
  registered DOI must match the claimed DOI — a mismatch is `invalid`
  ("stitched fake": each key real, pointing at different papers).
- **Journal name** (v1.6): claimed source vs DOI-registered container-title.
  NLM-style abbreviations are treated as equivalent (word-initial sequential
  match, stop-words skipped); cross-language names are not comparable and are
  skipped. A real mismatch downgrades to `partial` (journals do rename).
- **Author names** (v1.7): claimed surnames matched against the CSL author
  list; any hit counts (spelling variants tolerated); single-letter initials
  never substring-match (APA "Torvalds, L." would otherwise match any "G.").
  CJK-vs-Latin names are skipped (not comparable). A full miss downgrades to
  `partial`.
- **arXiv** (v1.5): official export.arxiv.org API (≥3 s/request politeness
  pause). Unknown ID or API error element → `invalid`. Same 0.50/0.82
  similarity thresholds as DOI.
- **Retraction** (v1.8, semantics current as of v4.1): Crossref REST API
  `updated-by[]` (Retraction Watch data, updated daily). Notice types are
  graded, not binary: retraction / partial-retraction / withdrawal →
  `partial` + human-review flag (retracted flag in workpaper); Expression of
  Concern → caps `verified` at `partial`; correction → note only. A failed
  check is flagged explicitly (`check_failed`) — never silently skipped and
  never penalize a reference for the checker's network.
- **OpenAlex bibliographic check** (v1.8, v1.9 keys): for references without
  DOI/PMID/arXiv, title search against OpenAlex. Best of full/prefix title
  similarity ≥ 0.82 → "confirmed exists"; 0.60–0.82 → "near match, review";
  below → honest "no obvious match, not evidence of fabrication" (coverage
  lag). HTTP 403 → actionable hint to configure `--openalex-key` /
  `OPENALEX_API_KEY` (OpenAlex requires API keys for production use since
  2026-02; keyless calls still work within a free allowance).
- **Semantic Scholar third source** (v1.9): when a DOI reference's DOI.org
  metadata could not be fetched (network restricted / transient 5xx), the DOI
  is re-queried at the S2 Graph API. Confirmation (title similarity ≥ 0.82)
  adds a second-source note and enables the anti-bot rescue below. S2 record
  quality is uneven (real papers registered as journal ToC pages have been
  observed), so **S2 never speaks negatively**: mismatches and misses are
  silent. Optional `--s2-key` / `S2_API_KEY` (keyless shares a rate pool;
  client paces ≥1.5 s between S2 calls).
- **Semantic Scholar title search** (v1.10): references carrying neither
  DOI/PMID nor arXiv get one extra positive signal — the title is queried at
  the S2 `/paper/search` endpoint (best-of full/prefix similarity ≥ 0.82 →
  "confirmed exists"). Same discipline as above: confirmation only, misses
  and mismatches silent (titles < 18 chars are skipped — search noise).
  Per S2 API docs, hyphenated query terms return no results, so hyphens are
  normalized to spaces before encoding.

## Parallel verification & degraded-network mode (v1.10)

- `--workers N` (default 4): references are independent, so up to N of them
  are verified concurrently (offline mode and `--workers 1` stay serial).
  Progress lines print in completion order; the report/JSON keep strict
  index order. Shared state (host circuit breaker, arXiv/S2 rate pacing) is
  lock-protected, so politeness guarantees hold under parallelism. The
  per-reference `--interval` pacing applies to the serial path; the parallel
  path throttles through concurrency itself.
- **Degraded-network mode**: when ≥ 3 *different* hosts fail at the transport
  layer within one run (a restricted-egress signature), remaining lookups to
  not-yet-confirmed hosts are skipped immediately with an honest
  "global network degraded" note plus a one-line suggestion (configure a
  proxy / switch networks and rerun), and the run prints a summary advice
  line. Site-level HTTP responses (403/429 rate limits, anti-bot) never
  count toward degradation — the egress path itself is proven working when
  any server answers. Once degraded, transport retries stop (fast-fail).
  The per-host v1.6 circuit breaker still applies independently.
- **Intra-run cache**: a reference whose DOI/URL/PMID/arXiv matches an
  already-verified one reuses that verdict (note says so) instead of
  re-hitting the network. `mark_duplicates` still applies afterwards — the
  cache never promotes a duplicate.

## Rescue rules (anti-bot, anti-flaky-network)

- Landing page 403/429 but registry metadata confirmed (DOI.org, arXiv, or
  S2): existence is proven, so the reference is NOT `unreachable` — it is
  judged on tier/fields like any 200 page (trusted tier + complete fields →
  `verified`; any partial adjustment or missing field → `partial`). This
  prevents "metadata confirmed + 403 blog page" from slipping through.
- arXiv resolver 404 with unconfirmed metadata → `invalid` (official registry
  says no such ID).
- Wayback Machine (v1.5): every `unreachable` link is checked against
  archive.org; an archived copy adds a dated comparison link for human review.

## Rate limiting & resilience

- Host circuit breaker (v1.6): 2 consecutive *transport* failures
  (timeout/DNS/refused) → remaining calls to that host are skipped for the
  batch with an honest note. HTTP responses (403/404/429…) never trip it.
  Retries within one logical call count once.
- Transient failures retry once; error notes carry the cause (timeout / DNS /
  refused) and the fix (`--timeout 20` for slow links).
- 429 with `Retry-After` (v1.9): the DOI metadata check waits the requested
  duration (capped at 5 s) before its retry.
- `--mailto you@lab.edu` (v1.9): appended to Crossref requests — enters the
  Crossref polite pool with more generous rate limits. Recommended for CI and
  institutional batches. arXiv politeness (3 s/request) and S2 pacing (1.5 s
  keyless) are always on — both are global under parallel verification.
- OpenAlex hints (v1.10): 403 and 429 both explain the key situation —
  OpenAlex has required API keys for production use since 2026-02 (keyless:
  100 credits/day); configure `--openalex-key` / `OPENALEX_API_KEY`.

## Exports

- `--export bibtex`: verified-only bibliography, Zotero/EndNote-ready (PMID /
  arXiv eprint noted). Field values sanitized (brace/newline stripped).
- `--export csv`: full audit ledger (all refs, all fields, formula-injection
  neutralized, utf-8-sig for Excel).
- `--export auditjson` (v1.9): machine-readable working paper — per reference,
  which checks ran and what they found (`checks_catalog` documents every check
  type), plus a generation timestamp. Purpose: transparency and institutional
  audit. The July 2026 arXiv survey of citation checkers (arXiv 2607.22693)
  found none of five evaluated tools reliable enough to run unsupervised and
  calls for "transparent multi-source detection systems" — the audit trail is
  this skill's answer: a human can re-trace every mechanical verdict.

## Persistent disk cache (v1.12)

`--cache` is on by default. Stable verdicts (`verified` / `partial` /
`invalid`) are stored in a local SQLite database
(`~/.cache/cite-holmes/cache.sqlite3`, standard library) keyed by every
judgment-relevant input: identifier, claimed title/year/source/authors, tier,
verifier version, and profile — the same DOI with a different claimed title is
a different cache key, because title-similarity verdicts depend on the claim.
TTL is 168 h (`--cache-ttl`); `unreachable` is never cached (transient);
`--offline` results are never cached; `--strict` bypasses cache reads so CI
always runs live; `--refresh-cache` bypasses reads but still writes;
`--no-cache` disables the store entirely. Cache hits append an explicit
"磁盘缓存命中" note with the age, so an audited report always shows when a
verdict came from the network and when from the local store. What this buys:
re-running or extending a bibliography no longer re-travels the ocean —
the repeat-run pain flagged in every evaluation's Trust score.

## Proxy support (v1.12)

`--proxy http://host:port` (scheme optional) routes all verification traffic
through the given proxy; without the flag, urllib's standard
`HTTP_PROXY`/`HTTPS_PROXY` environment handling applies. Combined with the
v1.10 degraded-network mode, restricted-egress environments get one fast,
honest pass instead of minutes of stalls.

## BibTeX input (v1.9)

`--refs bibliography.bib` is auto-detected (extension `.bib`, or content
starting with `@` when JSON parsing fails). Minimal pure-stdlib parser:
`@article`/`@inproceedings`/`@book`/`@misc` and other entry types, nested
braces, quoted and bare values, `@comment`/`@preamble`/`@string` skipped.
Mapped fields: title, author (` and ` → `, `), year, journal/booktitle/
journaltitle/publisher → source, doi, url (including `\url{...}` macros in
howpublished/note), pmid, eprint+archivePrefix → arxiv. Unparseable entries
degrade to missing-field references and are judged honestly by the normal
pipeline; zero entries → actionable error.

## Verdict meanings (unchanged since v1.3)

| Verdict | Meaning | Score |
|---|---|---|
| `verified` | reachable + trusted tier + fields complete | +10 |
| `partial` | reachable but community tier / field or metadata concerns | +4 |
| `unreachable` | fetch failed — needs human check, ≠ nonexistent | 0 |
| `unverified` | skipped (`--offline`) | −2 |
| `invalid` | no identifier, registry says no, or stitched fake | −8 |

## arXiv 第二源 fallback（v1.11）

export.arxiv.org API 对批内多请求偶发 406/403（反机器人窗口；3 秒全局控频可降频
率、不能归零，实测单发全 200、批内可稳定 406）。v1.10 及之前 API 失败即静默跳过
内容核验，同一引用两次运行会漂移（一次 verified 一次 partial）。v1.11 起：

1. API 首败后指数退避（3s 时隙 + 5s 退避）重试一次；
2. 仍失败 → fallback 拉官方着陆页 `arxiv.org/abs/<id>`，剥掉 `[ID] ` 前缀后做
   标题相似度比对（0.50/0.82 阈值与 API 路径一致）；
3. 着陆页 404 → `invalid`（官方库查无）；着陆页也不可达 → 维持可达性路径判定，
   note 明示「元数据核验未完成」，不静默。

API 明确回答（Atom feed 正常返回）时行为不变：查无记录/格式错误 → `invalid`。
非 Atom 响应（反爬 HTML 页，常是合法 XML）**不作为查无依据**，走 fallback——
防止瞬态反爬把真论文误杀成编造。

## 批次耗时预期（2026-10 实测，20 条混合清单，DOI.org/Crossref/PubMed 全路径）

| 场景 | 实测 | 推算 100 条 |
|---|---|---|
| 冷缓存 · `--workers 4`（默认） | ~18s（≈0.9s/条） | ~1.5–3 分钟 |
| 热缓存重跑（同清单 7 天内） | ~7s | 秒级～1 分钟 |
| 冷缓存 · `--workers 1` | ~47s（≈2.3s/条） | ~4–8 分钟 |

影响因素：条目类型（DOI+URL 双核验最慢）、注册库当刻限流（429 退避）、
弱网（`--cn` 下限 25s 会让 unreachable 判定更慢但更稳）。大批量（>100 条）
建议先 `--preflight` 看注册库状态，再用 `--workers 4` 默认并行；CI 里加
`--strict` 时把任务超时按上表 ×2 预留。

## 多语言处理边界（中英之外）

判定守卫按**文字系统族**工作（v3.15）：Latin / Cyrillic / Greek / Han /
Kana（日文）/ Hangul（韩文）。声称题名与注册库登记题名**主导文字系统不同**
时——俄文引文对英文登记、希腊文对拉丁、日文对中文——相似度不作编造依据，
一律走跨语言守卫（partial 转人工或桥接核验升级）。

- 同族同语（德文声称 vs 德文登记、法语 vs 法语）：正常相似度比对 ✓
- 同族跨语（德文声称 vs **英文**登记）：相似度比对照常——西文互译题名差异大，
  低相似度会被判 invalid；此类引用请附原文题名，或把英文题名一并写入
  `title`（分号分隔均可识别）
- 桥接核验的三级通道（original-title / DOI 落地页 / OpenAlex）对各族语言
  同样生效；OpenAlex 对非英语文献的收录有滞后，「桥接未命中」不构成编造证据

## 无标识符医学引用（Vancouver 格式）核验（v4.0.0）

医学文档参考文献的主流形态是 Vancouver 纯文本（作者. 题名. 期刊. 年;卷(期):页.，
无 DOI/PMID/URL）。v4.0.0 起：

1. **直接核验**：`--refs` 接受 `.md` 文件——自动从「## 参考文献」节提取 Vancouver
   编号条目（`1. 作者. 题名. 期刊. 年;卷(期):页.`），无需手工转 JSON。
2. **PubMed 题名反查**：无标识符引用先走 PubMed 题名实词检索（区分词 [Title] AND，
   5→4→3 词递减放宽）——命中且题名相似度 ≥0.82（序列+词集 Jaccard 双通道取大）升
   `verified` 并回填 PMID 锚；0.50-0.82 近似命中转人工；未命中静默转 OpenAlex/S2。
   查无永不判死（收录面=生物医学，中文文献/非生物医学未命中属预期）。
3. **大批量限流边界**：反查走 E-utilities（无 key 3 req/s）——实测 30 条连续反查中后段
   可能触发 NCBI 限流静默未命中。大批量医学文档建议：配 `NCBI_API_KEY`（提至 10 req/s）
   或分批（每批 ≤20 条）重跑；报告 `checks.pubmed_reverse` 的限流注记可辨识受影响条目。

## `--review-kit`（v4.9.0 综述工作台）

报告与 JSON 之外另出 `<out-stem>.review_kit.md` 三件套：综述表格（verified
优先、同判定保持原序，带被引数与 ⚠需人工 旗标）/标注书目（判定语义+注记
摘要+DOI/PMID 链）/即贴 GB/T 7714 参考文献表。未显式给 `--export` 时自动补
`gbt7714,bibtex` 导出（显式指定则完全以用户为准）。

- **被引数来源（零新增外呼）**：优先核验期 S2 citation contexts
  （`checks.citation_contexts.cited_by`，仅 DOI 条目）；`--discover` 场景回退
  OpenAlex 检索响应自带的 `cited_by_count`；两者皆无显示「—」。
- **GB/T 内联表与 `--export gbt7714` 同一构造器**（`_gbt7714_entry`），
  收录策略同为「宁缺毋错」：verified 全收，partial 仅当 DOI 元数据一致。
- **判定语义原样透出**：partial/invalid 绝不混入「已核实」观感；工作台是
  交付物形态，不是判定升级通路（铁律：存在性佐证与判定分离）。


## 学界用法与分歧信号（v5.0.0 usage_line / v5.9.0 context_signal）

- **学界用法一句话**（报告/工作台/HTML 三处共用）：S2 引文语境的用法分布
  （方法学/背景/结果——S2 官方 intents 三分类）+高影响引用数+第一条例引。
- **分歧信号（v5.9.0，启发式 advisory）**：S2 intents 不标注争议性，本地对
  抽样语境做对比/质疑句式扫描（however/然而/质疑/并不一致等中英模式），
  命中 ≥50% 抽样才提示「学界对该文结论存在不同声音」——保守阈值避免把
  常规转折词误渲染成学术争议。**纯呈现层：绝不改判定、不挂复核旗**；
  启发式双向皆有边界（漏报：反讽/转述式批评不在模式库；误报：转折词的
  非分歧用法），提示语一律引导人工复核原文语境，不代下结论。
- 语境层零新增外呼：复用核验期已取的 S2 citation contexts；无语境数据
  整段不渲染（老输出逐字节不变）。


## 深度研究控制（v5.2.0：--plan / --preset deep / --source-policy / --trace）

- **`--plan plan.json --plan-out plan.md`**：研究计划的机械层校验与渲染。
  硬失败（exit 2）：subquestions 非非空字符串数组 / budget_searches 非正整数 /
  结构非对象；CALIBRATE 四要素（scope/timeframe/audience/format）缺失=WARN 不
  阻断（agent 可用声明过的默认值）。md 是渲染产物，JSON 才是执行锚点；仅
  `--plan` 不带核验输入时渲染完即退（协作定稿流）。
- **`--preset deep`**：discover 上限抬至 25、超时下限 20s（单调抬升不覆盖用户
  显式更大值）；搜索预算 ≤40 轮由 agent 侧遵守；建议配 `--workers 8`。
- **`--source-policy`**：段格式 `journal_only` / `allow-domain=a.org|b.org` /
  `deny-domain=x.com`，逗号分隔可组合。discover 期：journal_only 硬过滤
  （PubMed 题录天然期刊；OpenAlex 按 source.type==journal）。核验期：违规
  **只注记+转人工**（checks.source_policy + note + needs_human_check），判定
  永不因政策改变——政策是策展偏好，不是真伪证据（ADR-0005）。
- **`--trace trace.md`**：append-only 研究底稿，discover/verify 各轮追加
  （时间戳/主题/命中/判定分布/CiteScore）；只追加绝不改写；写失败静默
  （底稿绝不阻断主流程）。


## 持久研究档案与公开评测（v5.3.0：--research-profile / tools/run_eval.py）

- **`--research-profile p.json`**：跨会话研究偏好。三键（preset / source_policy /
  export）作**默认值**注入——显式 CLI 旗标优先，只填空缺；未知键注记忽略；
  非法值 exit 2。档案是过程偏好，绝不改判定语义（与 ADR-0005 同纪律）。
- **`tools/run_eval.py`**：留出集评测公开口径——内置金标集（8 条 3 预埋伪造）
  默认 offline 跑，输出 capture_rate / strict_capture / false_kill_rate /
  判定分布；`--refs your_labeled.json` 自备标注集（expected: planted/clean）、
  `--net` 在线口径。方法论与最新数字：`docs/benchmark.md`（数字可复现，
  在线口径只对当日快照负责）。


## 审查与审计（v5.4.0：--reviewer / --audit-mode）

- **`--reviewer`**：核验报告尾部追加审稿人预演问题单（--grill 同款生成器
  就地嵌入，免二跳）；判定不变。
- **`--audit-mode`**：输出 `<out>.audit.md` 稿件审计报告——疑点三级分层
  （P0 编造嫌疑=invalid / P1 高风险=撤稿·不可达 / P2 复核=政策注记·partial
  缺字段）+完整性（--check-document 时含覆盖率/孤儿）+行动清单。面向
  编辑/审稿人/教师场景；机械层口径，只重组既有判定与线索，绝不新造判定。
- **MCP 后端形态**：mcp/README.md 含「作为任何 Deep Research agent 的
  核验后端」接线示例（verify_references 进研究循环、invalid 触发重搜）。


## 投稿前审计包（v6.1.0：--check-paper / tools/selfcheck.py）

- **`--check-paper doc.md`**：一条命令产出投稿前审计包——内部组合
  `--check-document`（同一条稿件解析通路，复用不重造）+ `--audit-mode`
  （P0/P1/P2 分级）+ `--strict` + GB/T/BibTeX 导出，另出 `<out>.INDEX.md`
  总览件：机械层投稿就绪结论（READY/NOT READY）+判定分布+阻断清单/
  待办清单+包内工件导航。
- **就绪判据**（`submission_readiness`，与 audit 分级同源）：P0=0 且撤稿=0
  且不可达=0 → READY；P2 与完整性问题不阻断（有明确人工复核路径），
  只列待办。**诚实边界：机械层就绪 ≠ 学术就绪**——语义支撑、查重、期刊
  格式由作者与期刊流程负责，READY 结论行强制随附该声明。
- **组合旗标不改判定语义**：--check-paper 与逐项手敲同批参数的判定/导出/审计报告内容一致
  （同批口径；各件嵌生成时间戳故非逐字节相同，只多 INDEX 一件）。
- **`tools/netcheck.py`**（v6.3.0 真网稳定性自检；v6.5.0 增 N5）：注册库实时可达性+
  判定圆环+埋雷矩阵+跨库一致性一条命令验证——N1 八注册库探针/N2 PubMed 实时圆环
  （esearch→esummary 登记题名原样）/N3 Crossref 实时圆环/N4 埋雷矩阵
  （错配 DOI/编造 DOI/假 arXiv/死链域全落网+真引用零误伤）/N5 跨注册库一致性
  （同一真实 DOI 在 Crossref/OpenAlex/PubMed 三库的登记题名归一互比 ≥0.85；
  引擎判定依赖多库元数据交叉，库间不一致=输入面失真信号；任一库不可达=SKIP
  诚实边界，三库齐才可比）。引用数据全部当场实时拉取；`--quick` 只跑探针+埋雷。
  退出码 0/1，agent 宿主/CI 可当部署后验证钩子。诚实边界：测「判定通路在真实
  网络下的稳定性」，不测注册库覆盖率；单库抖动属诚实态（探针 ≥6/8 过）。
- **两级验证体系**：`selfcheck.py`（offline 安装验证，零外呼）+
  `netcheck.py`（真网稳定性验证）——装好后先 selfcheck、部署/配网后
  netcheck，两级全绿即安装与环境双重就绪。
- **`tools/selfcheck.py`**（随包自检；v6.5.0 增 --tests）：安装完整性一条命令验证——引擎
  壳+七层布局导入、核心判定 API 在位、金标集 offline 真跑（3 处预埋伪造
  全落网+干净条目零误杀，capture 100% 同 docs/benchmark.md 口径）、GB/T
  导出冒烟；`--mcp` 加测 mcp/ 副本独立加载与 CLI；`--tests` 加测随包 sealed
  测试子集（v6.5.0 F57：tests/shipped_manifest.json 清单制，run_tests.sh
  --shipped，ADR-0011 修订 ADR-0010 边界——sealed 子集随包可复验，全量矩阵
  仍开发侧）。退出码 0/1，agent 宿主
  可当安装验证钩子。

## 本地文献库与下一轮种子（v5.5.0：--refs-dir / --next-round）

- **`--refs-dir DIR`**：目录（或单文件）下全部 .json/.bib/.md 按文件名排序一次
  装载进同一核验批；README* 跳过；坏文件警告跳过（批量韧性），全零才失败。
  Zotero/JabRef 导出目录即扫即验。
- **`--next-round report.json`**：从核验 JSON 提取未决条目
  （partial/unreachable/unverified；**invalid 不回收**——终局判定不重撞）
  生成 `<stem>_next_round.json` 重验骨架（`refs` 数组 + `_retry_reason` 供人读，
  引擎忽略未知键）。零网络，判定原样透出，骨架是输入不是结论。

## arXiv 标题别名守卫（v5.5.0 整合，判定语义修订点）

`arxiv_metadata_match` 在相似度 <0.50 的判死分支前新增别名检查：用户题名
实词（≥2 个；拉丁按词、CJK 按字符——中文无分隔符，停用字表「的与和及对在中」
独立维护）**全部**出现在登记题名中 → 判
「截短/异序别名」partial（转人工+登记全称建议），而非 invalid。
反伪造面不变：编造引用（ID 指向完全无关论文）与登记题名词集交集低，仍走
invalid。dogfood 实证：STOP(0.42)/Neutropenia/Transaminitis 等 4 例截短题名
此前被误判 invalid——真文献×不精确题名 ≠ 编造。


## 开放获取与 MCP 工具面（v5.6.0）

- **开放获取查询（Unpaywall）**：verified 的 DOI 条目且配置 `--mailto` 时，
  查 Unpaywall 官方 API 得 is_oa/license/oa_url（`checks.open_access`）。
  报告头部出「开放获取 X/N 条可免费读取」汇总，综述工作台书目逐条标注。
  **纯数据富集**：无 mailto/失败/未收录一律静默；绝不参与判定（ADR-0005）。
  Unpaywall 要求 mailto 礼貌标识——复用 `--mailto`（Crossref polite pool 同源）。
- **MCP 新工具**：`discover_references`（主题检索双源+出生即核验，深度研究
  agent 的检索步直连；limit 封顶 25）、`build_review_kit`（results 数组→
  综述就绪三件套 markdown，零网络）。工具面从 3→5。
