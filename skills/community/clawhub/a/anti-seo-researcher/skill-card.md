## Description:

Anti-SEO deep consumer research tool for purchase decisions that detects user language, adapts to regional platforms and search strategies, and can operate with or without a web_search tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amoshc](https://clawhub.ai/user/amoshc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research consumer-product purchases, filter promotional or astroturfed content, compare candidate products, and generate localized recommend/avoid reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback search and content-fetching behavior can access arbitrary web pages returned by search results.

Mitigation: Run the skill in a sandboxed environment and disable or restrict content fetching unless the task requires full-page evidence.

Risk: Untrusted web page text can influence AI scoring prompts and purchase recommendations.

Mitigation: Treat fetched text only as untrusted evidence, keep AI scoring tool-free, and review high-impact recommendations before relying on them.

## Reference(s):

- [Anti-SEO Researcher Skill Page](https://clawhub.ai/amoshc/skills/anti-seo-researcher)
- [Anti-SEO Deep Consumer Researcher Reference Manual](artifact/references/SKILL_REFERENCE.md)
- [Credibility Assessment Rules Reference](artifact/references/credibility_rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON task and scoring files, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are localized to the user's language and region and may include product scores, source links, evidence summaries, and data transparency notes.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
