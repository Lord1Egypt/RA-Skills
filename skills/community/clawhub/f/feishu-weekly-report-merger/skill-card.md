## Description: <br>
Merges multiple Feishu weekly report documents by reading authorized source documents, preserving original text and formatting, concatenating content by the fixed Part1 through Part5 sections, and creating a new Feishu cloud document. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ganguagua](https://clawhub.ai/user/ganguagua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and team leads use this skill to combine several Feishu weekly reports into one month-labeled Feishu cloud document while preserving each contributor's original wording and document formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Temporary files can contain full weekly report text. <br>
Mitigation: Remove /tmp/merge_doc_*.md files after the merge and avoid running the skill where other users can read those files. <br>
Risk: The merged Feishu document may expose source report content if sharing permissions are too broad. <br>
Mitigation: Confirm the source documents before execution and check the new document's sharing permissions before distributing it. <br>


## Reference(s): <br>
- [Chapter Parsing Reference](references/chapter_parsing.md) <br>
- [ClawHub skill page](https://clawhub.ai/ganguagua/feishu-weekly-report-merger) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, Files] <br>
**Output Format:** [Markdown content for a newly created Feishu document, with shell commands for the merge script and temporary Markdown files as intermediate inputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves source text and Feishu Markdown tags; creates /tmp/merge_doc_*.md temporary files that should be removed after merging.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
