## Description:

Framer CRM API helps agents manage Framer CMS content through the Server API, including listing, creating, reading, updating, and deleting collections and items, uploading images, publishing previews, deploying to production, and managing project assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[berthelol](https://clawhub.ai/user/berthelol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to automate Framer CMS and publishing workflows from an agent session, including article creation, asset uploads, preview publishing, and production deployment with confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and mutate Framer CMS content, project structure, code overrides, and deployment state.

Mitigation: Use it only with Framer projects where agent-driven changes are acceptable, and prefer a project-scoped API key.

Risk: Destructive or live-site actions can remove data, alter pages or code, add redirects, run screenshots, or deploy to production.

Mitigation: Require explicit user confirmation before deletes, schema changes, page or code changes, screenshots, redirects, production deploys, or bulk operations.

Risk: The Framer API key can expose broad project access if committed, logged, or reused across projects.

Mitigation: Keep FRAMER_API_KEY out of source control and logs, store it in the environment or .env files ignored by git, and rotate it if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/berthelol/skills/framer-crm-api)
- [CMS Operations Reference](artifact/references/cms-operations.md)
- [Onboarding Flow](artifact/references/onboarding.md)
- [Project Assets & Configuration](artifact/references/project-assets.md)
- [Publishing & Deployment](artifact/references/publishing.md)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FRAMER_PROJECT_URL, FRAMER_API_KEY, node, npm, and the framer-api package.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
