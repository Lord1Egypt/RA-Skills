## Description: <br>
Creates styled HTML presentation decks in 24 design styles and can help convert presentation content to editable PowerPoint files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xcjl](https://clawhub.ai/user/0xcjl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to turn topics, outlines, or uploaded PowerPoint files into styled HTML slide decks and optional PPTX files for editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated chart slides may load Chart.js from a CDN, which can expose viewing context to a third party or fail in restricted networks. <br>
Mitigation: Review generated HTML before sharing sensitive decks, and replace CDN loading with a local or approved pinned asset when network access is not acceptable. <br>
Risk: Optional Vercel deployment publishes generated files to third-party hosting. <br>
Mitigation: Confirm which files will be uploaded and where they will be hosted before approving any deployment command. <br>
Risk: Presentation inputs and generated decks may contain sensitive content processed on the local machine. <br>
Mitigation: Install and run the skill only where local processing of presentation files is acceptable, and review outputs before opening or distributing them. <br>


## Reference(s): <br>
- [Cjl Slides on ClawHub](https://clawhub.ai/0xcjl/cjl-slides) <br>
- [Style Previews](artifact/STYLE_PREVIEWS.md) <br>
- [Chart.js CDN Mirror Referenced by Skill](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with generated HTML, optional shell commands, and optional PPTX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated decks use a 16:9 slide layout and may include inline CSS, JavaScript, Chart.js charts, and extracted presentation assets.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
