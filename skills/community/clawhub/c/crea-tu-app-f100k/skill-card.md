## Description:

Guides a FÓRMULA 100K student through choosing, building, branding, connecting, and publishing a personalized AI app for her business.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External FÓRMULA 100K users use this skill to create a custom AI app for their business without writing code. The agent interviews the user, recommends an app concept, captures brand direction, coordinates build and design phases, guides account key setup, and helps publish to the user's Vercel account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide deployment to a user's Vercel account.

Mitigation: Require explicit user approval immediately before any production deployment and confirm that the target Vercel account belongs to the user.

Risk: The workflow may involve service keys or secrets for AI providers, Stripe, Supabase, or Vercel.

Mitigation: Avoid sending secrets through chat, keep keys server-side only, store local test keys only in ignored environment files, and rotate any key shared during testing.

Risk: Generated apps may process sensitive personal content such as faces, photos, chats, documents, audio, or business data.

Mitigation: Add privacy safeguards appropriate to the app's data type before public release and clearly tell the user which accounts, keys, and data flows they control.

Risk: Artifact behavior contains conflicting approval guidance for production deployment.

Mitigation: Follow the stricter posture: obtain approval at the deployment checkpoint before publishing and document the final deployment URL and account ownership.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/crea-tu-app-f100k)
- [Catálogo de Apps IA](references/catalogo-apps.md)
- [Perfil de Marca](references/perfil-marca.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Conversational guidance with generated project files, Markdown handoff notes, shell commands, and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshots, a deployed app URL, environment variable names, and a fallback project archive when deployment is not available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
