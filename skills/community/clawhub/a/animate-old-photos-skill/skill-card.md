## Description: <br>
Animate old photos into AI-generated 5-second MP4 videos using the Animate Old Photos API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shurshanx](https://clawhub.ai/user/shurshanx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to authenticate with Animate Old Photos, upload a local JPEG or PNG image, submit an animation job, poll for completion, and download the resulting MP4. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends the selected photo, optional motion prompt, and API credentials to Animate Old Photos and its storage provider. <br>
Mitigation: Use an environment variable or secret manager for the API key, avoid sensitive photos unless the provider is trusted, and review the provider's privacy and retention practices. <br>
Risk: Each animation uses paid service credits. <br>
Mitigation: Confirm the 3-credit charge and available balance with the user before submitting each animation job. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shurshanx/animate-old-photos-skill) <br>
- [Animate Old Photos](https://animateoldphotos.org/) <br>
- [Animate Old Photos API Reference](references/animate-old-photos-api.md) <br>
- [Animate Old Photos MCP Endpoint](https://animateoldphotos.org/api/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown guidance with Bash commands and a downloaded MP4 file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a 5-second MP4 video; requires a local JPEG or PNG image, an API key, and 3 credits per animation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
