## Description: <br>
Baoyu Design helps file-capable agents create polished self-contained HTML design artifacts, including UI mockups, interactive prototypes, wireframes, dashboards, mobile app screens, slide decks, videos, documents, and reusable design systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimliu](https://clawhub.ai/user/jimliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, product teams, and file-capable agents use this skill to produce, preview, iterate on, and export design artifacts as HTML-based deliverables. It is suited for UI mockups, prototypes, wireframes, decks, mobile screens, design-system authoring, and related visual exploration workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read design source files that the user points it at. <br>
Mitigation: Review requested source paths before use and provide only files that are appropriate for the design task. <br>
Risk: The skill writes generated artifacts under project design folders. <br>
Mitigation: Keep generated work in the requested designs/ project folder and review outputs before sharing or deploying them. <br>
Risk: Preview, export, and connector workflows may run local tools or use services such as GitHub, Figma, Canva, image generation, or Google Fonts. <br>
Mitigation: Use those workflows only when needed, confirm connector scope with the user, and review generated files before execution or publication. <br>


## Reference(s): <br>
- [Skill entry point](SKILL.md) <br>
- [Core design workflow](system-prompt.md) <br>
- [Codex harness reference](references/codex.md) <br>
- [Claude harness reference](references/claude.md) <br>
- [Cursor harness reference](references/cursor.md) <br>
- [Hi-fi design workflow](built-in-skills/hi-fi-design.md) <br>
- [Interactive prototype workflow](built-in-skills/interactive-prototype.md) <br>
- [Deck creation workflow](built-in-skills/make-a-deck.md) <br>
- [Editable PPTX export workflow](built-in-skills/export-as-pptx-editable.md) <br>
- [Video export workflow](built-in-skills/export-as-video.md) <br>
- [Design system authoring workflow](built-in-skills/design-system-authoring-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, JSX, JSON, and shell command snippets; generated deliverables are typically files under a designs/ project folder.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce self-contained or multi-file HTML artifacts and optional exports such as PPTX, PDF, video, or design-system bundles when the corresponding workflow is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
