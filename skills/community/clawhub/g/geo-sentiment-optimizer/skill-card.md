## Description: <br>
Audit and optimize brand messaging to improve how AI platforms portray your brand. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geoly-geo](https://clawhub.ai/user/geoly-geo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External marketing, brand, and GEO teams use this skill to audit brand-facing content for AI sentiment signals and produce prioritized rewrite recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rewritten marketing claims can become inaccurate, overstated, or misleading if accepted without review. <br>
Mitigation: Review generated copy against source-of-truth product facts, customer proof points, and approved brand guidance before publishing. <br>
Risk: The audit script accepts user-supplied content and file paths, which can lead to incorrect analysis or unintended local file reads if inputs are not checked. <br>
Mitigation: Quote and validate user-supplied domains, content paths, and output paths before running commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/geoly-geo/geo-sentiment-optimizer) <br>
- [Sentiment Signals Reference](references/sentiment-signals.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports with checklist findings, priority rewrite recommendations, and example shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script prints a simple sentiment score and counts positive and negative content signals.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
