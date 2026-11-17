## Description:

Generates platform-agnostic AKA framework content plans, markdown pages, internal linking maps, SEO metadata, and optional WordPress deployment guidance for authority sites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lebtiga](https://clawhub.ai/user/lebtiga)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, developers, and site operators use this skill to plan and generate AKA content hubs, internal-linking maps, SEO metadata, and optional WordPress deployment assets for authority sites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run unpinned external code.

Mitigation: Pin and verify npm packages before running them, and review commands before execution.

Risk: The optional WordPress deployment path can publish or modify many pages.

Mitigation: Use dry-run or report-only modes first, deploy to staging before production, keep backups, and use a dedicated low-privilege WordPress account.

Risk: Generated content may include inaccurate, misleading, or non-compliant claims.

Mitigation: Manually review generated content, ratings, claims, and regulated-industry material before publication.

Risk: WordPress application passwords can expose publishing access if retained or over-scoped.

Mitigation: Use a dedicated Editor-role account and revoke the application password after deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lebtiga/skills/aka-seo-wireframe)
- [AKA SEO Wireframe overview](https://rabihrizk.com/aka-seo-wireframe)
- [AKA Strategy Planner](references/strategy-planner.md)
- [AKA Content Generator](references/content-generator.md)
- [AKA Internal Linker](references/internal-linker.md)
- [AKA WordPress Deployer](references/wordpress-deployer.md)
- [AKA SEO Optimizer](references/seo-optimizer.md)
- [Master Prompts Collection](references/prompts-library.md)
- [AKA Framework WordPress Theme README](assets/aka-framework-theme/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON files with optional shell commands and WordPress deployment guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces strategy JSON, generated content markdown, link maps, SEO reports, and optional WordPress deployment assets; generated content requires review before publication.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
