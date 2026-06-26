## Description: <br>
Analyze SKILL.md files for security risks, quality issues, and best-practice violations before installing or sharing OpenClaw skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gpunter](https://clawhub.ai/user/Gpunter) <br>

### License/Terms of Use: <br>
Free to use <br>


## Use Case: <br>
Developers, engineers, and agents use this skill to audit OpenClaw SKILL.md files or URLs for security risks, quality issues, and best-practice violations before installation, comparison, or report sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trust scores may create a false sense of assurance because the skill uses heuristic static review. <br>
Mitigation: Treat audit results as advisory and combine them with human review before installing or publishing a skill. <br>
Risk: Sensitive information could be exposed if secrets are included in audit inputs or generated reports. <br>
Mitigation: Audit only selected files or URLs and remove credentials, tokens, or private data before sharing reports. <br>
Risk: Runtime-only behavior and external URL safety may not be fully detectable from SKILL.md content alone. <br>
Mitigation: Review runtime dependencies, network behavior, and external endpoints separately when a skill has executable behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Gpunter/claw1-skill-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/Gpunter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown audit report with trust score, severity counts, findings, and recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include warning IDs, comparison notes, and follow-up recommendations; trust scores are heuristic and advisory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and SKILL.md Version section) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
