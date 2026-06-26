## Description: <br>
Explore a codebase to find opportunities for architectural improvement, focusing on making the codebase more testable by deepening shallow modules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emersonbraun](https://clawhub.ai/user/emersonbraun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to inspect codebases, identify shallow or tightly coupled modules, compare interface designs, and prepare refactor RFCs that improve testability and maintainability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create a GitHub issue without final user review. <br>
Mitigation: Require the agent to draft the RFC locally, show the target repository, title, labels, and full issue body, and run `gh issue create` only after explicit approval. <br>


## Reference(s): <br>
- [Reference](artifact/REFERENCE.md) <br>
- [ClawHub skill page](https://clawhub.ai/emersonbraun/eb-improve-codebase-architecture) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with prose, code sketches, issue RFC content, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include GitHub issue creation commands after the user has selected a refactor interface.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
