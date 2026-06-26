## Description: <br>
Capture Website helps an agent take command-line screenshots of web pages and save or share the resulting image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silencezx007](https://clawhub.ai/user/silencezx007) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to capture screenshots of public or intended web pages, save them to a workspace path, and optionally share them through supported messaging channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshots can capture sensitive or private page content and make it shareable. <br>
Mitigation: Capture only URLs intended for sharing and review screenshots before sending them through Discord or Feishu. <br>
Risk: The skill depends on a globally installed npm CLI. <br>
Mitigation: Install capture-website-cli only from a trusted source and prefer a pinned version when possible. <br>
Risk: Screenshots are saved to local storage by default. <br>
Mitigation: Choose an appropriate output path and clean up retained files when local retention is not desired. <br>


## Reference(s): <br>
- [Capture Website on ClawHub](https://clawhub.ai/silencezx007/capture-website) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, files, guidance] <br>
**Output Format:** [Markdown with inline shell commands and local image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local screenshot files, typically PNG or JPEG; sharing through Discord or Feishu should happen only after reviewing the image.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
