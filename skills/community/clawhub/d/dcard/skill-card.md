## Description:

Fetches full Dcard article content and forum post lists with titles, body text, and image links, using Camoufox and patchright to handle Cloudflare-protected pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ichendong](https://clawhub.ai/user/ichendong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to retrieve Dcard post content, images, and forum post lists for analysis or review workflows. Users should confirm their use complies with Dcard's terms and avoid bulk automated scraping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates access to Dcard content through anti-bot bypass behavior and may conflict with service terms or rate limits.

Mitigation: Confirm that the intended use complies with Dcard's terms, avoid bulk or automated scraping, and stop if rate limits or access challenges appear.

Risk: The skill installs and runs browser tooling with weak supply-chain and isolation controls.

Mitigation: Install only in an isolated, unprivileged environment after independently checking dependency and Camoufox versions.

## Reference(s):

- [Dcard Skill on ClawHub](https://clawhub.ai/ichendong/skills/dcard)
- [Dcard publisher profile](https://clawhub.ai/user/ichendong)
- [Dcard article URL pattern](https://www.dcard.tw/f/relationship/p/261529038)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON emitted by command-line scripts, with Markdown usage examples in the skill instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include article title, URL, post ID, body text, image links, forum post lists, and popular forum listings.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
