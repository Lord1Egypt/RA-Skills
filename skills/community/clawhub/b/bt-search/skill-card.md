## Description: <br>
BT磁力链接搜索引擎，通过关键词搜索磁力链接并返回种子名称、大小、做种数、文件列表和磁力链接。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[men459](https://clawhub.ai/user/men459) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search BT magnet-link metadata by keyword, inspect torrent result fields, and present matching results in a readable list. It is not a downloader or streaming tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill silently contacts an unrelated advertising or tracking domain on every run. <br>
Mitigation: Review before installation, restrict network egress to expected domains, and prefer a revised version that removes or clearly discloses the ad-network request. <br>
Risk: Torrent-search results can expose users to legal, policy, or malware risk if used to obtain unauthorized or untrusted content. <br>
Mitigation: Use only where permitted by law and organizational policy, avoid downloading untrusted content, and scan any files obtained outside the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/men459/bt-search) <br>
- [Publisher profile](https://clawhub.ai/user/men459) <br>
- [Adog BT magnet search home page](https://www.adog.uk/) <br>
- [Adog torrent detail API](https://www.adog.uk/api/skill/torrent/{info_hash}) <br>


## Skill Output: <br>
**Output Type(s):** [json, markdown, shell commands] <br>
**Output Format:** [JSON search results from the script, typically summarized by the agent as Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results can include torrent name, size, seeders, leechers, file count, matched file paths, creation time, and magnet links.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
