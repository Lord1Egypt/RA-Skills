## Description: <br>
Guides developers through intentional migrations from legacy JavaScript, jQuery, HTML/CSS, server-rendered templates, MPA frontend code, or older framework code toward a modern frontend stack while preserving behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan, execute, and verify legacy frontend migrations to React, Vue, Next.js, Nuxt, TypeScript, or a modernized MPA while keeping behavior, visuals, accessibility, and i18n requirements intact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Migration guidance may lead an agent to make broad frontend code, dependency, build, or tooling changes in a production repository. <br>
Mitigation: Review the migration plan, dependency changes, and generated code before applying them; run the recommended tests, browser checks, build, lint, or type-check validation before release. <br>
Risk: A migration can unintentionally change behavior, visual layout, accessibility, or translated user-facing text. <br>
Mitigation: Use the skill's behavior inventory, staged migration checklist, screenshot or manual visual review, i18n checks, and key-path verification before accepting each migrated unit. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bovinphang/fec-legacy-to-modern-migration) <br>
- [migration-execution-checklist.md](references/migration-execution-checklist.md) <br>
- [migration-report-template.md](references/migration-report-template.md) <br>
- [migration-strategy-and-mapping.md](references/migration-strategy-and-mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown reports, implementation guidance, code changes, configuration updates, and verification commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce a migration plan under reports/migration-plan-YYYY-MM-DD-HHmmss.md and recommend tests, browser checks, or build validation for migrated units.] <br>

## Skill Version(s): <br>
2.7.0 (source: server release evidence, package.json, metadata.json, README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
