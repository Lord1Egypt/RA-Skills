## Description: <br>
Generates and downloads ChatGPT images through a remote Camoufox browser reachable over a tailnet, using the browser session to submit prompts and capture downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lotfinity](https://clawhub.ai/user/lotfinity) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to generate ChatGPT images through a trusted remote residential browser session and save the resulting image locally when local IP reputation or direct image downloads are unreliable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generated images pass through a remote Camoufox browser and ChatGPT session. <br>
Mitigation: Use only with a trusted remote browser host and session, and avoid sensitive prompts unless that routing is acceptable. <br>
Risk: Generated images are saved locally. <br>
Mitigation: Choose an output path you can manage and delete generated files when they are no longer needed. <br>
Risk: The workflow depends on a specific remote browser endpoint and current ChatGPT image-generation UI behavior. <br>
Mitigation: Confirm the remote browser is reachable before use and inspect the helper script if selectors or download behavior need adjustment. <br>


## Reference(s): <br>
- [ClawHub Skill Release](https://clawhub.ai/lotfinity/chatgpt-image-tailnet) <br>
- [ChatGPT](https://chatgpt.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; the helper script prints JSON status and saves a PNG image file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-driven; optional base URL, user, session, output path, and timeout parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
