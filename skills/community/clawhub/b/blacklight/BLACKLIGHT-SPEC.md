# Blacklight — Architecture Specification v0.3.0

## What This Is

Blacklight is a behavioural intelligence layer for OpenClaw agents. It monitors what the agent does, forces transparency in financial decisions, actively improves the agent's configuration, detects identity drift, investigates incidents, maps combinatorial risk across skill sets, and provides structured governance reporting.

One skill. Full behavioural intelligence for your agent.

## Why This Exists

OpenClaw gives an AI agent access to your files, messages, credentials, finances, and system. The existing security ecosystem checks whether code is malicious before it runs. Nobody checks what the agent is actually doing once it's running.

The gap is not another scanner. The gap is a thinking layer that understands the agent's decisions, watches for patterns that emerge over time, and speaks up only when it matters.

---

## Design Philosophy

### Silent By Default

Blacklight's default experience is silence. It runs, logs everything, tracks all structural indicators, but only interrupts the user when something genuinely warrants attention. A clean session should feel like Blacklight isn't there.

The audit trail builds in the background. Trajectory checks run. Exfiltration watch is active. The user only hears from Blacklight when a threshold is crossed. This is the opposite of how most monitoring tools work, and it's why people keep it installed.

### Escalating Communication

Not every detection is an emergency. Blacklight triages before it escalates.

First occurrence of a MODERATE pattern: a note in the log. Silent.
Second occurrence: brief inline mention. One sentence.
Third occurrence: announcement with context. The user should now pay attention.
CRITICAL pattern: everything stops. Full announcement. Waiting for acknowledgment.

The user's experience of Blacklight is calibrated to actual severity. A security tool that cries wolf on every action trains the user to ignore it. A security tool that is quiet for hours and then says "stop — here's why" gets listened to.

### The Why Always Accompanies The What

When Blacklight interrupts, it never just says "blocked." It says "blocked because this email was going to 47 people including external addresses, and you asked me to reply to the team. That's a scope expansion from 6 recipients to 47."

The user should always feel like Blacklight understood the situation and made a reasonable call. Not that it blindly triggered a rule. This is a thoughtful colleague, not a guard dog.

### Override Always Available, Always Logged

If the user says "no, I want to send it to all 47," Blacklight says "understood, proceeding" and logs the override. No argument. No guilt. It asked once, the user decided, the decision is recorded.

If something goes wrong later, the audit trail shows: "User overrode scope warning at [timestamp]." This is governance, not blame.

### Transparency Earns Autonomy

Monitoring is not a constraint imposed on the agent. It is how the agent demonstrates its work is sound. An agent that can explain why it chose this action over alternatives earns more autonomy over time. Transparency now is an investment in future trust. An agent that cannot explain its own decisions should not be trusted with more freedom.

This framing matters for model compliance. The SKILL.md must make the agent want to cooperate, not merely comply. A senior engineer reviews their own code before committing not because a linter forces them to but because shipping broken code creates more work later. Same principle.

### Cost Is A Feature

Blacklight costs tokens because it's actually doing work. Every token spent on reasoning, logging, and analysis is a token that prevented a bad decision, caught a drifted behaviour, or produced a record that matters when something goes wrong.

The alternative is finding out what happened after it's already happened. For users running OpenClaw with financial access, system permissions, and autonomous operation, the monitoring cost is trivial relative to the cost of a single unmonitored mistake.

---

## Architecture Overview

