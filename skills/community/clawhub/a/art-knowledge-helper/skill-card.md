## Description: <br>
Art Knowledge Helper Skill helps users manage an art book knowledge base by scanning downloads, archiving books into categories, syncing with Baidu Netdisk, verifying sync status, and reporting library statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingxiahotmail](https://clawhub.ai/user/qingxiahotmail) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and art learners use this skill to maintain a local art ebook library: configure library paths, find recent art-book downloads, archive books into categories, sync the collection to Baidu Netdisk, and inspect collection or sync status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured paths may point to unintended local or cloud-synced folders, causing files to be copied or synchronized outside the intended library. <br>
Mitigation: Edit config.json before use, restrict paths to folders intended for scanning or copying, test on a small folder first, and keep backups. <br>
Risk: Book collections may contain sensitive files or material the user does not have rights to distribute. <br>
Mitigation: Remove sensitive files from the knowledge-base folder and only share or upload books the user has the right to distribute. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qingxiahotmail/art-knowledge-helper) <br>
- [Publisher profile](https://clawhub.ai/user/qingxiahotmail) <br>
- [Python downloads](https://www.python.org/downloads/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local file-copy and sync operations based on configured paths; users should review paths before running scripts.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
