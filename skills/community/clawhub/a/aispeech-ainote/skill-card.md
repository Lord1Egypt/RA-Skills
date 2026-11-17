## Description:

Helps OpenClaw users access notes, todos, personal search, label knowledge bases, and hotwords for Aispeech office notebooks and recording cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fairylong](https://clawhub.ai/user/fairylong)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users can find and summarize personal meeting notes, manage todos and labels, search their knowledge base, and manage hotwords for supported Aispeech office devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A long-lived access token is stored in the OpenClaw environment and could expose personal notes and tasks if disclosed.

Mitigation: Limit access to ~/.openclaw/.env and grant only the note, todo, label, knowledge, and hotword scopes needed.

Risk: Delete and broad write actions can change or remove personal content without clear confirmation safeguards.

Mitigation: Confirm the exact items and intended changes with the user before deletes or broad writes.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/fairylong/skills/aispeech-ainote)
- [Aispeech office service](https://aiworks.cn)
- [API reference](artifact/api_reference.md)
- [API details](artifact/references/api-details.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include note summaries, todo details, and personal search results.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
