## Description: <br>
Audits Claude skills from GitHub repositories for effectiveness, token usage, safety, and best-practice compliance, then automatically generates bilingual social media posts about the findings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangran](https://clawhub.ai/user/yangran) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill reviewers use this skill to audit Claude skill repositories, assess quality and safety, and generate structured audit reports with follow-up social media post drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes cloned repository contents and generated audit folders may retain source snapshots or logs. <br>
Mitigation: Use the skill only in a controlled workspace, audit public or intentionally shared repositories, and delete generated audit folders when retained content is not needed. <br>
Risk: The workflow runs an unbundled sibling post-generator script. <br>
Mitigation: Inspect the ../post-generator directory before running Step 7 and confirm it is trusted in the active workspace. <br>
Risk: The security verdict is suspicious despite a legitimate audit purpose. <br>
Mitigation: Review the skill before installing and keep execution scoped to repositories and folders intended for audit. <br>


## Reference(s): <br>
- [Audit Criteria](references/audit-criteria.md) <br>
- [Skill Best Practices Checklist](references/skill-best-practices.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/yangran/fenz-skill-auditor) <br>
- [Publisher Profile](https://clawhub.ai/user/yangran) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON metadata, process logs, shell command output, and bilingual Markdown post drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates audit folders containing source snapshots, audit-report.md, process-log.md, metadata.json, posts-en.md, and posts-zh.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
