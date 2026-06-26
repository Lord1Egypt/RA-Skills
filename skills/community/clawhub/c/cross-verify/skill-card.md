## Description: <br>
Cross Verify helps agents check pasted text or data for factual accuracy, bias, logic gaps, and an overall credibility score. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[irvinezhao](https://clawhub.ai/user/irvinezhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to cross-check pasted claims, data, or assertions and return a structured verification report with claim status, bias markers, logic gaps, source assessment, and summary advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may prompt web searches for claims in pasted text, which can expose confidential or sensitive material if users paste it. <br>
Mitigation: Avoid pasting sensitive material unless web browsing is acceptable; redact private details before requesting verification. <br>
Risk: Fact-checking outputs can still be incomplete or misleading when sources are unavailable, conflicting, or low quality. <br>
Mitigation: Review sources and treat unverifiable claims as needing additional evidence before relying on the report. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes credibility scoring, claim status labels, bias markers, logic gap labels, source assessment, and summary advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
