## Description:

Helps agent builders set up golden tests, automated evaluations, improvement tracking, and ablation testing to measure and improve agent behavior over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dario-github](https://clawhub.ai/user/dario-github)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to install and apply an agent evaluation workflow with golden tests, multidimensional scoring, ablation experiments, and iterative improvement loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer downloads mutable remote code and runs it locally.

Mitigation: Review the upstream repository before installation, prefer a pinned release or commit, and install in an isolated virtual environment.

Risk: The installer can delete the directory selected by EVOLUTION_INSTALL_DIR during fallback reinstall.

Mitigation: Set EVOLUTION_INSTALL_DIR only to a disposable installation path and avoid directories containing important data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dario-github/skills/agent-self-evolution)
- [Agent Self-Evolution Homepage](https://github.com/dario-github/agent-self-evolution)
- [nous-safety Companion Project](https://github.com/dario-github/nous)
- [biomorphic-memory Companion Project](https://github.com/dario-github/biomorphic-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require Python 3.11+, an LLM API key for evaluation judging, and local shell execution for installation.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact frontmatter says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
