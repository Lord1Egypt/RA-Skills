## Description:

Start/stop/status for a ComfyUI instance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xtopher86](https://clawhub.ai/user/xtopher86)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to check whether a configured local ComfyUI instance is reachable. The release documentation also describes run and stop actions, but the security evidence advises treating this version as a status-check skill only.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation describes run and stop actions, while the security evidence says this version should not be relied on to start or stop ComfyUI.

Mitigation: Use this release for status checks only, and verify run or stop behavior in a future release before depending on those actions operationally.

Risk: The documentation mentions optional basic-auth environment variables, but the current evidence does not show protected credential handling for this version.

Mitigation: Avoid storing COMFYUI_USER or COMFYUI_PASS in the skill .env file unless a future version actually uses them and documents how they are protected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xtopher86/skills/comfyui-runner)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [JSON status response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports health-check success, HTTP status, host, port, or unreachable error details; run and stop actions return an unsupported-action response in this version.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
