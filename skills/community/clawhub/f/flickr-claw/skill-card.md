## Description: <br>
Access Flickr with local user-supplied API credentials and OAuth tokens to verify authorization, export or download recent and album photos, and edit tags, titles, and descriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanestane](https://clawhub.ai/user/stanestane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage Flickr account workflows from an agent, including OAuth setup checks, album and recent-upload export, local image review downloads, and reviewed metadata updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flickr credentials and OAuth tokens are local secrets under ~/.openclaw. <br>
Mitigation: Protect token files as secrets and use read-only tokens for browsing, exports, and downloads whenever write access is not required. <br>
Risk: Write-capable commands can change Flickr photo tags, titles, and descriptions. <br>
Mitigation: Review photo IDs and proposed metadata before running write commands, and create write tokens only when metadata edits are intended. <br>
Risk: CSV exports and downloaded images can leave local copies of account photo metadata or image content. <br>
Mitigation: Delete exported CSVs and downloaded image directories after review unless the user explicitly wants to keep them. <br>


## Reference(s): <br>
- [Flickr Claw on ClawHub](https://clawhub.ai/stanestane/flickr-claw) <br>
- [Flickr workflow](references/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands; script output may include terminal text, CSV files, downloaded image files, and JSON manifests.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Flickr API credentials and OAuth token files; write operations can update photo tags, titles, and descriptions.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
