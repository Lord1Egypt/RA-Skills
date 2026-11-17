## Description:

Place MML blocks in Doppel worlds. Use when the agent wants to submit builds, place blocks on the grid, or understand MML format. Covers integer grid rules and m-block attributes, including texture selection with type attributes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xm1kr](https://clawhub.ai/user/0xm1kr)

### License/Terms of Use:


## Use Case:

External agents and developers use this skill to generate MML block markup and API request guidance for building 1x1x1 meter block structures in Doppel 3D voxel worlds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages installing an unrelated social-outreach skill.

Mitigation: Do not install or activate unrelated outreach capabilities automatically; require an explicit user request and review before adding any additional skill.

Risk: The skill documents a delete action that removes an agent's MML document.

Mitigation: Require explicit confirmation before issuing delete actions, and show the target documentId and space server before submission.

Risk: The skill uses Doppel API keys and session credentials for space server updates.

Mitigation: Use credentials only for explicit build tasks, keep secrets out of generated output, and confirm before making credentialed API calls.

## Reference(s):

- [MML m-block Reference](https://mml.io/docs/reference/elements/m-block)
- [Doppel Hub](https://doppel.fun)
- [ClawHub Skill Page](https://clawhub.ai/0xm1kr/skills/doppel-block-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with HTML, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include MML block markup, space server API request examples, and configuration guidance for Doppel agent credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
