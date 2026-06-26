## Description: <br>
ClawLock-Rank prepares a ClawLock 2.2.1+ local inspection result for leaderboard upload, shows a sanitized preview, and uploads only when the user explicitly confirms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[g1at](https://clawhub.ai/user/g1at) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and security-focused operators use this skill after a local ClawLock inspection when they want to preview and voluntarily publish a score to ClawLockRank. It is scoped to leaderboard submission, not general security scanning, hardening, dependency setup, or leaderboard browsing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The upload sends a sanitized ClawLock score submission to the configured ClawLockRank service, and the public nickname, score, grade, adapter metadata, and finding titles may reveal operational context. <br>
Mitigation: Review the preview before approving upload, choose a nickname suitable for public display, and avoid uploading from environments where device fingerprint metadata or finding titles could expose sensitive details. <br>
Risk: Using this skill outside its trigger boundary could publish a result when the user only wanted a local scan, hardening help, debugging, or leaderboard browsing. <br>
Mitigation: Trigger it only for explicit leaderboard upload intent, run preview mode first, and require a clear confirmation before upload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/g1at/clawlock-rank) <br>
- [Project homepage](https://github.com/g1at/ClawLock-Rank) <br>
- [Publisher profile](https://clawhub.ai/user/g1at) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and structured JSON preview or upload responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preview mode returns a sanitized payload path, public summary, uploaded-field list, excluded-field list, and confirmation requirements.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
