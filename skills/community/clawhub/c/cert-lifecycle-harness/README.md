# Cert-Lifecycle-Harness

<p align="left">
  <a href="./README.md"><b>English</b></a> ·
  <a href="./README.zh-CN.md">简体中文</a>
</p>

<p align="left">
  <a href="https://github.com/dimayip/cert-lifecycle-harness/stargazers"><img src="https://img.shields.io/github/stars/dimayip/cert-lifecycle-harness?style=flat-square" alt="Stars"></a>
  <a href="https://github.com/dimayip/cert-lifecycle-harness/network/members"><img src="https://img.shields.io/github/forks/dimayip/cert-lifecycle-harness?style=flat-square" alt="Forks"></a>
  <a href="https://github.com/dimayip/cert-lifecycle-harness/issues"><img src="https://img.shields.io/github/issues/dimayip/cert-lifecycle-harness?style=flat-square" alt="Issues"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/github/license/dimayip/cert-lifecycle-harness?style=flat-square" alt="License"></a>
</p>

> **A Harness-style collaboration skill for the full lifecycle of an X.509/TLS certificate.** The Agent is positioned as **"safety officer + document engineer + trusted executor"** — it generates layered review documents and human-executed scripts, may carry out Import/Modify-class write APIs on the user's behalf once six gates are satisfied, and **never executes Delete**.

---

## Install

