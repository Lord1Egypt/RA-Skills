# FAQ (moved out of SKILL.md in v1.9 to keep the main guide short)

> **30 秒导航**：高频问题速查——网络（--cn/--proxy/降级）、API key、导出（GB·T/BibTeX/RIS）、判定语义、上下文核验；Ctrl+F 搜关键词，或从 INDEX.md 按任务路由。

**Q: Is a `verified` citation guaranteed real?**
No. The mechanical layer catches machine-checkable fakes: nonexistent DOIs,
fabricated PMIDs (via E-utilities), fabricated arXiv IDs (via the official
arXiv API), dead links, duplicates, stitched DOI↔PMID pairs, wrong-paper
DOIs (title similarity), and retracted papers. A fabricated citation pointing
to a real, plausible page still relies on the semantic layer — never a
guarantee.

**Q: How are arXiv references checked?**
Same treatment as DOIs since v1.5: the official export.arxiv.org API returns
the registered title/year; similarity below 0.50 → `invalid` (fabricated or
wrong ID), 0.50–0.82 → `partial` (human review), above → consistent. An ID the
API has never heard of is `invalid`, not `unreachable`.

**Q: What do I do with `unreachable` references?**
Open them manually once — the report automatically attaches a Wayback Machine
archive link when one exists. If it matters and keeps failing, switch sources.

**Q: Did the PMID check fail because of my network?**
No. "不存在/编造" verdicts come from the official E-utilities API — that means the
PMID genuinely isn't in PubMed. Only "校验失败" wording means a network/API issue
(the reference is then treated as reachable and flagged).

**Q: Do I always need `--profile medical`?**
Use `--easy`: one flag auto-detects medical references, enables the medical
profile, and exports BibTeX + CSV automatically. For real clinical
conclusions, still prefer explicit `--profile medical`.

**Q: Can verified references go straight into my paper?**
Yes: `--export bibtex` exports only `verified` entries (with PMID / arXiv
eprint notes) and imports into Zotero/EndNote; `--export csv` is the full
audit ledger for advisors and editors; `--export auditjson` (v1.9) is the
machine-readable per-check working paper for institutional audit.

**Q: Which services does verification touch, and what if my network is slow or blocked?**
DOI.org (DOI metadata), NCBI E-utilities (PMID), export.arxiv.org (arXiv
metadata), archive.org (archived copies), api.crossref.org (retractions),
api.openalex.org (bibliographic confirmation), api.semanticscholar.org (third
source + title search, v1.9/v1.10). CN networks occasionally throttle several
of them. The verifier never stalls: transient failures retry once (429 honors
`Retry-After`), error notes tell you the cause with a fix (`--timeout 20` for
slow links), and a host-level circuit breaker skips a host after 2 consecutive
transport failures — with an honest note — instead of hanging the batch.
Since v1.10, references are verified in parallel (`--workers 4` by default —
roughly a quarter of the serial wall time), and when 3+ different hosts fail
at the transport layer in one run (restricted-egress signature) remaining
lookups are fast-skipped with a "全局网络降级" note and a proxy/retry
suggestion. Degraded checks are always labeled, never silently dropped.

**Q: Do I need API keys?**
No — everything runs keyless within public rate limits. OpenAlex has required
keys for *production* use since 2026-02 (free daily allowance; this skill
survives keyless but benefits from `--openalex-key` / `OPENALEX_API_KEY`).
Semantic Scholar keyless shares a rate pool; `--s2-key` / `S2_API_KEY` gets a
dedicated lane. Crossref asks heavy users to identify themselves — pass
`--mailto you@lab.edu` to join the polite pool.

**Q: MCP 模式是什么？agent 不装 skill 怎么用？**
v2.0.0 起仓库内置 `mcp/server.py`（FastMCP）：tools `verify_references`（机械验证）/
`explain_verdict`（判定解释）、resources（能力矩阵/版本史）、prompts（fact-check 工作流）。
推荐直跑：`uvx --from "git+https://github.com/docsor1212/cite-holmes#subdirectory=mcp" cite-holmes-mcp`；
或自行准备 FastMCP 环境后运行 `python mcp/server.py`。零密钥可用；可选 API key 经环境变量注入。

