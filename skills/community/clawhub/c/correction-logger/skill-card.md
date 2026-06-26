## Description: <br>
Records and manages user corrections, agent mistakes, and improvement suggestions with priority ranking, effectiveness feedback, and full-text search while preserving compatibility with the existing correction log format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whoisme007](https://clawhub.ai/user/whoisme007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to persist correction memories, review recent corrections, search prior fixes, and check planned actions against high-priority correction history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved corrections may contain sensitive prompts, credentials, or private user data because the skill writes persistent local correction memory. <br>
Mitigation: Avoid logging secrets or confidential data, and periodically review or delete corrections.md, corrections_enhanced.db, and archived correction files. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/whoisme007/correction-logger) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation with Python examples, shell commands, YAML configuration, and local correction records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates persistent local correction memory in Markdown and SQLite files under ~/self-improving by default.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
