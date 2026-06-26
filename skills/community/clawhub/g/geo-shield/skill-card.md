## Description: <br>
Geo Shield generates heuristic credibility reports for URLs, combining domain reputation rules with GEO manipulation-pattern and content-quality checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rfdiosuao](https://clawhub.ai/user/rfdiosuao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
ClawHub and OpenClaw users can invoke the skill in chat to triage whether a URL or source may show AI-targeted misinformation, SEO-style manipulation, or GEO poisoning indicators. Its report should be used as a starting point for verification rather than a final factual determination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may assign credibility scores and warnings for a URL without inspecting the live page content. <br>
Mitigation: Treat reports as heuristic triage only; independently open and review the source content before relying on the score or recommendations. <br>
Risk: The report can create false confidence for consequential decisions. <br>
Mitigation: Do not use the output as the sole basis for moderation, security, health, financial, legal, or factual decisions; confirm with authoritative sources and domain experts where needed. <br>
Risk: Rule-based pattern matching can misclassify legitimate or malicious content. <br>
Mitigation: Review detected patterns manually and cross-check the claim, publisher, citations, and date against trusted independent sources. <br>


## Reference(s): <br>
- [Geo Shield on ClawHub](https://clawhub.ai/rfdiosuao/geo-shield) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [ClawHub](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with credibility score, risk level, score tables, detected pattern counts, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Chinese and English triggers are documented; a URL is required for report generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, skill.json, README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
