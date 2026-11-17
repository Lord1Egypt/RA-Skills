## Description:

File system manager for ChatMOSP that creates MSR and KMC task directories, generates task names, and applies scoped file-operation checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanyangye](https://clawhub.ai/user/sanyangye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers using ChatMOSP use this skill to create standardized MSR and KMC task directory structures, generate task names, and prepare handoffs between companion simulation skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and copy task files under mosp-for-chatMOSP/OUTPUT/.

Mitigation: Review destination paths and overwrite intent before allowing file writes.

Risk: Companion-skill guidance includes unpinned installation sources and a GitHub fallback.

Mitigation: Install companion skills only from trusted, verified, preferably pinned ClawHub sources.

Risk: Documentation inconsistencies may affect cross-skill handoffs.

Mitigation: Confirm the intended ChatMOSP workflow and required companion skills before relying on automated handoffs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sanyangye/skills/chatmosp-file-organizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides creation and organization of MSR and KMC task files under mosp-for-chatMOSP/OUTPUT/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
