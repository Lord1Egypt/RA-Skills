## Description: <br>
ClawLite Mark helps an agent post to Facebook, read comments, draft context-aware replies, submit approved replies, and track engagement threads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-rayluan](https://clawhub.ai/user/x-rayluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Community operators and brand maintainers use this skill to manage Facebook posting and comment engagement from an agent, with modes for automatic replies, drafted replies, or per-reply confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post or reply publicly from a logged-in Facebook account. <br>
Mitigation: Start in Draft or Query mode, verify the target account and post, and require human approval for major announcements or sensitive replies. <br>
Risk: The skill uses a persistent Facebook browser profile and stores comments, receipts, logs, and screenshots. <br>
Mitigation: Use a dedicated browser profile, restrict access to generated artifacts, and periodically clear stored comments, receipts, logs, and screenshots. <br>
Risk: The artifact references a hardcoded private local style file. <br>
Mitigation: Remove or replace the local style-file reference before use and avoid granting the agent access to unrelated personal files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/x-rayluan/clawlite-mark) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON files, guidance] <br>
**Output Format:** [Markdown responses with plain text Facebook drafts and JSON receipt files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write receipts, comment snapshots, and error logs under ~/.openclaw/workspace/mark/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
