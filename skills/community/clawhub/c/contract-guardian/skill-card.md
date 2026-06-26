## Description: <br>
合同卫士 — AI合同审查助手，识别风险条款、提取关键信息、追踪到期日 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanjing5024064](https://clawhub.ai/user/hanjing5024064) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to review Chinese contract files, extract parties, amounts, dates, and terms, identify risky clauses, compare contract versions, and track upcoming contract expirations. It produces structured review reports and local contract metadata for follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Contract contents and archived contract metadata can be sensitive even when processed locally. <br>
Mitigation: Use explicit file paths, avoid unrelated private files, configure CG_DATA_DIR intentionally, and archive only metadata that should be retained locally. <br>
Risk: Generated contract risk reports may be incomplete or unsuitable as legal advice. <br>
Mitigation: Treat outputs as reference material, review flagged clauses manually, and consult a qualified lawyer for important or ambiguous contracts. <br>


## Reference(s): <br>
- [Risk Checklist](references/risk-checklist.md) <br>
- [Contract Templates](references/contract-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local contract files and may store contract metadata under CG_DATA_DIR.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
