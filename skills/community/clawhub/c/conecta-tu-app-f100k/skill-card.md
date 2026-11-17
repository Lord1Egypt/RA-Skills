## Description:

Guides an agent through connecting an existing app to Supabase, authentication, paid-member access control, payment workflows, an admin control center, and Vercel deployment using provided templates and Spanish step-by-step instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, small-business operators, and developers use this skill to connect an existing app to database, login, paid-access checks, billing platform workflows, admin operations, and deployment. It is intended for agent-assisted setup where the user owns the accounts and performs sensitive panel actions while the agent edits files, runs commands, and verifies each module.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can deploy to production and change paid-member access automatically.

Mitigation: Review it as a high-authority deployment and billing-access skill; use a project-scoped Vercel token, prefer preview or staging first, and require explicit confirmation before production deployment.

Risk: Service-role, webhook, billing, and deployment secrets could expose the app or paid-access data if handled incorrectly.

Mitigation: Keep service-role and billing secrets server-only, store them in environment variables, avoid chat history for secret values, and verify env files are ignored before commits.

Risk: Automated membership refreshes and webhooks can remove or grant access incorrectly if source data or billing events are wrong.

Mitigation: Back up membership tables, preview list changes, preserve manual access exceptions, use the built-in large-change guard, and verify webhooks or cron jobs against live test cases before relying on them.

Risk: The Stripe template is under-scoped for paid access decisions.

Mitigation: Add product or price allowlists before using the Stripe templates to grant production paid access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/conecta-tu-app-f100k)
- [01 · Base de datos (Supabase)](references/01-base-de-datos.md)
- [02 · Login](references/02-login.md)
- [03 · El portero](references/03-portero.md)
- [04 · Cobrar según tu país](references/04-cobros-por-pais.md)
- [05 · Centro de control](references/05-centro-de-control.md)
- [06 · Publicar](references/06-publicar.md)
- [07 · Varias apps, un portero](references/07-varias-apps-un-portero.md)
- [Prompts para copiar y pegar](references/prompts-para-copiar.md)
- [Prompts por plataforma](references/prompts-por-plataforma.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Spanish Markdown guidance with inline shell commands, code edits, configuration steps, and reusable template files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Next.js, Supabase, Vercel, webhook, cron, SQL, and admin-panel templates; asks the user to provide or enter secrets in their own accounts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