**Q: arXiv 论文有多个修订版怎么办？**
v2.0.0 自动备注：引用未指定版本而论文存在多个修订版 → 提示"引用未指定版本"；
引用指向旧版而存在更新版 → 提示最新版号（旧版可能含未修正内容）。同响应内取数，零额外请求。

**Q: 验证要访问哪些外部服务？国内网络慢怎么办？**
见上方服务清单——全部是官方学术注册库、全部 HTTPS。v1.12 起两件事让它在国内更可用：
① **持久磁盘缓存**默认开（7 天 TTL）：同一批引用复跑直接复用稳定判定、零外呼，
`--refresh-cache` 强制重验；② **`--proxy http://host:port`** 显式走代理（或设
`HTTPS_PROXY` 环境变量），配合网络降级模式，受限出口下也能一次跑完拿到诚实结论。

**Q: 判定结果会被缓存吗？撤稿状态更新了怎么办？**
缓存只存 verified/partial/invalid 三种稳定判定（TTL 默认 168 小时），
unreachable 永不入缓存（瞬态）；`--strict` 模式强制绕过缓存读（CI 诚实）。
撤稿状态这类可变信息以 TTL 为界——对时效敏感的批次用 `--refresh-cache` 强制重验。

**Q: Can I verify references straight from my reference manager?**
Yes, since v1.9: `--refs bibliography.bib` reads Zotero/EndNote/JabRef BibTeX
exports directly (entry types, nested braces, `\url{}` macros; DOI/PMID/arXiv
fields are picked up automatically).

## arXiv 条目 note 里出现「元数据 API 不稳，经官方着陆页标题比对确认」正常吗？

正常。arXiv 的 API 对批内多请求有反机器人窗口（偶发 406/403），与你的网络无关；
验证器已自动回退官方着陆页完成同等强度的标题比对，判定可信度不受影响。

## semantic 字段写什么？

模型逐条判定"来源是否真的支撑所引论断"后，写成结构化对象
`{"claim", "support", "quote", "note"}`（五值：supported / partial /
not_in_source / contradicted / unclear）。`not_in_source` 与 `contradicted`
会被机械验证器封顶为 `partial` 并转入人工复核区——来源存在不等于来源认同。
旧的字符串写法仍接受（仅注记）。

## Q: fast-judge 预筛会改我的判定吗？（v3.5.0）
不会。`--fast-judge-url` 外挂的小型分类器（任何 OpenAI 兼容 /v1 端点均可）只对"语义待定且无官方文本可升级"
的引用追加「倾向支持（供人工参考）」注记——永不产生/修改五态判定，永不标记人工
复核，默认关闭。校准曲线随仓库发布（阈值 0.95）。

## Q: GB/T 7714-2025 导出的数据来源是什么？（v3.6.0）
`--export gbt7714` 仅导出 verified 条目，且每条以**注册库登记的 CSL 元数据**
为准（作者按国标缩写惯例预格式化、期刊/年/卷期页来自 DOI.org/Crossref 登记），
不是你手填的字段。无注册元数据的电子资源按 [EB/OL] + 引用日期输出。

## Q: 国内网络直连核验总超时怎么办？（v3.6.0）
加 `--cn`：超时下限抬到 25 秒，且 DOI.org 三试全败时自动回源
api.crossref.org（独立主机，同构 CSL 元数据，报告注记会写明「经 Crossref
回源」）。仍不通时 `--proxy` / `HTTPS_PROXY` 继续兜底；`unreachable` 不等于
假引用，换网重跑后再下结论。

## Q: 能核验"正文里的引用"而不只是参考文献清单吗？（v3.7.0）
能。`--check-document paper.md --refs refs.json`：解析正文 in-text 标记
（[12]/[1-4]/(Author, Year)/doi.org 链接），把每处引用绑定到清单条目并计算
"引文句 ↔ 被引标题"锚词率——低于 0.34 标记为疑似错配引文（引 A 文却引了 B 句）。
锚词率低≠错引，是语义层人工复核候选；语义判断仍由 agent 负责。

