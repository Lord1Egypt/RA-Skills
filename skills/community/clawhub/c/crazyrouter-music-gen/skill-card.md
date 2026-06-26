## Description: <br>
AI music generation via Crazyrouter API using Suno. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xujfcn](https://clawhub.ai/user/xujfcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate music or songs from text prompts, optional lyrics, style, title, and model settings through a Crazyrouter-compatible Suno endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, lyrics, titles, and the Crazyrouter API key are sent to the configured Crazyrouter-compatible service. <br>
Mitigation: Use non-sensitive inputs and install only when that data sharing is acceptable. <br>
Risk: CRAZYROUTER_BASE_URL can direct requests to a configured compatible endpoint. <br>
Mitigation: Leave CRAZYROUTER_BASE_URL unset or verify that it points to a trusted service. <br>
Risk: Generated audio can be written to a user-provided local output path. <br>
Mitigation: Choose output paths that will not overwrite important files. <br>


## Reference(s): <br>
- [Crazyrouter](https://crazyrouter.com) <br>
- [Crazyrouter API base](https://crazyrouter.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated audio may be saved as a local file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CRAZYROUTER_API_KEY and may use CRAZYROUTER_BASE_URL when configured.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
