## Description:

Generate music using Volcengine Imagination API. Supports vocal songs, instrumental BGM, and lyrics generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate vocal songs, instrumental background music, soundtracks, or lyrics through Volcengine's Imagination API and return generated audio URLs or lyrics to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts, lyrics, and music metadata to Volcengine and may incur API charges.

Mitigation: Use it only with approved content and billing expectations; avoid sensitive prompts unless the Volcengine account and data handling terms are acceptable.

Risk: The skill requires VOLCENGINE_ACCESS_KEY and VOLCENGINE_SECRET_KEY and includes guidance that could lead an agent to persist credentials in workspace files.

Mitigation: Configure credentials through a secure secret store or process-scoped environment variables, and do not write them into repository or workspace files.

Risk: The security verdict is suspicious due to credential-handling concerns and unpinned dependencies.

Mitigation: Review the skill before deployment and pin dependencies to approved versions for production use.

## Reference(s):

- [Volcengine Music Generation Parameters](references/parameters.md)
- [Volcengine Music Generation Docs](https://www.volcengine.com/docs/84992)
- [Volcengine API Signature Guide](https://www.volcengine.com/docs/6369/67269)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON result fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns an audio_url for song or BGM generation, lyrics for lyrics mode, or a task_id for timeout follow-up.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
