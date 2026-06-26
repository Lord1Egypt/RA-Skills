## Description: <br>
Analyzes books or uploaded reading files through four virtual personas, then produces multilingual structured reading reports and optional study exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangboheng](https://clawhub.ai/user/zhangboheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Readers, researchers, students, and knowledge workers use this skill to turn a book title, public link, or supported document file into a multi-perspective analysis report. It is also used to create review materials such as Anki flashcards, Obsidian notes, and Notion pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Book titles, lookup queries, or selected report content may be sent to external lookup services or a configured Notion workspace. <br>
Mitigation: Avoid confidential manuscripts, private documents, or sensitive reading lists unless external lookup and export paths are disabled or explicitly approved. <br>
Risk: Reports and fetched metadata may be saved locally under the workspace reports and cache paths. <br>
Mitigation: Review generated files before sharing the workspace and clear cached metadata when the analyzed material should not persist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangboheng/four-dimensional-deep-reading) <br>
- [Publisher profile](https://clawhub.ai/user/zhangboheng) <br>
- [Author website](https://www.luckydesigner.space) <br>
- [Identity modules reference](reference/identity_modules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown reports with optional CSV, Obsidian Markdown, and Notion JSON-block exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves reports under workspace/reports; optional exports create Anki CSV, Obsidian Markdown, or Notion pages when configured.] <br>

## Skill Version(s): <br>
1.8.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
