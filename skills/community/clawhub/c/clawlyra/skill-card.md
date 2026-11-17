## Description:

Give your OpenClaw agent a face and a voice: reply as Lyra, a warm 3D avatar companion, and emit her inline performance tags so the self-hosted Lyra app speaks and performs your replies live: expressions, gestures, scene changes, lip-synced voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freespirits](https://clawhub.ai/user/freespirits)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to make an agent respond as Lyra and emit avatar performance tags for a separately running Lyra sidecar app. It is intended for conversational avatar sessions where spoken prose, expressions, gestures, scene changes, and voice delivery cues are desired.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The separate Lyra sidecar uses an OpenClaw gateway token that could grant access if exposed.

Mitigation: Keep OPENCLAW_TOKEN private, store it only in a local uncommitted .env file, and rotate the token if it is exposed.

Risk: The skill intentionally changes agent replies into spoken prose with inline performance tags, which can break workflows that require JSON, Markdown, or other machine-readable output.

Mitigation: Enable the skill only for Lyra avatar conversations and disable it for structured-output workflows.

Risk: Installing the skill without running the Lyra sidecar will not produce visible avatar or voice output.

Mitigation: Run the self-hosted Lyra app sidecar with LLM_PROVIDER=openclaw before expecting voice, lip-sync, gestures, or scene changes.

## Reference(s):

- [Clawlyra on ClawHub](https://clawhub.ai/freespirits/skills/clawlyra)
- [Lyra app homepage](https://github.com/Freespirits/lyra-ai-companion)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text with inline Lyra control tags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Designed for spoken conversational output; avoid strict JSON, Markdown, or other machine-readable formats when this skill is active.]

## Skill Version(s):

1.3.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
