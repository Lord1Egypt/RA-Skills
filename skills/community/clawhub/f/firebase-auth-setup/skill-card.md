## Description: <br>
Configures Firebase Authentication - providers, security rules, custom claims, and React auth hooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guifav](https://clawhub.ai/user/guifav) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add Firebase Authentication to Next.js App Router projects, including client auth hooks, provider UI, server-side token verification, custom claims, and Firebase-to-Supabase profile sync. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Server-side Firebase Admin credentials and Supabase service-role keys can expose privileged access if placed in prompts, logs, or client code. <br>
Mitigation: Keep private keys and service-role keys in server-only environment variables, never include real credential values in prompts or client bundles, and review generated environment examples before committing. <br>
Risk: Auth middleware and custom-claim changes can lock out existing users or grant incorrect roles. <br>
Mitigation: Review generated middleware and claim-setting code before applying it, test sign-in and role flows in staging, and preserve a fallback administrative path during rollout. <br>
Risk: Firebase-to-Supabase profile synchronization can break user mapping or row-level security assumptions. <br>
Mitigation: Verify Firebase UID to Supabase profile mapping and RLS behavior with test accounts before production deployment. <br>


## Reference(s): <br>
- [Firebase Auth Setup on ClawHub](https://clawhub.ai/guifav/firebase-auth-setup) <br>
- [Artifact homepage](https://github.com/guifav/openclaw-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with TypeScript and TSX code blocks, setup steps, and security checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose file changes for Next.js Firebase client/admin setup, middleware, auth routes, Supabase sync, and manual Firebase Console steps.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence; artifact manifest and changelog report 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
