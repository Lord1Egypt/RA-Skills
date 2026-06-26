## Description: <br>
Use when you need end-to-end GA4 + GTM tracking delivery across discovery, schema, sync, and verification phases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jtrackingai](https://clawhub.ai/user/jtrackingai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and marketing-technology engineers use this skill to coordinate GA4 and GTM tracking work across site discovery, page grouping, event schema design, GTM sync, preview verification, and publish handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes users to external analytics-tracking tooling that uses Google OAuth and can change or publish GTM containers. <br>
Mitigation: Install only if the external tooling is trusted, use a limited Google/GTM account, verify requested OAuth scopes, and require explicit account, container, workspace, and publish confirmation. <br>
Risk: OAuth token caches and workflow artifacts may contain sensitive GTM context, credentials, URLs, referrers, or tracking-plan details. <br>
Mitigation: Keep artifact directories private, strip sensitive URL or referrer data before collection where possible, and delete or revoke credentials.json when the workflow is finished. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/jtrackingai/analytics-tracking-automation) <br>
- [Skill Map Reference](references/skill-map.md) <br>
- [Architecture Reference](references/architecture.md) <br>
- [Output Contract](references/output-contract.md) <br>
- [Crawl Guide](references/crawl-guide.md) <br>
- [Event Schema Generation Guide](references/event-schema-guide.md) <br>
- [GA4 Event Guidelines](references/ga4-event-guidelines.md) <br>
- [GTM Troubleshooting](references/gtm-troubleshooting.md) <br>
- [Shopify Workflow](references/shopify-workflow.md) <br>
- [Preview Report Guide](references/preview-report.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON or JavaScript configuration artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Coordinates workflow artifacts such as site analysis, event schemas, GTM configuration, preview reports, tracking health reports, and Shopify custom pixel files.] <br>

## Skill Version(s): <br>
1.0.12 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
