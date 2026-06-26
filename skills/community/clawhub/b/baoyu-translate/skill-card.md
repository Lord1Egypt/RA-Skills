## Description: <br>
Baoyu Translate helps agents translate files, URLs, or inline text across quick, normal, and refined workflows with glossary support and Markdown-preserving output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimliu](https://clawhub.ai/user/jimliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content teams use this skill to translate Markdown articles, documents, URLs, and inline text into a target language. It supports quick direct translation, analysis-informed translation, and refined publication-quality review and polish workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow writes source-derived analysis, drafts, chunks, final translations, preferences, and backups to local disk. <br>
Mitigation: Avoid highly sensitive documents unless local file persistence is acceptable; review or delete generated output and backup directories after use. <br>
Risk: Generated translations may be inaccurate, omit nuance, or preserve source-language text in embedded images. <br>
Mitigation: Review final translations against the source, use refined mode for important material, and check text-heavy images before publication. <br>
Risk: Long-document workflows may run local Bun or npx commands to split Markdown into chunks. <br>
Mitigation: Run the skill in a trusted workspace and review the generated shell command before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jimliu/baoyu-translate) <br>
- [Project homepage](https://github.com/JimLiu/baoyu-skills#baoyu-translate) <br>
- [EXTEND.md schema](references/config/extend-schema.md) <br>
- [First-time setup](references/config/first-time-setup.md) <br>
- [Workflow mechanics](references/workflow-mechanics.md) <br>
- [Refined workflow](references/refined-workflow.md) <br>
- [EN-ZH glossary](references/glossary-en-zh.md) <br>
- [Subagent prompt template](references/subagent-prompt-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, local configuration files, shell commands, and concise guidance summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes final translations to translation.md and may preserve intermediate analysis, prompt, draft, critique, revision, chunk, backup, and preference files on disk.] <br>

## Skill Version(s): <br>
1.117.3 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
