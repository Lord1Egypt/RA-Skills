## Description: <br>
Eridian Carapace provides OpenClaw agent security hardening guidance for prompt injection defense, credential protection, data exfiltration prevention, URL allowlisting, approval flows, and security audits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iampaulpatterson-boop](https://clawhub.ai/user/iampaulpatterson-boop) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to harden OpenClaw agent configurations, add defensive AGENTS.md patterns, audit security posture, and reduce prompt injection, credential leakage, and unauthorized operation risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copied AGENTS.md security patterns may introduce incorrect or overly broad operational guidance if applied without review. <br>
Mitigation: Review each copied section before deployment and adapt it to the agent's actual tools, trust boundaries, and approval model. <br>
Risk: Attack examples and credential-related snippets may be misunderstood as live instructions if pasted into persistent agent rules without clear labels. <br>
Mitigation: Keep examples clearly labeled as examples, use redacted or presence-only checks for secrets, and avoid storing credential values in instructions. <br>


## Reference(s): <br>
- [Attack Vectors & Defenses](references/attack-vectors.md) <br>
- [Security Audit Template](references/audit-template.md) <br>
- [Security Patterns Reference](references/security-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with checklists and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes copy-ready AGENTS.md security patterns, audit checklist items, and browser allowlist configuration examples.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
