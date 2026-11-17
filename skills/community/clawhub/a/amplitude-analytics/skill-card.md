## Description:

Analyze product events, cohorts, releases, dashboards, and experiment insights via the Amplitude Analytics API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and analytics operators use this skill to query Amplitude event analytics, cohorts, retention, funnels, releases, dashboards, and experiment insights from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a third-party ClawLink plugin that stores and injects Amplitude API credentials.

Mitigation: Verify the ClawLink plugin publisher and version before installation, use a dedicated least-privilege Amplitude credential, and revoke the credential when the integration is no longer needed.

Risk: Amplitude write and delete actions can alter analytics state, including irreversible GDPR/CCPA deletion requests, user mapping, cohort changes, releases, and annotations.

Mitigation: Keep write and delete actions opt-in, preview changes first, and require explicit user confirmation for the target resource and intended effect.

Risk: Analytics queries and cohort downloads may expose product usage data or large datasets from the connected Amplitude project.

Mitigation: Scope access to the intended project, prefer filtered or paginated queries, and avoid sharing returned data outside approved workflows.

## Reference(s):

- [Amplitude Analytics API](https://amplitude.com/docs/apis)
- [Amplitude API Reference](https://developers.amplitude.com/)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/amplitude-analytics)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown with inline shell commands and structured API call parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live Amplitude query results, tool previews, error guidance, and confirmation prompts for write or delete operations.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
