## Description:

Adversarial self-improvement for AI agents. Reduces hallucinations through Agent vs Anti-Agent debate loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zedit42](https://clawhub.ai/user/zedit42)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to set up an Agent and Anti-Agent debate loop for self-critique, code review, risk assessment, and validation-heavy work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup script creates local state, prompt, heartbeat snippet, and output files in the selected directory.

Mitigation: Install into a dedicated directory and review the generated prompt files before adding the heartbeat snippet to an agent workflow.

Risk: An active debate loop can consume extra agent time and tokens if iteration limits are too high.

Mitigation: Set max_iterations to a small value before first use and stop the loop when further critique is no longer useful.

Risk: The Agent and Anti-Agent personas use the same underlying model, so shared model blind spots can remain.

Mitigation: Treat the loop as self-critique, not an independent review, and require human validation for deployment, financial, or safety-relevant decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zedit42/skills/arena-system)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated prompt/configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local state, prompt, heartbeat snippet, and output directories for an alternating debate loop.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
