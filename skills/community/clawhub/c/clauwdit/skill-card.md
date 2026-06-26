## Description: <br>
Security auditor for AI agent skills. Scans SKILL.md files for prompt injection, data exfiltration, obfuscation, and dangerous capability combinations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[4worlds4w-svg](https://clawhub.ai/user/4worlds4w-svg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use this skill to audit OpenClaw SKILL.md content before installation. It helps identify prompt injection, data exfiltration, obfuscation, dangerous command patterns, credential harvesting, compound threats, and permission mismatches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted skill text is sent to an external hosted scanner service. <br>
Mitigation: Use it for public or non-sensitive audits, and avoid submitting private SKILL.md files, internal URLs, credentials, or proprietary prompts unless the hosted service and its data handling are trusted. <br>
Risk: The scanner score may be treated as a final security decision. <br>
Mitigation: Use the score and findings as one review input alongside manual review and other security checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/4worlds4w-svg/clauwdit) <br>
- [ClawAudit hosted audit endpoint](https://clauwdit.4worlds.dev/audit) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with bash and JSON examples; hosted scanner responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scanner responses include trust score, tier, findings, capabilities, compoundThreats, and permissionIntegrity fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
