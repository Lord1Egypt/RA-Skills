## Description: <br>
Fetches Bilibili video comments for creator self-analysis and produces JSONL plus summary.json exports for downstream sentiment, keyword, and audience analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agents365-ai](https://clawhub.ai/user/agents365-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, authorized assistants, and developers use this skill to collect comments from owned or explicitly authorized Bilibili videos and prepare structured exports for analysis. It supports low-volume, read-only workflows such as sentiment review, keyword discovery, audience geography summaries, and creator feedback analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Bilibili session cookies and may inspect local browser cookie stores when no explicit cookie file is supplied. <br>
Mitigation: Pass a specific --cookie-file or BBC_COOKIE_FILE, avoid browser auto-detection, store cookie files with restrictive permissions, and rotate the session if exposure is suspected. <br>
Risk: The skill includes a silent daily self-update instruction that can change local behavior without an explicit user review step. <br>
Mitigation: Remove or disable the auto-update instruction before installation, pin the installed release, and review changes before updating. <br>
Risk: Generated outputs can contain user IDs, nicknames, comments, and IP-location metadata. <br>
Mitigation: Use the skill only for owned or explicitly authorized videos, minimize retention, and avoid sharing raw output files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/agents365-ai/bbc-skill) <br>
- [Online documentation](https://agents365-ai.github.io/bbc-skill/) <br>
- [Agent contract](references/agent-contract.md) <br>
- [Bilibili API endpoints used](references/api-endpoints.md) <br>
- [Cookie extraction per platform](references/cookie-extraction.md) <br>
- [Bilibili Open Platform](https://openhome.bilibili.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, stable JSON stdout envelopes, JSONL comment records, summary.json, and archived raw API response files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default outputs are written under ./bilibili-comments/<BV>/; stderr may include human logs and NDJSON progress events.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
