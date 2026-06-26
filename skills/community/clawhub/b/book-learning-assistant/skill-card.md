## Description: <br>
Helps learners study books by building structured book overviews from searched book metadata or user-provided EPUB files, then producing chapter-focused explanations with source-grounded examples and freshness checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzhanchao883](https://clawhub.ai/user/wangzhanchao883) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners and educators use this skill to turn a book title or a supplied EPUB into a structured study path, chapter summaries, key ideas, thinking tools, and accessible examples. It is also useful when an agent needs to read local ebook content before preparing study notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read ebook files supplied by the user, which can expose private reading materials or local file paths to the agent. <br>
Mitigation: Use only ebook files you are comfortable sharing with the agent, and limit access to the specific file needed for the study task. <br>
Risk: The artifact mentions writing generated notes into Obsidian and Notion without fully scoping destinations. <br>
Mitigation: Require an explicit preview and confirmation before any write action, and specify the exact vault, database, page, or folder where notes may be written. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangzhanchao883/book-learning-assistant) <br>
- [EBOOK_README.md](artifact/EBOOK_README.md) <br>
- [output-examples.md](artifact/references/output-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Structured Markdown, JSON from the ebook helper script, and occasional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs emphasize source-grounded book summaries, chapter explanations, simple examples, and knowledge freshness notes.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata; frontmatter reports 1.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
