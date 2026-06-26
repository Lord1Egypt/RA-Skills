## Description: <br>
Save web content to an Obsidian vault, with routing for Twitter/X, WeChat MP, Xiaohongshu, YouTube, Bilibili, and general web pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pazzilivo](https://clawhub.ai/user/pazzilivo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users who collect web references use this skill to fetch supported URLs, save the resulting content as Markdown in an Obsidian vault, and return structured status for the clipping operation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved clips are automatically pulled, committed, and pushed to the detected vault's Git remote. <br>
Mitigation: Install and run the skill only for vaults where automatic Git sync is intended, and verify the vault path and remote before clipping. <br>
Risk: Private or sensitive URLs and clipped content may be sent to external fetch services, image proxies, or the configured Git remote. <br>
Mitigation: Avoid clipping sensitive content unless those services and the remote repository are approved for that data. <br>
Risk: The skill may affect the wrong Obsidian vault if vault detection selects an unintended path. <br>
Mitigation: Confirm or explicitly provide the vault path before running clipping workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pazzilivo/clipper) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/pazzilivo) <br>
- [x-reader dependency](https://github.com/runesleo/x-reader) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown files in an Obsidian vault plus JSON status from the clipping scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Twitter/X and general web clipping can run from a URL; WeChat MP clipping may require browser snapshot guidance before saving.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
