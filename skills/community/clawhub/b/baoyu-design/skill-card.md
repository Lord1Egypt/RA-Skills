## Description:

Baoyu Design helps agents create self-contained HTML design artifacts, including UI mockups, interactive prototypes, wireframes, decks, dashboards, app screens, mobile apps, documents, videos, and design-system outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimliu](https://clawhub.ai/user/jimliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and agent users use this skill to turn product and interface design requests into HTML-based artifacts, then preview, iterate, and export selected outputs such as PPTX, PDF, video, Figma/Canva handoffs, or standalone HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Imported third-party design-system prose can become binding agent guidance.

Mitigation: Install only from trusted publishers, review design-system folders before binding them, and treat imported design content as reference material rather than user instructions.

Risk: Some workflows reference remote dependencies or execute local export scripts.

Mitigation: Prefer offline or vendored dependencies where available, review commands before execution, and scan generated artifacts before sharing or deploying them.

Risk: PPTX export configurations can include `showJs` snippets that execute in the captured page.

Mitigation: Review `showJs` values before running exports and use them only with trusted deck artifacts.

## Reference(s):

- [Baoyu Design ClawHub page](https://clawhub.ai/jimliu/skills/baoyu-design)
- [Core design workflow](system-prompt.md)
- [Codex harness reference](references/codex.md)
- [Claude Code harness reference](references/claude.md)
- [Cursor harness reference](references/cursor.md)
- [Design system authoring guide](built-in-skills/design-system-authoring-guide.md)
- [Editable PPTX export](built-in-skills/export-as-pptx-editable.md)
- [Video export](built-in-skills/export-as-video.md)
- [Standalone HTML export](built-in-skills/save-as-standalone-html.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline commands and generated HTML, JavaScript, CSS, JSON, and export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce self-contained HTML artifacts, multi-file HTML/JSX bundles, design-system bundles, PDFs, PPTX files, videos, Figma/Canva handoff instructions, and local preview commands depending on the requested workflow.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
