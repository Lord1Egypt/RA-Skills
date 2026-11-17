## Description:

Generate AI comic book panels, manga strips, and graphic novel art from text descriptions via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate comic panels, manga-style strips, storyboards, and graphic novel artwork from text prompts. It is suited for agent workflows that need a direct image URL from a third-party image generation service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference image identifiers are sent to the Neta/TalesOfAI service.

Mitigation: Use only prompts and references suitable for third-party processing, and avoid sensitive personal, proprietary, or secret content.

Risk: The Neta API token is a credential used to access the image generation service.

Mitigation: Treat the token as a secret, avoid exposing it in shared terminals or logs, and rotate it if it may have been exposed.

Risk: Untrusted or unpinned installs can introduce supply-chain risk.

Mitigation: Install from a trusted source and prefer a pinned or ClawHub-managed install path when available.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/blammectrappora/skills/comic-panel-generator)
- [Neta API Access](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text image URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token and may use an optional size preset or reference image UUID.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
