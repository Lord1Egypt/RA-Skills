## Description: <br>
Create and manage reusable filter rules for email, news, search results, and structured task streams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ProjectSnowWork](https://clawhub.ai/user/ProjectSnowWork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create reusable allowlist, blocklist, and priority-based filter rules for repeated email, news, search, task stream, and JSON-like data workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Filter criteria are saved locally and may include sensitive personal terms if the user enters them. <br>
Mitigation: Avoid putting secrets or highly sensitive personal terms into criteria, and periodically review or delete the local rules file. <br>
Risk: Saved rules can become outdated and continue shaping future filtering workflows. <br>
Mitigation: Review stored rules before reuse and remove rules that no longer match current workflow needs. <br>


## Reference(s): <br>
- [ClawHub Filter Skill](https://clawhub.ai/ProjectSnowWork/filter) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration] <br>
**Output Format:** [Text summaries and local JSON rule files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates ~/.openclaw/workspace/memory/filter/rules.json when the bundled script is run.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
