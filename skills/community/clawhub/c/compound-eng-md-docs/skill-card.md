## Description: <br>
Manages project documentation for CLAUDE.md, AGENTS.md, README.md, and CONTRIBUTING.md when asked to update, create, or initialize those context files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iliaal](https://clawhub.ai/user/iliaal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to initialize or refresh project documentation after checking the actual repository structure, tooling, commands, and conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation updates can encode incorrect project commands, paths, or conventions if repository state is not checked first. <br>
Mitigation: Use dry-run or request a planned diff before writes, then verify generated documentation against current files and project manifests. <br>
Risk: Initialization or migration can create or replace a CLAUDE.md symlink. <br>
Mitigation: Check whether CLAUDE.md contains unique content before allowing migration or symlink replacement. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iliaal/compound-eng-md-docs) <br>
- [Update context files workflow](references/update-agents.md) <br>
- [Initialize context workflow](references/init-agents.md) <br>
- [Update README workflow](references/update-readme.md) <br>
- [Update CONTRIBUTING workflow](references/update-contributing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise change summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or update documentation files such as AGENTS.md, CLAUDE.md, README.md, CONTRIBUTING.md, or DOCS.md when the user requests those workflows.] <br>

## Skill Version(s): <br>
4.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
