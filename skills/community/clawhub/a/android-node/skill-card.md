## Description:

Convert Android phones running Termux into local Ollama inference nodes for AI task processing without cloud or special hardware.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to provision Android phones running Termux as local Ollama worker nodes and route AI inference jobs to healthy devices on a trusted network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote setup and downloaded binaries can execute unreviewed code during installation.

Mitigation: Use the inspected local setup code, avoid remote curl-to-bash installation, and verify downloaded binaries before running them.

Risk: Phone nodes expose local Ollama inference over the network, and sensitive prompts could be sent without authenticated encryption.

Mitigation: Run nodes only on a trusted isolated network or authenticated encrypted overlay, and do not send sensitive prompts unless transport protection is in place.

## Reference(s):

- [Android Node on ClawHub](https://clawhub.ai/albionaiinc-del/skills/android-node)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
