## Description:

A product and competitor intelligence assistant for cross-border sellers that monitors Amazon ASIN changes and tracks TikTok product trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xifengzhu](https://clawhub.ai/user/xifengzhu)

### License/Terms of Use:

MIT-0

## Use Case:

External cross-border e-commerce sellers use this skill to maintain Amazon ASIN and TikTok keyword watchlists, run scans, detect market changes, and generate daily or weekly intelligence reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill forwards a privileged OpenClaw gateway token to a configurable external API.

Mitigation: Install only after trusting the publisher and backend, and constrain INTEL_API_URL to the intended service endpoint.

Risk: The skill stores watchlists, snapshots, alerts, reports, and raw provider data locally.

Mitigation: Review local retention requirements and protect the OpenClaw state directory before use.

Risk: The skill exposes broad helper functions beyond the documented user-facing commands.

Mitigation: Review the exported API surface and restrict agent/tool access to functions required for the intended workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xifengzhu/skills/cross-border-intel)
- [README](artifact/README.md)
- [Historical architecture reference](artifact/docs/architecture.md)
- [Backend API base URL](https://api.haixia.ai)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Markdown and JSON results from slash commands, TypeScript API calls, and command-line wrappers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include watchlists, scan summaries, alerts, local report data, and configuration values.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
