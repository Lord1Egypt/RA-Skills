## Description:

1panel-skills lets agent runtimes inspect a 1Panel instance through authenticated module-grouped API calls for monitoring, websites, apps, containers, logs, cronjobs, task-center records, nodes, and reserved future management actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1panel](https://clawhub.ai/user/1panel)

### License/Terms of Use:

GNU General Public License v3.0

## Use Case:

Developers, operators, and agent-runtime users use this skill to query 1Panel resource status, websites, applications, containers, logs, cronjobs, task-center records, and node information through a signed CLI/API workflow. Reserved mutation endpoint definitions can guide future managed write flows, but current documented use focuses on inspection and status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes broad authenticated 1Panel management access beyond a narrow read-only surface.

Mitigation: Install it only for agents that should have trusted operator access, use a dedicated least-privilege API key, and restrict the 1Panel API allowlist to known runtime IPs or a VPN.

Risk: Logs, configuration reads, certificate data, raw request/sign output, and signed headers can contain sensitive operational information.

Mitigation: Treat command output as sensitive, redact secrets before sharing, and avoid storing real API keys or signed header output in prompts, logs, or version control.

Risk: Disabling TLS verification can expose authenticated requests to interception.

Mitigation: Use HTTPS with certificate validation and avoid setting ONEPANEL_SKIP_TLS_VERIFY except in controlled test environments.

## Reference(s):

- [Module Groups](references/module-groups.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON CLI/API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured 1Panel base URL and API key; CLI calls may return sensitive logs, configuration, certificate, and signed header data.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
