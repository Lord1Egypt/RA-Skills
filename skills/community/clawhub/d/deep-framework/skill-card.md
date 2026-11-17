## Description:

Implementation of the Dynamic Ethical Entity Personality (D.E.E.P.) v2 Framework.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dacptn](https://clawhub.ai/user/dacptn)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to create persistent personality-memory files and run D.E.E.P. alignment, synchronization, and action-check commands for agent identity and continuity workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent personality and memory files may contain sensitive personal, relationship, or behavioral state.

Mitigation: Do not store secrets, credentials, private relationship data, or authoritative safety rules in D.E.E.P. memory files.

Risk: deep_triple_check always approves actions without real validation.

Mitigation: Treat check output as advisory and independently review critical actions until validation is implemented and fails closed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dacptn/skills/deep-framework)
- [personality_template.md](artifact/personality_template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The sync command writes a local soul_vault.json file from personality-memory Markdown files.]

## Skill Version(s):

2.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
