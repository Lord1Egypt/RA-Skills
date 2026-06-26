## Description: <br>
RAG-enhanced compliance Q&A with regulatory interpretation guardrails, source attribution, and escalation triggers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dangsllc](https://clawhub.ai/user/dangsllc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, compliance staff, and reviewers use this skill to answer questions from supplied compliance documents, with citations, explicit context gaps, and escalation cues for active incidents or high-stakes legal/compliance decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat document-grounded compliance answers as legal advice or rely on them for high-stakes decisions. <br>
Mitigation: Treat outputs as an aid only and escalate active incidents, contradictions, or high-stakes compliance decisions to qualified counsel or compliance staff. <br>
Risk: Sensitive compliance materials or URLs could be supplied to the skill without proper authorization. <br>
Mitigation: Provide only documents and URLs the user is authorized to share. <br>
Risk: The provided context may be incomplete or contradictory. <br>
Mitigation: Require citations for claims, explicitly flag context gaps, and recommend human review when documents conflict or do not answer the question. <br>


## Reference(s): <br>
- [Compliance Qa ClawHub listing](https://clawhub.ai/dangsllc/compliance-qa) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with summary, analysis, caveats, confidence, and escalation sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses citations to supplied documents and flags insufficient context instead of filling gaps from general knowledge.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
