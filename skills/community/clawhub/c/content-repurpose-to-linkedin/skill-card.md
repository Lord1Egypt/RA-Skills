## Description:

Turns source content into polished LinkedIn posts and publishes them through ClawLink only after user approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to turn articles, notes, transcripts, or launch material into LinkedIn-ready post drafts, compare variants, and publish only after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing and allowlisting an unpinned third-party ClawLink plugin can grant persistent mediation of LinkedIn account actions.

Mitigation: Review the plugin provenance, prefer a pinned and verified version, confirm LinkedIn OAuth scopes, and proceed only if the user accepts that access.

Risk: A LinkedIn draft could be published to the wrong profile or organization page if the target or approval is unclear.

Mitigation: Preview the exact post and target, use ClawLink preview tooling when available, and call publish tools only after explicit confirmation.

## Reference(s):

- [Content Repurpose to LinkedIn release page](https://clawhub.ai/hith3sh/skills/content-repurpose-to-linkedin)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=content-repurpose-to-linkedin)
- [ClawLink OpenClaw docs](https://docs.claw-link.dev/openclaw)
- [ClawLink verification](https://claw-link.dev/verify)
- [LinkedIn API documentation](https://developer.linkedin.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with draft post text, confirmation prompts, and inline bash setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live ClawLink tool discovery and explicit user confirmation before publishing.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
