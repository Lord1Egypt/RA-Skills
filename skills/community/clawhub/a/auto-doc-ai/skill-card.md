## Description: <br>
Auto Doc AI helps developers generate Google Style docstrings for Python code by analyzing code structure with AST-based parsing and LLM assistance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonia-sz](https://clawhub.ai/user/antonia-sz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to add or refresh Google Style docstrings across individual Python files or directories, with dry-run and overwrite modes for reviewable edits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recursive or overwrite runs can replace existing docstrings or modify many Python files. <br>
Mitigation: Use dry-run first, keep code under version control, and review diffs before applying changes. <br>
Risk: The clone-and-run option points to an external GitHub repository that is not confirmed by server-resolved provenance. <br>
Mitigation: Prefer the ClawHub release when possible and separately inspect the external repository before executing it. <br>


## Reference(s): <br>
- [Auto Doc AI on ClawHub](https://clawhub.ai/antonia-sz/auto-doc-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and Python docstring code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can modify Python source files when run without dry-run; supports recursive and overwrite modes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
