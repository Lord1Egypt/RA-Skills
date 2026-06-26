## Description: <br>
Claimback Radar scans user-provided emails and bills to extract billing details, identify subscription and refund risks, and produce prioritized savings recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[schchit](https://clawhub.ai/user/schchit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals, support agents, and financial workflow agents use this skill to turn subscription emails, bills, and renewal notices into structured billing summaries, risk flags, and action receipts for refunds, cancellations, reviews, or savings opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided billing, financial, or identity-related text is sent to OpenAI for processing. <br>
Mitigation: Submit only data whose external processing is acceptable, and avoid account numbers, identity documents, or highly sensitive financial details unless that data flow has been approved. <br>
Risk: The skill requires an OpenAI API key and can load a local .env file. <br>
Mitigation: Prefer setting OPENAI_API_KEY explicitly and keep unrelated secrets out of the working directory and any .env file used with the skill. <br>
Risk: Dependency versions are range-based rather than locked. <br>
Mitigation: For stricter production use, install with pinned dependencies or a reviewed lockfile. <br>
Risk: Generated refund, cancellation, or savings recommendations may be incomplete or wrong. <br>
Mitigation: Review the extracted facts, deadlines, links, and proposed steps before making payments, cancellations, refund claims, or account changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/schchit/claimback-radar) <br>
- [OpenAI API](https://api.openai.com) <br>
- [Input Schema](schema/input.json) <br>
- [Output Schema](schema/output.json) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, JSON] <br>
**Output Format:** [JSON object containing a confirmation card, action receipts, risk flags, and an optional summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are generated from user-provided billing text through OpenAI and should be reviewed before acting on financial or account changes.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata, clawhub.json, pyproject.toml, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
