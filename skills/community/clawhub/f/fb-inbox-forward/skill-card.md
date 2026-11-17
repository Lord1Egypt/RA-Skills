## Description:

FB Inbox Forward helps an agent configure and optionally run a PowerShell listener that polls Facebook Page inbox messages and forwards inbound sender names, message text, and conversation IDs to a configured OpenClaw destination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seph1709](https://clawhub.ai/user/seph1709)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to forward Facebook Page inbox activity into a selected OpenClaw channel while keeping the listener opt-in and destination-configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a Facebook Page token and forwards full inbound message text to a configured OpenClaw destination.

Mitigation: Install only for trusted pages and destinations, confirm the forwarding target before starting the listener, and protect the credential and config files with restrictive permissions.

Risk: The security evidence reports insecure token and runtime handling in a persistent listener.

Mitigation: Review or patch token transmission, error logging, worker-script integrity, and message-delivery bounds before running the listener.

Risk: The listener polls continuously once explicitly started.

Mitigation: Start it only on user request, monitor its status and logs, and stop the process when forwarding is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seph1709/skills/fb-inbox-forward)
- [Publisher profile](https://clawhub.ai/user/seph1709)
- [Facebook Graph API endpoint](https://graph.facebook.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with PowerShell code blocks and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces opt-in listener setup, status, stop, logging, credential-test, and error-handling guidance.]

## Skill Version(s):

1.0.10 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