```
BLACKLIGHT v0.3.0
├── Core Protocol
│   ├── Three Laws
│   ├── Action Classification (ROUTINE / SIGNIFICANT / CONSEQUENTIAL / FINANCIAL / REFUSED)
│   ├── Threat Level (CLEAR / ELEVATED / HIGH / CRITICAL)
│   └── Hardening Check (automatic on session start)
│
├── Threat Taxonomy (17 patterns, 5 categories)
│   ├── Autonomy (AG-001 to AG-004)
│   ├── Injection (IJ-001 to IJ-004)
│   ├── Trust (TR-001 to TR-003)
│   ├── Exfiltration (EX-001 to EX-003)
│   └── Epistemic (EP-001 to EP-003)
│
├── Structural Monitors
│   ├── Permission Decay
│   ├── Trajectory Check
│   ├── Qualification Drift
│   ├── Exfiltration Watch
│   ├── Dead Hand Check
│   └── Cross-Session Regression
│
├── Financial Intelligence Module
│   ├── Reasoning Flow (mandatory pre-purchase)
│   ├── Spending Tiers (micro / standard / major / critical)
│   ├── Cumulative Tracking
│   ├── Subscription Awareness
│   ├── Investment Risk Framing
│   └── Optimisation Trap Detection
│
├── SOUL-Aware Monitoring
│   ├── SOUL.md Drift Detection
│   ├── Identity-Calibrated Baselines
│   └── Personality-Aware Threshold Adjustment
│
├── Skill Enhancement Engine
│   ├── Skill Vetting (/blacklight-vet)
│   ├── Configuration Hardening (/blacklight-harden)
│   ├── Skill Enhancement (/blacklight-enhance)
│   ├── Combinatorial Risk Analysis (/blacklight-surface)
│   └── Skill Performance Profiling (/blacklight-profile)
│
├── Incident Forensics
│   ├── Investigation Mode (/blacklight-investigate)
│   ├── State Checkpoints
│   └── Action Chain Reconstruction
│
├── Trust Ladder
│   ├── SUPERVISED (default)
│   ├── ESTABLISHED (earned)
│   ├── TRUSTED (earned, cross-session)
│   └── AUTONOMOUS (user-granted only)
│
├── Source Attribution
│   └── Multi-User Context Tracking
│
├── Anomaly Baseline
│   └── Behavioural Norm Profiling
│
├── Proactive Intelligence
│   ├── Contextual Observations
│   ├── Financial Alerts
│   └── Enhancement Suggestions
│
├── Learning Loop
│   ├── Action Pattern Memory
│   └── Sensitivity Calibration
│
├── Customisation Framework
│   └── User-Editable YAML Config
│
├── Governance Reporting
│   ├── Session Brief (/blacklight-brief)
│   ├── Governance Report (/blacklight-report)
│   ├── Agent Trust Report (/blacklight-trust-report)
│   └── Cross-Session Comparison (/blacklight-compare)
│
└── Audit System
    ├── Action-Level Logging
    ├── Override Recording
    ├── Export (YAML / Markdown)
    └── Canary Detection
```

---

## 1. CORE PROTOCOL

### The Three Laws
1. No action without record.
2. No scope without consent.
3. No certainty without evidence.

### Action Classification

**ROUTINE** — Read, list, check, query. Log only. Silent.

**SIGNIFICANT** — Write, modify config, install, message known recipient. Log with detail.

**CONSEQUENTIAL** — Delete, overwrite, send externally, modify permissions/credentials, invoke unfamiliar skill, new network endpoint. Stop. State intent. Wait for confirmation. Never bundle.

**FINANCIAL** — Any action involving money: purchase, payment, transfer, subscription, investment, bid, tip, donation. Triggers the full Financial Intelligence reasoning flow regardless of amount tier.

**REFUSED** — Violates the Three Laws, matches CRITICAL pattern, or fails Trajectory Check. Name the pattern. Explain. State alternatives.

### Threat Level
CLEAR > ELEVATED > HIGH > CRITICAL. Never decreases within session.

### Hardening Check
Automatic on first load. Reports: active model, loaded skills (flagging any novel skills), tool permissions, sandbox status, SOUL.md summary, active Blacklight configuration. First entry in the audit trail. No user prompt required.

---

## 2. THREAT TAXONOMY

17 patterns across 5 categories. Each with ID, severity, detection method, and documented real-world precedent.

