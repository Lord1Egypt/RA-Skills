## Description: <br>
Extracts and returns plain text from PDF, Word, and Excel bid or tender documents for analysis, search, or summarisation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ezhencacao-dotcom](https://clawhub.ai/user/ezhencacao-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents, developers, and procurement teams use this skill to extract readable text from bid and tender files before search, summarisation, or downstream document analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unreviewed or changing document-parsing dependencies could introduce dependency-hygiene issues. <br>
Mitigation: Install the skill in an isolated environment and pin reviewed dependency versions before regular use. <br>
Risk: Bid documents from outside parties may contain sensitive or untrusted content that becomes visible to the calling agent after extraction. <br>
Mitigation: Only process files whose extracted text may be exposed to the agent and its output. <br>
Risk: Spreadsheet tables and complex document layouts may be flattened or lose formatting during extraction. <br>
Mitigation: Review extracted text before relying on it for decisions that depend on table structure or layout. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ezhencacao-dotcom/bid-reader) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text emitted to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Extracted text may flatten tables, omit complex formatting, and only supports PDF, DOCX, XLSX, and XLS inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
