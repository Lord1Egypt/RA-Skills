## Description: <br>
Develop, deploy, and verify changes to a Vercel + Supabase project covering a marketing site, CRM, and customer portal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dyagil](https://clawhub.ai/user/dyagil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to ship code changes, run Supabase migrations, handle cache busting, and verify production behavior for an Oganim-style Vercel and Supabase application. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through live production deploys, database migrations, admin login, magic-link generation, and customer account changes. <br>
Mitigation: Require explicit human approval before deploys, migrations, admin login, magic-link generation, or account changes; prefer staging and dedicated test users. <br>
Risk: The skill depends on sensitive Vercel and Supabase credentials, including service-role keys and admin passwords. <br>
Mitigation: Keep secrets out of logs and reports, avoid printing credential values, and use least-privilege or temporary credentials where possible. <br>
Risk: Testing workflows may alter real customer authentication state or passwords. <br>
Mitigation: Avoid changing real customer passwords; use dedicated test accounts and reset any temporary credentials immediately after verification. <br>


## Reference(s): <br>
- [Migration Template](references/migration-template.sql) <br>
- [Playwright Recipes for Oganim Verification](references/playwright-recipes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash, SQL, JavaScript, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose production deploy, database migration, and Playwright verification steps that require human review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
