## Description: <br>
Generates high-quality code from tasks, design documents, contracts, and coding specifications, with support for new projects and legacy-project context awareness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lf951515851](https://clawhub.ai/user/lf951515851) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to generate backend, frontend, test, and scaffold files from task descriptions, design documents, contracts, and coding standards. It is intended for both new project creation and changes to existing repositories where generated code should follow established architecture and style. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify many project files during code generation or scaffold initialization. <br>
Mitigation: Install only in a version-controlled project and review planned file lists and diffs before accepting generated changes. <br>
Risk: Broad natural-language triggers or automatic modes may start larger code-generation workflows than intended. <br>
Mitigation: Prefer explicit /gen-code commands and review context, task scope, and file targets before using --auto or batch execution. <br>
Risk: Generated configuration may include placeholder values for databases, Redis, or other services. <br>
Mitigation: Do not place real secrets in generated placeholders; replace them through environment-specific secret management. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/lf951515851/gen-code) <br>
- [Publisher profile](https://clawhub.ai/user/lf951515851) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Prompt](artifact/prompt.md) <br>
- [Scaffold templates](artifact/scaffold-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown responses with generated source code, file paths, command examples, status tables, and implementation summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or modify multiple project files, update task status documents, and produce scaffold configuration for supported frontend and backend stacks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
