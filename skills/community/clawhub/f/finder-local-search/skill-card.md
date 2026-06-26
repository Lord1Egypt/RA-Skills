## Description: <br>
Searches Finder for TikTok, YouTube, and Instagram creator candidates using platform, region, language, tag, follower, view, and engagement criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaobai1226](https://clawhub.ai/user/xiaobai1226) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, creator discovery, and agent-assisted research users use this skill to configure Finder access and search for creator candidates across TikTok, YouTube, and Instagram. It helps translate plain-language requirements into Finder search parameters and returns concise guidance or results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Finder API key is stored in ~/.finder/config.json and may be exposed if pasted into chat or shared logs. <br>
Mitigation: Enter the key locally when possible, restrict file access to the config file, and rotate or revoke the key if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xiaobai1226/finder-local-search) <br>
- [Finder service](https://finder.optell.com) <br>
- [Finder API key page](https://finder.optell.com/api-key) <br>
- [Configuration reference](references/config.md) <br>
- [Search filters reference](references/filters.json) <br>
- [Example conversations](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with command snippets and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Finder API requests, local configuration guidance, and concise search-result summaries; similar-creator search is out of scope.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
