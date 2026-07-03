## Description: <br>
Collects public Bilibili search results, creator-space video lists, video details, comments, and danmaku using agent-browser and public Bilibili APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[excalibursssooo](https://clawhub.ai/user/excalibursssooo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to collect public Bilibili video, creator, comment, and danmaku data for analysis. It can emit focused JSON fetch results or larger harvest folders with Markdown reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use Bilibili browser or cookie session context, including sensitive login cookies such as SESSDATA or bili_jct. <br>
Mitigation: Install only if comfortable with that scraper behavior, avoid adding login cookies unless needed, treat cookie values like passwords, and consider a separate browser profile. <br>
Risk: Harvested comments, danmaku, user metadata, video metadata, and reports can remain on disk in the skill data directory. <br>
Mitigation: Configure the data directory deliberately, keep it out of shared workspaces and version control, and delete harvested data when it is no longer needed. <br>
Risk: The authoritative security verdict is suspicious because warnings around sensitive login cookies are weak. <br>
Mitigation: Review the security summary and guidance before deployment and scan the release in the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/excalibursssooo/skills/bilibili-universal) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>
- [Pitfalls and debugging notes](docs/pitfalls.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Console text plus JSON data files and Markdown harvest reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save harvested comments, danmaku, user metadata, video metadata, and reports under the configured data directory.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
