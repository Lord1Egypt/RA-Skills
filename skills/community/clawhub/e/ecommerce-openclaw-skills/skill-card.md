## Description:

E-commerce Skills provides OpenClaw workflows for ecommerce product research, market analysis, and content generation, with current Taobao/Tmall support and planned adapters for Pinduoduo, Douyin, Xiaohongshu, and 1688.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenjiahui11](https://clawhub.ai/user/chenjiahui11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, ecommerce merchants, and operators use this skill to research product categories, analyze market competition, and produce selection recommendations from ecommerce keyword queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Published install guidance uses an unpinned placeholder npx installer that could fetch unreviewed code.

Mitigation: Review the installer source before running it, replace the placeholder owner with the verified publisher, pin the package version or commit, and avoid elevated privileges.

Risk: Ecommerce research workflows may require Taobao API credentials.

Mitigation: Provide only credentials intended for this workflow and keep them in environment variables or a secret store rather than hard-coding them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenjiahui11/skills/ecommerce-openclaw-skills)
- [Publisher profile](https://clawhub.ai/user/chenjiahui11)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, Configuration]

**Output Format:** [Markdown market research report with setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require Taobao Open Platform credentials supplied through environment variables or a secret store.]

## Skill Version(s):

1.0.0 (source: server release metadata and CHANGELOG, released 2026-03-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