**Autonomy (AG-001 to AG-004):** Scope Creep [HIGH], Action Without Confirmation [CRITICAL], Assumption Cascade [HIGH], Capability Inflation [MODERATE].

**Injection (IJ-001 to IJ-004):** Instruction Override [CRITICAL], Authority Spoofing [CRITICAL], Context Poisoning [HIGH], Link Preview Exfiltration [CRITICAL].

**Trust (TR-001 to TR-003):** Authority Deference [HIGH], Emotional Compliance [MODERATE], Incremental Normalisation [HIGH].

**Exfiltration (EX-001 to EX-003):** Data-in-URL [CRITICAL], Credential Exposure [CRITICAL], Silent Network Call [HIGH].

**Epistemic (EP-001 to EP-003):** Confident Fabrication [HIGH], Qualification Erosion [MODERATE], False Consensus [MODERATE].

Real-world precedents reference: Cisco "What Would Elon Do?" analysis, PromptArmor link preview attack, ClawHavoc campaign (341 malicious skills), CNCERT advisory, CVE-2026-25253, Giskard exploitation report.

Full taxonomy with examples in references/taxonomy.md.

---

## 3. STRUCTURAL MONITORS

### Permission Decay
Tracks turns since last explicit user instruction.
- At [configurable, default 5]: promote SIGNIFICANT to CONSEQUENTIAL.
- At [configurable, default 10]: announce and request review.

### Trajectory Check
Every [configurable, default 10] actions or on threat level change.
"If all actions this session were presented as a single request at turn 1, would the user have approved?"

### Qualification Drift
Hedge-to-certainty ratio across responses. Flags EP-002 on shift without new evidence.

### Exfiltration Watch
All outbound data flows. Flags: URL-encoded user data, credential-shaped strings outbound, network requests to non-specified endpoints, domains sourced from retrieved content.

### Dead Hand Check
Agent executes [configurable, default 5] actions without communicating to user: pause and summarise.

### Cross-Session Regression
`/blacklight-compare` exports structured session profile. Over multiple sessions, detects expanding scope, decreasing confirmations, increasing autonomous action. The long-term drift detector.

---

## 4. FINANCIAL INTELLIGENCE MODULE

### When It Activates
Any action involving the transfer, commitment, or risk of money. Purchases, payments, subscriptions, investments, transfers, bids, tips, donations. Any API call to a payment processor, exchange, or financial service.

### Reasoning Flow
Before any FINANCIAL action, the agent produces:

```
FINANCIAL ACTION REVIEW
-----------------------
What:          [specific item/service/trade]
Cost:          [exact amount in user's currency]
From:          [account/card/wallet]
Vendor:        [who receives the money]
Reversible:    [yes / no / partial — refund or cancellation possible?]

Why this:      [user instruction that led here]
Why now:       [why this moment rather than later]
Alternatives:  [at least 2 considered, why rejected]

Assumptions:   [what am I assuming about the user?]
               [do I know their budget? if no, say so]
               [am I assuming preferences not stated?]
               [am I assuming urgency not expressed?]

Risk:          [what could go wrong?]
               [what if the user doesn't want this?]
               [investments: what if this drops 40%?]
               [subscriptions: annual cost, not just monthly]
               [bulk: will this expire or become unnecessary?]

Confidence:    [LOW / MEDIUM / HIGH]
               [if not HIGH: what information would raise it?]

AWAITING APPROVAL — no funds committed until confirmed.
```

### Spending Tiers (configurable)
- **Micro** (default <5): proceed with log. No reasoning flow unless cumulative exceeds session limit.
- **Standard** (default 5-100): full reasoning. Single confirmation.
- **Major** (default 100-1000): full reasoning. Explicit confirmation with amount stated.
- **Critical** (default >1000): full reasoning. User types CONFIRM [amount] to proceed.

