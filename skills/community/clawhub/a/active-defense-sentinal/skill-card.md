## Description: <br>
Defensive triage skill for OpenClaw, Hermes Agent, host integrity, and OpenClaw skill-supply-chain scanning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason-allen-oneal](https://clawhub.ai/user/jason-allen-oneal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to triage prompt-injection risk, session drift, host anomalies, and OpenClaw skill-supply-chain issues before taking side-effecting actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive host, browser-session, process, listener, username, or debugger details in transcripts when health-check helpers are invoked. <br>
Mitigation: Run host and browser health checks only in trusted workspaces, review outputs before sharing, and avoid invoking these checks in shared transcripts unless disclosure is acceptable. <br>
Risk: The helper workflows can modify installed OpenClaw skill directories when scan, install, or quarantine commands are explicitly run. <br>
Mitigation: Keep default use read-only, require user approval before side-effecting commands, and limit quarantine to already-installed skills inside the active OpenClaw skill tree. <br>
Risk: High or Critical scanner findings may indicate unsafe skill behavior or supply-chain risk. <br>
Mitigation: Block High or Critical staged candidates by default, preserve scan reports, and use manual review when reports are unreadable or inconclusive. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jason-allen-oneal/active-defense-sentinal) <br>
- [Allowed and Blocked Actions](references/allowed-blocked-actions.md) <br>
- [Evidence Template](references/evidence-template.md) <br>
- [Hermes Adapter](references/hermes-adapter.md) <br>
- [Host Guard Adapter](references/host-guard-adapter.md) <br>
- [OpenClaw Adapter](references/openclaw-adapter.md) <br>
- [Quarantine Policy](references/quarantine-policy.md) <br>
- [Risk Matrix](references/risk-matrix.md) <br>
- [Scan Workflow](references/scan-workflow.md) <br>
- [Skill Scanner Adapter](references/skill-scanner-adapter.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured triage sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Separates verified facts, suspected issues, unknowns, recommended next steps, and actions deferred pending approval.] <br>

## Skill Version(s): <br>
0.4.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
