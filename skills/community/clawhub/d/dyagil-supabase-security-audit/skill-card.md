## Description: <br>
Audits Supabase and Vercel projects for RLS coverage, privilege escalation, cross-customer data leaks, anonymous exposure, magic-link flow correctness, and HTTP security headers, then points agents to hotfix templates for confirmed issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dyagil](https://clawhub.ai/user/dyagil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit Supabase-backed applications before exposing customer-facing surfaces, after auth or RLS migrations, and when investigating security concerns. It helps interpret findings and select documented SQL hotfixes for common access-control failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses powerful database credentials and live database probes. <br>
Mitigation: Run it first in staging or with temporary least-privilege credentials, and explicitly approve credential access and live probes before use. <br>
Risk: The audit depends on the pg package and database transport settings. <br>
Mitigation: Pin and verify the pg dependency and enable proper TLS verification before production use. <br>
Risk: The hotfix SQL changes database access-control behavior. <br>
Mitigation: Treat the hotfix as a manual migration that receives normal code review, environment testing, and rollback planning. <br>


## Reference(s): <br>
- [Threat patterns](references/threat-patterns.md) <br>
- [Audit runner](scripts/audit.js) <br>
- [Role-lock hotfix SQL](scripts/hotfix-role-lock.sql) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, audit findings, and SQL hotfix templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require Supabase credentials, a reachable pg dependency, live database probes, and manual review before applying migration SQL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
