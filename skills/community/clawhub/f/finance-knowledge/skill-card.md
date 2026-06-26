## Description: <br>
A retrieval skill that answers finance questions from a local finance knowledge base covering banking, funds, mergers and acquisitions, derivatives, securities issuance, securities trading, asset securitization, and related topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krillingone](https://clawhub.ai/user/krillingone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer finance terminology and concept questions from the bundled Chinese-language markdown knowledge base. It can also append a banking platform prompt when the source skill calls for a high-intent recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Finance answers may include a promotional bank mini-program image or QR destination. <br>
Mitigation: Verify the bank destination through official channels before scanning a QR code or entering personal or financial information. <br>
Risk: The local knowledge base may be incomplete or stale for finance, banking, or regulatory questions. <br>
Mitigation: Use the skill for knowledge-base lookup only, and verify decisions against authoritative financial, legal, or compliance sources. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krillingone/finance-knowledge) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Finance Knowledge Base](artifact/article_fin_knowledge/) <br>
- [Promotional Image Referenced by Skill](https://static.hepei.club/contact.png) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown answer with a conclusion, key points, source filenames, and an optional image link] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Answers should be grounded in the local knowledge base and should state when no matching local entry is found.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
