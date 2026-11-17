## Description:

Caches user-specified context fragments in a file to avoid redundant processing and enable reuse across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaoxiang616](https://clawhub.ai/user/shaoxiang616)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to save explicitly selected context fragments and reuse them across later sessions to reduce repeated setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and reloads conversation context in a persistent plaintext file without sufficient scoping, review, or retention controls.

Mitigation: Use only explicit fragment selection, avoid storing secrets or client data, review cached content before reuse, and avoid startup auto-loading unless cached content is treated as untrusted reference text.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent guidance for saving, listing, clearing, and optionally preloading cached context fragments.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
