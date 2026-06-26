## Description: <br>
Control IKEA Dirigera smart-home devices, check device status, manage lights and outlets, trigger scenes, monitor batteries, and help find the hub IP address or generate an API token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Falderebet](https://clawhub.ai/user/Falderebet) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to operate IKEA Dirigera smart-home devices through a Dirigera hub, including device discovery, status checks, light and outlet control, scene activation, battery monitoring, and hub setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control real IKEA Dirigera devices, including lights, outlets, and whole-home scenes. <br>
Mitigation: Require explicit user confirmation before broad or disruptive actions such as turning off all outlets, all lights, or triggering whole-home scenes. <br>
Risk: The token generation workflow stores a local `dirigera_token.txt` hub token. <br>
Mitigation: Treat the token file as a secret, store it only in a private location, and delete it after use when persistence is not required. <br>
Risk: The skill may be used through a Cloudflare tunnel to reach the smart-home environment. <br>
Mitigation: Restrict tunnel access and avoid exposing the hub or control endpoint to unauthorized users. <br>


## Reference(s): <br>
- [Dirigera API Complete Reference](references/api.md) <br>
- [Common Usage Patterns](references/patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Falderebet/dirigera-control) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local token files and smart-home control commands that affect physical devices.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
