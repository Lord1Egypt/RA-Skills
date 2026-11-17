## Description:

Generates CEFR-adapted English reading materials from current RSS news and returns a Feishu cloud document link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chegangan](https://clawhub.ai/user/chegangan)

### License/Terms of Use:

MIT

## Use Case:

External users and language learners use this skill to generate English reading practice from selected global news, business, technology, science, and culture RSS sources. The skill rewrites articles to a configured CEFR level, adds vocabulary explanations, preserves source links, and creates a Feishu cloud document for reading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation uses unpinned network packages and documentation suggests sudo as a fallback.

Mitigation: Review install commands before use, avoid sudo, and install dependencies in a sandbox or virtual environment with pinned versions where possible.

Risk: The skill depends on third-party RSS feeds and cloud document permissions.

Mitigation: Review RSS source URLs before execution and confirm that Feishu permissions and cloud storage of article titles, source URLs, and generated materials are acceptable.

Risk: Generated reading materials rewrite third-party news content and may be unsuitable for redistribution without review.

Mitigation: Keep source attribution and original URLs, and review publisher terms before distributing generated materials beyond personal learning use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chegangan/skills/daily-englishnews-reader)
- [ClawHub publisher profile](https://clawhub.ai/user/chegangan)
- [Feishu OpenClaw plugin documentation](https://bytedance.larkoffice.com/docx/MFK7dDFLFoVlOGxWCv5cTXKmnMh)
- [Default RSS source configuration](artifact/config/rss_sources.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown-style reading materials and a Feishu cloud document link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates four rewritten articles per run with CEFR difficulty, target word count, vocabulary explanations, source attribution, and duplicate tracking.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
