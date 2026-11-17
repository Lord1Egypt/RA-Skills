## Description:

Generate AI podcast episodes from PDFs, text, notes, and links using MagicPodcast in OpenClaw, with two-person dialogue audio, custom language selection, podcast links, and dashboard progress tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoliuzhu](https://clawhub.ai/user/chaoliuzhu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn PDF URLs or pasted text into AI-generated podcast episodes through MagicPodcast. The skill guides topic, source, language, confirmation, creation, and completion-link retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected PDF URLs or pasted text are sent to MagicPodcast for external processing.

Mitigation: Ask for explicit confirmation before generation and avoid sensitive or confidential documents unless external processing has been approved.

Risk: Podcast generation depends on a MagicPodcast API key and remote service availability.

Mitigation: Verify MAGICPODCAST_API_URL and MAGICPODCAST_API_KEY are configured before use, and surface API errors directly to the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chaoliuzhu/skills/delonix-ai-podcast)
- [Publisher profile](https://clawhub.ai/user/chaoliuzhu)
- [MagicPodcast homepage](https://www.magicpodcast.app)
- [MagicPodcast OpenClaw API key setup](https://www.magicpodcast.app/openclaw)
- [MagicPodcast dashboard](https://www.magicpodcast.app/app)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and generated podcast links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, MAGICPODCAST_API_URL, and MAGICPODCAST_API_KEY; returns MagicPodcast dashboard and share URLs when available.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
