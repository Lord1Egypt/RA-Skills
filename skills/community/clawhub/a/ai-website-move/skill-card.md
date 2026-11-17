## Description:

An end-to-end website migration orchestration skill for moving an existing site to a target SaaS builder platform while preserving content, SEO elements, URL mappings, and 301 redirect continuity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hsqduron](https://clawhub.ai/user/hsqduron)

### License/Terms of Use:

MIT-0

## Use Case:

Website operators, developers, and migration teams use this skill to inventory an old site, structure its content, generate a replacement site, map old URLs to new URLs, prepare 301 redirects, and run SEO and GEO checks before go-live.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on remote third-party skills that may not be pinned or independently verified.

Mitigation: Review and verify dependency packages before installation, record the resolved dependency names, and do not proceed to migration or write operations until dependencies are confirmed.

Risk: A 1:1 migration can copy executable site code such as JavaScript into a new production site.

Mitigation: Manually review JavaScript and other executable assets before upload, upload only approved assets, and confirm no old-site resource URLs remain before go-live.

Risk: Source-site reads and content copying can be unauthorized or target the wrong domain.

Mitigation: Require source-site ownership verification before any crawl or snapshot, prefer DNS TXT verification, avoid HTTP or meta verification unless hardened, and recheck ownership before write stages.

Risk: Migration logs, inventories, and copyright freeze lists may contain operational or rights-related information.

Mitigation: Define retention and access rules for migration records before use, and keep tokens and target-site credentials out of chat transcripts and saved files.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/hsqduron/skills/ai-website-move)
- [Migration templates and checklists](references/migration-templates.md)
- [Source site ownership verification](references/source-site-ownership-verification.md)
- [YunZhi trial site signup](https://www.72e.net/autoweb/edition.aspx)
- [Website builder dependency](https://skillhub.cn/skills/org-b0bh4w8c/jian-zhan)
- [SEO check dependency](https://skillhub.cn/skills/org-b0bh4w8c/seo-skill)
- [GEO check dependency](https://skillhub.cn/skills/org-b0bh4w8c/geo-tools)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, structured checklists, migration mappings, redirect rules, configuration guidance, and implementation snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include migration inventories, site generation guidance, URL and 301 mapping tables, SEO/GEO findings, and go-live checklists.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
