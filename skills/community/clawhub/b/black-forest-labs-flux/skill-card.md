## Description: <br>
Generates images with Black Forest Labs FLUX models through the direct BFL API using a local shell script and BFL API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gamaleldientarek](https://clawhub.ai/user/gamaleldientarek) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate images through the Black Forest Labs API when a direct BFL API key and FLUX model endpoint are required instead of another image provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and image parameters are sent to Black Forest Labs using the configured BFL API key. <br>
Mitigation: Avoid including secrets or sensitive personal data in prompts and use the skill only when sending this data to Black Forest Labs is acceptable. <br>
Risk: The script sources /root/.clawdbot/.env before calling the API. <br>
Mitigation: Keep that environment file trusted and limit access to credentials stored there. <br>
Risk: Generated image files are written to a local output path. <br>
Mitigation: Choose output paths intentionally and review generated files before sharing or reusing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gamaleldientarek/black-forest-labs-flux) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and local generated image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses BFL_API_KEY, prompt text, an optional output file path, and optional BFL_MODEL, BFL_WIDTH, and BFL_HEIGHT environment overrides.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
