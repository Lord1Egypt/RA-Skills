## Description:

Clawnoter Obsidian saves web articles into a local Obsidian vault with image capture, Markdown conversion, YAML frontmatter, and optional user notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liz-npa](https://clawhub.ai/user/liz-npa)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to collect useful web articles, extract page content and images, and save the result as structured notes in a local Obsidian vault.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch unrestricted URLs and disclose submitted links to Jina.ai.

Mitigation: Use only public, non-sensitive URLs unless URL validation and a Jina opt-in or local-only mode are added.

Risk: Unsafe configuration can write generated notes outside the intended Obsidian vault.

Mitigation: Confirm the configured vault and subfolder before saving; add vault containment checks before broad deployment.

Risk: The skill downloads page-selected images and scans common local folders for vault discovery.

Mitigation: Run it only with user-approved targets and review downloaded assets and discovered paths before trusting the saved note.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liz-npa/skills/clawnoter-obsidian-save)
- [WebNoter Chrome Extension](https://chromewebstore.google.com/detail/webnoter/hmijljoffeceeloaigodmlojbfmgfdkp)
- [WebNoter Product Introduction](https://mp.weixin.qq.com/s/bwqHGb9WGC6L0wL7qVicSA)

## Skill Output:

**Output Type(s):** [markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown notes with YAML frontmatter, local image files, JSON command results, and concise setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates Obsidian note files and an images subdirectory in the configured vault path.]

## Skill Version(s):

1.1.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
