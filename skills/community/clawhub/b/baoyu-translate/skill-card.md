## Description:

Baoyu Translate helps an agent translate text, files, or URLs with quick, normal, and refined workflows plus configurable language, audience, style, glossary, and chunking support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimliu](https://clawhub.ai/user/jimliu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to translate articles, documents, inline text, and URL-sourced content into a target language. It supports fast direct translation as well as analysis, review, and polish workflows for publication-quality Markdown output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may execute Bun through npx when a local Bun runtime is unavailable.

Mitigation: Install and use a trusted Bun runtime before running the skill, or review the command path before allowing npx-based execution.

Risk: Translation workflows save source material, intermediate analysis, drafts, critiques, revisions, chunks, and final translations as local files.

Mitigation: Avoid translating sensitive documents unless local intermediate storage is acceptable, and remove generated working files when they are no longer needed.

Risk: Existing output directories may be moved to timestamped backups during conflict resolution.

Mitigation: Check the target output directory before running the skill and review backup folders after completion.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jimliu/skills/baoyu-translate)
- [Project Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-translate)
- [EXTEND.md Schema](references/config/extend-schema.md)
- [First-Time Setup](references/config/first-time-setup.md)
- [Workflow Mechanics](references/workflow-mechanics.md)
- [Translation Workflow Details](references/refined-workflow.md)
- [Subagent Translation Prompt Template](references/subagent-prompt-template.md)
- [English to Chinese Glossary](references/glossary-en-zh.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files with concise status text and occasional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final output is translation.md; normal and refined modes may also produce analysis, prompt, draft, critique, revision, and chunk files.]

## Skill Version(s):

1.117.3 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