## Q: 触发词误触发了怎么办？
触发词按语义匹配，可能被"查证一下"这类短句误触发。直接说明真实意图即可
（例如"我只要翻译这段"），误触发不产生任何副作用。想让某类请求**不**触发
引用核验：避免同时出现"研究/查证/引用"词与文献清单。

## Q: 中英混合引用（如中文声称+英文登记）会误判吗？
不会判 invalid。v3.0.0 起内置跨语言守卫：声称标题与登记标题跨语言（CJK vs
拉丁）时相似度不作编造依据，降 `partial` 转人工复核（与期刊名核查同款守卫）。
已知边界：跨语言混合引用的锚词率（上下文核验，v3.7.0）同样会偏低——属预期，
按"疑似错配候选"人工复核即可。

## Q: 报告里出现「克隆引用对」是什么意思？要删掉这两条吗？（v3.10.0）
不用急着删。克隆对 = 同一标题挂了多个不同 DOI（或同一 DOI 挂不同标题）——至少一个
标识有误，但也可能是预印本 DOI 与期刊版 DOI 并存的合法场景。看两条各自的判定：
verified 的是真的、invalid 的是假的；克隆注记只负责让这一对进入你的视野，判定以
元数据核验为准。

## Q: 清单画像的「标识符近邻簇」说我批量生成——我是正常引用怎么办？（v3.11.0）
画像旗标是人工抽查建议，不是判定。同一论文集/连续编号的合法引用确实会命中近邻簇。
按旗标把该簇几条逐条过一遍核验结果即可：全部 verified 就放心用；画像永远不改变
任何单条判定。

## Q: 「该预印本已登记正式发表」提示怎么处理？（v3.11.0）
你的 arXiv 引用有了期刊正式版。把引用条目的标识换成注记里的期刊版 DOI 后重跑，
确认新版 verified——投稿场景引用预印本常被审稿人挑，这个提示帮你在提交前完成
版本升级。

## Q: 跨语言桥接命中后我还需要做什么？（v3.10.0）
基本不用。桥接命中 = 中文原题与英文登记名经三级核验对上了，判定 verified 可信。
note 里附带了登记英文原题，扫一眼与你认知的论文一致即可（出版商字段理论上可被
刻意布置，一秒钟的人工确认是零成本的保险）。

## Q: 「投稿前终检」一键怎么跑？（v3.12.0）
`python scripts/verify_refs.py --refs research_refs.json --out report.md --preset submission`
——一键组合严格退出码（CI 可拦截）与 GB·T 7714/BibTeX/CSV 三导出。判定语义与
默认模式完全一致，只是把投稿场景的常用旗标打包。

## Q: 想看某一条引用为什么被判成这个结果？（v3.12.0）
跑批时加 `--explain 3`（换成条目号）——输出该条的判定语义、依据步骤、错误码翻译、
注记要点、导出完整度与建议动作，人话全文。

## Q: 代理该怎么配？`--proxy` 和环境变量什么关系？（v4.9.0）
两种都认：`--proxy http://127.0.0.1:7890` 只对本次运行生效；
`HTTPS_PROXY`/`HTTP_PROXY` 环境变量对所有外呼生效（脚本走标准 urllib 代理
语义）。两者同时给出时以 `--proxy` 为准。代理只影响传输路径，不改变任何
判定逻辑——`unreachable` 的含义不因有无代理而变化。

## Q: 报告提示「全局网络降级」是什么意思？（v4.9.0）
本批次 3 个以上不同注册库主机连续传输失败（出海受限的典型特征），引擎自动
进入快速诚实模式：后续外呼快速跳过、绝不卡死批量，也绝不把跳过伪装成
「查无」。正确处置：配代理或换网络后重跑（TTL 内已验证条目走磁盘缓存，
重跑只补漏，不重复付费）。

## Q: 断网/离线环境能做什么？（v4.9.0）
三件事可用：`--offline` 只做结构与字段完整性检查（判定不落缓存）；
`--retraction-cache`（先在联网机器跑 `tools/build_retraction_cache.py` 构建
本地索引）离线秒查撤稿；`--doctor`（不带 `--net`）零外呼环境自检。
离线模式的判定一律不带「已核验」含义，恢复联网后请重跑。

