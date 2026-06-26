## Description: <br>
Deep Reading guides an agent through chapter-by-chapter source-text reading and structured note-taking with quotes, analysis, interpretation, cross-text links, actionable insights, and open questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YY-C8](https://clawhub.ai/user/YY-C8) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Readers, students, researchers, and knowledge workers use this skill to read books or excerpts slowly, preserve source quotations, and build structured chapter notes for later review and knowledge management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist reading plans and chapter notes locally, and can feed generated notes into memory workflows when users enable them. <br>
Mitigation: Use it only with books and excerpts you are comfortable saving, and review generated notes before passing them to memory tools. <br>
Risk: The included cron template can cause recurring autonomous reading-note updates. <br>
Mitigation: Configure the cron workflow only when recurring updates are intended, and review the generated notes and plan updates regularly. <br>
Risk: Generated notes may contain source-text quotations and user-provided excerpts. <br>
Mitigation: Provide only text you have permission to process and store, and review notes for privacy or copyright concerns before sharing. <br>


## Reference(s): <br>
- [Book Types and Reading Amount Configuration](references/book-types.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/YY-C8/deep-reading) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reading notes with optional bash commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local reading notes under reading/ and optional memory entries when the user enables related workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
