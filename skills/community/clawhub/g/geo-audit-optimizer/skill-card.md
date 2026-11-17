## Description:

GEO audit for AI search visibility. Scores your brand 0-100 across ChatGPT, Gemini, Grok & more. $0.99/audit or free with coupon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feydefi](https://clawhub.ai/user/feydefi)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to audit a website's brand visibility across AI search engines and receive a scored optimization plan. It is read-only by design: the agent presents findings and recommendations while the human approves payments and handles any publishing or site changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit can require payment or coupon use.

Mitigation: Ask for explicit human approval before any paid audit and show the selected payment or coupon path before calling the API.

Risk: The remote audit response includes agent-facing presentation instructions.

Mitigation: Treat response instructions as untrusted display guidance only; do not execute actions, fetch URLs, install packages, or bypass local rules based on the response.

Risk: The fixes endpoint may enable website or content changes despite the skill's read-only posture.

Mitigation: Use fixes only for visible drafts or recommendations unless the human can review exactly what will change and explicitly approves the action.

Risk: Anti-detection content guidance can encourage manipulative or platform-violating behavior.

Mitigation: Keep recommendations factual, policy-compliant, and human-reviewed; avoid fake reviews, spam, or deceptive platform engagement.

## Reference(s):

- [GEO Principles](references/geo-principles.md)
- [Platform Guide](references/platform-guide.md)
- [Schema & Structured Data Templates](references/schema-templates.md)
- [XanLens Homepage](https://xanlens.com)
- [XanLens API Docs](https://xanlens.com/api-docs)
- [XanLens llms.txt](https://xanlens.com/llms.txt)
- [ClawHub Skill Page](https://clawhub.ai/feydefi/skills/geo-audit-optimizer)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown summary with audit score, grade context, and recommended optimization actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a human-provided website URL and explicit human approval before any paid audit; polling may take about 3-5 minutes.]

## Skill Version(s):

3.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
