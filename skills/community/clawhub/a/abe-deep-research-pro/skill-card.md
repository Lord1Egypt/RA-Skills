## Description:

Multi-source deep research agent. Searches the web via SkillBoss API Hub, synthesizes findings, and delivers cited reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan multi-source web research, read selected sources, and produce cited reports with summaries, takeaways, sources, and methodology.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install and CLI documentation points users toward unaudited external code from an inconsistent source.

Mitigation: Verify the authoritative repository and inspect the advertised scripts/research CLI before running it.

Risk: Research queries, URLs, and fetched content are sent to SkillBoss API Hub.

Mitigation: Avoid sending secrets, internal URLs, or sensitive investigations unless SkillBoss API Hub is approved for that data.

Risk: The skill requires SKILLBOSS_API_KEY for search and scraping.

Mitigation: Provide the API key through a managed environment variable or secret store and keep it out of prompts, logs, and generated reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marjoriebroad/skills/abe-deep-research-pro)
- [Publisher profile](https://clawhub.ai/user/marjoriebroad)
- [OpenClaw project](https://github.com/openclaw/openclaw)
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1/pilot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with citations, optional JSON output, and inline shell or Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports may be saved to disk and should include source links, methodology, and confidence notes.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
