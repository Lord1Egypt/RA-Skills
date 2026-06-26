## Description: <br>
Helps visual-capable agents design and maintain a 3-brain filesystem and memory system with LEFT/RIGHT visual, text, and API cross-checking for verification and retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DeepSeekOracle](https://clawhub.ai/user/DeepSeekOracle) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and visual-capable agents use this skill to organize local memory folders, reference stubs, visual evidence, and reconciliation notes for LYGO Haven workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local notes, indexes, logs, and screenshots can persist sensitive information from private documents, dashboards, or account pages. <br>
Mitigation: Use a dedicated workspace and avoid saving private pages unless persistence is acceptable; review visual artifacts and logs before sharing. <br>
Risk: Visual observations can conflict with structured API data or receipt-based records. <br>
Mitigation: Log discrepancies explicitly and prefer auditable receipts or APIs over UI-only observations when sources disagree. <br>
Risk: Filesystem setup can add folders, indexes, logs, or visual evidence files to an existing workspace. <br>
Mitigation: Ask before structural changes, extend existing folders when present, and avoid deleting or overwriting existing files. <br>


## Reference(s): <br>
- [BOOK BRAIN VISUAL READER examples](references/book-brain-visual-examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/DeepSeekOracle/book-brain-visual-reader) <br>
- [Eternal Haven portal](https://EternalHaven.ca) <br>
- [LYGO Champion Hub](https://deepseekoracle.github.io/Excavationpro/LYGO-Network/champions.html#champions) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with filesystem paths, reference stubs, log entry templates, and optional JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; agents may propose or create local folders, indexes, notes, and selected screenshots when the user approves.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
