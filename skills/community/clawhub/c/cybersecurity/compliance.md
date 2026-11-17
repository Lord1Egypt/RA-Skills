# Compliance — Regimes, Evidence, Audits, Customer Reviews

Compliance is a claim about controls, evidenced. The work is the evidence pipeline, not the document — and the notification clocks in SKILL.md are legal deadlines that run whether or not the technical investigation is finished.

**Before any audit or customer review work**, read `## Environment` in `~/Clawic/data/cybersecurity/memory.md` (scope boundaries, systems, log retention — retention minimums are usually the first control to fail), `## Findings` for what is open and would be sampled, and `## Vendors` for the subprocessor list every regime asks about. `compliance_regime` in `config.yaml` decides which sections apply; with `none`, only the customer-review section is likely relevant.

**Contents:** [What Each Regime Actually Demands](#what-each-regime-actually-demands) · [Scope Is The Whole Game](#scope-is-the-whole-game) · [Control-To-Evidence Mapping](#control-to-evidence-mapping) · [Evidence That Passes](#evidence-that-passes) · [The Audit Itself](#the-audit-itself) · [Notification: The Clock Is Legal, Not Technical](#notification-the-clock-is-legal-not-technical) · [Customer Security Reviews](#customer-security-reviews) · [Where Compliance And Security Diverge](#where-compliance-and-security-diverge) · [Running It Without A Compliance Team](#running-it-without-a-compliance-team)

## What Each Regime Actually Demands

| Regime | Nature | What it really asks for | The part that surprises people |
|---|---|---|---|
| SOC 2 | Attestation by an auditor, against criteria you partly define | Your own stated controls, operating over a period, tested by sampling | You write the control descriptions — and then you are held to exactly what you wrote |
| ISO 27001 | Certification of a management system | A functioning ISMS: risk assessment, Statement of Applicability, internal audit, management review, and continual improvement | The management system is the certified object; the Annex A controls are selected by your own risk assessment |
| PCI DSS | Prescriptive contractual standard | Specific technical requirements on the cardholder data environment | Scope reduction — tokenization, redirect or hosted payment fields — is worth more than any control |
| HIPAA | US law, no certificate | Risk analysis, safeguards, business associate agreements, breach notification | The mandatory, documented risk analysis is what enforcement actions cite most |
| GDPR | EU law, no certificate | Lawful basis, data subject rights, records of processing, DPAs, security appropriate to risk, 72-hour notification | It applies to processing, not to systems, and your processors' breaches become yours |
| NIS2 | EU law for essential and important entities | Governance with management accountability, risk measures, supply-chain security, staged incident reporting | Management bodies can be held personally accountable; the 24-hour early warning is very short |
| DORA | EU law for financial entities | ICT risk management, incident classification and reporting, resilience testing, third-party oversight including a register | The register of ICT third-party arrangements is a substantial standing obligation |
| Customer contracts and DPAs | Private law | Whatever you signed | Frequently stricter than any statute — commonly 24-72 hours' notice — and nobody reads them until the incident |

Cross-regime constant: **evidence that a control operated**, repeatedly, over time. Not a policy stating it should.

## Scope Is The Whole Game

The cheapest compliance work is always scope reduction, and it happens before any control is implemented.

- **PCI**: never touching card data is dramatically cheaper than protecting it. A hosted payment field or a redirect moves the majority of requirements to the provider, and the difference between assessment types is an order of magnitude of effort.
- **SOC 2**: scope by product and system, not by company. A narrower, honest scope with clean evidence beats a broad one with exceptions.
- **GDPR and HIPAA**: minimize the data itself. Data you do not hold has no controls, no breach exposure and no subject-access burden — deletion is a security control with a compliance dividend.
- **Segmentation is the technical instrument of scope reduction** (`network-security.md`), and for PCI the segmentation must be tested, not asserted.
- Write the scope boundary down with what is explicitly out and why, and re-confirm it whenever the architecture changes. An out-of-date scope statement is the most common reason an audit expands mid-flight.

## Control-To-Evidence Mapping

One table, maintained continuously, is the entire operating model:

| Column | Content |
|---|---|
| Control | What you claim happens |
| Owner | A named person, not a team |
| Frequency | Continuous, daily, monthly, quarterly, annual |
| Evidence | The exact artifact — a specific report, export, ticket query or screenshot |
| Where it lives | The system and path the auditor will be shown |
| Automated? | Can the evidence be produced by a query, or does a human assemble it |
| Last produced | The date, which is what makes gaps visible before the auditor finds them |

Two rules that decide whether this survives:

- **One control, many regimes.** Access review satisfies SOC 2, ISO 27001, PCI and HIPAA simultaneously. Map controls to requirements many-to-many; implementing the same control once per framework is the most common source of wasted compliance effort.
- **Automate the evidence, not just the control.** A control that runs perfectly and produces no artifact fails the audit. If producing the evidence requires a person to remember, it will be missing for the month somebody was on holiday — and the sample will land on that month.

## Evidence That Passes

- **Dated, attributable and complete for the period.** A screenshot from today does not evidence a control that was supposed to operate monthly for twelve months.
- Population plus sample: the auditor picks the sample, so you must be able to produce the *complete* population — every access change, every ticket, every deployment in the period. Not being able to produce the population is itself a finding.
- Tickets are excellent evidence because they carry a timestamp, an actor and an approval. Route control activities through the ticketing system and the evidence assembles itself.
- Screenshots need the date, the system and the user visible; they are the weakest form and the most laborious. Prefer exports and reports.
- **Exceptions documented at the time beat exceptions explained afterwards.** A missed quarterly review with a dated note explaining why and what compensated is a managed exception; the same gap discovered by an auditor is a finding.
- Keep evidence for the retention the regime requires plus one cycle, and know where it lives before the audit starts.

## The Audit Itself

- Readiness assessment first, then the real audit. Discovering a design gap during the audit is expensive; discovering it during a readiness pass is a task.
- **Sampling is the mechanism**: the auditor picks from a population and tests. Consistency matters more than perfection — a control that operated eleven times out of twelve is an exception, while a control that operated inconsistently all year is a design failure.
- One coordinator, one evidence repository, one channel. Auditors asking five people the same question get five answers, and the differences become findings.
- Answer exactly what was asked. Volunteering scope, systems or problems the auditor did not ask about expands the audit — this is not concealment, it is answering the question.
- Where a control genuinely does not exist, say so early with the compensating control and the plan. Auditors discover it anyway, and the difference between disclosed and discovered is the difference between a management response and a qualified opinion.
- Findings get owners and dates like any other finding — they go in `## Findings`, not in a separate compliance spreadsheet that diverges from reality within a month.

## Notification: The Clock Is Legal, Not Technical

SKILL.md's Notification Clocks table holds the deadlines. The operational discipline around them:

1. **Write the awareness timestamp the moment it exists**, with its timezone. Every clock starts there and it is unrecoverable an hour later.
2. **Awareness is not certainty.** Most regimes start at awareness of a possible breach, not at the completion of the investigation. Waiting for full understanding is the standard way a 72-hour deadline is missed.
3. **Notify in phases.** GDPR, NIS2 and DORA all contemplate an initial notification with what is known and a later completion. A phased notification on time beats a complete one late, in every regime.
4. **Counsel owns the wording and the determination**; the technical team owns the fact pattern and the timestamp. Materiality and notification are legal calls with legal consequences.
5. **Check the contracts, not only the statutes.** Customer DPAs frequently impose 24-hour notice, which is shorter than every regulator.
6. **The insurer's notice clause runs in parallel** and can be shorter still — and engaging your own IR firm before notifying can void coverage (`~/Clawic/data/finances/subscriptions.md`).
7. Personal data goes into the record as counts and categories, never records — that is what the notification needs anyway.

Decide the notification decision tree *before* an incident, as an artifact with the thresholds, the contacts and the templates. Making these calls for the first time at hour three is how the wrong statement gets published.

## Customer Security Reviews

The sales-blocking version of compliance, and speed is the whole product:

- Maintain a standard response package: current audit report under NDA, a security overview, the subprocessor list, the penetration-test summary, and a completed standard questionnaire. Most reviews close on the package alone.
- Answer honestly with dates. "Not yet, planned for Q3" survives; a yes that becomes an exception during their audit does not, and it is a contractual misrepresentation.
- Track what customers ask for that you do not have. Three requests for the same control is a roadmap item with revenue attached — that list is the best security-budget argument that exists.
- Push back on bespoke spreadsheets by offering the package first; the marginal review costs hours you can spend on the controls they are asking about.
- Their questionnaire is also intelligence: it tells you what your market will require in eighteen months.

## Where Compliance And Security Diverge

Real, and pretending otherwise loses credibility with engineers:

| Compliance says | Security says | Resolution |
|---|---|---|
| Rotate passwords every 90 days | Rotation without breach evidence drives weaker passwords; NIST SP 800-63B removed routine expiry in favour of breach-list screening and phishing-resistant factors | Comply with the letter where an auditor demands it, put the real defence into MFA and screening, and document the reasoning |
| Annual penetration test | Continuous testing and detection engineering find more | Do both; the annual test is the evidence, the continuous work is the security |
| Antivirus on every system | EDR with response beats signature scanning | Map EDR to the requirement explicitly — most frameworks accept it, and the mapping is a one-line argument |
| Quarterly access review | Review by exception and on role change catches more, sooner | Do both, with the exception-driven review as the working control and the quarterly as the evidenced one |
| Encrypt data at rest | Full-disk encryption does nothing against a live application compromise | Be precise about the threat each encryption layer addresses; state it in the control description |
| Documented policies for everything | A policy nobody follows is a liability, since you are audited against your own text | Write the shortest true policy; never claim a control you do not operate |

**The rule that prevents the worst outcome: never write a policy claiming a control you do not operate.** You are audited against your own document, and in an incident it becomes evidence of what you said you would do.

## Running It Without A Compliance Team

The realistic sequence for a small organization facing its first SOC 2 or ISO certification:

1. Decide the scope, narrowly, and write it down.
2. Build the control-to-evidence table. Most controls already exist informally; the work is naming the owner and the artifact.
3. Automate the evidence for the high-frequency controls first — access reviews, change management, vulnerability management, backups. These are the ones with twelve samples a year rather than one.
4. Fix the two or three genuine gaps, which are usually formal risk assessment, access review, and vendor management.
5. Run a readiness pass and fix what it finds.
6. Then the audit period starts. Evidence quality during the period is what determines the outcome, not effort at the end — and a Type II covering a short first period is a legitimate way to start.

Compliance platforms automate evidence collection and are worth their cost for a small team; they do not create the controls, and a platform showing green while the control is not operating is the worst of both worlds. Verify the automation against reality once per cycle.

Write it (`memory-template.md`): the scope boundary, in-scope systems, data classifications and retention minimums in `## Environment`; every audit finding, control gap and remediation as a `## Findings` row with an owner, a due date and the attack path or requirement it addresses — one register, never a parallel compliance spreadsheet; each accepted gap in `## Risk Accepted` with its expiry and a `## Due` row; every recurring control — access review, risk assessment, internal audit, penetration test, tabletop, policy review, evidence collection — as a `## Due` row with its last-run date, because the missing sample is always the month nobody was watching; each subprocessor and audited vendor in `## Vendors` with its report date; counsel, the DPO, the auditor and the regulator contact in `~/Clawic/data/contacts/contacts.md`; the control-to-evidence map, the notification decision tree and the standard customer-review package in `~/Clawic/data/cybersecurity/artifacts/`, each with its `## Boxes` line and read-when condition in the same turn. Notified incidents carry the awareness timestamp and the notification times in `incidents/<year>.md`; affected people are counts and categories, never records.
