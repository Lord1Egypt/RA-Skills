## Description: <br>
Create and manage Canva designs, upload assets, export content, and manage brand templates via the Canva Connect API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to coordinate Canva design workflows from chat, including design management, asset uploads, exports, and brand template operations through a connected Canva account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to a user's Canva account through ClawLink and can perform write actions on Canva designs, assets, exports, and brand templates. <br>
Mitigation: Review ClawLink's trust posture, connect only the intended Canva account, and approve only actions that match the specific Canva resource and change requested. <br>
Risk: Write or destructive operations may alter Canva content or team brand assets. <br>
Mitigation: Use the live tool catalog and preview flow before execution, confirm the target resource and intended effect with the user, and stop if the preview does not match the request. <br>


## Reference(s): <br>
- [Canva Developer Documentation](https://www.canva.com/developers/) <br>
- [Canva Connect API](https://www.canva.com/developers/docs/connect/) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes OAuth connection guidance, live tool discovery steps, and confirmation guidance for write actions.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
