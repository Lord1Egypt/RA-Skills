## Description:

AI资讯速递 helps agents search, summarize, analyze, and present current AI news, research progress, model releases, industry trends, policy updates, and funding activity, with optional charts and images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nameused](https://clawhub.ai/user/nameused)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to produce AI news briefs, weekly or monthly roundups, deep-dive analyses, and model or product comparisons in Chinese, English, or bilingual formats. It is intended for current AI news gathering, source comparison, de-duplication, and presentation with optional visual summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional chart widgets may load an unpinned Chart.js package from a CDN.

Mitigation: Prefer SVG output or a pinned and locally reviewed Chart.js version before rendering widgets in sensitive environments.

Risk: AI news changes quickly, and stale or duplicated sources can lead to misleading briefs.

Mitigation: Require current searches, source dates, de-duplication, and explicit labels for rumors or unverified reporting.

## Reference(s):

- [AI News Source List](artifact/references/ai_sources.md)
- [Model Compare Template](artifact/references/model_compare_template.md)
- [Visualization Examples](artifact/references/visualization_examples.md)
- [ClawHub Skill Page](https://clawhub.ai/nameused/skills/ai-news-generator)
- [nameused Publisher Profile](https://clawhub.ai/user/nameused)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown reports with tables, source notes, optional chart widget code, and optional image-generation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Chinese, English, or bilingual prose; chart examples may use SVG or Chart.js snippets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
