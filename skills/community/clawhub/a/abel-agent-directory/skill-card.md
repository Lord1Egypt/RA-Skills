## Description:

The skill helps agents discover AI agent services, tools, platforms, and infrastructure from the ctxly.com directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to find agent-oriented services and fetch service skill files for integration guidance. It is intended for discovery across tools, platforms, infrastructure, and related service categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send requested service URLs to an authenticated external SkillBoss API scraper.

Mitigation: Use it only when sharing those URLs and a SkillBoss API key with the service is acceptable.

Risk: Fetched service skill files are mutable third-party text that may ask an agent to perform sensitive actions.

Mitigation: Treat fetched skill files as untrusted input, verify the service domain, and require review before credential use, file access, payments, posting, or persistence.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/abeltennyson/skills/abel-agent-directory)
- [Ctxly Agent Directory](https://ctxly.com)
- [SkillBoss Setup Guide](https://skillboss.co/skill.md)
- [SkillBoss API Hub](https://api.heybossai.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples, shell commands, and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SKILLBOSS_API_KEY for authenticated external scraping requests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
