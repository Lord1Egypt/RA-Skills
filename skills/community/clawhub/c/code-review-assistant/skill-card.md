## Description:

Provides command-line Markdown code review and diff report output for code quality, bug, and security review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers can use this skill to request review-style reports, diff summaries, and guidance for code quality and security review workflows. Its outputs should be treated as advisory because the server security evidence says the current release can emit canned findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create false confidence by presenting canned code review or security findings as if they came from real analysis.

Mitigation: Use it only for advisory or illustrative review output unless it is changed and revalidated to inspect actual files, diffs, and pull requests.

Risk: Generated findings may not correspond to the requested target path or repository changes.

Mitigation: Validate any reported issue against the actual source code and pair this skill with established linters, tests, and security scanners before using results in CI or merge decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunshine-del-ux/skills/code-review-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and terminal text with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review and diff outputs may contain placeholder findings rather than analysis of the requested files.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
