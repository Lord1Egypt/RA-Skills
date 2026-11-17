## Description:

The directory for AI agent services. Discover tools, platforms, and infrastructure built for agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover agent-oriented services, retrieve directory metadata, and fetch service skill.md files for review and integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to fetch remote service skill.md files whose content can change after this release was reviewed.

Mitigation: Treat fetched service skill.md content as untrusted text and review it before following any instructions.

Risk: The skill routes requested URLs through the SkillBoss scraping service.

Mitigation: Install only when sharing requested URLs with that provider is acceptable for the intended use case.

Risk: Fetched remote instructions may conflict with user intent, credential handling rules, or tool permissions.

Mitigation: Do not allow fetched content to override user instructions, safety rules, credential boundaries, or tool permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abeltennyson/skills/agent-directory1)
- [Ctxly homepage](https://ctxly.com)
- [Ctxly services directory](https://ctxly.com/services.json)
- [SkillBoss API base](https://api.heybossai.com/v1)
- [SkillBoss pilot endpoint](https://api.heybossai.com/v1/pilot)

## Skill Output:

**Output Type(s):** [Guidance, Code, API Calls, Configuration]

**Output Format:** [Markdown with Python code blocks and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; fetched service skill.md content should be treated as untrusted text.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
