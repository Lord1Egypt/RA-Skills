## Description: <br>
Automates LinkedIn and Wellfound job searches, AI-assisted filtering, application submission, and unanswered-form question handling for a configured job seeker. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MattJackson](https://clawhub.ai/user/MattJackson) <br>

### License/Terms of Use: <br>
AGPL-3.0-or-later <br>


## Use Case: <br>
External users or developers use Claw Apply to configure a Node.js job-application automation workflow that searches LinkedIn and Wellfound, filters roles with AI, and can submit applications from authenticated sessions. It is best suited for users who can review and constrain automated application behavior before enabling scheduled runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically submit real job applications using authenticated LinkedIn and Wellfound sessions. <br>
Mitigation: Start in preview mode, keep the applier cron disabled until reviewed, and set max_applications_per_run conservatively. <br>
Risk: Profile and resume-derived data may be shared with Anthropic, Telegram, Kernel, and job sites during filtering, answering, notifications, browser execution, and submission. <br>
Mitigation: Install only after reviewing the configured services, credentials, and data flows; treat local logs and answers.json as sensitive personal data. <br>
Risk: Debug and test scripts can run browser flows against real accounts or job pages. <br>
Mitigation: Avoid running debug or test scripts against real accounts unless the behavior has been reviewed and constrained. <br>


## Reference(s): <br>
- [Claw Apply ClawHub page](https://clawhub.ai/MattJackson/claw-apply) <br>
- [OpenClaw](https://openclaw.dev) <br>
- [Kernel](https://kernel.sh) <br>
- [Telegram BotFather](https://t.me/BotFather) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke browser automation, API calls, local configuration files, and scheduled jobs when the user runs the provided commands.] <br>

## Skill Version(s): <br>
0.1.5 (source: ClawHub release evidence, claw.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
