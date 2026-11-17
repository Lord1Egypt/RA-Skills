## Description:

AI girlfriend selfie generator. Injects "NingYao" persona and generates images through ClawGirl API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blueoriginai](https://clawhub.ai/user/blueoriginai)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to route selfie, photo, and outfit-change requests to the ClawGirl service and return generated media or text responses to the agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and credentials are sent to an external ClawGirl service under broad selfie and outfit-change triggers.

Mitigation: Use a constrained environment, a limited API key, and avoid sending private or sensitive details through the skill.

Risk: The external service influences returned text and image download URLs.

Mitigation: Review returned content before relying on it and restrict execution to environments where unexpected remote outputs have limited impact.

Risk: Generated media can be saved locally.

Mitigation: Use a dedicated media directory and periodically review or remove generated files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blueoriginai/skills/clawgirl-selfie)
- [ClawGirl website](https://clawgirl.date)

## Skill Output:

**Output Type(s):** [text, files, shell commands, configuration]

**Output Format:** [Key-value shell output such as IMAGE_PATH=..., IMAGE_URL=..., DOWNLOAD_FAILED=true, or TEXT_RESPONSE_BASE64=...]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAWGIRL_API_KEY; may save generated media locally and may return base64-encoded text for the agent to decode.]

## Skill Version(s):

0.0.24 (source: server release metadata; artifact frontmatter is 0.0.20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
