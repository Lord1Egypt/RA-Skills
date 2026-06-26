## Description: <br>
Publishes finished Markdown articles to X Articles drafts by parsing content, preparing rich text, mapping images and dividers, and syncing local X/Twitter cookies for Playwright session reuse. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cellinlab](https://clawhub.ai/user/cellinlab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to move an already finished Markdown long-form article into an X Articles draft while preserving title, cover, body images, dividers, and rich-text formatting. It also prepares Playwright storage state from local X/Twitter cookies when available, without auto-publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and persists local X/Twitter session cookies, which can expose account access if the storage-state file is shared, committed, or synced. <br>
Mitigation: Keep the storage-state file private, avoid committing or syncing it, use a dedicated browser profile when possible, and delete it after publishing if session reuse is not needed. <br>
Risk: Draft content can include remote image URLs or matched local image filenames that may not be the intended upload assets. <br>
Mitigation: Review Markdown image URLs, downloaded remote images, and matched local filenames before creating the draft. <br>
Risk: Browser automation may operate with an unintended logged-in X account if reused cookies come from the wrong browser profile. <br>
Mitigation: Confirm the active X account after storage-state injection and choose or refresh the browser cookie source before drafting. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cellinlab/cell-x-article-publisher) <br>
- [Homepage](https://github.com/cellinlab/cell-skills/tree/main/skills/x-article-publisher) <br>
- [Workflow](references/workflow.md) <br>
- [Cookie Sync](references/cookie-sync.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON parsing output, generated HTML, image files, and Playwright storage-state configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local intermediate files for HTML, images, clipboard transfer, table images, and X/Twitter cookie storage state.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
