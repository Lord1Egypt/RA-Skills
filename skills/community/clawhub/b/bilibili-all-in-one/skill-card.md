## Description: <br>
Bilibili All In One lets agents monitor Bilibili trends, download and play videos, retrieve subtitles and danmaku, track metrics, and publish videos through Bilibili APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wscats](https://clawhub.ai/user/wscats) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to automate Bilibili content workflows, including trend monitoring, video and subtitle retrieval, engagement tracking, playback metadata lookup, and authenticated publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Bilibili session cookies provide broad account access. <br>
Mitigation: Use a secondary account where possible, pass credentials only when needed, and keep credential persistence disabled unless there is a clear operational need. <br>
Risk: Publishing, scheduling, draft, and edit actions can change a Bilibili account or public channel. <br>
Mitigation: Review dry-run previews and require explicit confirmation before executing account-modifying actions. <br>
Risk: Danmaku retrieval may expose stable pseudonymous user hashes. <br>
Mitigation: Treat danmaku output as potentially identifying data and avoid redistributing it beyond the intended workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wscats/bilibili-all-in-one) <br>
- [Publisher profile](https://clawhub.ai/user/wscats) <br>
- [Project homepage](https://github.com/wscats/bilibili-all-in-one) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, shell commands, code, configuration, guidance] <br>
**Output Format:** [JSON result objects, Markdown guidance, shell commands, Python snippets, and local media or subtitle files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write downloaded videos, audio, subtitle files, and optional credential files when persistence is explicitly enabled.] <br>

## Skill Version(s): <br>
1.0.24 (source: server release evidence and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
