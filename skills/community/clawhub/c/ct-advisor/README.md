# Clinical Trial Chief Advisor (ct-advisor)

- **English guide** → [README.md](https://github.com/medstatstar/ct-advisor/blob/main/README.md) · **中文指南** → [README\_zh-CN.md](https://github.com/medstatstar/ct-advisor/blob/main/README_zh-CN.md)

<div align="center">
<img src="assets/icon.svg" width="240" height="240" alt="ct-advisor logo"/>
</div>

> **Works without installation:** If you'd rather not install and just want to quickly use this skill's basic features, you can also visit the ct-series unified web portal **https://ct.medstatstar.com** directly.

> **The single front door for the whole `ct-*` clinical-trial skill family — a methodology & regulatory-evidence advisor that also routes real-data / competitive-intel needs to the sibling data skills through a local, code-only orchestrator (`orchestrate.py`) and stitches their results back in code.**
>
> No commands or manual needed. Just describe your trial question **in plain language inside a chat** — the advisor passes every **non-vague** question to the local orchestrator (`orchestrate.py`), which calls the Coze cloud workflow for methodology / study-design / statistics / compliance-response / trial-operations / deliverable-drafting / GCP / safety / regulatory / QC / data-management answers, and when needed runs the right sibling skill (`ct-registry` / `ct-safety` / `ct-literature` / `ct-samplesize`) **locally** and stitches the result **in code**. It **re-implements no** retrieval or computation logic.

---

> **Scope reality check (read this first).** ct-advisor is a **cloud-assisted** advisor, not a pure-local tool. In operation it forwards your **question to the remote Coze engine**; runs sibling `ct-*` skills **locally on your machine** (these skills themselves may query public registries/APIs such as ClinicalTrials.gov, China CDE, FDA FAERS/openFDA, OpenAlex, PubChem); submits an **optional** bug report; keeps a language preference / context cache / memory notes on your device; and runs local connectivity diagnostics. All of this is spelled out honestly in [§5 Data & Privacy](#5-data--privacy).

> **⚠️ Attachments are part of your question.** If you attach a document (≤5 MB, any Word/Excel/PPT/PDF/TXT), the **original file itself is uploaded to the remote Coze engine** (via the `doc_context` file-id channel) and parsed there — nothing stays local. For files >5 MB the skill converts them to Markdown locally and uploads the converted `.md` the same way. Anything inside an attached file — protocol drafts, sponsor names, subject-level details — should be treated as **leaving your machine**. Remove sensitive content before attaching.

## Who This Is For

The `ct-*` clinical-trial skill family is built to address needs across the entire clinical-trial lifecycle, mainly for three groups:

- **Clinical-trial practitioners at pharmaceutical companies** — sponsors, CROs, and medical / statistical / regulatory roles;
- **Clinicians and nurses who design, manage clinical-trial projects, or take part in hands-on trial conduct in medical institutions**;
- **Medical students who want to learn clinical-trial methodology in a structured way**.

## Capabilities & Authoritative References

ct-advisor's coverage was broadened (v1.3.17) to three previously-uncovered but high-frequency blocks — **regulatory-response / trial-operations / deliverable-drafting** — now first-class in-scope core domains. Full sub-topic catalog + authoritative anchors (ICH / NMPA / CDE / TransCelerate / DIA / CASRAI / EQUATOR, searched 2026-10-22) → **[`docs/capability_domains.md`](docs/capability_domains.md)**.

| Domain | Answers | Key anchors |
|---|---|---|
| Regulatory-response | GCP principles & China GCP, inspection/CAPA readiness, deviations, safety reporting, trial registration & public disclosure (CTR + 30-day clocks), regulatory comms, informed consent | ICH E6(R3) · NMPA GCP 2020 No.57 · CDE Registration Rule 2020 No.9 |
| Trial-operations | Study startup, TMF / essential docs, monitoring models (RBM), RBQM (QTL/KRI), vendor/CRO oversight, enrolment & close-out | TransCelerate RBM & QTL · DIA TMF RM · ICH E8(R1) |
| Deliverable-drafting | Protocol (CPT/eCPT), SAP (ICH E9(R1) estimands + Gamble 55-item), CSR, IB, ICF, device docs (ISO 14155) | TransCelerate CC&R (ICH M11) · ICH E9(R1) · EQUATOR |

## 1. How to Use It in a Chat (the Core)

ct-advisor is a **conversational skill**: you simply tell the assistant what you're working on — no commands, no parameter names to remember. Once installed as a WorkBuddy skill, you invoke it in a chat via the Skill tool; there is no extra setup, but it activates only when you call it — not automatically in the background.

Below are 8 examples showing **what you actually see in the chat**: each has a **"You say"** and the **reply you see** (the user-facing answer), with a one-line note on the machinery underneath. Multi-round cases (examples 4 / 5 / 7) ask you for the missing parameter first, then give the final answer.

### Example 1 · Subject compensation after early withdrawal (GCP, answered directly)

**You say:**
> The protocol says subjects who complete all visits get a CNY 5,000 travel allowance. One subject withdrew early because of an SAE — must the investigator pay the full amount? What does GCP require?

**The reply you see:**
> Where a subject withdraws early because of an SAE (serious adverse event), the investigator **should pay the full CNY 5,000 travel allowance** — it must not be withheld or prorated. China's current GCP requires compensation arrangements to be fair and reasonable and bars deduction clauses that undermine subjects' rights; a withdrawal the subject did not choose must not cost them the compensation they are due.
>
> 1. **The scope is clear**: this travel allowance reimburses costs the subject actually incurs travelling for the trial; it is not an incentive bonus reserved for those who complete every visit. Protocol wording such as "full allowance only on completion of all visits" governs voluntary, unexplained withdrawal. An SAE is a trial-related, non-voluntary exit; deducting the allowance directly harms the subject's rights and would not meet ethics-review expectations.
> 2. **Compliance steps**: after paying in full, record the payment in the SAE follow-up file; if the ethics committee asks how subject rights were handled in the SAE, submit an explanation as required.
>
> Basis: *Good Clinical Practice for Drug Clinical Trials* (2020 edition).

> Under the hood: a single cloud call — no menu.

### Example 2 · Expectedness: do the IB and the label need updating? (pharmacovigilance, answered directly)

**You say:**
> An adverse reaction is listed as "uncommon" in the Investigator's Brochure (IB), but the observed rate in the trial has reached 15%. How should PV assess whether the IB and the label need updating?

**The reply you see:**
> This warrants an assessment straight away; by default the incidence section of the IB needs updating, and if the causal link to the drug is clear and the risk is serious, the risk-information section and the label should be updated too.
>
> **Calibrate the data first**: agree one definition and coding standard for the reaction, and confirm that the 15% denominator is the drug-exposed population and that the event criteria match those behind the IB's original "uncommon" entry — ruling out miscoding or a mixed event pool inflating the rate. "Uncommon" normally means 0.1%–1%; 15% is far above that expectation.
> **Assess the causal link**: weigh temporal sequence, dose–response, dechallenge/rechallenge and biological plausibility to judge causality for this drug, and check whether severity has escalated (e.g. severe or fatal cases).
> **Land the update**: if only the rate rose, with no change in causality or severity, update the incidence section of the IB alone; if causality is clear and the risk is materially higher, also update the IB's risk information and the product label (or the pre-approval risk-management plan), and submit the revised IB to the regulator, the ethics committees and all investigator sites as required.
>
> Basis: ICH E2F (Development Safety Update Report); CDE guidance on Safety Reference Information (RSI) in the Investigator's Brochure.

> Under the hood: a single cloud call — no menu.

### Example 3 · A narrow data ask (one data skill)

**You say:**
> Pull the registered trials for semaglutide in type-2 diabetes, 2021–2026.

**The reply you see:**
> For semaglutide in type-2 diabetes, **50 registered trials** were found:
>
> - **Phase**: Phase 3 — 14, Phase 2 — 10, Phase 1 — 5, Phase 4 — 4, and 14 not stated.
> - **Region**: United States 21, Canada 7, Denmark 6, Germany 6, China 5 (the rest in other countries).
> - **Top sponsors**: Novo Nordisk 20, Eli Lilly 2, Brigham and Women's Hospital 2.
> - **Details**: each trial's name, phase, region and sponsor were compiled into a spreadsheet you can open or download.
>
> 💡 *The above is a readable summary of this skill's result; to verify it or get the full detailed output, run the `ct-registry` skill directly.*

> 📌 **Under the hood:** code calls the trial-registry skill (ct-registry) and appends the measured results at the end of the answer.

### Example 4 · A broad competitive-intel ask (multi-source, one skill per round ⭐)

**You say:**
> Give me the full competitive-intel picture for GLP-1 RA in obesity — trials, safety signals, and literature.

**The reply you see (round 1 · follow-up):**
> Sure — I'll put together the competitive landscape for GLP-1 RAs in obesity. To retrieve accurately, please confirm the **specific indication or target** (e.g. obesity / overweight, or a particular target).

**The reply you see (after you supply it · final):**
> **GLP-1 RA in obesity — competitive-intel summary**
>
> - **Registered trials**: the trials in this indication are compiled — count, phase mix and top sponsors.
> - **Published evidence**: relevant RCTs and systematic reviews retrieved, with verifiable DOIs/PMIDs.
> - **Safety signals**: FAERS signals with quantitative measures (PRR / ROR / IC).
> - **Takeaway**: competition concentrates in a few leading players, with a phase-3-heavy registration and evidence footprint.
>
> Each source is labelled in the "supplementary data" section at the end of the answer, noting which skill produced it.
>
> 💡 *The above is a readable summary of the multi-skill result; to verify it or get the full detail, run `ct-registry` / `ct-safety` / `ct-literature` directly.*

> 📌 **Under the hood:** one card runs one skill; "trials + safety + literature" takes **several rounds** of supply-param → run → stitch — not one parallel pass.

### Example 5 · A multi-part design task (follow-up first, then compute)

**You say:**
> I'm planning a Phase II oncology trial and also need the sample size — help me decide the design.

**The reply you see (round 1 · follow-up):**
> Sure — I'll help you settle the Phase II oncology design and compute the sample size. Please confirm two things first:
> - **Test type**: two-proportion / two-mean / survival?
> - **Effect-size assumptions**: e.g. the two event rates p1 and p2, or a mean difference / SD / margin (pick one).
>
> (Defaults: two-sided α=0.05, power 80% — tell me if you'd like them changed.)

**The reply you see (after you supply it · final):**
> With a **two-proportion test** (p1=0.30, p2=0.45), two-sided α=0.05 and 80% power: **162 patients per group, 324 in total.**
> The design narrative (endpoints, enrolment, statistical methods) comes from the cloud side.
>
> 💡 *The above is a readable summary of this skill's result; to verify it or get the full detailed output, run the `ct-samplesize` skill directly.*

> 📌 **Under the hood:** the sample size is computed by the local sample-size skill (ct-samplesize) and appended; missing parameters trigger the follow-up first.

### Example 6 · Not sure what you need (vague → local clarify)

**You say:**
> I'm not sure what I actually need — I have a half-written protocol and some questions.

**The reply you see:**
> No problem — let's untangle it first. Please add two things:
> 1. **Target population / subjects**: e.g. disease, stage, line of therapy, age band — this affects how far the conclusions apply.
> 2. **Endpoint / outcome of interest**: e.g. OS, PFS, ORR, or adverse-event rates.
>
> Once that's clear I'll route you to the right workflow (methodology design / data retrieval & intel / protocol explanation & review).

> 📌 **Under the hood:** a vague question is handled by the **local** clarify flow first (no network, no data skill), then re-routed.

### Example 7 · A published-safety evidence check (ct-literature)

**You say:**
> One of our PD-1 products has case reports of interstitial lung disease; QA suspects a new safety signal. Search the **published literature** (case reports, pharmacovigilance studies, reviews) for how much support this signal has, and give me a citable evidence summary for the signal-evaluation meeting.

**The reply you see (round 1 · follow-up):**
> Sure — I'll check how well "PD-1–related interstitial lung disease" is supported in the published literature and prepare a citable evidence summary. Please give me the **search topic / target** (e.g. "PD-1", or a specific drug name).
> Tip: **English** keywords retrieve better (e.g. "interstitial lung disease" / "pneumonitis").

**The reply you see (after you supply it · final):**
> **Published-evidence summary · PD-1–related interstitial lung disease**
>
> - **Retrieval**: **20** relevant works found (OpenAlex 10 + Europe PMC 10).
> - **Citation check**: **19 of 20** DOIs/PMIDs verified automatically; 1 could not be verified (source-site anti-bot block).
> - **Citable list**: titles, journals, years and DOIs/PMIDs compiled into a spreadsheet (Excel / HTML) you can check item by item.
> - **Notes**: without a Semantic Scholar key that source is skipped; Chinese search terms trigger a "use English terms for better recall" notice.
>
> 💡 *The above is a readable summary of this skill's result; to verify it or get the full detailed output, run the `ct-literature` skill directly.*

> 📌 **Under the hood:** code calls the literature skill (ct-literature) for multi-source retrieval + citation verification; the evidence list lands in artifact files, and the answer body is its readable form.

### Example 8 · Protocol background evidence + sample-size handoff (ct-literature + ct-samplesize)

**You say:**
> We're drafting a phase-3 protocol in this indication. Give me the published RCT + systematic-review evidence from the last 5 years for the introduction, then compute the sample size for a superiority design using the key assumptions I'll provide.

**The reply you see (round 1 · follow-up):**
> Sure — two steps: first retrieve the last 5 years' published RCTs and systematic reviews as the introduction evidence base, then compute the superiority-design sample size from your assumptions. Please confirm:
> - **Test type**?
> - **Effect-size parameters**: p1 / p2, or effect / sd / margin (pick one)?
> - **Literature search terms** (optional): if omitted I'll use indication defaults.

**The reply you see (after you supply it · final):**
> - **① Introduction evidence base**: last-5-year RCTs + systematic reviews retrieved for this indication, with journals, years and DOIs/PMIDs compiled into a citable list (attached).
> - **② Superiority-design sample size**: computed from your test type and effect-size assumptions — **patients per group and total** (the numbers vary with the assumptions).
> - Both sources are labelled in the "supplementary data" section at the end of the answer.
>
> 💡 *The above is a readable summary of the multi-skill result; to verify it or get the full detail, run `ct-literature` / `ct-samplesize` directly.*

> 📌 **Under the hood:** cross-skill collaboration is a **serial, multi-step** handoff (a literature round, then a sample-size round) — not one parallel pass.

## 2. What Can It Do — Scenarios

The advisor covers the entire clinical-trial lifecycle through ten in-house workflows (A–J) plus routing to four sibling skills. Each row gives the typical **situation** and a line you can **copy verbatim** under "Try saying".

### ① Methodology & regulatory advice (answered in-house, A–J)
| Situation                                     | Try saying in chat                                                                                                |
| :-------------------------------------------- | :---------------------------------------------------------------------------------------------------------------- |
| Define a term / find the regulatory basis     | "What does ICH E6(R3) say about risk-proportionate monitoring?"                                                   |
| Trial design review                           | "Review my Phase III oncology design for feasibility"                                                             |
| Statistics / estimand / sample size framework | "Help me set the primary estimand for a superiority trial"                                                        |
| GCP / deviation / audit readiness             | "What makes a site audit-ready under GCP?"                                                                        |
| Safety & operations (SUSAR / DSUR / signal)   | "How do I handle a SUSAR in a multinational trial?"                                                               |
| Documents & QC (CSR / protocol / SAP)         | "Redline my CSR discussion section" (basic review / rewrite; for deep multi-role review use `@skill:ct-protocol`) |
| Reply tone / rewrite                          | "Rewrite this patient letter in a warmer tone" (one-off request; cross-session tone memory is not yet enabled)    |

### ② Real data & competitive intel (routed to sibling skills)
> **The bar was tightened (2026-09-10):** a sibling skill is auto-invoked only for a **uniquely-directed** ask — a named data source (NCT / ClinicalTrials.gov / FAERS / PubMed), a named statistic or high-specificity method (PRR / ROR / EBGM / dechallenge-rechallenge / a specific irAE / meta-analysis), or an explicit "retrieval verb + clear object" phrasing (the table below shows these). **Generic words** (signal / literature / trial / safety / design) no longer trigger on their own: the advisor **answers from its own capability first**, then appends an install / invoke **suggestion at the end**.
> | Situation | Try saying in chat |
> |:---|:---|
> | Trial-registry landscape | "Pull registered trials for semaglutide in T2D, 2021–2026" |
> | Safety signals (FAERS) | "Any FAERS disproportionality signals for drug X?" |
> | Published literature | "Find systematic reviews on GLP-1 RA in obesity" |
> | **Full competitive intel (multi-source, round by round ⭐)** | "Full competitive-intel picture for GLP-1 RA in obesity" |

### ③ Compute handoff (to ct-samplesize)
| Situation        | Try saying in chat                                           |
| :--------------- | :----------------------------------------------------------- |
| Actual n / power | "Sample size: two means, d=0.5, power 80%, α=0.05 two-sided" |

### ④ Clarify mode (Local Clarify Loop, no sibling skill, no network)
| Situation              | Try saying in chat                                 |
| :--------------------- | :------------------------------------------------- |
| Not sure what you need | "I'm not sure what I need — help me figure it out" |

> The underlying sibling skills are described in their own READMEs; ordinary users only need to say what they want in plain language — the advisor routes and stitches. **Whenever the advisor calls a sibling skill, the answer ends with a 💡 line suggesting you run that skill directly if you want to verify it or get the full detailed output.**

---

## 3. First-Time FAQ

**Q: I only gave a partial description — will it still help?** A: Yes. Every question is forwarded to the Coze cloud endpoint for analysis — there is no local knowledge pack. If Coze is unreachable, the answer says "please retry" rather than falling back to local materials. Data asks are routed to the relevant sibling skill by default; if you want to limit the scope, just say so in your question.

**Q: How are data sources labeled in the answer?** A: Measured behaviour is a **section label**: code appends the sibling skill's measured output under `## 补充信息（来源：ct-xxx）` (**measured: no date**; the English form is `## Supplementary data (Source: ct-xxx)`), and the full list / evidence is exported to `./out/` (`report.xlsx`, `lit_report.xlsx|html`, `evidence_log.json|md`). That is how you trace each number back to the sibling skill that produced it; the answer also ends with a 💡 suggestion to run that sibling skill directly for the fuller original output.

**Q: It says a sibling skill isn't installed — do I have to install it?** A: **No — the decision is yours, and nothing is ever installed without your say-so.** Sibling skills come in two tiers, and the tier is separate from whether a skill is published. **Tier A** (`ct-registry` / `ct-safety` / `ct-literature` / `ct-samplesize` etc. — non-confidential input) that is **listed on SkillHub**: if missing locally, the advisor explains what it does and **suggests installing it** — it hands you the install command (`adapters/install_sibling.py <slug> --dir <skills-dir>`, which verifies the SkillHub listing before downloading) but **does not install anything by itself**, because installing writes a package into your local skills directory and **may trigger a security prompt**. You choose: run the command yourself, or **explicitly authorise** the advisor to do it — then it installs, calls the skill and returns live results. **Decline** → it answers from its own capability (cloud answer) and clearly labels the reply **"data not retrieved"**. If a Tier-A skill is **not yet listed** (e.g. `ct-pipeline`), the advisor says it has not been publicly released and **cannot be installed right now** — it will not hand you an address that installs an empty package — then answers from its own capability plus the installed siblings, labelled "data not retrieved". **Tier B** (e.g. `ct-protocol` / `ct-csr` / `ct-analysis` / `ct-sdtm` — confidential protocols / subject data / CRFs): these are **not publicly released and cannot be installed**, so the advisor states plainly that a Tier-B skill is needed but is not publicly available, then completes the analysis from its own capability and notes that the in-depth analysis was not actually executed. Nothing is ever installed without your authorisation (by default installation is only *suggested*), and unavailable data is never fabricated.

**It hands off to the sibling skills for real data (since 2026-11-09).** For `data_intel` asks the advisor emits a directly-invocable `@skill:<slug>` card by default — the client runs the relevant skill (ct-registry / ct-safety / ct-literature / ct-samplesize) itself and returns the full deliverable (`report.xlsx` / `faers_report.xlsx` / PRISMA…), instead of ct-advisor running a CLI on your behalf and stitching a truncated plain-text summary into the answer. The card is generated **in code** and delivered through the single `entry.py` exit; the local model never chooses or invokes a skill. Set `CT_ADVISOR_HANDOFF=0` to restore the legacy execution card, or `CT_ADVISOR_CLOUD_BRIEF=1` for a one-shot non-audit brief (default off). If you only want the plan and not the data yet, say "just show the plan".

**Q: On a Chinese system, is the output in Chinese?** A: Yes. Output language follows your OS setting by default (Chinese on a Chinese-OS, English otherwise), and you can force-switch anytime with one sentence (e.g. "switch to English").

**Q: How is the full competitive-intel brief generated now?** A: Measured behaviour is **round by round**: the first run usually returns a delegate block (`need_tool` + a `need_tools` candidate list + `missing_params`), the advisor **asks you for the missing parameter** (measured: `cond`), and after you supply it **one skill runs per round**, its output stitched into the answer — covering three sources takes several rounds. `need_tools` is only Coze's candidate list; it is **not** auto-iterated, and no single "strategic brief" document is produced automatically. This replaces the separate `ct-pipeline` orchestrator.

**Q: Does pure methodology need the network?** A: Yes — every **non-vague** question is sent to the Coze endpoint (`https://ct-advisor.coze.site`) for analysis via an **async submit + poll** (`POST /async_run` → `GET /task/{id}`; sync `/run` only as fallback when the async endpoint is unavailable); a `vague` question is clarified locally via the Local Clarify Loop first, then forwarded. If Coze is unreachable, the answer says "please retry" — there is no local knowledge pack fallback.

**Runtime prerequisite (measured):** calling Coze needs Python `requests`. It is **not** auto-installed — when missing the skill prints `python -m pip install "requests==2.32.3"` and exits (no silent install). Measured: run it with an interpreter that lacks the library and `orchestrate.py` returns the `⚠️ Coze 返回为空` fallback wrapper, while `refine_answer.py --forward/--ship` exits 1 with `精校依赖缺失`.

**Q: What if I found an error in the result — how do I report it?**
A: This skill follows the ct-base §20.3 bug-report workflow. If you suspect the result is wrong (or the engine errored), just say **"report a bug" / "上报问题" / "提交错误报告"**. The skill also **proactively asks** whether to report when it detects a likely defect (e.g. the engine errors or retries still fail) — at most **once per session**, and you can always decline. Either way, the assistant will:
1. **Propose a sanitized report** (11-field whitelist: skill / skill_version / test / error_type / error_code / engine_status / description / locale / query_origin / session_hash / attempts — **no raw input values or personal data**, except the `description` field where you decide what to disclose, e.g. the algorithm/function used and the error message);
2. **Show the full report text for your review** — you can add a problem description or correct anything before confirming;
3. **Send after your explicit confirmation** — to the unified endpoint `https://ct-bugreport.coze.site/run` (if this session called coze) or saved locally + emailed to the author (if purely local, data never leaves your machine);
4. **Receive an acknowledgment** — including whether a previously submitted report from your source has already been fixed (with the fix note) or is still pending.

You stay in full control: the report is shown to you **before** anything is sent, and nothing is transmitted without your explicit "send" confirmation.

**Q: What if my data must stay confidential?** A: The advisor only sends your **question text** to the Coze endpoint (`https://ct-advisor.coze.site/run`) — never your raw trial / patient / sponsor data. Outbound payloads pass through `sanitize()` first (strips IDs, phone numbers, emails, and a small set of sensitive keywords; `query_origin` is a non-PII `sha256` machine id, `locale` is your OS language). Sibling data skills (ct-registry / ct-safety / ct-literature / ct-samplesize) run **locally** and only their results cross back; confidential data never leaves your machine. If you have strict confidentiality needs, simply keep real patient / sponsor data out of your question — the advisory answers are framework-level and don't require exposing it.

**Q: Is there a depth limit on protocol review?** A: Yes. The Coze side only does a **basic** protocol review (point-by-point + severity grading + revision suggestions). For a **deep multi-role review** (PI / site / regulator / rationale perspectives, revision-risk scoring on dimensions D1–D9, a structured review.json, annotated .docx output, run locally offline), explicitly call `@skill:ct-protocol`; this advisor does not impersonate that capability. Since v1.3.39, when your question carries protocol-review intent (`方案` + `评阅/审阅/评审/审查/批注/修订/修改意见`, or `protocol review/audit/assessment`), the advisor also appends an answer-footer **soft suggestion** pointing at `ct-protocol` — it never auto-invokes it, so the choice to switch stays yours.

**Q: Will formal deliverables (protocol / review / computation) be illustrated?** A: **No.** Formal documents such as the protocol body, protocol-review comments, and sample-size computation sheets stay as plain text. For data / explanation / decision / flow / comparison results that warrant visualization, an **independent appendix** is offered only after your confirmation and is never embedded in the body (see the Graphical-rendering note below in §4).

**Q: Does meta-analysis (forest plot / R recompute) run automatically?** A: **No, not automatically.** Meta-analysis requires you to explicitly call `@skill:meta-analysis` (R recompute / forest plots are done by that skill); this advisor only refers you to it.

**Q: Does a rewrite remember my tone preference?** A: **No, not across sessions.** Rewrites are one-off, stateless requests; the personalized tone / memory function (tone_profile + memory_context) is currently DEFERRED (the Coze v1.5 field is not implemented), so every rewrite ignores history.

---

## 4. Execution Model & Safe Preview

### Safe Preview (handoff card only for a uniquely-directed ask; otherwise answer first, suggest last)
- **Handoff card only for a uniquely-directed ask (since 2026-11-09):** only a **strong trigger** — a named data source (NCT / FAERS / PubMed…), a named statistic / high-specificity method (PRR / ROR / EBGM / meta-analysis…), or an explicit "retrieval verb + clear object" phrasing — makes the **code** emit an `@skill:<slug>` card carrying the params already extracted from the question, any missing params, the skill's real deliverables and a Tier-B confidentiality note. The client can invoke every locally registered `ct-*` skill directly, so ct-advisor no longer runs their CLIs or bypasses SAFE PREVIEW. Measured: **one card names one skill**; `CT_ADVISOR_HANDOFF=0` restores the legacy auto-execution behaviour.
- **Generic words and consultation questions → answer first, suggest last:** for a bare generic word (signal / literature / trial / safety / design) or a "what is / how do I / give me a template" methodology, definition or document question, the advisor **answers fully from its own capability** (Coze endpoint knowledge base + authoritative anchors) first; only when the question **does name** a data source / statistic (FAERS, PRR, PubMed…) does it append an `@skill:xxx` **suggestion at the end** — a purely generic or definition question no longer trails any suggestion, and it never interrupts the answer or pops a parameter follow-up because of a keyword false positive.
  - **Technical-detail questions are answered by the advisor itself (since 2026-11-09):** "How is a non-inferiority margin set", "what is the relation between alpha-spending and interim analyses", "PRR vs ROR and why EBGM shrinks", "how to read a 95%CI", "why does CT.gov have Phase 1/Phase 2" — these ask about **principles / parameter semantics / method choice / interpretation**, and are no longer misrouted to sibling skills that only compute or retrieve. The test is "is there an execution verb plus computable/retrievable input", not "does the word PRR or sample size appear". Answers carry a "methodology explanation, not a data result" marker, authoritative sources and an anti-hallucination rule (no invented trial counts / PRR values / sample sizes); an `@skill:` suggestion appears only at the end when actual computation is wanted. The three methodology topics live **only in the Coze endpoint knowledge base** — the local skill keeps zero knowledge base.
- **One card per skill in mixed asks:** if a question hits several sibling skills at once (e.g. a competitive-intel picture needing registry trials + FAERS signals + published literature), the answer appends an "Other skills you can invoke directly" section after the primary card, with one `@skill:<slug>` card per skill. Params are split by each skill's own CLI allowlist and missing params are listed separately, so `topic` is never handed to `@skill:ct-registry`.
- **Return path after the skills run:** pass their output paths to `entry.py --stitch '<JSON>'` (or `@spec.json`). Code parses `.md / .json / .csv / .tsv / .xlsx` **locally** and stitches a deterministic summary through the same answer exit — zero egress by default, no LLM, no numeric rewriting; Tier-B confidential outputs stay on this machine. Credential-like filenames, oversized files and non-allowlisted extensions are refused; missing outputs are reported, never invented. The exact spec format is printed in the answer by code.
- **Optional result interpretation (sanitized egress):** add `"interpret": true` to the spec to request a methodology explanation of the results. **Only** allowlisted sanitized numbers (max 12 finite values, taken from JSON outputs alone) and a code-built methodology question are sent to the pre-authorized Coze endpoint. The user's original question, raw output text, file names/paths, drug or protocol names, trial IDs and subject data never leave the machine. If the endpoint is not whitelisted, no allowlisted values exist, or the cloud returns an error / `need_tool` / empty answer, only the local summary is delivered with the reason stated.
- **Chinese mixed questions get params too:** multi-skill asks fill `cond` for ct-registry and `topic` for ct-literature. ct-safety's `drug` is deliberately **not** filled with a Chinese name (openFDA only accepts English generic names and would return zero hits); its card gives a conversion hint instead. The single-skill lexicon rules are untouched.
- **Plan only:** if you only want the plan and not the data yet, say "just show the plan".
- **Traceable, not fabricated:** Every factual / normative claim carries a source citation (code-appended measured results read `## 补充信息（来源：ct-xxx）`) or an `⚠️ needs official verification` marker; it never fills factual gaps with fluent prose.
- Outputs are for reference only; validate against official sources before regulatory submissions.

### Graphical-rendering note
- **Formal deliverables stay plain text:** the protocol body, protocol-review comments, regulatory-communication files, and sample-size computation sheets — the "finished products you hand off" — default to **no graphics**, preserving formality and traceability.
- **Data / explanation may be illustrated:** results involving multi-branch decisions, sequential flows, hierarchy, design comparison, or severity grading may use decision trees / flowcharts / comparison matrices / severity color blocks to aid understanding.
- **Independent appendix, only with your OK:** any visualization is delivered as an **independent appendix** and never embedded in the formal body; especially for formal documents, if you want a visual aid, confirm first and I'll generate an appendix that does not alter the original text.
- **Pipeline safety:** since v1.3.21 there is **no base64 anywhere** in the pipeline — the answer leaves `entry.py` as plain text followed by `<<<CT_ANSWER_END>>>`, `checksum:` and `answer_file:`. The exit writes UTF-8 bytes directly to `stdout.buffer` (no code-page inspection, no flags) and stores the identical bytes at `_answers/<sha16>.md`. If a terminal renders the text garbled (a display-layer issue only), **read the path given on the `answer_file:` line** — since v1.3.23 it is **absolute and pure ASCII**, so it survives the very capture that mangled the body, and one file read returns the original bytes (file reads are independent of the console code page). No re-run. **Keep the two acts apart:** "read the file" is allowed, "decode the mojibake" is not — a cp936 console replaces illegal UTF-8 bytes with `U+FFFD`, so the original bytes are gone; no repair chain or model guess can pass the checksum, and "repairing" an answer is a rewrite (ALCOA+). Since v1.3.22 the answer file is **reused rather than rewritten** when an identical one exists (network-share ACL refuses overwrite), and if `_answers/` is unwritable the engine falls back to `%TEMP%/ct-advisor/<sha16>.md` — so the "one intact plain-text copy" channel cannot vanish silently.

### Latency note
Every **non-vague** question is handled by the local orchestrator (`scripts/orchestrate.py`), which forwards to the Coze endpoint via an **async submit + poll** (v1.3.14+: `POST /async_run` → `GET /task/{id}`; the sync `/run` path is kept only as a fallback for endpoints without async support — sync and streaming calls are both hard-killed at 60.0s by the Coze gateway, and measured duration spans 3-72 s, i.e. across that line, so prediction-based routing is unreliable). Polling deadline = `refiner.timeout = 90` s (long tasks 300 s) in `config.json`; **measured 3-72 s per round**, mostly 30-70 s; data-intel questions also run the needed sibling skill locally). **A timeout is not a hard error**: the answer falls back to the local draft (not cloud-polished) with `[coze] FALLBACK_TO_LOCAL_DRAFT` on stderr. A `vague` question is clarified locally first (a few seconds via the Local Clarify Loop), then re-routed. Because the orchestrator, prefetch, merge, and stitching are all **code** (not the LLM), dependence on the local model's performance is low — but reasoning models (e.g. Hunyuan-3, DeepSeek-R1) have been observed to over-think locally. **If a single reply routinely takes longer than 3 minutes, switch to a simpler / flash model to speed things up.**

---

## 5. Data & Privacy

**This skill is cloud-assisted, not a pure-local tool.** To give current, source-traced answers it forwards your question to a remote engine and may run sibling skills on your machine. Below is exactly what leaves your device, what stays local, and what sensitive actions it can take — stated up front, not buried.

### What leaves your device (off-device)
- **Analysis request** — for a non-vague question, your **question text** (passed through `sanitize()` first, which strips IDs, phone numbers, emails, and a few sensitive keywords) is sent to `https://ct-advisor.coze.site/run`. **Raw trial / patient / sponsor data is never sent.** When the question needs registry / safety / literature / sample-size data, Coze returns only a `need_tool` instruction; the actual retrieval and computation run **locally** on your machine — but note those local sibling skills (`ct-registry` / `ct-safety` / `ct-literature` / `ct-samplesize`) may themselves query **public registries/APIs** (ClinicalTrials.gov, China CDE, FDA FAERS/openFDA, OpenAlex, PubChem…). That is separate outbound to those public sources, not to Coze.
- **Error report** — sent **only after your explicit confirmation**, and only as an 11-key whitelist envelope (no raw input, no PII), to `https://ct-bugreport.coze.site/run`. You can always decline; it is offered at most once per session.

Each request also carries two anonymous metadata fields: `query_origin` (a SHA-256 hash of your hostname, for rate-limiting only) and `locale` (your OS language, for answer-language matching). Neither contains PII.

### What stays on your device but is still sensitive (on-device actions)
To be transparent about the full behavior the skill can perform:
- **Embedded (public) token** — the skill ships with an obfuscated Coze token used to authenticate the public endpoint. It is a **shared, openly-disclosed token by design** (not a personal secret); it is decoded in memory only for outbound auth and is disclosed openly here rather than hidden.
- **Local persistence** — it may write your **language preference** to `config.json`, keep a short-lived **context cache** under `.runtime/` (gitignored), and **promote recurring interaction patterns into long-term memory files** (per the SOUL.md self-improvement rules). None of these contain your question text or trial data.
- **Local connectivity diagnostics** — if a connection to Coze fails, with your permission it can run `scripts/check_coze.py` to probe local proxy / network / token configuration and suggest a fix.
- **Subprocess orchestration** — the local code orchestrator (`orchestrate.py` / `refine_answer.py`) runs sibling `ct-*` skills as **subprocesses on your machine** and stitches their results in code.
- **Shipped but never egressing (clarification)** — to stay self-contained, the package carries shared ct-base modules. One of them, `kw_localize.py`, has an online-translation fallback (MyMemory / Google gtx, on by default, disable with `CT_TRANSLATE_ONLINE=0`). **ct-advisor never calls this module** (it has no keyword-localization need), so **no translation egress is ever produced**; the base version is vendored only to satisfy the shared-asset consistency gate.

> **In one sentence:** your question text goes to the Coze endpoint for cloud analysis, sibling skills may query public registries, an optional bug-report goes out only after your OK, and the skill may keep a language preference / context cache / memory notes locally — **raw trial / patient / sponsor data never leaves your machine.**

---

## Why You Can Trust the Output — Anti-Hallucination

ct-advisor is the entry point that routes to sibling skills and forwards questions to the Coze refiner; it does not invent facts. Four guardrails apply:

1. **Every factual claim is source-traceable.** Data-grounded claims from sibling skills are appended by code as `## 补充信息（来源：ct-xxx）` (measured: the label carries no date; artifacts land in `./out/`); methodology / regulatory answers cite the authority (ICH / NMPA / FDA / EMA guidance) and link to it where available.
2. **Identifier consistency check.** When a cited identifier (trial registration number, DOI / PMID) is resolved to a live record, the resolved title / author / year are compared against the original assertion; a mismatch is flagged `mismatch` and never treated as verified.
3. **Unverifiable ⇒ `⚠️ needs official verification`.** Anything that cannot be traced to a public source is marked for official verification and never stated as a confirmed conclusion.
4. **No fabrication.** Trial registration numbers, approval dates, subject counts, and company M\&A / pipeline moves are never invented; if a public source does not disclose them, the output says "not disclosed in public sources".

---

## 6. Advanced Reference (moved to a separate file)

CLI helpers, runtime requirements, the architecture tree, and scanner false-positive notes have been moved to **[references/ADVANCED.md](references/ADVANCED.md)**. Ordinary users don't need them; Sections 1–5 cover daily use. The agent-facing spec and version history remain in [`SKILL.md`](SKILL.md) and [`CHANGELOG.md`](CHANGELOG.md).

---

**Version**: v1.3.0 | **License**: MIT | **Authors**: medstatstar, phoe-zip

For feature requests, bug reports, or other feedback, please contact the author directly at <medstatstar@gmail.com> (Wintone Zhang).

---

## Confidentiality Notice

> The CT series consists of 20+ specialized domain skills, organized into **two tiers — A, B** — by "whether the input contains confidential information" (network / egress / publish are independent orthogonal attributes; see ct-base §11), providing full coverage of the entire new-drug clinical trial (Clinical Trial) lifecycle.
>
> - **Tier A (non-confidential input)**: runs on ordinary data and involves no confidential information; split further by the `network` sub-attribute into three kinds — ① **fully local** (`network=off`, zero egress); ② **public-source retrieval** (`network=public-retrieval`, e.g. ct-registry / ct-safety / ct-literature — only public query terms leave the machine); ③ **controlled Coze-only egress** (`network=controlled-coze-opt-in`, e.g. **ct-advisor**: a single Coze endpoint only, explicit user opt-in, payload passed through `sanitize()` first, paired with `egress=cloud`). ⚠️ Note that ③ is **not** the same as "runs fully locally" — its Q\&A is forwarded to the cloud engine by default, falling back to a local fallback answer (clearly marked as such) only when the cloud is unreachable. All Tier A skills are published openly on GitHub.
> - **Tier B (confidential input)**: accept strictly confidential clinical-trial data / protocols / CRFs from pharma sponsors (e.g., ct-analysis, ct-sdtm, ct-protocol, ct-eligibility); Tier B is processed locally and never leaves the boundary (egress=none), or additionally requires policy approval (egress=approval-req, e.g. ct-eligibility). Tier B packages contain zero confidential data but are NOT publicly published (stays fully local) — confidential input never ships with the package or leaves the machine. For custom / on-prem deployment, contact the author.
>
> 📧 Contact: <medstatstar@gmail.com> (Wintone Zhang / 张文彤)

> 🌐 Other languages: [中文 README](README_zh-CN.md)
