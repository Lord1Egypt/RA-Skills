## Description:

Use the frigatebird npm package to interact with X from the CLI with bird-style command parity, posting/reply/article support, and list automation without X API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oceanswave](https://clawhub.ai/user/oceanswave)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run bird-style X workflows from the command line, including reading timelines, posting replies or articles, and managing lists without X API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use X session cookies and browser profiles as credentials.

Mitigation: Protect cookies and browser profiles as account credentials, run in a least-privilege environment, and avoid sharing session material with untrusted processes.

Risk: The skill can perform live account actions such as posting, replying, following, and changing lists.

Mitigation: Require explicit confirmation before mutations and review command arguments before execution.

Risk: The documented install flow uses an unpinned npm package.

Mitigation: Use a pinned, reviewed package version before deployment.

Risk: X web UI selector drift can break browser-driven workflows.

Mitigation: Validate the session and command behavior with non-mutating checks before relying on read or mutation flows.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/oceanswave/skills/frigatebird)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include commands that read from or perform live actions on an authenticated X account.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
