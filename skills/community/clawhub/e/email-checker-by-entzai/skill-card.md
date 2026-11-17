## Description:

Automated email assistant for Apple Mail that checks unread inbox messages, scores priority, drafts replies with an optional LLM, and sends scheduled email reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[entzclaw](https://clawhub.ai/user/entzclaw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers on macOS use this skill to monitor a Mail.app inbox, prioritize unread messages, receive digest reports, and prepare replies for review through OpenClaw or direct scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads Mail.app inbox content and may send email content to a configured LLM or report destination.

Mitigation: Use a dedicated bot mailbox when possible, prefer local-only LLM mode for sensitive mail, and review destination and LLM settings before enabling scheduled runs.

Risk: Scheduled execution can mark unread messages as read and change mailbox state without active supervision.

Mitigation: Run manually first, inspect generated reports and logs, and enable cron only after confirming the selected account and behavior.

Risk: Generated replies may be incomplete, incorrect, or inappropriate for the thread context.

Mitigation: Treat drafts as review material and manually approve every reply before sending.

Risk: AppleScript automation and Mail.app permissions broaden local access to mailbox data.

Mitigation: Grant only the permissions needed for Mail automation and avoid Full Disk Access unless reviewed and required for the deployment.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/entzclaw/skills/email-checker-by-entzai)
- [Publisher Profile](https://clawhub.ai/user/entzclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and generated email report text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, Python 3, osascript, Mail.app, and optional OpenAI-compatible LLM configuration.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
