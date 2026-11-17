## Description:

Develop, deploy, and verify changes to a Vercel + Supabase project covering a marketing site, CRM, and customer portal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dyagil](https://clawhub.ai/user/dyagil)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project maintainers use this skill to ship code changes, apply Supabase migrations, cache-bust Vercel deployments, verify browser behavior with Playwright, and apply known fixes for CRM and portal issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent through production deployment, database, CRM, and Supabase admin workflows using broad credentials.

Mitigation: Use isolated execution, restrict secret-file access, prefer staging data, pin dependencies, and require explicit approval before production changes.

Risk: The Playwright recipes include production account-testing workflows, including temporary customer-password mutation.

Mitigation: Remove the customer-password mutation recipe before use and avoid admin-surface probes unless necessary with sensitive values scrubbed from logs.

Risk: Supabase migrations and RLS policy changes can weaken access controls if applied incorrectly.

Mitigation: Review migrations before execution, include role resets, lock sensitive profile fields in UPDATE policies, and run a focused security audit after RLS or auth changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dyagil/skills/dyagil-oganim-deploy)
- [Migration Template](artifact/references/migration-template.sql)
- [Playwright Recipes for Oganim Verification](artifact/references/playwright-recipes.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline bash, JavaScript, SQL, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose deployment, migration, cache-busting, and verification steps that require human approval before production use.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
