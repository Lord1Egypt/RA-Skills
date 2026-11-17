## Description:

LLM-driven e-commerce customer service email automation for classification, sentiment detection, multilingual replies, escalation, and dashboard monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External customer support teams and e-commerce operators use this skill to triage inbound support email, classify customer intent and sentiment, generate multilingual replies, and escalate high-risk messages for human handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic SMTP replies can send customer-facing messages before the workflow is reviewed.

Mitigation: Start with demo mode or test mailboxes and require human approval for outgoing replies until classification, templates, and escalation behavior are reviewed.

Risk: The dashboard and ticket APIs can expose stored customer ticket data if reachable without authentication.

Mitigation: Bind the dashboard to localhost, add authentication before any network exposure, and avoid exposing ticket APIs publicly.

Risk: Customer email content may be sent to LLM and webhook services.

Mitigation: Redact customer data before LLM or webhook use and configure only approved providers and endpoints.

Risk: Dependencies are specified as version ranges rather than exact pinned versions.

Mitigation: Pin or verify dependencies and scan the environment before production deployment.

## Reference(s):

- [AI Email Agent ClawHub listing](https://clawhub.ai/bettermen/skills/ai-email-agent)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration steps, generated email reply text, and JSON status or statistics output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 plus LLM, IMAP, and SMTP credentials; dashboard output depends on local ticket data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
