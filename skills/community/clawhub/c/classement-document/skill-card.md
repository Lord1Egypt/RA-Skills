## Description: <br>
Classifies an already identified accounting document by copying it into the appropriate client, year, and month folder with a normalized filename and duplicate detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trendex](https://clawhub.ai/user/trendex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Accounting automation users and agents use this skill as the final filing step after document analysis and client identification. It copies invoices, bank statements, and expense notes into the client folder tree, routes incomplete or uncertain inputs to review folders, and reports the classification result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/trendex/classement-document) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON classification result with concise human-facing status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Copies source files into the configured clients directory, writes an index for classified documents, and leaves the source file in place.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
