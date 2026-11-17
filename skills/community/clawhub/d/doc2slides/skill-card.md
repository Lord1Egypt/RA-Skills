## Description:

Converts PDF, Word, and Markdown documents into designer-grade PowerPoint presentations with AI-assisted layout selection, built-in charts, and local-first defaults.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lifei68801](https://clawhub.ai/user/lifei68801)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and document authors use this skill to turn PDFs, Word files, or Markdown into presentation decks for thesis defenses, status reports, technical training, business pitches, and reading notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document contents may be sent to configured AI services when optional LLM providers or custom endpoints are used.

Mitigation: Use true offline mode for confidential documents, or confirm the selected provider and endpoint are approved before enabling API keys.

Risk: Generated HTML is rendered for slide previews and may have weak browser isolation.

Mitigation: Render untrusted or sensitive content in a contained environment and review generated previews before sharing outputs.

Risk: Setup installs Python dependencies into the active environment.

Mitigation: Run setup in an isolated virtual environment or disposable workspace rather than a privileged or shared global Python install.

## Reference(s):

- [Design Principles](references/design-principles.md)
- [ClawHub Skill Page](https://clawhub.ai/lifei68801/skills/doc2slides)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [PPTX files with optional PNG previews, plus Markdown and inline shell commands for setup and execution guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local documents, writes local presentation outputs, and can optionally use configured LLM provider API keys for content analysis.]

## Skill Version(s):

3.8.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
