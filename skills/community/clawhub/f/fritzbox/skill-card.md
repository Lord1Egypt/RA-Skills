## Description:

Control AVM FRITZ!Box routers and FRITZ!DECT smarthome devices via TR-064 and Web API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[first-it-consulting](https://clawhub.ai/user/first-it-consulting)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect and manage AVM FRITZ!Box routers, WLAN state, connected devices, internet reconnects, and paired FRITZ!DECT smarthome devices from an agent-assisted command workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses credentials that can control router and smarthome functions.

Mitigation: Use a dedicated least-privilege FRITZ!Box account, protect any .env file, and avoid passing passwords on the command line.

Risk: WLAN, reconnect, and smarthome switch commands can disrupt network access or physical devices.

Mitigation: Require explicit user confirmation before running disruptive WLAN, reconnect, or smarthome actions.

Risk: Credentials could be exposed if the configured host or local credential storage is mishandled.

Mitigation: Verify FRITZBOX_HOST points to the user's own local router and restrict access to local credential files.

## Reference(s):

- [FRITZ!Box skill page](https://clawhub.ai/first-it-consulting/skills/fritzbox)
- [Publisher profile](https://clawhub.ai/user/first-it-consulting)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and textual command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute router and smarthome actions that require explicit user confirmation for disruptive changes.]

## Skill Version(s):

1.0.5 (source: server release metadata and artifact _meta.json; changelog released 2026-05-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
