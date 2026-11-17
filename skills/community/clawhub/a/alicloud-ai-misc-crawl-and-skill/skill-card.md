## Description:

Refreshes an Alibaba Cloud Model Studio model crawl and builds derived model summaries and coverage guidance for related AI skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to refresh Alibaba Cloud Model Studio model listings, produce structured summaries, and inspect coverage for related AI skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks agents to run an unpinned third-party npx crawler package.

Mitigation: Pin and review the crawler package version, and run it in a workspace without secrets or broad filesystem access.

Risk: The release security summary says the skill overstates its skill-regeneration behavior because the included script currently produces a coverage report.

Mitigation: Treat generated coverage as review guidance and verify any skill changes manually before relying on them.

## Reference(s):

- [Alibaba Cloud Model Studio Models](https://help.aliyun.com/zh/model-studio/models)
- [Source List](references/sources.md)
- [ClawHub Skill Page](https://clawhub.ai/cinience/skills/alicloud-ai-misc-crawl-and-skill)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands; generated artifacts include Markdown and JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, Node.js, and network access when running the crawler workflow.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
