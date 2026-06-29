## Description: <br>
Parses local Antom Settlement Detail CSV or XLSX report files for settlement amount validation, fee analysis, and reconciliation knowledge Q&A while rejecting unsupported report types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antom-tech](https://clawhub.ai/user/antom-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Merchants and finance operators use this skill to analyze local Settlement Detail reports, validate settlement formulas, review fee breakdowns, and ask reconciliation knowledge questions. It is scoped to settlement and payment-processing tasks and does not fetch reports online. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches reconciliation rules and knowledge from an external Antom/Marmot CDN. <br>
Mitigation: Install only when outbound HTTPS access to the documented CDN is acceptable for the deployment environment. <br>
Risk: User-confirmed update guidance may include commands that update or replace the local skill directory. <br>
Mitigation: Review the generated command and source repository before running updates, and start a new session after updating. <br>
Risk: The skill handles financial reconciliation outputs that could affect merchant review decisions. <br>
Mitigation: Review settlement findings against source reports and use the skill's strict file-type and report-type checks before relying on analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/antom-tech/antom-reconciliation-expert) <br>
- [Antom reconciliation rules documentation](https://cdn.marmot-cloud.com/page/antom_bill_reconciliation_doc/rules/) <br>
- [Antom reconciliation wiki documentation](https://cdn.marmot-cloud.com/page/antom_bill_reconciliation_doc/wiki/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown analysis reports, merchant-facing guidance, and optional shell commands for user-confirmed updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference generated local files for large report outputs instead of pasting full datasets into the conversation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
