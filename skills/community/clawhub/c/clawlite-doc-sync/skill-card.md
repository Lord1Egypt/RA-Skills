## Description: <br>
Synchronizes post-release project documentation with actual changes by updating README, architecture, contributing, agent instruction, changelog, TODO, and version-related documentation when appropriate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-rayluan](https://clawhub.ai/user/x-rayluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill after code changes and before PR merge to keep Markdown documentation aligned with the implementation, changelog wording, TODO status, and version decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can update Markdown documentation and create a documentation commit. <br>
Mitigation: Run it on a feature branch and review the resulting diff and commit before merging. <br>
Risk: Documentation updates around security wording, large rewrites, version bumps, and new TODO items can affect project meaning or release expectations. <br>
Mitigation: Use the skill's stop-and-ask behavior for those decisions and confirm the requested changes before applying them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and concise status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May edit documentation files and create a scoped documentation commit when changes are needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
