## Description:

Fixes browser automation failures. Snapshot-first workflow + API discovery behind any website UI. Use when: 'browser not working', 'can't click', 'flaky UI', 'DOM not exposed', 'scrape website', 'browser keeps failing', 'automate this website', 'web scraping', 'element not found'.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whooshinglander](https://clawhub.ai/user/whooshinglander)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to troubleshoot browser automation failures, inspect pages before acting, and find underlying API endpoints when UI automation is brittle.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated API-discovery workflows can expose browser session cookies or tokens if live credentials are copied into shell commands.

Mitigation: Prefer unauthenticated or least-privilege requests, confirm the destination origin, and avoid copying live cookies or tokens into shell commands.

Risk: Direct API calls can bypass visible UI safeguards and perform authenticated or state-changing actions.

Mitigation: Require explicit user approval before any authenticated, state-changing, purchase, payment, or irreversible request.

## Reference(s):

- [API Discovery Procedure](references/api-discovery.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes browser workflow guidance, API discovery steps, and safeguards for browser sessions.]

## Skill Version(s):

1.0.2 (source: server release metadata, released 2026-03-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
