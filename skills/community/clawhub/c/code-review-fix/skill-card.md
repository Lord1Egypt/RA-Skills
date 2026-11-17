## Description:

Reviews source files for common bug, security, style, and performance issues, reports findings, and can apply simple automated repairs when requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[landyun](https://clawhub.ai/user/landyun)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to scan code for common quality and security issues, receive concise fix suggestions, and optionally apply straightforward local edits. It is intended for routine code review assistance, not as a substitute for human review of complex changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may contact skillpay.me for balance checks, payment links, and paid per-call charging after the free trial.

Mitigation: Review billing behavior before installation and set an explicit SKILLPAY_USER_ID so usage is tied to an intended account identifier.

Risk: The package includes a live-looking billing API key.

Mitigation: Treat the packaged key as sensitive third-party billing material and avoid running the skill in sensitive environments until the publisher confirms the intended key handling.

Risk: Using --fix can modify source files in place.

Mitigation: Run on a clean working tree, inspect diffs after execution, and keep automatic fixes disabled unless local file changes are expected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/landyun/skills/code-review-fix)
- [Publisher profile](https://clawhub.ai/user/landyun)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Console text and Markdown-style review output, with optional in-place source code edits when --fix is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local usage state file and may modify the reviewed file when automatic fixes are enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