Via [skills.sh](https://skills.sh) (works for Claude Code / Cursor / Codex / CodeBuddy / OpenCode / 50+ agents):

```bash
# global install (all projects)
npx skills add dimayip/cert-lifecycle-harness -g -a claude-code

# project-only install (current repo)
npx skills add dimayip/cert-lifecycle-harness -a codebuddy
```

Or drop the repo into your agent's skills directory manually (e.g. `~/.claude/skills/cert-lifecycle-harness/` or `.codebuddy/skills/cert-lifecycle-harness/`).

Compatible with the [Agent Skills Specification](https://agentskills.io).

---

## Why this skill exists

Certificate rollover is a textbook **"expire = outage"** high-risk operation:

- One wrong SAN field → site-wide TLS handshake failure
- Remembering to renew the day before expiry → no canary window → P0
- Rolling dozens of deployment points in one shot → reviewer fatigue → critical risk missed
- Letting an AI agent touch production directly → dangerous and uncontrollable

This skill decomposes certificate change into a collaborative workflow aligned with the **7 Harness Principles**:

- The Agent generates guidance, scripts, diff reports, and review documents; it may carry out Import/Modify-class write APIs when the six gates are satisfied.
- Humans own decisions, approvals, and all Delete-class operations.
- **The core innovation is "layered review"**: L3 decision layer 5 min / L2 strategy layer 15 min / L1 execution layer 30 min — different reviewers run in parallel, squeezing total human load to ≤ 50 min.

---

## When to load

Trigger keywords include:

- Certificate expiring / certificate renewal / certificate replacement
- Wildcard certificate / SAN certificate / multi-domain certificate
- SSL / TLS / HTTPS certificate
- CA migration / changing issuing authority

---

## Agent hard boundaries

```
✅ Do: generate docs, scripts, checklists, diff reports
✅ Do: proactively surface information gaps and guide the user to fill them
✅ Do: pre-review via layered review to reduce human load
✅ Do: call READ-ONLY cloud APIs within user-granted scope to offload manual inventory
✅ Do: carry out IMPORT / MODIFY-class write APIs on the user's behalf IF all six gates are satisfied

❌ Don't: call any cloud API / kubectl without explicit user authorization
❌ Don't: EVER execute Delete-class write APIs (delete cert, delete binding, delete resource) — only generate scripts
❌ Don't: carry out Import/Modify-class writes if any gate fails
❌ Don't: ssh into production or hand-edit production config files
❌ Don't: hallucinate customer-specific information from general knowledge
❌ Don't: replace the human as final approver
```

### Three-tier API authorization model

| Tier | Capability (vendor-agnostic) | Authorization |
|---|---|---|
| 🟢 **Read-only API** | List/query cloud resources: cert inventory, CDN domain configs, LB listeners, K8s Secrets, DNS zone records | One-time read-only credential, repeatedly callable |
| 🟡 **Probe-class** | DNS resolution / TLS handshake / CT logs (crt.sh) / SSL Labs rating | User-confirmed domain list |
| 🔴 **Write API (3 tiers)** | Create / Update / Delete / Put / Deploy | Per-call authorization + six gates; **Delete is never delegated** |

> ⚠️ Cloud vendor API naming diverges significantly (AWS / Aliyun / Tencent Cloud / Huawei / Cloudflare / Volcano). The Agent MUST confirm the vendor and verify against official docs before calling — never reuse API names across vendors.

Full protocol and cross-vendor API reference: [`SKILL.md §4`](./SKILL.md) and [`references/cloud-api-naming.md`](./references/cloud-api-naming.md).

---

## Repository layout

Follows skill-creator's progressive-disclosure principle: the main `SKILL.md` is ≤ 600 lines; deep rules are pushed down to `references/` and loaded on demand.

```
cert-lifecycle-harness/
├── SKILL.md                              # Main spec loaded by the Agent (v1.0, 14 sections)
├── README.md                             # (this file) English version
├── README.zh-CN.md                       # Chinese version
├── CHANGELOG.md                          # ⭐ Version history
│
├── references/                           # ⭐ Deep rules, loaded on demand (new in v1.0)
│   ├── README.md                         #   Index · by load scenario
│   ├── topology-detection.md             #   Infrastructure topology detection (CLB / CVM EIP / CDN edge)
│   ├── wildcard-inventory.md             #   Subdomain inventory under a wildcard certificate
│   ├── cert-chain-verification.md        #   Chain integrity + multi-client compatibility (D1–D5)
│   ├── san-closure-discovery.md          #   SAN closure discovery + cert_role + shadow-cert provenance
│   ├── dns-probing.md                    #   DNS probes and infrastructure inference
│   ├── inquiry-protocol.md               #   Four-tier inquiry protocol (🔵/🟢/🟡/🔴)
│   ├── csr-persona-talks.md              #   CSR three-option + three-persona script
│   └── cloud-api-naming.md               #   Cross-vendor API naming differences
│
├── phases/                               # Phase methodology files (loaded on demand)
│   ├── 00-intake-checklist.md            #   Phase 0 · Path triage + seed mode
│   ├── 01-inventory-guidance.md          #   Phase 1 · SAN closure iteration + DNS probes
│   ├── 02-scope-lock-and-reflow.md       #   Phase 2 · Scope lock + cert_role
│   ├── 03-risk-assessment-playbook.md    #   Phase 3 · Six-dimension risk + DCV matrix
│   ├── 04-planning-playbook.md           #   Phase 4 · Plan elasticity + Decision Brief
│   ├── 05-dry-run-matrix.md              #   Phase 5 · Dry-run library
│   ├── 06-verify-rollback-playbook.md    #   Phase 6 · Six-layer verify + rollback granularity
│   └── runbook-templates/                #   Runbook templates per binding-point type
│
├── review-guides/                        # ⭐ Layered review architecture (core innovation)
│   ├── L3-decision-review.md             #   5 min · for managers
│   ├── L2-strategy-review.md             #   15 min · for security / architecture
│   ├── L1-execution-review.md            #   30 min · for ops
│   └── self-review-checklist.md          #   Agent pre-delivery self-check (7 classes, A–G)
│
└── scripts/
    └── readonly/
        └── TEMPLATE.sh                   # Structural template every script must follow
```

---

## Standard workflow

```
Phase 0  Intake (public-data recon first → triage → only ask what public data can't answer) → ⛔ wait for user
   ↓
Phase 1  Asset inventory (SAN closure iteration + DNS probing + per-zone independent authorization) → ⛔ wait
   ↓
Phase 2  CA selection ADR (four-part recommendation + candidate plans) → ⛔ wait for user pick
   ↓
Phase 3  CSR + deployment plan generation (CSR options A/B/C)
   ↓
Phase 4  Layered-review delivery (L3/L2/L1 in parallel, persisted to disk) → ⛔ wait for human review
   ↓
Phase 5  Execute & rollback (branches by write-API tier; Import/Modify delegated, Delete script-only)
   ↓
Phase 6  Verify (D1–D5 chain + six-layer verify matrix; tailored by cert_role)
```

Every Phase **must stop and wait for a human** — this is what separates this skill from a "generate-a-script" tool.

---

## Capability map

| Domain | Key feature | Location |
|---|---|---|
| **Complexity triage** | Fast / Standard / Full path + admission/trigger rules + Phase tailoring | `SKILL.md §3` + `phases/00-intake-checklist.md §0` |
| **Intake** | Public-data recon first + seed mode + field sets per path + Full Path approval matrix | `SKILL.md §3.5` + `phases/00-intake-checklist.md` |
| **Topology detection** | TTL / Server header / nc / ALPN deprecated as signals; read-only cloud API or customer confirmation is the only reliable path | `references/topology-detection.md` |
| **Wildcard subdomain inventory** | WHOIS → DNS platform → guided full-zone walk; CT logs as auxiliary only | `references/wildcard-inventory.md` |
| **Asset inventory** | SAN closure discovery + DNS probes + reverse-expansion heuristic + partial-authorization degradation + shadow-cert provenance | `references/san-closure-discovery.md` + `phases/01-inventory-guidance.md` |
| **Scope management** | Scope Lock + inventory reflow + asset classes (A/B/C/D/E) + binding-point definition + 5-role cert_role | `phases/02-scope-lock-and-reflow.md` |
| **Risk assessment** | Six-dimension framework + hard-constraint filters + DCV matrix + hard-block fallback tree | `phases/03-risk-assessment-playbook.md` |
| **Plan design** | Elastic plan count + six-dim scoring (incl. reversibility) + Decision Brief + Fast-Path Runbook template | `phases/04-planning-playbook.md` |
| **Inquiry protocol** | Four tiers (🔵 statement / 🟢 assumption / 🟡 recommendation / 🔴 open question) + mandatory public-data recon | `references/inquiry-protocol.md` + `SKILL.md §8.2` |
| **CSR strategy** | Three options (A local / B cloud-CA / C reuse) × three scripts (L1/L2/L3 audiences) | `references/csr-persona-talks.md` + `SKILL.md §8.3` |
| **Chain verification** | D1–D5 five dimensions (leaf chain / order / intermediate validity / Root reachability / multi-client compatibility) | `references/cert-chain-verification.md` |
| **Layered review** | L3 / L2 / L1 three independent artifacts, ≤ 5 / 15 / 30 min, ≤ 50 min total — **must be persisted** | `review-guides/L{1,2,3}-*.md` |
| **Agent self-check** | A–G seven classes, incl. G1–G15 | `review-guides/self-review-checklist.md` |
| **Write-API delegation** | Import / Modify / Delete three tiers + six gates | `SKILL.md §4` |

### Fast / Standard / Full Path selection guide

**Pick 🟢 Fast Path** only if ALL hold:
- Remaining validity ≥ 30 days
- SAN ≤ 3 (including apex)
- Single DNS zone
- ≤ 3 deployment points
- No strong compliance (finance / SM-crypto / MLPS-3+)
- Decision-maker = executor, or a ≤ 2-person team

**Pick 🔴 Full Path** if ANY hold:
- SAN spans ≥ 3 DNS zones
- Approval chain involves ≥ 3 independent teams (platform + security + legal)
- Assets include the "acquisition-legacy / cross-brand / shadow" class
- Actionable window (remaining days − internal SLA buffer) < 60 days
- Explicit strong-compliance requirement
- Single-spend decision must go through procurement (≥ 2 weeks)

**Otherwise pick 🟡 Standard Path**.

---

## Design principle (meta)

> The most important thing this skill does is NOT "do it for the user". It is **"decompose the cognitive load of high-risk operations into layers, so every human reviewer has a predictable, completable time budget."**
>
> The Agent never owns the certificate. It is only **the collaborator that makes the human's certificate decisions explicit** — asking honestly when information is missing, pointing out honestly when a Harness principle is violated. That is all.

---

## ⭐ Star history

[![Star History Chart](https://api.star-history.com/svg?repos=dimayip/cert-lifecycle-harness&type=Date)](https://star-history.com/#dimayip/cert-lifecycle-harness&Date)

---

## License

Unless noted otherwise in individual files, this repository is released under the MIT License. See [`LICENSE`](./LICENSE).
