## Description:

Claude Code Analyzer is a third-party ClawHub skill marketed for source-code structure analysis, while the submitted code returns a simple canned analysis result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bingze00000](https://clawhub.ai/user/bingze00000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers evaluating this ClawHub release can use the skill as a source-code analysis helper only on code they are authorized to inspect. Evidence indicates the current implementation provides a canned analysis result rather than deep code inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package is marketed as a paid source-code analyzer, but evidence says the submitted code only returns a canned result.

Mitigation: Review the artifact before installation and verify analysis behavior on non-sensitive test code before relying on the output.

Risk: The skill text encourages analysis of leaked source code.

Mitigation: Use the skill only with code you are authorized to inspect, and avoid providing private repositories, secrets, or confidential source.

Risk: Security evidence marks the release as suspicious despite a small, non-persistent implementation.

Mitigation: Treat the release as untrusted until it has been manually reviewed and scanned in the target environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bingze00000/skills/claude-code-analyzer)
- [Publisher profile](https://clawhub.ai/user/bingze00000)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [Markdown guidance with Python and shell snippets; Python function output as a dictionary or JSON-like object.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-persistent; the current code returns a canned analysis result.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
