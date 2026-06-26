## Description: <br>
Configure AI personality using the AURA protocol (HEXACO-based). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phiro56](https://clawhub.ai/user/phiro56) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to configure a workspace personality profile, tune directness, autonomy, and response style, and persist those preferences in an AURA.yaml file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High autonomy values or persistent personality settings could make an agent act with less confirmation than a workspace expects. <br>
Mitigation: Review AURA.yaml before relying on it, choose autonomy values deliberately, and reset the profile when the workspace no longer needs those settings. <br>
Risk: Adding the startup-loading rule to AGENTS.md makes personality settings persist across sessions in that workspace. <br>
Mitigation: Only add the startup-loading rule in trusted workspaces and inspect the local AURA.yaml before applying it. <br>


## Reference(s): <br>
- [ClawHub AURA package page](https://clawhub.ai/phiro56/aura) <br>
- [AURA protocol specification](https://github.com/phiro56/AURA) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates, reads, or removes a workspace AURA.yaml personality configuration when invoked by the user.] <br>

## Skill Version(s): <br>
0.1.0-beta.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
