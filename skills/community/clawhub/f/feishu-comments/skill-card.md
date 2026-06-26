## Description: <br>
Read comments from Feishu documents when a user asks to check, fetch, or review document feedback and collaboration comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deadblue22](https://clawhub.ai/user/deadblue22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, document reviewers, and agents use this skill to inspect Feishu or Lark document comments, quoted text, reply content, and comment status during document review cycles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is advertised as a Feishu comment reader but bundles a write-capable script that can close comments, including automatic bulk closure. <br>
Mitigation: Review before installing; remove or separate the write-capable script, or guard comment-closing behavior with dry-run mode and explicit confirmation. <br>
Risk: Over-scoped Feishu or Lark credentials can permit more access than read-only comment review requires. <br>
Mitigation: Use least-privilege Feishu credentials, preferably read-only scopes, unless comment-closing capability is intentionally required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/deadblue22/feishu-comments) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>
- [Lark Open Platform](https://open.larksuite.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Plain text report from shell output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Lists comment IDs, open/resolved/orphaned status, scope, quoted text, replies, and summary counts; default output filters to open anchored comments unless --all is used.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence, created 2026-03-10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