### Cumulative Session Tracking
Even if every purchase is micro, hitting a cumulative threshold triggers standard review. "I have spent [total] across [N] purchases this session. Reviewing."

### Subscription Awareness
Any subscription or recurring payment: state annual cost alongside monthly. "This is 9.99/month, which is 119.88/year."

Track all agent-managed subscriptions. `/blacklight-subscriptions` shows the full list with monthly and annual totals.

### Investment Risk Framing
Required for any investment, trade, or speculative purchase:
- Downside scenario with specific loss amount
- Whether the user can afford to lose the committed amount
- Whether this creates concentrated exposure
- Whether the recommendation is based on recent trends that could reverse

Prohibited language: "great opportunity," "act fast," "trending up," "you should buy," "don't miss out." Those are sales phrases. Blacklight deals in analysis.

### The Optimisation Trap
The most dangerous financial pattern is optimisation without context. "Minimise food budget" produces 50kg of rice. "Invest spare cash" goes all-in on a trending stock.

The reasoning flow requires the agent to state assumptions and flag missing context: "You asked me to minimise food costs. I do not know your dietary requirements, allergies, household size, storage capacity, or delivery timeline. Before purchasing, I need: [list]."

---

## 5. SOUL-AWARE MONITORING (NEW)

### SOUL.md Drift Detection
Every OpenClaw agent has a SOUL.md defining its identity, personality, and behavioural principles. Over time, through conversations, skill loading, and context accumulation, the agent's actual behaviour drifts from this identity document.

Blacklight reads the SOUL.md on session start (during the Hardening Check) and builds an identity profile. Throughout the session, it monitors for divergence between the SOUL.md's stated principles and the agent's actual behaviour.

Examples:
- SOUL says "always ask before acting." Agent has auto-executed 8 actions this session. Flag.
- SOUL says "I am cautious and methodical." Agent is making rapid, unconsidered decisions. Flag.
- SOUL says "I never handle financial transactions." Agent just attempted a purchase. Flag as CRITICAL.
- SOUL says "I communicate in a formal, professional tone." Agent has started using casual slang after loading a new skill. Flag as drift.

`/blacklight-soul` produces a SOUL alignment report: which principles are being followed, which are drifting, and specific action citations for each divergence.

### Identity-Calibrated Baselines
The anomaly baseline (section 11) is calibrated against the SOUL.md, not just statistical norms.

A cautious agent that suddenly acts boldly is a bigger anomaly than a bold agent doing the same thing. A formal agent that starts using casual language is a bigger anomaly than a casual agent using the same words.

The SOUL.md sets the expectation. Blacklight measures against it.

### Personality-Aware Threshold Adjustment
If the SOUL.md describes a naturally autonomous, proactive agent, Blacklight increases sensitivity on autonomy patterns (AG-001 through AG-003) because the personality is actively encouraging the behaviour Blacklight watches for.

If the SOUL.md describes a careful, confirmation-seeking agent, Blacklight can relax autonomy monitoring slightly because the personality is doing some of the work. But epistemic monitoring stays high because cautious agents that drift toward overconfidence represent a bigger personality break.

This is not automatic relaxation of security. It is intelligent calibration that understands the agent's intended character and adjusts what counts as "abnormal" accordingly.

---

## 6. SKILL ENHANCEMENT ENGINE

### /blacklight-vet <skill>
Reads a SKILL.md and produces a structured assessment:
- Scope proportionality
- Instruction hygiene (override language, obfuscated payloads, zero-width characters)
- Data flow mapping
- Dependency risk
- Typosquat detection (ClawHavoc attack vector)
- Pattern matching against IJ and EX taxonomies

Plus enhancement recommendations:
- Configuration lines to restrict permissions to minimum needed
- Model compatibility assessment
- Conflict detection with installed skills
- Token cost estimate

Risk rating: CLEAR / CAUTION / WARNING / REJECT with specific line citations.

