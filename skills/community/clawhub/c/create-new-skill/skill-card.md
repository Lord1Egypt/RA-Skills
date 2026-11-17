## Description:

Create a new skill through a guided conversation for authoring a skill from scratch, choosing quick or full guidance, analyzing documentation to extract behavior patterns, generating a functional skill with proper workflow, and explaining how to make the new skill take effect.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaohaoxing](https://clawhub.ai/user/xiaohaoxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create new AgentSkills-compatible skills through a guided conversation. It helps define triggers, required tools, workflow steps, expected outputs, constraints, install location, and generated skill files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent skill files that change future agent behavior.

Mitigation: Install it only when persistent skill creation is intended, prefer the workspace install location by default, and review the preview before confirming file writes.

Risk: Documentation analysis may expose sensitive local content or process untrusted source material.

Mitigation: Avoid pointing the documentation step at sensitive local paths or untrusted sources.

Risk: Generated workflow guidance can be incorrect, incomplete, or misleading.

Mitigation: Review and scan generated skills before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaohaoxing/skills/create-new-skill)
- [Artifact skill definition](artifact/SKILL.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [CLI-style prompts and Markdown skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes SKILL.md and README.md after user confirmation; may analyze documentation sources when requested.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
