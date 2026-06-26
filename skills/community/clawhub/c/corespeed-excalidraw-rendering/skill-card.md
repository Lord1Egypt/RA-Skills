## Description: <br>
Render Excalidraw (.excalidraw) files to PNG images and take screenshots of web pages using headless Chrome via the brow CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zypher-agent](https://clawhub.ai/user/zypher-agent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to render Excalidraw diagrams as PNG files and capture website screenshots through the brow CLI. It is useful when a workflow needs a saved image artifact rather than an in-chat diagram or page preview. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup path uses an unpinned remote installer for the brow CLI and downloads a managed Chrome browser. <br>
Mitigation: Install only after trusting the brow CLI source, review the installer in environments that require change control, and run the managed browser install in an approved local cache. <br>
Risk: Screenshot commands can capture sensitive page content when pointed at authenticated or private URLs. <br>
Mitigation: Use explicit, user-chosen files, URLs, and output paths, and avoid screenshotting sensitive authenticated pages unless local capture is intended. <br>


## Reference(s): <br>
- [Corespeed brow CLI](https://github.com/corespeed-io/brow) <br>
- [Corespeed skills support](https://github.com/corespeed-io/skills/issues) <br>
- [Corespeed](https://corespeed.io) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and saved image path guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides rendering to local PNG files and instructs the agent to report the saved path without reading generated images back.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
