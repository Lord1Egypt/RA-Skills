## Description: <br>
Analyzes legal documents such as leases, contracts, NDAs, terms of service, and employment agreements into plain-English clause summaries with risk ratings, jurisdiction-aware enforceability notes, and pushback language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dglassman12](https://clawhub.ai/user/dglassman12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use Clausebreaker to understand legal documents clause by clause, identify higher-risk terms, and draft negotiation language without treating the output as legal advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may paste sensitive personal, financial, medical, or confidential business information into the hosting AI platform. <br>
Mitigation: Redact sensitive identifiers before analysis and review the hosting platform privacy policy before sharing contract text. <br>
Risk: Capability tags indicate wallet and purchase behavior even though the artifact says it performs text analysis only. <br>
Mitigation: Do not grant wallet, purchase, transaction, external API, or external service permissions during installation or use. <br>
Risk: Legal document explanations and enforceability notes can be incomplete or wrong for a user's jurisdiction. <br>
Mitigation: Treat the output as educational guidance, confirm jurisdiction-specific issues independently, and consult a qualified lawyer for high-consequence documents. <br>


## Reference(s): <br>
- [Clausebreaker on ClawHub](https://clawhub.ai/dglassman12/clausebreaker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with clause breakdowns, risk ratings, summary tables, disclaimers, and optional redline text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OCR-derived text analysis, translation notes, jurisdiction prompts, and suggested negotiation language.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
