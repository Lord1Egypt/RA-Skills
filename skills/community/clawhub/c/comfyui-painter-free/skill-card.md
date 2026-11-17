## Description:

ComfyUI画图基础版 helps agents control a local ComfyUI API to generate text-to-image PNG files on a local GPU with basic model aliases, manual generation parameters, lifecycle checks, and idle shutdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and agent users use this skill to run basic local ComfyUI text-to-image workflows, choose among a small set of model aliases, tune core parameters manually, and receive generated image file paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad local file, command, and network-related authority for ComfyUI workflows.

Mitigation: Install only in a trusted agent environment and review the skill before granting command execution or local read/write access.

Risk: The optional callback_url can send completion data to a destination outside the local workspace.

Mitigation: Use callback_url only with trusted HTTPS endpoints and omit it when callback delivery is not required.

Risk: Generated prompts and image outputs are stored locally and may persist after a session.

Mitigation: Review and clean temporary output directories according to the user's retention and privacy requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/comfyui-painter-free)
- [Artifact homepage](https://skillhub.cn/skill/)

## Skill Output:

**Output Type(s):** [Files, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with Python and shell snippets, JSON status examples, and PNG image file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated prompts and images are stored locally and may require manual cleanup.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
