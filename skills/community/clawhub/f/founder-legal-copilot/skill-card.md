## Description: <br>
Legal copilot that guides founders from incorporation to exit with 27 legal deliverables across 5 startup phases <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danillo7](https://clawhub.ai/user/danillo7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External startup founders and their counsel use this skill to draft and review startup legal materials, run legal readiness checks, and prepare diligence reports from incorporation through exit. It provides educational legal analysis and document drafts that should be reviewed by a qualified attorney before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat generated legal drafts or analysis as legal advice. <br>
Mitigation: Use the outputs as educational starting points only and require review by a qualified attorney before signing documents or making legal decisions. <br>
Risk: Sensitive legal documents, EINs, or personal background data may be transmitted to third-party services. <br>
Mitigation: Confirm authority to share the data, minimize submitted information, use least-privileged API keys, and keep PII scrubbing enabled where available. <br>
Risk: Due diligence outputs about people or companies may be incomplete or unsuitable for adverse decisions. <br>
Mitigation: Independently verify findings and do not use key-hire diligence output for employment or adverse decisions without qualified legal review. <br>
Risk: Persistent deal memory can retain confidential legal or transaction data. <br>
Mitigation: Use a secured Redis instance, limit access to stored deal data, and remove retained records when they are no longer needed. <br>


## Reference(s): <br>
- [Founder Legal Copilot on ClawHub](https://clawhub.ai/danillo7/founder-legal-copilot) <br>
- [LegalKit](https://legalkit.legal) <br>
- [YC SAFE Documents](https://ycombinator.com/documents) <br>
- [NVCA Model Legal Documents](https://nvca.org/model-legal-documents) <br>
- [Cooley GO](https://cooleygo.com) <br>
- [Orrick Start-Up Forms](https://orrick.com/practices/startups) <br>
- [Series Seed](https://seriesseed.com) <br>
- [SEC EDGAR](https://sec.gov/edgar) <br>
- [Apify MCP](https://mcp.apify.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown legal document drafts, structured Markdown reports, JSON risk reports, and plain-language guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include risk summaries, recommendations, checklist scores, citations to baseline templates, and multilingual narration-ready text.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