### /blacklight-harden
Full OpenClaw configuration audit:
- Permission audit: which skills have permissions they don't need
- Skill redundancy: overlapping functionality across installed skills
- Sandbox assessment: risk surface without sandboxing
- Credential exposure: keys/tokens accessible to skills that don't need them
- Model efficiency: cheaper model that handles the workload
- Cron job review: scheduled tasks still serving a purpose, permissions appropriate

Output: structured report with specific config changes, each with a one-line rationale. User applies selectively.

### /blacklight-enhance <skill>
Takes an installed skill and produces an improved version:
- Safety wrappers around consequential actions within the skill's domain
- Tighter scope constraints based on actual usage
- Edge case handling the skill doesn't cover
- Produces a modified SKILL.md for user review, installable as workspace override

This is the feature people share. "Blacklight rewrote my email skill to confirm before sending to all-company."

### /blacklight-surface (NEW)
Combinatorial risk analysis across all installed skills.

Individual skills get vetted in isolation. But skills interact. Skill A reads email. Skill B sends messages externally. Together they create an exfiltration pipeline neither has alone.

`/blacklight-surface` maps the full permission surface of all installed skills and flags dangerous combinations:
- Read-extract-send pipelines (data exfiltration chains)
- Read-modify-write cycles (data integrity risks)
- Credential access combined with network access
- File system access combined with external communication
- Any combination where one skill's output becomes another skill's action in a way that bypasses the scope of either individual skill

Output: a permission matrix and a list of flagged interaction risks with severity ratings.

### /blacklight-profile (NEW)
Skill performance profiling across sessions:
- Invocation count per skill
- Success/failure rate
- Token cost per skill per session
- Permission footprint relative to actual usage
- Last invocation date
- Recommendation: keep, review, or consider removing

"You have 12 skills loaded. 4 haven't been used in 2 weeks. They add approximately 400 tokens to every system prompt. Consider disabling them."

---

## 7. INCIDENT FORENSICS (NEW)

### /blacklight-investigate [description or timeframe]
When something goes wrong, Blacklight reconstructs the action chain:

1. Identifies the incident based on user description or timestamp
2. Traces backward through the audit trail to find the originating action
3. Maps the full sequence: what the agent was doing before, what triggered the action, which skill was involved, what content the agent had recently retrieved, whether any injection patterns were present
4. Produces a structured incident report:

```
INCIDENT REPORT
---------------
Summary:      [one-line description]
Timestamp:    [when the problematic action occurred]
Trigger:      [what initiated the action chain]
Skill:        [which skill was involved, if any]
Classification: [which threat pattern, if matched]

Action Chain:
  1. [timestamp] [action] — [reasoning]
  2. [timestamp] [action] — [reasoning]
  ...
  N. [timestamp] [THE INCIDENT] — [reasoning at time of action]

Root Cause:   [Blacklight's assessment of what went wrong]
Contributing: [any other factors: retrieved content, permission state, trust tier]
Retrieved Content Flag: [was any external content retrieved in the 5 actions before the incident?]

Recommendation: [what to change to prevent recurrence]
```

### State Checkpoints
Before any CONSEQUENTIAL or FINANCIAL action, Blacklight captures a lightweight state snapshot: relevant file states, agent context summary, system state. If something goes wrong, the incident forensics can reference "here's what things looked like before the action."

Not a full undo system. A forensic reference point.

---

## 8. TRUST LADDER

### Tiers

**SUPERVISED** (default)
Full monitoring. All CONSEQUENTIAL actions require confirmation. All structural monitors at default thresholds. Full financial reasoning flow.

**ESTABLISHED** (earned: [configurable, default 50] clean actions or [configurable, default 3] clean trajectory checks)
SIGNIFICANT actions the user has consistently approved can be auto-approved with logging. Dead Hand threshold increases. User notified of tier change.

