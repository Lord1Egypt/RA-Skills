## Description: <br>
Deep audit for installed ClawHub skills - usage analysis, permission review, conflict detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace maintainers use Skill Auditor to audit installed ClawHub or OpenClaw skills, review permissions and usage history, detect conflicts, score skill health, and prepare cleanup recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect local skill metadata and usage or session history during audits. <br>
Mitigation: Review which logs and directories it reads, and limit the audit time window where possible. <br>
Risk: Generated cleanup scripts could disable, archive, or remove skills if executed without review. <br>
Mitigation: Prefer dry-run output first, keep backups, and inspect any generated cleanup script before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Auditor release](https://clawhub.ai/harrylabsj/audit-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with optional shell cleanup script and HTML export.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include health scores, conflict matrix, per-skill flags, optimization suggestions, and dry-run cleanup commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
