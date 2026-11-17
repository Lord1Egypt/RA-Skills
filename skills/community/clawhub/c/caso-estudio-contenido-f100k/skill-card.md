## Description:

Orchestrates a Spanish-language content case study workflow that researches real viral references, drafts scripts and hooks, builds a 30-day calendar, and renders a one-page HTML portfolio deliverable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

Spanish-speaking content creators or Fórmula 100K students use this skill to complete a final content challenge by turning a niche brief into research, scripts, hooks, a 30-day publishing calendar, and a static case-study page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may direct live Vercel deployment using a user token without enough scoping or final deployment control.

Mitigation: Use a narrowly scoped Vercel token, require the target project or domain to be named before deployment, and review the generated page before any production deploy.

Risk: Telegram delivery of the page or calendar could send materials to an unintended recipient.

Mitigation: Verify the recipient or channel before delivery and keep files inside the confirmed conversation or destination.

Risk: The workflow may use external services such as Apify or Composio when available.

Mitigation: Review the skill before installation if those services should not be used, and require explicit approval before account-connected integrations run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/caso-estudio-contenido-f100k)
- [Publisher profile](https://clawhub.ai/user/formula100k)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Spanish-language guidance plus generated JSON, CSV, XLSX when available, and static HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a required human checkpoint between research and production; viral metrics should be real or explicitly marked pending.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
