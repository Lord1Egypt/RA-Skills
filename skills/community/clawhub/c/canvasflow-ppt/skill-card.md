## Description: <br>
Generates magazine-style presentation decks from a topic or outline, with guided theme selection, layout planning, quality checks, and optional HTML or PPTX output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwbwin](https://clawhub.ai/user/wwbwin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Presentation creators, speakers, and agent users can use this skill to turn a topic, outline, or source material into a polished visual deck. It is best suited for product launches, demo days, private talks, and visually expressive presentations rather than dense tables, training materials, or collaboratively edited slides. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts automatically open generated files on macOS through shell commands. <br>
Mitigation: Review scripts before use, remove the auto-open behavior, or gate it behind an explicit option that uses a non-shell subprocess call. <br>
Risk: Generated HTML may reference third-party CDN assets. <br>
Mitigation: For sensitive presentations, pin, vendor, or remove external assets before sharing or opening the generated deck. <br>
Risk: Generated presentations may be visually polished but still contain inaccurate or unsuitable content. <br>
Mitigation: Review the deck against the supplied quality checklist and source material before using it in a public or commercial setting. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wwbwin/canvasflow-ppt) <br>
- [README.md](README.md) <br>
- [Layout System](references/layouts.md) <br>
- [Theme Presets](references/themes.md) <br>
- [Quality Checklist](references/checklist.md) <br>
- [Component Guide](references/components.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTML, JSON outline, and optional PPTX or single-file HTML presentation outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local presentation files and uses optional python-pptx for PPTX export.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
