## Description: <br>
Captures webpage screenshots from a provided URL, including full-page or viewport captures, mobile and tablet viewport presets, delayed rendering waits, and PNG output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, SEO practitioners, and content reviewers use this skill to capture rendered webpage screenshots for visual checks, archival snapshots, previews, and compatibility review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens user-provided URLs in a browser engine. <br>
Mitigation: Use explicit public HTTP/HTTPS targets and avoid private network, localhost, or authenticated pages unless that is the intended test. <br>
Risk: A custom screenshot output path can write PNG files to caller-selected locations. <br>
Mitigation: Review the output path before running and prefer a temporary or project-specific directory. <br>
Risk: Rendered pages may include sensitive content if authenticated or private pages are captured. <br>
Mitigation: Run only against pages approved for capture and avoid authenticated content unless the screenshot is expected to contain that data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-web-screenshot) <br>
- [Publisher profile](https://clawhub.ai/user/freedompixels) <br>
- [AISoBrand](https://aisobrand.com) <br>


## Skill Output: <br>
**Output Type(s):** [files, text, shell commands] <br>
**Output Format:** [PNG screenshot file plus JSON status text and command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports full-page or viewport-only capture, mobile and tablet viewport presets, custom output paths, and configurable wait time before capture.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
