## Description: <br>
Create animation-rich HTML presentations from scratch or by converting PowerPoint files, with visual style discovery for users who want polished web slide decks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liberalchang](https://clawhub.ai/user/liberalchang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and presenters use this skill to create self-contained browser presentations, enhance existing HTML decks, or convert PPTX content into styled web slides. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PPTX conversion can extract slide text, images, and speaker notes into local files. <br>
Mitigation: Use a dedicated project folder and avoid converting confidential decks into synced or public directories. <br>
Risk: Optional Python packages may be installed to support PPTX conversion. <br>
Mitigation: Install optional dependencies in a virtual environment before running conversion commands. <br>
Risk: Generated presentations may reference CDN-hosted fonts. <br>
Mitigation: Use local or system fonts, or remove CDN font links, when decks must work offline or avoid third-party font requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liberalchang/frontendslides) <br>
- [README](artifact/README.md) <br>
- [Style presets reference](artifact/STYLE_PRESETS.md) <br>
- [HTML template reference](artifact/html-template.md) <br>
- [Animation patterns reference](artifact/animation-patterns.md) <br>
- [Viewport base CSS](artifact/viewport-base.css) <br>
- [PPTX extraction script](artifact/scripts/extract-pptx.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with generated HTML, CSS, JavaScript, JSON extraction data, and local asset files when converting PPTX decks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces self-contained HTML presentations and may create local preview, asset, and extracted-slide files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
