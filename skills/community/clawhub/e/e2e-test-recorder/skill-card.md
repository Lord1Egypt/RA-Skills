## Description: <br>
Records browser interactions for end-to-end tests and generates videos or GIFs with configurable encoding and annotations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[13770626440](https://clawhub.ai/user/13770626440) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and test engineers use this skill to record browser-driven end-to-end test flows and produce shareable MP4, GIF, or WebM evidence with optional annotations, watermarks, and test reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recordings may capture credentials, personal data, or sensitive application state. <br>
Mitigation: Use dummy accounts and sanitized data when recording, and review generated recordings before sharing. <br>
Risk: Bundled publishing scripts can use GitHub tokens, create public repositories, push code, tag releases, and force-push. <br>
Mitigation: Install in an isolated test project and avoid running auto-release, github-api-release, or deploy scripts unless publishing is intended and the GitHub token and git push behavior are fully understood. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/13770626440/e2e-test-recorder) <br>
- [Puppeteer documentation](https://pptr.dev/) <br>
- [puppeteer-screen-recorder](https://github.com/adrielcodeco/puppeteer-screen-recorder) <br>
- [FFmpeg](https://ffmpeg.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JavaScript, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local scripts that create MP4, GIF, WebM, and JSON report files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
