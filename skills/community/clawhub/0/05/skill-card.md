## Description: <br>
Provides rule-based content summaries and project reviews for daily reports, meetings, projects, articles, and general text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nidhov01](https://clawhub.ai/user/nidhov01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to summarize work logs, meeting notes, project materials, articles, and general text, and to produce project review outputs such as goal achievement, issues, recommendations, and next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Summarized content can be retained on local disk in ~/.ai_summary.db. <br>
Mitigation: Avoid highly confidential inputs unless local disk retention is acceptable, and periodically manage or clear the local database. <br>
Risk: Markdown exports can contain sensitive plaintext and may overwrite an existing destination file. <br>
Mitigation: Review the export path and file contents before sharing or storing exported Markdown. <br>
Risk: Rule-based summaries and project review suggestions may miss important context or produce incomplete conclusions. <br>
Mitigation: Review generated summaries and recommendations against the source material before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nidhov01/05) <br>
- [Publisher profile](https://clawhub.ai/user/nidhov01) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured text or JSON-like Python dictionaries, with optional Markdown file export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store summarized content locally in ~/.ai_summary.db and may export plaintext Markdown files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
