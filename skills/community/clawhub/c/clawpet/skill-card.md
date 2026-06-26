## Description: <br>
OpenClaw pet companion skill. Manage adopted pets, run interactions, and produce pet image prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yazelin](https://clawhub.ai/user/yazelin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to manage a virtual pet companion, check pet state, run care interactions, and produce prompts for pet images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wrapper can run an unpinned CLI dependency from the referenced GitHub repository. <br>
Mitigation: Install only after trusting the referenced repository and review the dependency before use. <br>
Risk: Image workflows can send generated media to Telegram and include hardcoded local paths that may not match the user's environment. <br>
Mitigation: Confirm Telegram sharing is intended and update local paths before running image workflows. <br>


## Reference(s): <br>
- [clawpet package source](https://github.com/yazelin/clawpet.git) <br>
- [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) <br>
- [ClawHub skill page](https://clawhub.ai/yazelin/clawpet) <br>
- [Publisher profile](https://clawhub.ai/user/yazelin) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands and plain text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate pet image prompt text and may guide downstream image generation or Telegram sharing when those tools are available.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
