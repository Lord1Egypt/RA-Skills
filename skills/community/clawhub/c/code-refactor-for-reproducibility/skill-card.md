## Description: <br>
Refactors research code for publication-ready reproducible workflows by adding documentation, parameterization, error handling, environment specifications, and validation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ewankeynes](https://clawhub.ai/user/ewankeynes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and engineers use this skill to turn existing analysis scripts into reproducible, shareable research code with documented inputs, pinned environments, tests, and publication-oriented project files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write project files and run local tooling in the selected workspace. <br>
Mitigation: Install or run it only in the intended project, keep version control or backups enabled, review generated diffs, and choose an empty output directory for scripts/main.py. <br>
Risk: The included requirements.txt has unpinned dependencies and an unclear src entry. <br>
Mitigation: Avoid installing the included requirements.txt until dependencies are pinned and the src entry is removed or clarified. <br>
Risk: Generated research-project templates include placeholders that are not publication-ready without review. <br>
Mitigation: Replace placeholder project, citation, contact, and repository details before sharing or archiving generated outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ewankeynes/code-refactor-for-reproducibility) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks plus optional generated project files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a reproducible project skeleton under a user-selected output directory when scripts/main.py is run.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and tile.json; artifact frontmatter metadata lists 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
