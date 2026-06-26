## Description: <br>
Daily Beauty searches Xiaohongshu for a selected creator profile and returns nine full-body image files while filtering previously used, wallpaper, AI-generated, and marketing accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lorexxar](https://clawhub.ai/user/lorexxar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and end users use this skill to fetch a daily Xiaohongshu image set, receive a short blogger summary, and obtain local image paths for follow-up messaging or review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports a hard-coded Feishu recipient for sending results. <br>
Mitigation: Remove or change the recipient before use and require explicit confirmation before sending messages. <br>
Risk: The security guidance notes Xiaohongshu searches, local image downloads, persistent deduplication records, and image conversion on remote files. <br>
Mitigation: Run in a restricted workspace, review downloaded files and retained records, and keep image conversion tooling patched. <br>
Risk: The security summary reports broad triggers that could run the workflow unintentionally. <br>
Mitigation: Narrow trigger phrases or require a confirmation step before network searches, downloads, or messaging. <br>


## Reference(s): <br>
- [Blacklist Filtering Reference](references/blacklist.md) <br>
- [Whitelist Blogger Reference](references/whitelist.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands] <br>
**Output Format:** [JSON status object with local PNG image file paths and optional messaging command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads up to nine images to the local OpenClaw workspace and updates local deduplication JSON files.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
