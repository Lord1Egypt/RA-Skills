## Description: <br>
Cross-ref helps maintainers find duplicate GitHub pull requests and missing issue-to-PR links, then report clustered findings and optional actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Glucksberg](https://clawhub.ai/user/Glucksberg) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and repository maintainers use this skill to audit active GitHub repositories for duplicate pull requests and missing issue-to-PR links before deciding whether to comment, label, or close items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk GitHub write actions can post comments, add labels, or close pull requests in repositories where the user has write access. <br>
Mitigation: Start in plan mode, review every proposed action manually, require explicit approval before execute mode, and use least-privileged GitHub credentials. <br>
Risk: Automation framed around avoiding abuse detection can be misused to disguise bulk activity or bypass platform protections. <br>
Mitigation: Use rate limiting transparently, keep comments human-reviewed, and do not use the bulk posting behavior to evade GitHub protections. <br>
Risk: Cross-reference suggestions can be wrong when evidence is ambiguous or incomplete. <br>
Mitigation: Treat manual_review_required findings as non-actionable until a maintainer verifies the full PR diff, issue body, and comments. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/Glucksberg/cross-ref) <br>
- [Decision principles](references/principles.md) <br>
- [Commenting strategy](references/commenting-strategy.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with structured JSON intermediate files and shell commands for GitHub data collection and optional comments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Starts in plan mode by default; GitHub write actions require user approval and should be rate limited.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
