## Description:

Carrusel del radar F100K turns a selected trend or user-provided topic into an Instagram carousel workflow with a script, caption, rendered slides, Telegram approval gates, and optional publication through a connected Instagram account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, social media operators, and marketing teams use this skill to turn radar-selected trends or requested topics into reviewed Instagram carousel posts. The workflow supports drafting, rendering, revision, handoff, and publication only after explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can use local brand/profile materials, Gemini image generation, Telegram review messages, and a connected Composio Instagram account.

Mitigation: Install only in environments where those local materials, companion skills, and connected accounts are trusted and intended for this workflow.

Risk: Instagram publication is a user-visible action that cannot be undone by the agent once published.

Mitigation: Keep the final explicit publish phrase requirement in place and review the rendered slides and caption before approving publication.

Risk: A publication run interrupted near the final publish step could create confusion about whether a post already went live.

Mitigation: Use the stored state and recent-post checks described by the artifact before attempting to publish again.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/carrusel-del-radar-f100k)
- [formula100k publisher profile](https://clawhub.ai/user/formula100k)
- [estado.schema.json](references/estado.schema.json)
- [mensajes-telegram.md](references/mensajes-telegram.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files, API calls]

**Output Format:** [Markdown guidance with JSON state, shell command snippets, carousel image files, caption text, and publication status messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains one active carousel state at a time and requires explicit approval before publication.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
