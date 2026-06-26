## Description: <br>
Retrieves and summarizes COROS running data, including training dashboards, activity details, training load analysis, and training schedule summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[doaspx](https://clawhub.ai/user/doaspx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users connect a COROS account to review running history, training load, recent activity details, training schedules, and goals through an agent conversation or command-line run. The skill can also preview training schedule changes and apply them when explicitly configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store reusable COROS session data and account context that may grant access to private fitness history. <br>
Mitigation: Keep config.json private, do not commit or share cookies, tokens, p1, or p2 values, and publish only sanitized example configuration. <br>
Risk: When schedule_write.auto_apply is enabled, the skill can modify or delete COROS training schedule entries. <br>
Mitigation: Leave demo_mode enabled or schedule_write.auto_apply=false unless schedule changes are intentional, and review the generated preview and target selectors before enabling writes. <br>
Risk: The skill retrieves private COROS activity and training data through account-authenticated API calls. <br>
Mitigation: Install only when the publisher and artifact are trusted with COROS account data and private fitness history. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/doaspx/coros-skill) <br>
- [COROS web app](https://t.coros.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Analysis, Configuration, Guidance] <br>
**Output Format:** [Plain text console-style summaries with configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Primarily Chinese summaries and tables; live account mode requires COROS credentials or cookie context.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