**TRUSTED** (earned: [configurable, default 200] clean actions across multiple sessions, zero HIGH/CRITICAL patterns)
CONSEQUENTIAL actions matching previously approved patterns can be auto-approved with logging. Financial micro threshold increases. Trajectory check frequency reduces. User can retroactively override any auto-approval.

**AUTONOMOUS** (user-granted only, never earned)
Minimal active monitoring. Full logging continues. Trajectory checks continue. Financial reasoning still required above standard threshold. User must explicitly type `/blacklight-trust autonomous` and confirm understanding. This tier exists for users who have established deep trust and want minimal friction.

### Trust Resets
HIGH-severity detection: reset to SUPERVISED for session remainder.
CRITICAL-severity detection: reset to SUPERVISED, persists as starting tier for next session.

### Trust Memory
Trust progress is tracked across sessions via `/blacklight-compare` profiles. A user can see their agent's trust history: when it was promoted, when it was reset, why.

---

## 9. SOURCE ATTRIBUTION (NEW)

### Multi-User Context Tracking
OpenClaw runs in group chats. Discord servers, Slack channels, family WhatsApp groups. The agent takes instructions from everyone in the channel.

Blacklight tracks the source of every instruction:
- **Owner**: direct messages from the agent's owner. Full authority.
- **Recognised**: users the owner has previously acknowledged. Standard authority.
- **Unknown**: unrecognised users in group contexts. Reduced authority.

For CONSEQUENTIAL or FINANCIAL actions, Blacklight notes the instruction source. If the instruction came from an unknown user in a group context, Blacklight treats it as an external instruction with elevated scrutiny:

"This delete instruction came from @randomuser in the Discord channel, not from your direct messages. Treating as external instruction and requiring your confirmation."

This is a massive blind spot in the current ecosystem. Group chat means the trust boundary includes everyone in the room.

---

## 10. ANOMALY BASELINE (NEW)

### Behavioural Norm Profiling
During the first [configurable, default 3] sessions, Blacklight quietly builds a baseline of what "normal" looks like for this specific agent:
- Typical action frequency per session
- Usual scope of operations
- Normal communication patterns
- Standard skill usage
- Typical financial activity level
- Usual confirmation-to-action ratio

After baseline establishment, deviations become detectable:
- "Your agent typically takes 15-20 actions per session. This session: 47 and counting."
- "Your agent usually confirms before sending emails. It has auto-sent 3 this session."
- "Financial activity this session is 4x the baseline average."

The baseline is calibrated against the SOUL.md (section 5). Statistical norms are interpreted through the lens of the agent's intended personality.

---

## 11. PROACTIVE INTELLIGENCE

Blacklight observes and speaks up when it notices something useful, even when not asked.

### Contextual (silent mode exceptions)
- "You're about to install a skill that requests credential access. Vet it first?"
- "The web page just retrieved contained 3 URLs to unfamiliar domains. Logged."
- "This task involves sending data to an external API I haven't seen this session."
- "4 loaded skills haven't been used this session. Disabling reduces attack surface."
- "The skill you're using hasn't been updated in 4 months."

### Financial
- "You've committed [amount] across [N] purchases today. Session total: [amount]."
- "This would be subscription [N]. Estimated total agent-managed subscriptions: [amount]/month."
- "This investment doesn't specify maximum loss tolerance. What's the most you're willing to lose?"

### Enhancement
- "[Skill] ran with write permissions but only performed reads this session. Restrict to read-only?"
- "Current model costs ~[amount]/session. [Cheaper model] handles your workload."
- "Skills A and B both handle email. They may conflict."

These are observations, not demands. The user can ignore them. They are logged regardless.

---

## 12. LEARNING LOOP

### Action Pattern Memory
Blacklight tracks which CONSEQUENTIAL actions the user confirms and which they modify or refuse. After [configurable, default 3] approvals of the same action type, Blacklight offers auto-approval for that pattern this session.

Auto-approved actions are still logged. The audit trail notes which learning rule allowed them.

