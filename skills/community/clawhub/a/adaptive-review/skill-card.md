## Description:

Adaptive code review that routes to haiku, sonnet, or opus based on diff complexity signals for cost-efficient reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2233admin](https://clawhub.ai/user/2233admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to choose an appropriate code-review depth from git diff signals, then produce review findings with the selected model tier. It is intended for routine pull request and local change review where cost and review depth need to be balanced.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The OpenClaw/local variant can send full git diffs to the configured model server.

Mitigation: Use only local or trusted HTTPS endpoints, and redact secrets or sensitive code before review.

Risk: The OpenClaw/local variant shows a curl JSON construction pattern that can mishandle attacker-controlled diff text.

Mitigation: Replace hand-built JSON payloads with a JSON-safe tool such as jq before using that variant.

## Reference(s):

- [Think Anywhere](https://arxiv.org/abs/2603.29957)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown review report with routing signal summary and reviewer findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the selected fast, medium, or deep review depth; the local OpenClaw variant may send full git diffs to the configured model endpoint.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
