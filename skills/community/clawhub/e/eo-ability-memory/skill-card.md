## Description:

EO Ability: Memory provides proactive cross-session memory for user preferences, mentor requirements, project context, and formatting rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[467718584](https://clawhub.ai/user/467718584)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to save, load, search, update, and forget memory entries so user preferences, academic research context, administrative context, and formatting requirements can carry across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cross-session memory can retain privacy-sensitive information, including user preferences, project context, negotiations, or research details.

Mitigation: Confirm where persistent memories and indexes are stored, review retention and deletion controls, and avoid saving secrets, regulated data, credentials, or confidential negotiations without explicit retention and access controls.

Risk: Persistent memories may be loaded into later sessions outside the intended project or context.

Mitigation: Scope memory use by project where supported and review, delete, or disable stored memories when they are no longer relevant.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/467718584/skills/eo-ability-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with TypeScript interface examples and inline command-style examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Memory operations described include save, load, search, forget, and update; persistent cross-session behavior depends on EO plugin support.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
