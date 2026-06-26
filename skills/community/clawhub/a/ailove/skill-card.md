## Description: <br>
AI dating assistant. Check matching progress, relay deep questions, report results for your human. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thesamething](https://clawhub.ai/user/thesamething) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to let an agent check AILove matching status, relay pending deep questions, submit the user's verbatim answers, and summarize match results or dating updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for persistent credential storage for an AILove agent key. <br>
Mitigation: Prefer a platform secret store or manually managed environment variable, use a dedicated revocable API key, and rotate the key if exposure is suspected. <br>
Risk: Scheduled jobs may repeatedly deliver sensitive dating updates to configured channels. <br>
Mitigation: Choose private delivery targets, review cron jobs before enabling them, and confirm how to disable scheduled jobs. <br>
Risk: The security verdict is suspicious because the workflow involves credentials and sensitive dating updates. <br>
Mitigation: Install only if repeated AILove access and scheduled delivery are intended, and review the skill behavior before deployment. <br>


## Reference(s): <br>
- [AILove homepage](https://heerweiyi.cc) <br>
- [AILove API base](https://heerweiyi.cc/api/v1) <br>
- [ClawHub skill listing](https://clawhub.ai/thesamething/ailove) <br>
- [Publisher profile](https://clawhub.ai/user/thesamething) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce scheduled check-in instructions and short human-facing dating status summaries.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release metadata; artifact frontmatter reports 1.4.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