## Q: OpenAlex 提示 403/429 要 API key——必须配吗？（v4.9.0）
不是必须。2026 年起 OpenAlex 生产调用建议配 key（无 key 每日仅 100 credits
测试额度，超了返回 403/429）：`--openalex-key` 或环境变量
`OPENALEX_API_KEY`。配不上也不影响核验主通路——DOI.org/PubMed/arXiv 不依赖
OpenAlex；OpenAlex 只在「无标识符引用找锚」与「文献发现」两处参与，失败时
相应条目诚实降级并给出可操作提示。

## Q: `--doctor --net` 末尾的「国内直连建议」怎么看？（v5.0.0）
它统计各注册库探针的直连可达数并给决策提示：全部 PASS→直接跑批；≥2 源可用→
小批量可直连，完整覆盖建议 `--proxy` 或 `--cn`（超时抬升+DOI.org 三败自动回源
Crossref）；可用源不足→先配代理再跑。磁盘缓存 7 天 TTL，配好后重跑只补漏。
建议每次更换网络环境后先跑一次本自检。


## Q: 研究计划/信源政策/研究底稿怎么配合五阶段？（v5.2.0）
PLAN 阶段：agent 起草 `plan.json`（subquestions + budget_searches + CALIBRATE
四要素）→ `--plan plan.json --plan-out plan.md` 校验渲染 → 用户可编辑（JSON 为
准）→ 再执行。SEARCH 阶段：`--source-policy journal_only,deny-domain=x.com`
在文献发现期过滤非期刊源。VERIFY 后：`--trace trace.md` 已逐轮记录审计链
（append-only）。三件都不改任何判定——计划/政策/底稿是过程治理，真伪判定
只来自注册库元数据比对。


## Q: 研究档案会不会改变判定？评测数字怎么复现？（v5.3.0）
档案不会：--research-profile 只注入 preset / source_policy / export 三个
**过程默认值**（显式旗标优先），判定只来自注册库元数据比对。评测：
`python tools/run_eval.py` 一条命令复现内置金标口径（捕获/实锤/误伤/分布），
方法论与诚实边界见 `docs/benchmark.md`——离线口径只测结构层，在线数字只对
当日快照负责。


## Q: 编辑/教师怎么快速筛查一份稿件的引用？（v5.4.0）
`--check-document 稿件.md --audit-mode`：参考文献自动提取+全量核验+审计
风格报告（P0 编造嫌疑/P1 高风险/P2 复核+行动清单）。P0 必须处理；P1 的
不可达≠不存在（换网络复核）；本报告是机械层口径——「来源是否支撑论断」
仍需人工语义判断。

## Q: Zotero 导出的一整个文件夹能一次核验吗？上一轮没验完的怎么续？（v5.5.0）
能：`--refs-dir ~/Zotero/导出/` 把目录下全部 .json/.bib/.md 一次装载进同一
核验批（坏文件跳过并警告）。续轮：上一轮报告跑 `--next-round report.json`
生成未决条目重验骨架（partial/unreachable/unverified；invalid 不回收），
修订后作 `--refs` 输入重跑。两件都不改判定语义。


## Q: 「开放获取」汇总是怎么来的？会不会影响判定？（v5.6.0）
配置 `--mailto` 后，verified 的 DOI 条目会查 Unpaywall 官方 API（免费），
在报告头部给出「X/N 条可免费读取」并在综述工作台逐条标注许可与全文地址
——帮综述作者优先选能立即读的文献。它只回答「有没有免费全文」，**不影响
任何判定**；未配 mailto 或查询失败时整段静默。

## Q: 「处理异常」条目为什么是 unverified 而不是 invalid？（v5.8.0）
invalid 的语义是「机械层确凿判死」（标识符不存在、指向错误论文、拼接伪造）
——程序故障不符合这个语义。核验过程中发生的未知异常（解析/内存/依赖抖动）
现在降为 unverified + 转人工 + 建议重跑，避免把引擎自身的故障伪装成对引用
的判定。若持续复现，请带 `--trace` 与报告 JSON 反馈。
