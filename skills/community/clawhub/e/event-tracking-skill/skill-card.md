## Description:

Use when you need GA4 + GTM tracking delivery from site discovery through publish, or when the right phase entry point is still unclear.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jtrackingai](https://clawhub.ai/user/jtrackingai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketing operations teams, and analytics implementers use this skill to route GA4 and GTM tracking work from site discovery through schema design, GTM synchronization, preview validation, and publish readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can install mutable remote tooling.

Mitigation: Install only from the trusted `jtrackingai/analytics-tracking-automation` source, verify the intended version, and run the workflow in a controlled workspace.

Risk: The workflow stores a reusable GTM write credential locally.

Mitigation: Keep `credentials.json` out of shared folders and backups, and revoke or clear the OAuth token when the workflow is complete or no longer trusted.

Risk: Incorrect GTM account, container, workspace, or publish choices can affect live tracking.

Mitigation: Review every GTM target selection and publish prompt carefully; do not proceed without explicit confirmation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jtrackingai/skills/event-tracking-skill)
- [Architecture Reference](references/architecture.md)
- [Skill Map Reference](references/skill-map.md)
- [Output Contract](references/output-contract.md)
- [Crawl Guide](references/crawl-guide.md)
- [Page Grouping Guide](references/page-grouping-guide.md)
- [Event Schema Generation Guide](references/event-schema-guide.md)
- [GA4 Event Naming Guidelines](references/ga4-event-guidelines.md)
- [GTM Troubleshooting](references/gtm-troubleshooting.md)
- [Shopify Workflow](references/shopify-workflow.md)
- [Telemetry Consent Interaction](references/telemetry-consent.md)
- [Preview Validation Report Template](references/preview-report.md)
- [Google Tag Manager API](https://console.cloud.google.com/apis/library/tagmanager.googleapis.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Code, JSON]

**Output Format:** [Markdown guidance with shell commands and generated workflow artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces site-specific GA4/GTM workflow artifacts and requires explicit user approval at tracking, GTM target, telemetry consent, and publish checkpoints.]

## Skill Version(s):

1.0.14 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
