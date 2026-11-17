## Description:

Auto-create or reuse a Conda environment for Python projects by scanning dependency files, matching existing environments, and handling CUDA/GPU needs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kazuya-ecnu](https://clawhub.ai/user/kazuya-ecnu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create or reuse isolated Conda environments for Python projects, install dependencies from common project files, and verify the resulting runtime including optional CUDA support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install project-controlled code or dependencies during environment setup.

Mitigation: Review dependency files and project install scripts before allowing project installation, especially for untrusted repositories.

Risk: The skill can suggest --break-system-packages, which bypasses Python package protections.

Mitigation: Allow this only after verifying the interpreter, target environment, and need; prefer isolated Conda environments first.

Risk: The skill creates or changes Python environments on the user's machine.

Mitigation: Confirm the target project path and environment name before execution, and avoid modifying the base Conda environment.

## Reference(s):

- [Auto Conda Env on ClawHub](https://clawhub.ai/kazuya-ecnu/skills/auto-conda-env)
- [PyTorch CUDA wheel index](https://download.pytorch.org/whl/cu118)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and an environment setup summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include environment name, Python version, installed dependencies, environment path, and activation command.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
