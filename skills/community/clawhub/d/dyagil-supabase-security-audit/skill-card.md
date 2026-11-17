## Description:

Audits Supabase and Vercel projects for RLS coverage, privilege escalation, cross-customer data leaks, anonymous exposure, magic-link correctness, and HTTP security headers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dyagil](https://clawhub.ai/user/dyagil)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit Supabase and Vercel applications before customer exposure, after auth or RLS migrations, or when investigating security concerns. It helps identify access-control gaps and points agents to related hotfix guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires powerful Supabase secrets and database credentials.

Mitigation: Narrow when the skill runs, remove unused service-role key requirements where possible, and prefer a dedicated least-privileged audit database role.

Risk: Dependency loading and database connectivity can weaken the audit environment.

Mitigation: Use pinned project-local dependencies and enable PostgreSQL certificate verification before running against sensitive environments.

Risk: Live probes use caller identifiers supplied at runtime.

Mitigation: Validate probe identifiers as UUIDs or parameterize claim handling before running live privilege-escalation and data-isolation probes.

## Reference(s):

- [Threat Patterns](references/threat-patterns.md)
- [Audit Runner](scripts/audit.js)
- [Role Lock Hotfix SQL](scripts/hotfix-role-lock.sql)
- [ClawHub Skill Page](https://clawhub.ai/dyagil/skills/dyagil-supabase-security-audit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, SQL, and audit findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are grouped by audit area and summarized by pass, warning, and critical counts.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
