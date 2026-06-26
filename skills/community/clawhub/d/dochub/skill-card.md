## Description: <br>
Dochub helps an agent turn .docx and .xlsx source documents into a structured Markdown knowledge base using a raw -> wiki -> schema architecture, with workflows for initialization, incremental updates, search/Q&A, and knowledge-base health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longjf25](https://clawhub.ai/user/longjf25) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to organize local office documents into a source-traceable Markdown knowledge base, then search it, ask document-grounded questions, apply incremental updates, and run health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reorganizes local documents into raw/, wiki/, and update/ structures, which can move or rewrite files in the chosen knowledge-base directory. <br>
Mitigation: Run it only in a clearly scoped folder, keep backups, and require explicit confirmation before initialization or updates. <br>
Risk: The security summary notes that the skill suggests disabling sandbox protection for Windows file moves. <br>
Mitigation: Keep sandbox protections enabled and adjust the workspace or permissions instead of disabling the sandbox. <br>
Risk: The skill may install document-conversion dependencies such as python-docx, openpyxl, or markitdown. <br>
Mitigation: Require user approval before dependency installation and install only in an isolated Python environment. <br>


## Reference(s): <br>
- [Dochub on ClawHub](https://clawhub.ai/longjf25/dochub) <br>
- [Publisher profile](https://clawhub.ai/user/longjf25) <br>
- [Entity type definitions](references/entity-types.md) <br>
- [Karpathy methodology](references/karpathy-methodology.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with file edits, generated knowledge-base files, shell commands, and structured status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates local raw/, wiki/, update/, _schema.md, index, overview, log, source-summary, concept, entity, comparison, and lint-report files.] <br>

## Skill Version(s): <br>
1.5.0 (source: ClawHub server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
