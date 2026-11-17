## Description:

Install, run, maintain, and troubleshoot a bundled local single-user AKShare financial data workbench, including project setup, FastAPI and React service control, cache management, YAML indicator catalog maintenance, and request-limit guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianyedavid](https://clawhub.ai/user/tianyedavid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to create and operate a local AKShare workbench, manage its local services and cache, maintain the indicator catalog, and troubleshoot conservative public-data request pacing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local AI assistant can store model-provider configuration and may send entered credentials to the configured endpoint.

Mitigation: Use HTTPS or a trusted local model endpoint, avoid high-value API keys, and rotate or delete keys saved in ai_config.json when finished.

Risk: Exposing the workbench services beyond localhost can increase access and data-leakage risk.

Mitigation: Keep the backend and frontend bound to localhost unless a reviewer has approved a hardened deployment.

Risk: Local caches may contain financial query results or sensitive workflow data.

Mitigation: Keep cache directories private and clear cached results when they are no longer needed.

Risk: The release has frontend development dependency risk noted by the security scan.

Mitigation: Update flagged frontend development dependencies before routine use on sensitive machines.

Risk: Public financial data providers can rate-limit, disconnect, or restrict bulk access.

Mitigation: Use the skill's slow pacing and cache defaults, avoid repeated forced refreshes, and use official or licensed data feeds for production, commercial, high-frequency, or bulk usage.

Risk: Financial data returned by the workbench may be inaccurate, delayed, incomplete, or unsuitable for decisions.

Mitigation: Verify important financial data with official or licensed sources and do not treat skill output as financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianyedavid/skills/akshare-local-workbench)
- [Project homepage](https://github.com/TianYeDavid/akshare-local-workbench)
- [Maintenance guide](references/maintenance.md)
- [Bundled workbench README](assets/akshare-workbench/README.md)
- [Bundled workbench disclaimer](assets/akshare-workbench/DISCLAIMER.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide local project file creation, service control, cache cleanup, tests, and environment variable settings.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
