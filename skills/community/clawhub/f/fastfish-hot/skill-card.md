## Description: <br>
Pulls trending news from api.pearktrue.cn and helps configure keyword-filtered Feishu, DingTalk, or Telegram push notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superxs777](https://clawhub.ai/user/superxs777) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and operators use this skill to fetch real-time trending topics, configure keyword-filtered news pushes, and create scheduled delivery workflows for Feishu, DingTalk, or Telegram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides installation and execution of external project scripts and dependencies. <br>
Mitigation: Review the repository and requirements before installation, pin the documented release tag, and run in a virtual environment or container without root privileges. <br>
Risk: Push delivery requires messaging credentials such as webhooks, bot tokens, chat IDs, and optional DingTalk signing secrets. <br>
Mitigation: Configure only the required channel credentials, keep secrets in environment variables or .env files, and avoid displaying or committing credential values. <br>
Risk: Scheduled push workflows can create or change recurring notification behavior. <br>
Mitigation: Keep a record of cron jobs and only create, modify, or remove scheduled jobs when the user explicitly requests that change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/superxs777/fastfish-hot) <br>
- [Publisher profile](https://clawhub.ai/user/superxs777) <br>
- [Artifact-listed fastfish-hot project repository](https://github.com/superxs777/fastfish-hot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON output from the underlying scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide use of environment variables, scheduled jobs, and messaging credentials for Feishu, DingTalk, or Telegram.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
