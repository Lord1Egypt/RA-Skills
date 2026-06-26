## Description: <br>
AI-powered deliverable evaluation via EvalLayer API that extracts factual claims, scores quality, and returns structured JSON verdicts with pass/fail, confidence scores, and payout recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanhall00](https://clawhub.ai/user/ryanhall00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to submit text deliverables to EvalLayer as a quality gate, receive structured evaluation verdicts, and review claim-level support signals before acting on agent work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted deliverables leave the local environment and are sent to EvalLayer over HTTPS. <br>
Mitigation: Review content before submission and avoid sending secrets, confidential business material, regulated data, or personal information. <br>
Risk: Extracted content may be stored for aggregation. <br>
Mitigation: Use the skill only for content that can be shared with EvalLayer under the user's data handling requirements. <br>
Risk: Automated pass/fail and payout recommendations may be inappropriate for consequential decisions if used without review. <br>
Mitigation: Use EvalLayer results as decision support and keep a human review step for consequential outcomes. <br>
Risk: The authenticated evaluation flow depends on an EvalLayer API key. <br>
Mitigation: Use a dedicated EvalLayer API key with minimal scope and rotate it if exposed. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/ryanhall00/evallayer-evaluator) <br>


## Skill Output: <br>
**Output Type(s):** [json, shell commands, guidance] <br>
**Output Format:** [JSON responses from shell-driven API calls, with setup and usage guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and python3; authenticated evaluation requires EVALLAYER_API_KEY.] <br>

## Skill Version(s): <br>
2.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
