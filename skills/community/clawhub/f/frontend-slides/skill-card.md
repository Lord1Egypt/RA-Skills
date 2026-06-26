## Description: <br>
Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ken0122](https://clawhub.ai/user/ken0122) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, presales, and presentation authors use this skill to create solution decks, client presentations, bid proposals, pitch decks, tutorials, conference talks, and internal presentations as browser-based HTML slides. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PowerPoint conversion extracts slide text, images, and notes into local output files that may include confidential presentation content. <br>
Mitigation: Review generated files and asset folders before sharing, publishing, or committing them. <br>
Risk: Generated presentations run local JavaScript in the browser. <br>
Mitigation: Inspect generated HTML before distributing it and open it in an appropriate local or sandboxed browser context when handling sensitive material. <br>
Risk: Optional browser edit mode may leave draft slide content in localStorage on the machine where it was used. <br>
Mitigation: Avoid edit mode on shared machines and clear browser storage after working with confidential decks. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ken0122/frontend-slides) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai/) <br>
- [STYLE_PRESETS.md](STYLE_PRESETS.md) <br>
- [HTML Architecture](reference/html-architecture.md) <br>
- [Viewport and Base CSS](reference/viewport-and-base.css) <br>
- [PPT Extraction](reference/ppt-extract.py) <br>
- [Image Processing](reference/image-processing.py) <br>
- [Animation Patterns](reference/animation-patterns.md) <br>
- [Edit Button Implementation](reference/edit-button-implementation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, Python, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces self-contained HTML slide decks and optional local asset folders when converting PowerPoint files or processing images.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
