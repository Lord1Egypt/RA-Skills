## Description: <br>
Automates Doubao Web with Playwright to generate images from prompts and save the resulting image locally. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[atmosphere16happy](https://clawhub.ai/user/atmosphere16happy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI assistant users can use this skill to generate Doubao Web images from natural-language prompts, with optional aspect ratio, quality, and output-path controls. The source README frames the project as programming learning, Playwright automation testing research, and technical exchange only. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates a logged-in Doubao browser session and stores reusable session data locally. <br>
Mitigation: Use a dedicated low-risk account where possible, review local session storage, and delete ~/.doubao-web-session when the skill is no longer needed. <br>
Risk: The release security summary notes possible platform terms issues from bypassing controls or obtaining watermark-free originals. <br>
Mitigation: Confirm Doubao Web terms and content rules before use, and prefer an official API when available. <br>
Risk: The skill writes generated images and may create debug files on the local filesystem. <br>
Mitigation: Choose explicit output paths, avoid sensitive directories, and remove generated or debug files after review. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/atmosphere16happy/doubao-web-image) <br>
- [Doubao Web chat](https://www.doubao.com/chat/) <br>
- [Project repository link from README](https://github.com/pjf6568/doubao-web-image) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Text confirmation with local image file paths and command-line parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create image files at the requested output path and store browser session data locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
