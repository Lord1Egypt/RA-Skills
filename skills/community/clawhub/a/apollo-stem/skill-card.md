## Description:

Apollo Stem helps an OpenClaw agent assess and plan self-renewal of its skill library while preserving useful experience.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to review whether an agent skill library needs updates, rebuilding, or new specialized skills. It is intended for capability maintenance workflows that balance core skill renewal with retention of existing useful experience.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad self-modification guidance could lead an agent to update, rebuild, or generate skills beyond the user's intent.

Mitigation: Require explicit user approval before update, generation, or rewrite steps, and keep triggers limited to clear user commands.

Risk: The bundled script reads OpenClaw workspace metadata and writes a local renewal status report.

Mitigation: Review the script before installation and run it only in workspaces where inspecting skill, workflow, and learning metadata is acceptable.

Risk: The security review notes limited disclosure and guardrails around local state inspection and reporting.

Mitigation: Document every file the skill reads or writes and serialize saved state in a controlled, reviewable location.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nic-yuan/skills/apollo-stem)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash script output and JSON status data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script writes a local OpenClaw renewal status JSON file.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
