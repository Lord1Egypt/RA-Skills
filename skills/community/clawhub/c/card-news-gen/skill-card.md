## Description: <br>
Generates Instagram and social carousel card-news assets from a topic by planning content, creating HTML designs, capturing Playwright screenshots, and preparing upload-ready images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gyeuun97](https://clawhub.ai/user/gyeuun97) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and agent operators use this skill to turn a topic into an Instagram-style carousel with planned card copy, HTML/CSS layout, screenshots, captions, and upload preparation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated images or captions could be published or sent externally before the user has checked them. <br>
Mitigation: Review every generated image and caption, then confirm the target account or recipient before upload or delivery. <br>
Risk: Publishing and sharing steps may use local credentials or external delivery channels. <br>
Mitigation: Run publishing steps only in an environment where the relevant account credentials and recipients have been intentionally approved. <br>
Risk: The JPEG helper invokes a shell conversion path and is not appropriate for untrusted output paths. <br>
Mitigation: Avoid the --jpeg helper with untrusted paths until the conversion command is made safer, or convert files with a reviewed local workflow. <br>


## Reference(s): <br>
- [Pretendard Webfont CSS](https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, and shell command snippets that produce image files and captions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces carousel card images such as PNG or JPEG screenshots plus caption text for review before publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
