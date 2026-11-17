## Description:

Art Critique helps artists get dialogue-based critique for work in image, text, audio, video, installation, performance, or mixed media, using close observation, open questions, session notes, and selected art-theory or art-history references to deepen the conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iiiantower](https://clawhub.ai/user/iiiantower)

### License/Terms of Use:

MIT-0

## Use Case:

External users, especially artists and creative practitioners, use this skill to receive reflective critique on in-progress or finished artwork without grading or prescriptive correction. The skill supports multi-round dialogue, medium-specific intake, local session notes, and concise contextual associations from a curated art reference library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted artwork and critique history may be stored locally in art-critique-sessions folders.

Mitigation: Use the skill only in workspaces where local storage of the artwork and critique notes is acceptable, confirm the write location before starting in shared or sensitive environments, and delete session folders when they are no longer needed.

Risk: The skill may copy submitted artwork files into the local session folder.

Mitigation: Avoid submitting confidential or rights-restricted artwork unless local copies are permitted, and remove copied files after the critique if retention is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iiiantower/skills/art-critique-skill)
- [Agent Skills overview](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview)
- [Association engine](references/association-engine.md)
- [Session notes template](references/session-notes-template.md)
- [Note frameworks](references/note-frameworks/README.md)
- [Four steps critique framework](references/note-frameworks/four-steps.md)
- [Time-based media critique framework](references/note-frameworks/time-based-media.md)
- [Demo walkthrough critique framework](references/note-frameworks/demo-walkthrough.md)
- [Curated art reference library](references/library/index.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Conversational text and Markdown session notes in local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a unique local art-critique-sessions folder for each new critique session and may copy submitted artwork into that folder.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
