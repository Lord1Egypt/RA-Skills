# Supply Chain — Dependencies, Builds, Vendors

Three surfaces that share one property: somebody else's compromise becomes yours, and your controls sit outside the thing you are protecting.

**Before assessing**, read `## Vendors` in `~/Clawic/data/cybersecurity/memory.md` — or `vendors.md` if `## Boxes` points there — so a third party already tiered does not get assessed from scratch with a different answer, plus `## Environment` for which data and which access each integration actually holds.

**Contents:** [Dependencies: Reachability Over Count](#dependencies-reachability-over-count) · [The Install-Time Attack](#the-install-time-attack) · [SBOM: Useful For One Thing](#sbom-useful-for-one-thing) · [Build Pipeline Integrity](#build-pipeline-integrity) · [Secrets In CI](#secrets-in-ci) · [Signing And Provenance](#signing-and-provenance) · [An Acquired Or Inherited Repository](#an-acquired-or-inherited-repository) · [Vendor Tiering](#vendor-tiering) · [Reading A SOC 2 Report Properly](#reading-a-soc-2-report-properly) · [Answering A Questionnaire, And Sending One](#answering-a-questionnaire-and-sending-one) · [When A Vendor Is Breached](#when-a-vendor-is-breached)

## Dependencies: Reachability Over Count

The scanner reports every CVE in every declared package. Most of them are not exploitable in your application, and treating them as equal is how a team spends a quarter on upgrades and closes no path.

Triage in this order:

1. **Is the vulnerable code path reachable from your code?** A parsing vulnerability in a library you use only for its formatting helpers is not your vulnerability. Reachability analysis — call-graph based, offered by several tools — routinely eliminates the large majority of raw findings, and it is the single highest-leverage filter in dependency management.
2. **Is it a direct or transitive dependency?** Direct is yours to fix. Transitive needs the intermediate package to update, or an override, which is a different piece of work with a different owner.
3. **Runtime, build-time or dev-only?** A vulnerability in a test framework is not in production — though it *is* in your build environment, which is itself a target (below).
4. **Does the exploit require attacker-controlled input reaching that path?** Trace it, do not assume it.
5. **Then apply the normal gate**: KEV, EPSS with exposure, crown-jewel reachability (`vulnerabilities.md`).

Hygiene that prevents the backlog rather than triaging it: lockfiles committed and enforced in CI, automated update pull requests with a test suite good enough to merge them, a policy on how old a dependency may get, and — for anything critical — pinning to a hash rather than a version range.

## The Install-Time Attack

The most direct compromise path, and it does not need a vulnerability at all: package installation runs code.

- **Install scripts** (npm `postinstall`, Python `setup.py`, and equivalents) execute with the developer's or the CI runner's privileges, before any of your code runs. Disable them where the ecosystem allows (`--ignore-scripts` with an explicit allowlist for the handful that genuinely need one).
- **Typosquatting and namespace confusion**: a package one character from a popular name, or with your internal package's name published publicly at a higher version. **Dependency confusion** — the resolver preferring the public registry over the private one — is a build-server compromise with no vulnerability involved. Scope internal packages, and configure the resolver to never fall back to public for internal namespaces.
- **Maintainer compromise and hostile handover**: a legitimate package gains a malicious version. The defences are lag (do not install a release the day it appears for non-security updates), pinning, and integrity hashes in the lockfile.
- Developer machines are the target as much as CI, because they hold cloud credentials, SSH keys and browser sessions. An install script on a laptop is initial access with full context.
- Vendor a mirror or a proxy registry for anything you care about, so a deleted or replaced upstream package cannot change your build.

## SBOM: Useful For One Thing

A software bill of materials is worth generating for exactly one reason: **when the next widely-exploited library vulnerability lands, you can answer "are we affected?" in minutes rather than weeks.** That single capability justifies the cost.

- Generate at build time, from the build itself, and store it with the artifact. An SBOM produced by scanning a repository afterwards describes the repository, not what shipped.
- It must cover what actually runs, including the base image's operating-system packages — which are usually the majority of findings in a container.
- A vendor's SBOM tells you what they say they include; it does not tell you it is current, and it does not tell you they will patch. Ask what their patch SLA is instead; that is the answer you actually need.
- Do not build a programme around SBOM production. The programme is the ability to answer the question, and the SBOM is one input.

## Build Pipeline Integrity

**The pipeline can deploy to production, so it is production.** Treat it with the controls you give the environment it deploys to — most organizations do not, which is why it is such a productive target.

| Control | Path it removes |
|---|---|
| Branch protection: review required, no force push, no self-approval, and protected branches actually enforced for administrators | A single account pushing straight to the deployed branch |
| Signed commits or verified authorship on release branches | Commit spoofing under someone else's name |
| Pinned, hash-referenced third-party CI actions and plugins | A mutable tag on somebody else's action silently changing what runs in your pipeline |
| Ephemeral, isolated runners; no shared self-hosted runner across trust levels | One repository's build stealing another's secrets from the runner's disk or memory |
| Least-privilege deploy credentials, scoped per environment, ideally OIDC-federated with no static secret | A leaked CI secret becoming production access |
| No secrets in build logs; pull-request builds from forks never see secrets | The classic exfiltration path: a pull request that prints the environment |
| Immutable artifact storage with retention, and the digest recorded at deploy | Not knowing what is actually running, and having nothing to roll back to |
| Audit logging of pipeline configuration changes, exported off-platform | A quiet change to the pipeline definition that nobody reviews |

The specific check worth running today: which identities can modify the pipeline definition, and does modifying it require the same review as modifying the application? In most organizations the answer is no, and that asymmetry is the finding.

## Secrets In CI

- Scoped per environment, short-lived, and federated where the platform supports OIDC — the best rotation policy is having no long-lived secret at all.
- Masked in logs, but never rely on masking: a base64 or split-string echo defeats it. Assume anything in the environment can be printed by any code that runs.
- Fork pull requests must not receive secrets. This is a default in some platforms and not in others; verify rather than assume.
- Rotate on any maintainer or runner compromise, and on offboarding of anyone who could read them.
- A secret found in a repository is rotated first and removed second; history rewriting without rotation is cosmetic (`appsec.md`).

## Signing And Provenance

- Sign what you ship — containers, packages, releases — and **verify at deploy**, because signing without verification is a ritual. The verification step is the control; the signature is just its input.
- Provenance attestation records what built the artifact, from which source commit, with which build system. It is what lets you answer "did this binary come from that commit?" months later, and frameworks like SLSA describe increasing levels of that guarantee.
- Keyless signing with short-lived certificates tied to a workload identity removes the signing-key management problem, which is the reason most signing programmes stall.
- Protect the signing identity like a crown jewel: a stolen code-signing capability makes your customers' controls work against them, and it is one of the few incidents that is genuinely existential.

## An Acquired Or Inherited Repository

The realistic first week, in order:

1. **Secrets scan across the full history**, not the current tree. Rotate everything found; assume it is public.
2. **Dependency inventory and age**: how far behind, and are any packages unmaintained or renamed?
3. **Who has access** — to the repository, to the pipeline, to the deploy credentials — and how many of those people still work there? Contractor accounts survive acquisitions with remarkable consistency.
4. **What does it deploy to, and with what permissions?** Frequently more than anyone remembers.
5. **Build reproducibility**: can you rebuild it at all, from a clean machine, without a person? If not, that is a security finding and an operational one.
6. **The undocumented external calls**: telemetry, licence checks, third-party scripts included at runtime. Anything the application fetches at runtime from someone else is a live dependency on their security.

Acquisitions inherit incidents as well as assets. Ask directly whether they have had one, and treat the absence of any security history as unknown rather than clean.

## Vendor Tiering

Assess proportionally, or you will assess nothing well. Tier on **what they hold and what they can reach**, never on contract value.

| Tier | Definition | Assessment |
|---|---|---|
| Critical | Holds regulated or crown-jewel data, or has privileged access to your systems, or your business stops without them | Full review, evidence, contractual security terms, annual reassessment, named security contact, incident notification clause |
| Important | Holds some business data or has scoped access | Questionnaire plus their audit report, reassessed on renewal |
| Standard | No sensitive data, no access | Baseline check, no ongoing cycle |

- **The tier is a function of access, not of spend.** The cheapest tool in the estate with an OAuth grant to your mail is a critical vendor; a large infrastructure contract with no data access may not be.
- Track it as a list of *integrations*, not companies: which token, which scopes, which data flows, granted by whom, used when. That list is what you need at 2am when they announce a breach.
- Fourth parties matter: your critical vendor's critical vendor. Ask who they depend on for the service you buy — concentration risk in a shared platform is real and invisible until it fails.
- Contractual terms worth having, in order of value: breach notification within a defined period, audit or evidence rights, subprocessor change notice, data deletion at termination with proof, and security requirements that survive renewal.
- Offboarding a vendor is a security task: revoke the tokens, remove the accounts, confirm deletion, and remove their row. Dormant integrations from cancelled vendors are live credentials with no owner.

## Reading A SOC 2 Report Properly

The report is evidence about a period, not a certificate. Read it in this order and you will read it faster than anyone who has read one before:

1. **Type I or Type II.** Type I is design at a point in time — nearly worthless. Type II is operating effectiveness over a period, which is the one to insist on.
2. **The period covered**, and whether it is current. A report ending 14 months ago needs a bridge letter, and a bridge letter is the vendor's own assertion, not the auditor's.
3. **The scope**: which systems, which trust service criteria. A report covering a different product than the one you are buying is common and is the most frequent mistake buyers make.
4. **The opinion**: unqualified, or qualified. A qualified opinion is a finding you must read in full.
5. **Section 4 exceptions.** This is where the actual information lives — the tests that failed and management's response. Most people never open it. An exception with a vague response is worth a direct question.
6. **Complementary user entity controls.** The list of things the report assumes *you* do. If you are not doing them, the assurance does not apply to you — this is the section that transfers risk back and nobody reads it.

An ISO 27001 certificate is even thinner on its own: read the Statement of Applicability and the scope, because a certificate whose scope is one office and one product tells you nothing about the service you buy.

## Answering A Questionnaire, And Sending One

Answering:

- Maintain a reviewed answer bank, with evidence attached, and refuse to invent. A wrong answer is a contractual misrepresentation, and it will be quoted back during an incident.
- "No, and here is the compensating control, and here is the date we will have it" is a strong answer. Auditors and customers trust a specific no far more than a vague yes.
- Offer your own audit report and a standardized response package to short-circuit bespoke spreadsheets. It is the highest-leverage sales-security investment there is.

Sending:

- **Ten questions that discriminate beat two hundred that do not.** Ask: how do your staff authenticate, how do you manage privileged access to our data, what is your patch SLA for internet-facing systems, do you encrypt our data and who holds the keys, what is your incident notification commitment, when did you last test recovery, who are your subprocessors, what happens to our data at termination, has your product been penetration tested and by whom, and have you had a breach.
- Ask for evidence on the answers that matter, rather than more answers.
- A questionnaire nobody reads after it is returned is theatre with a filename. If you will not read it, do not send it — tier the vendor instead and ask the ten questions.

## When A Vendor Is Breached

**Your exposure is whatever their access and their data reach, not whatever their statement says.** Statements are drafted to minimize, and they are usually wrong in the direction of optimism at first.

1. Enumerate independently: which integrations, which tokens, which scopes, what data they hold, and which of your systems they can reach.
2. Revoke or rotate the credentials at your end immediately — you control that, and it does not require their cooperation or their timeline.
3. Search your own logs for their integration's activity in the window. Their compromise shows up as their token behaving differently in your audit trail, and that is evidence you own.
4. Ask specific questions in writing: were our tenant's tokens in scope, what data was accessed, over what window, what is your evidence. Vague reassurance is not an answer, and the written record matters later.
5. Assess your own notification duty. A processor's breach of your personal data is frequently your notifiable breach, on your clock, from your awareness (`compliance.md`).
6. Reassess the tier afterwards, and record what their response told you about them — the quality of a vendor's incident communication is the best available predictor of the next one.

Write it (`memory-template.md`): every third party as a row in `## Vendors` with tier, data held, access granted, last review and next review date — and that next date also as a `## Due` row, because the register reminds nobody; their security contact and the person who owns the relationship in `~/Clawic/data/contacts/contacts.md`; the subscription and its cost in `~/Clawic/data/finances/subscriptions.md`; each pipeline, dependency or vendor gap as a `## Findings` row with owner, due date and the path it removes; the vendor assessment standard, the questionnaire answer bank and the CI hardening baseline in `~/Clawic/data/cybersecurity/artifacts/` with their `## Boxes` lines in the same turn. Tokens and deploy credentials are never recorded — the pointer only: `env:CI_DEPLOY_TOKEN`, `1password:Eng/Registry`.
