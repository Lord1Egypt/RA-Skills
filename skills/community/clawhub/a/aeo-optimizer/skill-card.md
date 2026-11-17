## Description:

Optimize an article for Answer Engine Optimization (AEO) so AI engines like ChatGPT, Perplexity, and Claude can extract, quote, and cite it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, marketers, and content teams use this skill to turn draft or published articles into AEO-ready Markdown with question headings, 50-80 word answer capsules, paragraph-length cleanup, and an audit of trust signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask an agent to fetch an article URL, which can expose private, authenticated, localhost, internal network, or otherwise sensitive pages.

Mitigation: Prefer pasted article text for confidential content, and only provide URLs the user is comfortable having the agent fetch.

Risk: AEO rewrites and audit scores can change editorial structure or introduce optimization guidance that may be inaccurate for the source article.

Mitigation: Review the rewritten article, answer capsules, readiness scores, and trust-signal claims against the original draft before publishing.

## Reference(s):

- [AEO Optimizer ClawHub release](https://clawhub.ai/mohitagw15856/skills/aeo-optimizer)
- [AEO Optimizer homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/aeo-optimizer.html)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown article rewrite followed by a structured Markdown AEO audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces question-format H2 headings, 50-80 word answer capsules, paragraph-length audit notes, trust-signal findings, readiness scores, and recommended next steps.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
