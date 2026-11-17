## Description:

Lianke Print Box guides agents through remote printing, printer status checks, print job management, and document scanning for Lianke cloud print box devices using the lk-print CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nullying](https://clawhub.ai/user/nullying)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers with Lianke cloud print box devices use this skill to install and authenticate the lk-print CLI, check device and printer status, submit or cancel print jobs, and create or retrieve scans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install command uses a mutable third-party Git package for lk-print.

Mitigation: Prefer a pinned or independently verified lk-print release before installing or running commands.

Risk: The skill handles ApiKey, DeviceId, and DeviceKey credentials.

Mitigation: Treat printer credentials as secrets and provide them only through trusted authentication or environment-variable flows.

Risk: The skill can submit print jobs and scan documents through Lianke devices.

Mitigation: Use it only with Lianke devices you control and only for documents you are authorized to print or scan.

## Reference(s):

- [Lianke open platform](https://open.liankenet.com)
- [lk-print install package from ClawHub metadata](https://github.com/liankenet/ai-lk-print-box.git)
- [ClawHub skill page](https://clawhub.ai/nullying/skills/ai-lk-print-box)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the lk-print CLI plus ApiKey, DeviceId, and DeviceKey credentials for Lianke devices.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
