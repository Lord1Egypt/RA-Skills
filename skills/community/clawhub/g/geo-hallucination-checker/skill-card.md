## Description: <br>
Detects and annotates hallucinations, unsupported claims, fabricated studies, and incorrect conclusions in text so agents can produce evidence-grounded reviews and safer rewrites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geoly-geo](https://clawhub.ai/user/geoly-geo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content reviewers use this skill to fact-check drafts, classify risky factual claims, and rewrite unsupported or overconfident language into citation-safe prose. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may miss current, domain-specific, or high-stakes factual issues when authoritative sources are not supplied or checked. <br>
Mitigation: Treat its output as a screening aid and verify medical, legal, financial, scientific, or current factual claims against authoritative sources before publishing or relying on them. <br>
Risk: Overly cautious classification can mark true claims as unsupported when evidence is unavailable in the current context. <br>
Mitigation: Provide explicit sources, citations, or source constraints with the content under review and use the results to prioritize follow-up verification. <br>


## Reference(s): <br>
- [Hallucination Guide](references/hallucination_guide.md) <br>
- [ClawHub release page](https://clawhub.ai/geoly-geo/geo-hallucination-checker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summary, claim-level analysis table, and optional hallucination-safe rewrite] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses status and risk labels such as Supported, Unsupported, Problematic, Contradicted, Speculative, Low, Medium, and High.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
