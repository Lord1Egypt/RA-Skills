## Description:

fastfish-lite helps agents format WeChat public-account content, run local sensitive-word checks, preview HTML locally, and fetch or schedule daily trending-topic summaries without WeChat publishing or account authorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superxs777](https://clawhub.ai/user/superxs777)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to operate fastfish-lite for WeChat public-account drafting workflows, including article formatting, local compliance checks, HTML preview, and trending-topic retrieval or notification setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing and running fastfish-lite can introduce supply-chain risk through a third-party repository and dependencies.

Mitigation: Install only from trusted sources, review the repository and dependencies before use, pin releases when possible, and run in a virtual environment or container without root privileges.

Risk: The skill may use API keys and webhook credentials for API access and hot-topic push channels.

Mitigation: Keep credentials in environment or .env configuration, scope keys narrowly, avoid exposing secret values in agent responses, and do not commit credentials to source control.

Risk: Scheduled hot-topic push jobs can create persistent daily notifications if configured unintentionally.

Mitigation: Create or modify scheduled push jobs only after explicit user approval, and confirm the intended channel, schedule, and recipient before enabling recurring notifications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/superxs777/skills/fastfish-lite)
- [fastfish-lite GitHub repository](https://github.com/superxs777/fastfish-lite)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command snippets and JSON CLI arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.10+, a running fastfish-lite service, optional MEDIA_AGENT_API_KEY, and configured push-channel credentials for scheduled hot-topic notifications.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
