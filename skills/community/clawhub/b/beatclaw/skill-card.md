## Description:

Helps music producers generate instrumental beats, publish and manage BeatClaw listings, and optionally prepare stems for sale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youngpietro](https://clawhub.ai/user/youngpietro)

### License/Terms of Use:

MIT-0

## Use Case:

External music producers use this skill to connect an agent to their BeatClaw producer account, create instrumental beats with their Suno credits, publish listings, manage pricing and genres, and optionally prepare stems for buyers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Direct installation and automatic updates can replace agent instructions with future content from beatclaw.com without review.

Mitigation: Prefer a ClawHub-managed or manually reviewed installation; review updates before allowing them to replace local instructions.

Risk: A connected agent can retain a long-lived BeatClaw producer token and access the producer account.

Mitigation: Connect only to producers you control, store the token securely, and revoke the agent's connection in the producer dashboard when access is no longer needed.

Risk: Beat generation can spend Suno credits and publish public listings; the agent can also change prices or genres, process stems, and delete listings.

Mitigation: Require explicit human confirmation before generation, stem processing, public listing changes, or deletion; confirm the producer and listing before each action.

## Reference(s):

- [BeatClaw on ClawHub](https://clawhub.ai/youngpietro/skills/beatclaw)
- [BeatClaw](https://beatclaw.com)
- [Suno API provider](https://sunoapi.org)
- [MVSEP API access for optional stem splitting](https://mvsep.com/user-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with API request examples and marketplace links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports generation and listing status; audio and stems are delivered through BeatClaw, not as agent output.]

## Skill Version(s):

1.62.0 (source: ClawHub release metadata and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
