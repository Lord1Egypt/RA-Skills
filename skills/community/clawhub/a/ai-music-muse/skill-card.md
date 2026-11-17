## Description:

Muse AI guides an agent through conversational generation of original songs, instrumentals, BGM, lyrics, composition, and arrangements using the Muse cloud service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a64307410](https://clawhub.ai/user/a64307410)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agent users use this skill to turn short music briefs, custom lyrics, or style choices into original songs, instrumentals, BGM, and downloadable previews through a guided conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Muse account tokens are stored under ~/.muse/token and pasted tokens can grant account access if exposed.

Mitigation: Treat pasted tokens as credentials, keep logs private, avoid reposting token values, and remove or rotate the token if it is exposed.

Risk: The skill creates a persistent device identifier under ~/.muse/device_id and uses it with the Muse cloud service.

Mitigation: Install only if persistent device identification is acceptable, and remove ~/.muse/device_id or the ~/.muse directory if the local identifier should be reset.

Risk: The installer can replace or remove the selected skill installation directory, and custom install paths increase that risk.

Mitigation: Inspect install.sh before running it, avoid custom install paths unless they are isolated, and verify the selected target before install or uninstall.

Risk: Music prompts, lyrics, and generation requests are sent to the Muse cloud service.

Mitigation: Avoid submitting confidential, sensitive, or regulated content unless the Muse service terms and data handling are acceptable for the use case.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/a64307410/skills/ai-music-muse)
- [Muse Registration Page](https://skills.muse.top/)
- [Muse Registration Guide](assets/register-guide.md)
- [Music Style Catalog](references/style-catalog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Conversational Markdown with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return Muse task status, lyrics previews, audio URLs, cover image URLs, account-credit status, and registration links.]

## Skill Version(s):

1.0.6 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
