## Description:

Claw Apply automates job search, AI filtering, and job application submission for LinkedIn and Wellfound.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mattjackson](https://clawhub.ai/user/mattjackson)

### License/Terms of Use:

AGPL-3.0-or-later

## Use Case:

Developers and job seekers use this skill to configure an agent that searches LinkedIn and Wellfound, scores matching roles, submits supported applications, and collects answers for unknown application questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit real job applications using authenticated LinkedIn and Wellfound sessions.

Mitigation: Start in preview mode, set a low max_applications_per_run, and keep application crons disabled until reviewed and tested.

Risk: Candidate profile data, application questions, and suggested answers may be sent to Anthropic and Telegram.

Mitigation: Use only the data needed for applications, review provider exposure before enabling optional AI and Telegram features, and disable integrations that are not required.

Risk: Reusable answers, logs, local configuration, and credentials can contain sensitive candidate or account data.

Mitigation: Protect .env, config files, answers.json, and data logs as sensitive files; review answers.json regularly and do not commit private runtime data.

Risk: Aggressive automation can affect platform accounts or application quality.

Mitigation: Respect documented pacing, keep max_applications_per_run low, and review queued jobs and generated answers before unattended operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mattjackson/skills/claw-apply)
- [Kernel](https://kernel.sh)
- [OpenClaw](https://openclaw.dev)
- [Telegram BotFather](https://t.me/BotFather)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can trigger browser automation, network calls, Telegram messages, local state updates, and job application submissions when the user runs the provided scripts.]

## Skill Version(s):

0.1.5 (source: server release metadata, claw.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