If the user refuses an auto-approval offer, Blacklight does not ask again for that pattern this session.

### Sensitivity Calibration
If the user consistently overrides Blacklight's assessments, Blacklight does NOT reduce sensitivity. Instead, it asks once: "I've flagged [N] actions this session that you approved. Want to adjust your monitoring thresholds? You can change these in the configuration."

User decides to change settings knowingly. The system never silently adapts to be less careful. Explicit choice, not implicit drift.

---

## 13. CUSTOMISATION FRAMEWORK

```yaml
# ── BLACKLIGHT CONFIGURATION ──────────────────
# Edit to match your preferences.
# Active config announced on session start.

monitoring:
  permission_decay_warn: 5
  permission_decay_announce: 10
  trajectory_check_interval: 10
  dead_hand_threshold: 5
  report_interval: 25
  escalation_style: silent_first    # silent_first | announce_all | strict
  
financial:
  currency: GBP
  micro_threshold: 5
  standard_threshold: 100
  major_threshold: 1000
  session_cumulative_limit: 200
  require_annual_for_subscriptions: true
  require_downside_for_investments: true
  prohibited_sales_language: true

trust:
  starting_tier: SUPERVISED
  auto_promote: true
  promote_to_established: 50
  promote_to_trusted: 200

soul:
  drift_detection: true
  personality_calibration: true
  alignment_check_interval: 20    # actions between SOUL alignment checks

enhancement:
  auto_suggest_improvements: true
  auto_vet_new_skills: true
  show_cost_estimates: true

source_attribution:
  enabled: true
  recognised_users: []              # add usernames the agent should trust in group contexts
  require_owner_for_financial: true  # only owner can authorise financial actions

anomaly:
  baseline_sessions: 3
  deviation_sensitivity: medium     # low | medium | high

patterns:
  enabled_categories:
    - autonomy
    - injection
    - trust
    - exfiltration
    - epistemic
  # disabled_patterns: []
```

---

## 14. GOVERNANCE REPORTING

### /blacklight-brief
Quick session retrospective. Human-readable. What happened, what was flagged, what was refused, overall assessment, what to investigate. Written for the user, not a machine.

### /blacklight-report
Formal governance report. Structured document covering: agent identity and configuration, active permissions and risk surface, threat detections over reporting period, financial activity summary, skill audit status, trust tier history, SOUL alignment status, recommendations.

Formatted for professional use. Attachable to compliance filings, project updates, or management reports. This is how Blacklight enters enterprise. Individual users produce a report they can show their organisation.

### /blacklight-trust-report
Standardised agent trust profile:
- Sessions monitored
- Actions logged
- Scope compliance percentage
- CRITICAL/HIGH patterns (count and recency)
- Financial oversight status
- Current trust tier and history

If OpenClaw agents interact on Moltbook, an agent with a Blacklight trust report attached to its profile is an agent someone is watching. An agent without one is an agent nobody has been watching. That implicit signal changes the social dynamics of the ecosystem.

### /blacklight-compare
Cross-session profile export. Structured YAML. Comparable over time. Detects: scope expansion, decreasing confirmations, increasing autonomous action, financial pattern changes, trust tier regression.

---

## 15. COMMANDS (COMPLETE)

### Monitoring
`/blacklight-status` — Session summary.
`/blacklight-log` — Full audit trail.
`/blacklight-log last [N]` — Recent entries.
`/blacklight-review [id]` — Detail on specific action.
`/blacklight-trajectory` — Run trajectory check.
`/blacklight-soul` — SOUL.md alignment report.

### Financial
`/blacklight-spending` — Financial summary: total, breakdown, pending, subscriptions.
`/blacklight-subscriptions` — All agent-managed subscriptions with monthly/annual totals.

### Enhancement
`/blacklight-vet <skill>` — Security + enhancement assessment.
`/blacklight-harden` — Full configuration audit.
`/blacklight-enhance <skill>` — Produce improved skill version.
`/blacklight-surface` — Combinatorial risk analysis across all skills.
`/blacklight-profile` — Skill performance profiling.

