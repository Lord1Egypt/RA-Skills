## Description:

Create animation-rich, self-contained HTML presentations from scratch, from PowerPoint files, or by enhancing existing decks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zarazhangrui](https://clawhub.ai/user/zarazhangrui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, presenters, and non-designers use this skill to plan, style, generate, convert, and refine web-based slide decks with responsive viewport fitting and animation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated presentations and PowerPoint conversion can create local HTML files and extracted asset folders.

Mitigation: Review generated files and output locations before sharing or publishing decks.

Risk: Optional browser editing can store deck text in localStorage.

Mitigation: Avoid enabling inline editing for sensitive content, or clear browser storage after editing.

Risk: Remote fonts can load resources from external font providers.

Mitigation: Use local or approved fonts for offline, private, or policy-restricted presentations.

Risk: PowerPoint conversion may require installing Python packages such as python-pptx.

Mitigation: Install dependencies in a virtual environment with pinned versions instead of a shared Python environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zarazhangrui/skills/frontend-presentations)
- [README](artifact/README.md)
- [HTML Presentation Template](artifact/html-template.md)
- [Viewport Base CSS](artifact/viewport-base.css)
- [Style Presets Reference](artifact/STYLE_PRESETS.md)
- [Animation Patterns Reference](artifact/animation-patterns.md)
- [PowerPoint Extraction Script](artifact/scripts/extract-pptx.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, and shell command snippets; generated artifacts are self-contained HTML files and optional extracted assets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local HTML/assets, optional browser localStorage edits, and PowerPoint extraction outputs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
