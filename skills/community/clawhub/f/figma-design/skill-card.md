## Description: <br>
Read files, manage comments, extract design tokens, download images, and create webhooks in Figma via the Figma REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, developers, and product teams use this skill to inspect Figma design files, export assets, manage comments and reactions, extract design tokens, and configure webhooks through an authenticated Figma connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an authenticated Figma connection and can access files, comments, resources, and webhooks available to the connected account. <br>
Mitigation: Install and connect it only for the intended Figma account, verify the live Figma integration before use, and rely on the documented scoped connection flow. <br>
Risk: Write-capable operations can create, update, or delete comments, reactions, and webhooks. <br>
Mitigation: Preview unfamiliar or write-capable calls, confirm the target resource and intended effect with the user, and execute only after the preview matches the request. <br>
Risk: Some webhook operations require team admin permissions or edit access and can affect event delivery for a file, project, or team. <br>
Mitigation: Confirm the webhook scope, endpoint, and permission level before creating, updating, or deleting webhooks. <br>
Risk: Scanner guidance notes clean telemetry but recommends deliberate use of high-authority authenticated workflows and setup commands. <br>
Mitigation: Review install, gateway, and authenticated tool commands before running them, especially in sensitive repositories or workspaces. <br>


## Reference(s): <br>
- [Figma API Overview](https://www.figma.com/developers/api) <br>
- [Figma REST API Reference](https://www.figma.com/developers/api/rest) <br>
- [Figma Webhooks](https://www.figma.com/developers/api/webhooks) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls, Code] <br>
**Output Format:** [Markdown guidance with bash command examples, JSON tool parameters, and returned Figma API data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool calls may produce Figma file JSON, comments, webhook status, exported image files or URLs, design tokens, and Tailwind configuration.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
