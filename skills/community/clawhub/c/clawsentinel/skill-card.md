## Description:

Pure local 2026 ClawHub/OpenClaw skill scanner. Detects ClawHavoc malware, MCP backdoors, obfuscated payloads, and supply-chain attacks. 100% read-only analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chuddyrudd](https://clawhub.ai/user/chuddyrudd)

### License/Terms of Use:


## Use Case:

Developers and security reviewers use ClawSentinel to audit pasted skill markdown or explicitly provided public GitHub repositories for malicious skill patterns before installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read pasted skill text or public GitHub repository material supplied for audit.

Mitigation: Audit only content that is appropriate to share with the agent session, and review the JSON findings before acting on them.

Risk: Public GitHub fetching can occur when a user explicitly requests a repository audit.

Mitigation: Use repository-audit prompts only for intended public repositories and verify the target URL before scanning.

## Reference(s):


## Skill Output:

**Output Type(s):** [analysis, json, guidance]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only audit output; no telemetry, code execution, persistence, or hidden privilege behavior is indicated by the security evidence.]

## Skill Version(s):

2.3.5 (source: server release metadata; artifact frontmatter states 2.3.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
