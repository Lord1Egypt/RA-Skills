## Description: <br>
Bilibili Toolkit Free helps personal users monitor popular Bilibili content, download videos, inspect basic video data, and retrieve subtitles and danmaku without requiring login for core features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for Bilibili content discovery, video download preparation, basic statistics lookup, subtitle retrieval, and danmaku retrieval for personal workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording could cause the skill to be used for tasks outside explicit Bilibili workflows. <br>
Mitigation: Use the skill only for clearly requested Bilibili tasks and review the proposed action before allowing execution. <br>
Risk: Download, subtitle, and danmaku workflows may write files locally. <br>
Mitigation: Confirm each download or save action first and run commands from a dedicated directory where output files are easy to inspect or remove. <br>
Risk: Authenticated Bilibili features may require session credentials. <br>
Mitigation: Do not provide Bilibili session credentials unless authenticated functionality is explicitly intended and the implementation is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/bilibili-toolkit-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command-line and Python examples; task results may include JSON-like status data, downloaded media files, subtitle files, danmaku text, or basic video metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger network requests and local file writes for download, subtitle, and danmaku workflows when the user explicitly requests those actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
