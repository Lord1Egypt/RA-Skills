## Description: <br>
Generates zero-dependency HTML presentations with 21 design presets, visual style exploration, playback mode, and speaker mode for pitches, product launches, and technical talks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaisersong](https://clawhub.ai/user/kaisersong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, presenters, and content teams use this skill to turn prompts, notes, or planned content into polished browser-based slide decks with selected visual styles, presentation controls, and optional in-browser editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated decks can make undeclared third-party font requests. <br>
Mitigation: Remove remote font links or self-host fonts before using decks in offline or privacy-sensitive settings. <br>
Risk: Generated decks may try to save edited HTML back to the current URL. <br>
Mitigation: Do not host generated decks on endpoints that accept PUT unless write-back behavior is intentional. <br>
Risk: Resource folders may be scanned and incorporated into deck planning. <br>
Mitigation: Use a dedicated resources or assets folder and exclude unrelated sensitive files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaisersong/genppt) <br>
- [Project homepage](https://github.com/kaisersong/slide-creator) <br>
- [Live demo](https://kaisersong.github.io/slide-creator/demos/blue-sky-en.html) <br>
- [Workflow reference](references/workflow.md) <br>
- [Style index](references/style-index.md) <br>
- [HTML template](references/html-template.md) <br>
- [Design quality rules](references/design-quality.md) <br>
- [Review checklist](references/review-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown plans and self-contained HTML presentation files with inline CSS and JavaScript.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated decks include presentation controls by default and may include browser editing behavior when enabled.] <br>

## Skill Version(s): <br>
2.14.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
