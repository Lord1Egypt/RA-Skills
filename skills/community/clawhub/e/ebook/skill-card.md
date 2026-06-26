## Description: <br>
Manage ebook collections, track reading progress, and export highlights using bash and Python. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Readers, researchers, and developers can use this skill to catalog a local ebook library, log reading sessions, manage highlights and reviews, and export library data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and edits ~/.ebook/data.jsonl, which can contain reading history, highlights, and reviews. <br>
Mitigation: Install only if local storage of this data is acceptable, and back up ~/.ebook/data.jsonl before delete, update, or bulk export workflows. <br>
Risk: Export commands can write library, highlight, or review data to a user-provided file path. <br>
Mitigation: Review the export path and destination permissions before running export commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/ebook) <br>
- [Publisher homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands; command output may be JSON, tables, CSV, Markdown, or local files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local JSONL library at ~/.ebook/data.jsonl and can export selected library data to a user-provided path.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
