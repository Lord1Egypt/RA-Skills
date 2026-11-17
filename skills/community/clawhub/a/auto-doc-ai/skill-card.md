## Description:

Auto Doc AI uses AST analysis and an LLM to generate Google Style docstrings for Python code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonia-sz](https://clawhub.ai/user/antonia-sz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze Python 3.7+ files or directories and generate or update Google Style docstrings, including dry-run previews and overwrite workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README includes direct clone and execution steps for an unpinned external repository that is not part of the reviewed artifact.

Mitigation: Prefer the reviewed OpenClaw install path, or pin and verify the exact external repository commit before running it.

Risk: Recursive and overwrite modes can modify many Python source files or replace existing docstrings.

Mitigation: Run in dry-run mode first, review proposed changes, and keep source control or backups available before using overwrite.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated Python docstring code.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify Python source files when used outside dry-run mode.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
