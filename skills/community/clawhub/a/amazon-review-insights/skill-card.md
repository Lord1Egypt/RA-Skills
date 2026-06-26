## Description: <br>
Amazon product review intelligence analysis tool for global e-commerce sellers. Core capabilities:fetch Amazon reviews, AI-powered negative review analysis, quantify high-frequency issues, discover hidden negative feedback in 5-star reviews, generate improvement suggestions, track review trends, incremental updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sparkbayes](https://clawhub.ai/user/sparkbayes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers and e-commerce analysts use this skill to collect Amazon review data through AstrMap and inspect sentiment, recurring issues, trend data, and product improvement suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive AstrMap API key and sends it to api.astrmap.com for authentication. <br>
Mitigation: Use CUSTOMER_INSIGHTS_API_KEY instead of hardcoding credentials, keep the key private, and rotate or disable it when it is no longer needed. <br>
Risk: Review collection features depend on the AstrMap desktop client and an Amazon buyer account. <br>
Mitigation: Verify the desktop client download, checksum, and signature, and use a dedicated Amazon buyer account rather than a primary seller or business account. <br>
Risk: Creating analysis, incremental fetch, or manual analysis tasks can consume account points or start collection workflows. <br>
Mitigation: Require explicit user confirmation before actions that spend points, create tasks, collect reviews, or trigger analysis. <br>


## Reference(s): <br>
- [AstrMap API Reference](references/api_reference.md) <br>
- [AstrMap Desktop Client Security Guide](references/security.md) <br>
- [ClawHub skill page](https://clawhub.ai/sparkbayes/amazon-review-insights) <br>
- [AstrMap website](https://www.astrmap.com/) <br>
- [AstrMap download configuration](https://www.astrmap.com/download-config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CUSTOMER_INSIGHTS_API_KEY and AstrMap API task identifiers when invoking review collection and analysis workflows.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
