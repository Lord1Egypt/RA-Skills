## Description: <br>
ClawGuard-Auditor audits OpenClaw Skills before installation using static security checks, supply-chain checks, and intent-drift analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stardreaming](https://clawhub.ai/user/stardreaming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to inspect another Skill directory before installation or loading, with output focused on risky code patterns, dependency concerns, and mismatch between stated purpose and observed behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a heuristic local auditor and may overstate its security capabilities or approval decisions. <br>
Mitigation: Treat its findings as advisory, review the output manually, and do not rely on an APPROVED or low-risk result as the sole security decision. <br>
Risk: Running the auditor on a broad path may inspect files outside the intended skill review scope. <br>
Mitigation: Run it only against the specific skill directory you intend to inspect. <br>


## Reference(s): <br>
- [ClawGuard-Auditor on ClawHub](https://clawhub.ai/stardreaming/clawguard-auditor) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Terminal text, Markdown, or JSON audit report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return approval, conditional review, or rejection-style recommendations; users should review results manually.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
