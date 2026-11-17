## Description:

Opens a browser tab for a human to highlight and comment on a Markdown file, then submits structured JSON comments for the agent to process.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxl-lxz](https://clawhub.ai/user/zxl-lxz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use comment-md when a Markdown document needs targeted human review before revision. The skill opens a local or static browser review flow and returns structured comments with selected text context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed Markdown is opened in a browser UI that contacts jsDelivr and executes remote JavaScript.

Mitigation: Use only when that dependency posture is acceptable, or bundle and integrity-pin browser dependencies before use with confidential content.

Risk: The renderer can fail open if Markdown sanitization is unavailable.

Mitigation: Avoid untrusted Markdown unless rendering fails closed when sanitization cannot load.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/zxl-lxz/commentmd/tree/main/skills/commentmd)
- [ClawHub skill page](https://clawhub.ai/zxl-lxz/skills/comment-md)

## Skill Output:

**Output Type(s):** [json, guidance]

**Output Format:** [JSON comment report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source file path, initial SHA-256, changed-during-review flag, comment count, and comments with quote, prefix, suffix, note, and timestamp fields.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
