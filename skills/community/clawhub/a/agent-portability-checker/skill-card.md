## Description: <br>
Audit agent skills for platform lock-in and cross-agent compatibility, including hardcoded platform paths, missing environment-variable support, and platform-specific dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[99rebels](https://clawhub.ai/user/99rebels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit agent skill directories for cross-agent portability issues and to apply supported fixes before distribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fix mode performs direct text replacements in the selected skill directory and does not create backups. <br>
Mitigation: Run audit mode first, use --fix only on skill directories intended for modification, and review the resulting diff before relying on the changes. <br>


## Reference(s): <br>
- [Portability Checklist](references/checklist.md) <br>
- [Channel Formatting](references/formatting.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/99rebels/agent-portability-checker) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Code] <br>
**Output Format:** [Markdown or terminal text for audit summaries, JSON for structured audit output, and code/text edits when fix mode is explicitly used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fix mode performs direct text replacements and should be reviewed with a diff after execution.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence and script VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
