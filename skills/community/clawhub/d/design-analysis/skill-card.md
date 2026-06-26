## Description: <br>
Design Analysis scans a local folder of design images and generates a structured, interactive HTML presentation report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jeasonxiang](https://clawhub.ai/user/Jeasonxiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and design reviewers use this skill to turn local UI screenshots or design drafts into a shareable HTML analysis presentation for review, documentation, or stakeholder walkthroughs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads images from the folder path supplied by the user. <br>
Mitigation: Run it against a dedicated design-assets folder and avoid including unrelated or sensitive files. <br>
Risk: The skill writes to the output HTML path supplied by the user and may replace an existing file. <br>
Mitigation: Choose a new output filename or back up any existing file before running the skill. <br>
Risk: The wrapper logs full input parameters, including optional context and custom section content. <br>
Mitigation: Do not pass secrets, private notes, or sensitive customer details in custom sections or context fields. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Jeasonxiang/design-analysis) <br>
- [HTML5 Presentation Patterns](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/Using_HTML5) <br>
- [CSS Flexible Box Layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout) <br>
- [README.md](artifact/README.md) <br>
- [OPENCLAW.md](artifact/OPENCLAW.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, HTML files] <br>
**Output Format:** [Markdown guidance and examples, shell commands, configuration parameters, and generated interactive HTML files with a JSON-like status summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local image files from a user-provided folder and writes a user-provided HTML output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
