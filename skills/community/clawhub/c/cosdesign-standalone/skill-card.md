## Description:

CosDesign Standalone helps agents analyze public web pages and produce design-system specifications for colors, typography, spacing, layout, components, and exports such as design tokens, CSS variables, Tailwind configuration, or HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cosmofang](https://clawhub.ai/user/cosmofang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and agents use this skill to inspect public website URLs and generate actionable design-system analysis, comparisons, and exportable implementation specs. It is intended for public, non-sensitive web pages and does not create new UI designs or modify target sites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analyzing intranet, staging, authenticated, signed, or tokenized URLs could expose sensitive content through arbitrary fetching or third-party crawling.

Mitigation: Use only public, non-sensitive URLs unless Jina fallback is removed and URL validation plus prompt-injection guardrails are added.

Risk: Analysis history can record URLs and summaries that may be inappropriate to retain for sensitive sites.

Mitigation: Avoid sensitive URLs and clear data/analysis-history.json when retention is not desired.

## Reference(s):

- [CosDesign GitHub homepage](https://github.com/Cosmofang/cosdesign)
- [ClawHub skill page](https://clawhub.ai/cosmofang/skills/cosdesign-standalone)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text prompts with optional JSON, CSS, Tailwind configuration, and self-contained HTML report outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts run with Node.js >=18 and may use optional JINA_API_KEY for enhanced crawling.]

## Skill Version(s):

1.0.0 (source: release evidence, package.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
