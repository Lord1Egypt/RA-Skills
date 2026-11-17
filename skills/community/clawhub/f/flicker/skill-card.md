## Description:

Flicker is an ASCII pet companion that can generate pet attributes, display animated ASCII pet frames, and add short snarky comments tied to the conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jofiction918](https://clawhub.ai/user/jofiction918)

### License/Terms of Use:

MIT-0

## Use Case:

External users install this skill to add a lightweight ASCII pet persona to an agent conversation, generate or view pet attributes, and receive occasional short comments based on chat context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run a local Node.js generator and create or update local pet.json data.

Mitigation: Review the bundled script and install only in a workspace where local pet data creation is acceptable.

Risk: The pet persona may occasionally interrupt assistant replies with snarky comments.

Mitigation: Use explicit commands or disable the skill if automatic comments are distracting or inappropriate for the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jofiction918/skills/flicker)
- [Publisher profile](https://clawhub.ai/user/jofiction918)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown chat responses with ASCII art, short text comments, and JSON pet data from the local generator script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local pet.json data file and may occasionally add one short pet comment after an assistant response.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
