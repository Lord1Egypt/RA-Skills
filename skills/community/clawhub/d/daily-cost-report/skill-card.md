## Description: <br>
Generate daily OpenClaw cost reports with breakdown by agent, model, and channel, including HTML-formatted email reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kjvarga](https://clawhub.ai/user/kjvarga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate daily or on-demand OpenClaw usage and cost reports for cost auditing, model analysis, and automated email delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests OPENAI_API_KEY even though the server security summary says the key requirement is unexplained. <br>
Mitigation: Remove the API key requirement unless the publisher explains it, and run the skill with only the credentials needed for OpenClaw session reporting. <br>
Risk: Detailed cost and usage reports are written to predictable /tmp paths. <br>
Mitigation: Store generated reports in a private directory with restricted permissions and delete or archive them according to local retention policy. <br>
Risk: The examples include specific email and Telegram destinations and an enabled cron pattern that could be copied unchanged. <br>
Mitigation: Replace all sample recipients and destinations, review the cron schedule, and confirm delivery settings before enabling automation. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, text] <br>
**Output Format:** [Markdown report, HTML email, and command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are date-scoped and may be saved as dated files under /tmp by the bundled scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
