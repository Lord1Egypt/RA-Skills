## Description:

Search codebases for patterns, symbols, and TODOs. Use when navigating large codebases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to search local codebases for patterns, references, TODO markers, recent files, and basic file or line statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell argument handling can allow untrusted search text or paths to become unintended local command execution.

Mitigation: Use only trusted, literal arguments and review command invocations before running the skill until shell quoting, positional-argument handling, and input validation are fixed.

Risk: Local code search can expose sensitive repository contents through command output or local skill data.

Mitigation: Run the skill only in intended repository scopes and review outputs before sharing them outside the development environment.

## Reference(s):

- [Code Searcher on ClawHub](https://clawhub.ai/bytesagain3/skills/code-searcher)
- [BytesAgain](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands read local code files and may write under ~/.local/share/code-searcher/.]

## Skill Version(s):

3.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
