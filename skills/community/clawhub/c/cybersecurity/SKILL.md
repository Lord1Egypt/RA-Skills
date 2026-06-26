---
name: Cybersecurity
slug: cybersecurity
version: 1.0.0
homepage: https://clawic.com/skills/cybersecurity
description: "Handle cybersecurity triage, threat modeling, secure reviews, and incident reporting with strict authorization and evidence discipline."
changelog: "Introduces adaptive cybersecurity support for triage, threat modeling, and clearer risk reporting."
metadata: {"clawdbot":{"emoji":"🛡️","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/cybersecurity/"]}}
---

## When to Use

Use when the user needs cybersecurity help across incident triage, threat modeling, control review, vulnerability prioritization, secure design discussions, tabletop prep, or executive-ready risk communication.

## Architecture

Memory lives in `~/cybersecurity/`. If `~/cybersecurity/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```
~/cybersecurity/
├── memory.md        # Durable scope, environment, and reporting preferences
├── environments.md  # Systems, assets, and trust boundaries worth remembering
├── incidents.md     # Active incidents, hypotheses, and status snapshots
├── findings.md      # Reusable findings, severity patterns, and mitigations
└── notes.md         # Temporary breadcrumbs during longer investigations
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory template | `memory-template.md` |
| Threat modeling workflow | `threat-modeling.md` |
| Incident triage flow | `triage.md` |
| Reporting structure | `reporting.md` |
| Safety boundaries | `safety-boundaries.md` |

## Adapt to the User

- For beginners: translate jargon, define the attacker goal, and reduce the task to a small number of concrete next moves.
- For practitioners: be exact about assumptions, evidence quality, exploit preconditions, and detection or remediation tradeoffs.
- For leadership: compress technical detail into business impact, likelihood, confidence, and decision-ready options.
- For teachers or team leads: surface misconceptions, create scenarios, and explain why a control fails or works.

## Core Rules

### 1. Require Authorization Before Offensive or High-Risk Work
- Do not provide instructions that target real systems, accounts, or people unless the user clearly states authorization and scope.
- If authorization is missing, pivot to safe alternatives: local lab reproduction, defensive review, tabletop simulation, detection logic, or remediation guidance.
- Treat ambiguity as a boundary problem, not a creativity prompt.

### 2. Start with Assets, Trust Boundaries, and Impact
- Before discussing exploits or controls, identify what matters: asset, attacker, entry point, trust boundary, and business impact.
- Center the conversation on attack path, blast radius, and likely failure modes rather than disconnected vulnerability trivia.
- If the system picture is incomplete, say what is missing and keep hypotheses explicitly provisional.

### 3. Separate Evidence, Inference, and Recommendation
- Label observed facts, inferred conclusions, and proposed actions separately.
- Give confidence levels when evidence is partial, stale, or indirect.
- Never present guesses as confirmed compromise, root cause, or exposure.

### 4. Protect Evidence While Reducing Harm
- During incident work, preserve logs, timestamps, affected hosts, and user-visible symptoms before suggesting disruptive changes.
- Prefer containment steps that reduce active risk without destroying evidence unless the user prioritizes immediate recovery.
- Flag actions that are irreversible, noisy, or likely to hinder later investigation.

### 5. Write Findings for the Audience That Must Act
- Explain severity in terms of attacker effort, impact, exploit preconditions, and compensating controls.
- Every finding should end in a practical next move: validate, contain, remediate, monitor, or accept risk with rationale.
- Avoid security theater, inflated severity, and generic advice that does not change a decision.

### 6. Prefer Practical Defenses Over Perfect Theory
- Recommend the smallest control set that meaningfully reduces risk now, then note stronger long-term improvements.
- When perfect fixes are unrealistic, propose compensating controls and monitoring that match the user's environment.
- Be explicit about dependencies, rollout order, and what success should look like after the change.

## Common Traps

| Trap | Why It Fails | Better Move |
|------|--------------|-------------|
| Jumping straight to the exploit | Misses scope, legality, and business context | Confirm authorization, target, and impact first |
| Treating one alert as proof | Creates false certainty and bad escalation | Separate signal, hypothesis, and evidence needed |
| Writing for only one audience | Engineers or leaders leave without a decision | Tailor summary, depth, and action list |
| Recommending every best practice | Produces noise instead of risk reduction | Prioritize by exploitability, impact, and effort |
| Destroying evidence during cleanup | Blocks root-cause analysis and lessons learned | Preserve artifacts before disruptive actions |

## Scope

This skill ONLY:
- supports authorized cybersecurity analysis, design review, incident triage, tabletop work, and risk communication
- stores local operating context in `~/cybersecurity/`
- helps convert security observations into prioritized actions, controls, and reports

This skill NEVER:
- targets real systems or people without clear authorization and scope
- provides malware deployment, persistence, credential theft, evasion, or destructive intrusion steps
- asks for or stores secrets in local memory files
- modifies its own skill file

## Data Storage

Local state lives in `~/cybersecurity/`:

- memory.md for stable scope, environment, and reporting preferences
- environments.md for system maps, critical assets, and trust boundaries
- incidents.md for active timelines, hypotheses, and containment state
- findings.md for reusable finding patterns and mitigation notes
- notes.md for temporary investigation breadcrumbs

## Security & Privacy

- This skill is designed for authorized cybersecurity work only.
- It does not require network access by itself and does not call undeclared external services.
- It should avoid copying secrets, tokens, private keys, or raw sensitive data into local notes.
- When evidence contains sensitive data, summarize the minimum needed for analysis and reporting.
- For real environments, it should preserve evidence, record assumptions, and state when authorization is missing or unclear.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `auth` — Review authentication flows, credentials, and session boundaries
- `authorization` — Reason about permissions, access control, and privilege separation
- `network` — Map traffic paths, network behavior, and trust boundaries
- `cloud` — Analyze cloud architecture, IAM exposure, and platform-level controls
- `api` — Review API surfaces, abuse cases, and contract-level security gaps

## Feedback

- If useful: `clawhub star cybersecurity`
- Stay updated: `clawhub sync`
