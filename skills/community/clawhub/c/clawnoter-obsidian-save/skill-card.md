## Description: <br>
Saves web articles and links into a local Obsidian vault with webpage extraction, image downloading, Markdown conversion, YAML frontmatter, and optional user notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liz-npa](https://clawhub.ai/user/liz-npa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to collect web articles, optional notes, and article images into a configured local or iCloud-synced Obsidian vault. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scans common local folders to discover Obsidian vaults. <br>
Mitigation: Review discovered paths and configure only the intended vault or subfolder before saving articles. <br>
Risk: Saved article URLs may be sent to Jina.ai and fetched from external websites. <br>
Mitigation: Avoid private, tokenized, intranet, login-only, or sensitive links unless the user accepts that disclosure risk. <br>
Risk: The skill writes Markdown notes and image files into a local Obsidian path. <br>
Mitigation: Use a dedicated save folder and verify the configured path before first use or after reconfiguration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liz-npa/clawnoter-obsidian-save) <br>
- [WebNoter Chrome extension](https://chromewebstore.google.com/detail/webnoter/hmijljoffeceeloaigodmlojbfmgfdkp) <br>
- [WebNoter product introduction](https://mp.weixin.qq.com/s/bwqHGb9WGC6L0wL7qVicSA) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes with YAML frontmatter, Obsidian callouts, local image references, and JSON status from helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes Markdown files and downloaded image assets to the user-configured Obsidian vault path.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
