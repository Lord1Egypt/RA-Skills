## Description: <br>
Track follower growth, detect unfollows, and analyze engagement trends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill as a local command-line helper for recording follower-related activity, checking status, searching logs, and reviewing local history. It should not be treated as verified social-platform analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-entered follower notes, account details, URLs, or other sensitive values can be saved under ~/.local/share/followers. <br>
Mitigation: Do not enter API tokens, passwords, private account notes, or sensitive URLs; delete ~/.local/share/followers when the records are no longer needed. <br>
Risk: The skill uses follower analytics language, but the security evidence describes it as a local logging helper rather than verified social-platform analytics. <br>
Mitigation: Use it for local tracking and notes only; validate any follower counts, engagement conclusions, or platform-specific analytics against the relevant source system. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain1/followers) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [BytesAgain publisher profile](https://clawhub.ai/user/bytesagain1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Terminal text output with local log and export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local records under ~/.local/share/followers.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
