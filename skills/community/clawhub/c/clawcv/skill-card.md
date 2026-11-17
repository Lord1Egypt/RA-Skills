## Description:

ClawCV helps agents analyze and rewrite resumes, match resumes to job descriptions and campus recruitment roles, export one-page PDFs, and provide job-search coaching through WonderCV-backed tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[000wonderclaw](https://clawhub.ai/user/000wonderclaw)

### License/Terms of Use:

MIT-0

## Use Case:

External job seekers and agents use ClawCV to turn resume, job-description, education, city, and career-planning inputs into structured resume feedback, targeted rewrites, matching guidance, campus recommendations, PDF export links, and career coaching.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release runs the current npm clawcv package as local MCP code.

Mitigation: Pin the package version during installation and review package updates before upgrading.

Risk: Resume, job-description, education, city, and career-planning data is sent to WonderCV services.

Mitigation: Use the skill only with data the user is comfortable sending to WonderCV, and prefer explicit invocation phrases so sensitive resume data is not routed accidentally.

Risk: Setup examples can expose API keys in shell commands or local MCP configuration.

Mitigation: Store the API key in environment-backed configuration, avoid pasting it directly into shell history, and check MCP config file permissions.

## Reference(s):

- [ClawHub ClawCV skill page](https://clawhub.ai/000wonderclaw/skills/clawcv)
- [WonderCV ClawCV API key and account page](https://www.wondercv.com/clawcv)
- [WonderCV website](https://wondercv.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown responses with structured tables, prioritized recommendations, rewritten resume text, job-match summaries, campus role listings, configuration snippets, and PDF links when export succeeds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on a valid WonderCV API key, account quota, network access to WonderCV services, and consistent session handling across related tool calls.]

## Skill Version(s):

1.1.0 (source: evidence.json release.version and artifact SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
