## Description:

Use when you need end-to-end GA4 + GTM tracking delivery across discovery, schema, sync, and verification phases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jtrackingai](https://clawhub.ai/user/jtrackingai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketing-technology engineers use this skill to plan and route GA4 and Google Tag Manager tracking work from site discovery through schema design, GTM sync, preview QA, and publish handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks users to install and run an external command surface and to execute browser-backed steps outside sandboxed environments.

Mitigation: Use a pinned release or reviewed commit, run only after publisher review, and keep human approval gates for page groups, schemas, GTM target selection, and publishing.

Risk: GTM sync uses Google OAuth and caches credentials in the artifact directory.

Mitigation: Keep credentials.json out of shared or synced folders, clear cached tokens when finished, and revoke tokens if access is no longer needed.

Risk: Selecting the wrong GTM account, container, or workspace could modify the wrong tracking setup.

Mitigation: Require explicit confirmation for every GTM target and verify publish prompts before approving changes.

## Reference(s):

- [Skill Map Reference](references/skill-map.md)
- [Architecture Reference](references/architecture.md)
- [Output Contract](references/output-contract.md)
- [Crawl Guide](references/crawl-guide.md)
- [Page Grouping Guide](references/page-grouping-guide.md)
- [Event Schema Generation Guide](references/event-schema-guide.md)
- [GA4 Event Naming Guidelines](references/ga4-event-guidelines.md)
- [Shopify Workflow](references/shopify-workflow.md)
- [Preview Validation Report Template](references/preview-report.md)
- [GTM Troubleshooting](references/gtm-troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON tracking artifacts, GTM configuration, reports, and optional Shopify pixel code.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, npm, Playwright Chromium for browser-backed steps, and interactive Google OAuth for GTM sync.]

## Skill Version(s):

1.0.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
