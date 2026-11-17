## Description:

Manages the ARGOS crypto trading bot by monitoring operations, troubleshooting Python issues, handling users and payments, and supporting marketing and reporting workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felix1983](https://clawhub.ai/user/felix1983)

### License/Terms of Use:


## Use Case:

Operators of the ARGOS crypto trading bot use this skill to keep the bot running, manage user and premium-payment workflows, prepare marketing content, and report operational status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for operator-level control over the ARGOS machine.

Mitigation: Restrict execution to a fixed ARGOS directory and require approval before code changes, payments, public posts, or service restarts.

Risk: The skill includes credential discovery and .env sourcing patterns.

Mitigation: Remove broad /home searches and provide required secrets explicitly through least-privilege secret provisioning.

Risk: The skill describes cron and nohup background jobs for monitoring and reports.

Mitigation: Use persistence only after separate review, document each scheduled job, and make every job easy to disable.

Risk: The skill can automate Telegram reporting and social posting.

Mitigation: Confirm recipients and channels before sending messages, and require approval for public posts and payment-related actions.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Portuguese Markdown instructions with inline bash and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PT-PT operational guidance that may propose file edits, cron jobs, API calls, status reports, and administrative actions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
