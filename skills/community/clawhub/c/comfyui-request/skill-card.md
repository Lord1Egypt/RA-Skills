## Description:

Send a workflow request to ComfyUI and return image results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xtopher86](https://clawhub.ai/user/xtopher86)

### License/Terms of Use:


## Use Case:

Developers and creators use this skill to submit ComfyUI workflow JSON to a configured ComfyUI server and receive generated image results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ComfyUI credentials and workflow contents may be sent over unencrypted HTTP.

Mitigation: Use localhost or an isolated private network, and avoid basic authentication unless the service is protected by a trusted TLS proxy or the skill is updated to support HTTPS and reject plaintext authenticated requests.

Risk: The skill depends on a user-configured ComfyUI network path.

Mitigation: Install only when the configured ComfyUI endpoint is trusted and reachable from the runtime environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xtopher86/skills/comfyui-request)
- [ClawHub publisher profile](https://clawhub.ai/user/xtopher86)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON response with success status, prompt identifiers, image metadata, and image URLs or error details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a reachable ComfyUI server and workflow JSON input.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