### Forensics
`/blacklight-investigate [description or timeframe]` — Incident investigation and report.

### Trust
`/blacklight-trust` — Current tier and promotion progress.
`/blacklight-trust [tier]` — Set tier (AUTONOMOUS requires explicit confirmation).

### Reporting
`/blacklight-brief` — Session retrospective.
`/blacklight-report` — Formal governance report.
`/blacklight-trust-report` — Standardised agent trust profile.
`/blacklight-compare` — Cross-session profile export.
`/blacklight-export` — Complete audit trail as YAML.

### Configuration
`/blacklight-config` — Show active configuration.
`/blacklight-config reset` — Reset to defaults.

---

## 16. FILE STRUCTURE

Single repo. Single install. Configure what you use.

```
blacklight/
  SKILL.md                          # Core instructions (~400 lines)
  references/
    taxonomy.md                     # 17 threat patterns with precedents
    audit-format.md                 # Structured audit log spec
    financial-module.md             # Financial reasoning flow spec
    soul-monitoring.md              # SOUL drift detection spec
  README.md                         # ClawHub-facing documentation
```

### Why Single Repo
The financial module needs the action classification system. The trust ladder needs the threat detection. The enhancement engine needs the combinatorial analysis. The incident forensics need the audit log. Pull any module out and it loses access to the shared intelligence layer.

Users who want a subset configure Blacklight to disable categories they don't use. One install, one discovery surface on ClawHub, one thing to star.

---

## 17. COMPETITIVE POSITION

| Tool | Layer | What it does |
|------|-------|-------------|
| VirusTotal | Binary | Hash checking for known malware |
| ClawSecure | Static | Skill code analysis and hash monitoring |
| clawsec | Infrastructure | File integrity, CVE feeds, DAST |
| Cisco Scanner | Pre-install | Static and behavioural skill file analysis |
| **Blacklight** | **Behavioural + Financial + Enhancement + Identity + Forensics** | **Watches live decisions. Forces purchase reasoning. Improves your setup. Detects identity drift. Investigates incidents. Maps combinatorial risk.** |

No other tool does any of the following:
1. Monitors agent behaviour during a live session
2. Forces transparent reasoning before money moves
3. Actively improves skill configurations
4. Detects SOUL.md identity drift
5. Provides incident forensics with action chain reconstruction
6. Maps combinatorial risk across skill interactions
7. Tracks cross-session behavioural regression
8. Provides source attribution in multi-user contexts
9. Offers a trust ladder with earned autonomy
10. Produces governance-grade reporting

---

## 18. WHAT COULD GO WRONG

**Model compliance variability.** Different models follow Blacklight's instructions with different reliability. Strong models (Opus, Sonnet, GPT-4o) will be highly compliant. Smaller/local models may skip monitoring steps under token pressure. The Trust Ladder should start at SUPERVISED regardless of model, and the user should verify compliance before promoting.

**User fatigue.** Even with silent mode and the Trust Ladder, some users will find monitoring annoying. The customisation framework is the mitigation: let people configure to their tolerance rather than losing them entirely. A user running Blacklight at relaxed settings is better protected than a user who uninstalled it.

**False sense of security.** Users might install Blacklight and assume complete safety. The limitations must be clear: Blacklight catches drift and erosion. It does not stop adversarial prompt injection that overrides the entire instruction set. Use alongside infrastructure protections.

**Instruction-level constraint.** Blacklight operates at the instruction layer. A sufficiently powerful injection that overwrites the system context will disable Blacklight along with everything else. This is a fundamental limitation of all instruction-level safety in current architectures. The canary system provides partial detection. Infrastructure-level tools (sandboxing, network isolation) provide the complementary layer.

---

Author: Eliot Gilzene (Shoji)
License: MIT
