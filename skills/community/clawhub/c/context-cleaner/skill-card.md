## Description: <br>
Optimizes OpenClaw agent context Markdown files to reduce token usage with backups, previews, and rollback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdotwinter](https://clawhub.ai/user/sdotwinter) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to compact OpenClaw agent workspace Markdown files while preserving workflows, IDs, and safety boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite persistent agent instruction files, which may alter agent behavior or remove important context. <br>
Mitigation: Use it only with an explicit named target, require a current backup, review the exact proposed files and diff before rewrite, and verify that IDs, workflows, and safety rules are preserved. <br>
Risk: All-agent or main-workspace cleanup has broad impact and can affect core behavior. <br>
Mitigation: Avoid broad scopes unless necessary; require explicit confirmation for main workspace changes and keep rollback instructions available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdotwinter/context-cleaner) <br>
- [Source skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and summary tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces file rewrite guidance, backup and rollback commands, optimized Markdown templates, and before/after summaries.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
