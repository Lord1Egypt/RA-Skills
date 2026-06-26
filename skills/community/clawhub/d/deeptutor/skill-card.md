## Description: <br>
Deeptutor is a personalized, content-driven deep reading tutor that reads EPUB chapters, writes original-text-first deep dives, can generate comprehension checks, and saves notes to Obsidian. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanjinlimkelvin-dot](https://clawhub.ai/user/tanjinlimkelvin-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Readers and agents use this skill to study books chapter by chapter from local EPUB files, producing close-reading Markdown deep dives, comprehension questions, and Obsidian reading notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes generated reading notes and navigation files into the configured Obsidian vault path. <br>
Mitigation: Review the hard-coded vault path before use and keep backups for important notes. <br>
Risk: Rerunning a chapter can overwrite that chapter note and refresh index or navigation files. <br>
Mitigation: Review generated content before saving and preserve previous notes when edits must be retained. <br>


## Reference(s): <br>
- [Chapter-by-Chapter Book Deep Study Prompt](references/chapter-by-chapter.md) <br>
- [How Jin should invoke deeptutor](references/invocation-prompts.md) <br>
- [Patterns for Book Deep Study](references/patterns.md) <br>
- [Quiz Templates for Book Deep Study](references/quiz-templates.md) <br>
- [ClawHub skill page](https://clawhub.ai/tanjinlimkelvin-dot/deeptutor) <br>
- [Publisher profile](https://clawhub.ai/user/tanjinlimkelvin-dot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with optional shell commands and saved Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write chapter notes, an index, and navigation links under the configured Obsidian vault path.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
