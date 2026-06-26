## Description: <br>
A powerful OpenClaw skill for managing and automating GPU container instances on the CFGPU cloud platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[r600a-code](https://clawhub.ai/user/r600a-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and content creators use this skill to discover CFGPU regions, GPU types, and images, then create, inspect, start, stop, release, or reimage GPU cloud instances through guided shell workflows and API examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist a CFGPU API token locally in a token file or shell startup file. <br>
Mitigation: Use a limited or short-lived token, avoid setup-env.sh unless plaintext local persistence is acceptable, and remove CFGPU_API_TOKEN entries from shell startup files when no longer needed. <br>
Risk: The skill can perform high-impact instance actions, including create, stop, release, and change-image operations that may affect cost, availability, or data. <br>
Mitigation: Manually verify instance IDs, billing implications, image choices, and backups before running release or change-image operations. <br>


## Reference(s): <br>
- [CFGPU API Reference](references/api-reference.md) <br>
- [CFGPU Platform](https://cfgpu.com) <br>
- [CFGPU API Base](https://api.cfgpu.com) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [ClawHub Release Page](https://clawhub.ai/r600a-code/cfgpu-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, curl examples, and JSON request or response snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that call CFGPU APIs with a user-provided CFGPU_API_TOKEN.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
