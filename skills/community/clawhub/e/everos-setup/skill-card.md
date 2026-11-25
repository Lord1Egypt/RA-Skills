## Description:

Set up, verify, or repair EverOS memory for OpenClaw. Use when the user asks to install EverOS or the EverOS memory plugin, wants OpenClaw to remember things across sessions with a self-hosted EverOS, or reports that EverOS memory is not recalling or not saving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[everos-ai](https://clawhub.ai/user/everos-ai)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to install and configure EverOS memory, confirm that recall and saving work, and troubleshoot common setup issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented npm install command does not pin a package version, so the installed package may change between installs.

Mitigation: Review the publisher and package version before installation, and pin an approved version when reproducibility matters.

Risk: The security scan was partial because a local path-like reference could not be resolved.

Mitigation: Review the unresolved reference and relevant package contents before relying on the scan as a complete assessment.

Risk: Conversation text is read by the local EverOS server and sent to the LLM and embedding providers configured by the user.

Mitigation: Obtain the user's consent and have them review the configured providers and their data handling before enabling conversation access.

## Reference(s):

- [OpenClaw EverOS plugin](https://github.com/EverMind-AI/Plugins/tree/main/openclaw)
- [EverOS project](https://github.com/EverMind-AI/EverOS)
- [EverOS Setup ClawHub release](https://clawhub.ai/everos-ai/skills/everos-setup)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers installation, consent, verification, troubleshooting, and optional settings.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
