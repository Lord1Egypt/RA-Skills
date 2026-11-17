## Description:

Write, debug, and optimize Adobe Illustrator automation scripts using ExtendScript (JavaScript/JSX) for documents, layers, paths, text frames, colors, symbols, artboards, export workflows, and related Illustrator DOM objects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhauga](https://clawhub.ai/user/jhauga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to create, debug, and adapt Illustrator ExtendScript automation for document editing, batch exports, artwork generation, text replacement, and DOM-based workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or adapted Illustrator scripts can save, export, delete, remove, or otherwise modify artwork and documents.

Mitigation: Review scripts before execution, test on copies of files, and confirm file paths and document targets before running batch or unattended workflows.

Risk: Startup or headless Illustrator scripts can run without visible prompts, especially when dialogs are suppressed.

Mitigation: Avoid placing unreviewed scripts in Startup Scripts, use explicit logging for unattended runs, and keep user interaction enabled unless the workflow requires suppression.

Risk: Scripts that open external files or use sidecar/log files may read or write unexpected paths if inputs are wrong.

Mitigation: Use known absolute paths, validate inputs, and inspect sidecar or log locations before running externally launched automation.

## Reference(s):

- [Illustrator JavaScript Object Model Quick Reference](references/object-model-quick-reference.md)
- [Illustrator Scripting Guide](https://ai-scripting.docsforadobe.dev/)
- [Illustrator Scripting Changelog](https://ai-scripting.docsforadobe.dev/introduction/changelog/)
- [ClawHub Skill Page](https://clawhub.ai/jhauga/skills/adobe-illustrator-scripting)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript/JSX code blocks, concise guidance, and optional command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Illustrator ExtendScript snippets, workflow checks, troubleshooting notes, and file path guidance.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
