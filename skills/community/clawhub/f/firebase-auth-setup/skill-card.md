## Description:

Configures Firebase Authentication providers, security rules, custom claims, and React auth hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guifav](https://clawhub.ai/user/guifav)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add Firebase Authentication to Next.js App Router projects, including client auth hooks, provider UI, server-side token verification, custom claims, and optional Supabase profile sync.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill configures Firebase login and Supabase profile sync with service-role database access, which can expose identity data if implemented too broadly.

Mitigation: Require explicit sync opt-in, keep FIREBASE_PRIVATE_KEY and SUPABASE_SERVICE_ROLE_KEY server-only, and limit writes to the minimum profile fields needed.

Risk: Auth middleware, token verification, or sync route changes could lock out users or break Firebase-to-Supabase profile mapping.

Mitigation: Plan file changes before editing, verify tokens on the server for protected routes, compile after each change, and test the auth flow end to end when possible.

Risk: The sync endpoint can be abused or leak implementation details if it lacks request controls.

Mitigation: Add rate limiting, use generic error responses, and verify Firebase ID tokens before any Supabase write.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guifav/skills/firebase-auth-setup)
- [CHANGELOG.md](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Shell commands, Guidance]

**Output Format:** [Markdown with TypeScript code blocks and setup steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify Next.js, Firebase, Supabase, middleware, hook, provider, and environment example files.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
