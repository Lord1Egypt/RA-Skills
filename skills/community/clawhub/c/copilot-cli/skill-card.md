## Description:

Guides developers through using GitHub Copilot CLI to analyze code, explore project structure, generate documentation, review code, and automate development tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biuyx](https://clawhub.ai/user/biuyx)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill for practical GitHub Copilot CLI setup and prompt patterns when analyzing repositories, finding code, generating documentation, reviewing files, and automating development tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide recommends storing a GitHub token in a plaintext file.

Mitigation: Use a fine-grained Copilot-only token and prefer an OS credential manager; if a file must be used, restrict file permissions.

Risk: The guide includes reduced-review execution with copilot --yolo.

Mitigation: Use --yolo only in disposable or well-backed-up workspaces after reviewing the proposed scope.

Risk: Repository contents may be sent to GitHub Copilot services during analysis.

Mitigation: Avoid using Copilot analysis on sensitive repositories unless organizational policy allows sending that context to GitHub Copilot services.

## Reference(s):

- [GitHub Copilot documentation](https://docs.github.com/en/copilot)
- [GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/cli-command-reference)
- [ClawHub skill page](https://clawhub.ai/biuyx/skills/copilot-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
