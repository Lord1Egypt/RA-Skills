## Description:

Christa is a Chinese-oriented body-shaping coach that runs an adaptive fitness assessment, scores readiness across five dimensions, and produces personalized fat-loss, nutrition, workout, and HTML report guidance from bundled coaching knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vvip2u](https://clawhub.ai/user/vvip2u)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill for Chinese-language fat-loss and body-shaping coaching, including readiness assessment, nutrition and workout planning, plateau troubleshooting, and generation of a self-contained HTML fitness report. It is intended for general fitness guidance, not medical diagnosis or individualized medical nutrition care.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat fitness and nutrition responses as medical advice for diagnosis, pregnancy, chronic disease, medication, eating disorders, kidney disease, diabetes, or injury decisions.

Mitigation: Use the skill only for general fitness education and route those cases to a licensed medical or nutrition professional.

Risk: Generated HTML reports can carry browser-rendering risk if user-provided text is inserted unsafely.

Mitigation: Escape user-provided text or render it as plain text before opening generated HTML in a browser.

## Reference(s):

- [8-Round Adaptive Assessment SOP and Five-Dimension Scoring](references/assessment-sop.md)
- [Body-Shaping Knowledge Base](references/knowledge-body-shaping.md)
- [Nutrition Knowledge Base](references/knowledge-nutrition.md)
- [HTML Fitness Report Template](references/report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Conversational Markdown and self-contained HTML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include an inline SVG radar chart in generated HTML reports; no external CDN is required.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
