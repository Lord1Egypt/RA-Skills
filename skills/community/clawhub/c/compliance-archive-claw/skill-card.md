## Description: <br>
Compliance Archive Claw helps archive enterprise legal documents and policy files, manage versions, mark obsolete records, search indexed metadata, and export archive listings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Compliance, legal, and operations teams use this skill to maintain a searchable digital archive of corporate policies, legal documents, templates, and version history. It supports new document archiving, version updates, obsolete-version marking, metadata search, and archive list exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The archive script can write files and update archive records. <br>
Mitigation: Review before installing in a real compliance environment and use backed-up test data until operational controls are confirmed. <br>
Risk: SQL inputs are insufficiently validated in the script. <br>
Mitigation: Parameterize or escape SQL inputs before using the skill with real compliance records. <br>
Risk: Version updates can mark existing records obsolete. <br>
Mitigation: Require user confirmation with a list of affected records before obsolete status changes are applied. <br>
Risk: Archive paths and document types may be too broad for sensitive files. <br>
Mitigation: Restrict document types to approved archive paths and confirm access controls before sensitive files are archived. <br>


## Reference(s): <br>
- [Version Control Rules](references/version-control.md) <br>
- [File Classification Standard](references/file-classification.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and archive metadata summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce archive numbers, archive paths, version-change summaries, search results, and exported document lists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
