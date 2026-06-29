## Description: <br>
Build and operate a privacy-preserving household information system for AI agents and assistants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[living-hi](https://clawhub.ai/user/living-hi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and household operators use this skill to initialize and maintain a private local workspace for family facts, plans, projects, decisions, reminders, risks, reviews, and long-term development paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill maintains a persistent local household record that may include sensitive family information in local plaintext files. <br>
Mitigation: Choose a private workspace path, review ~/.family-os/config.yaml, and avoid storing credentials, ID numbers, medical results, or detailed child, legal, or financial records unless local plaintext storage is acceptable. <br>
Risk: Automatic updates can write sensitive household information without an additional review step when privacy settings allow it. <br>
Mitigation: Disable auto_update or require confirmation for sensitive writes, especially for identity, medical, financial, legal, address, credential, and detailed child information. <br>


## Reference(s): <br>
- [Privacy Model](references/privacy-model.md) <br>
- [Workspace Structure](references/workspace-structure.md) <br>
- [Update Rules](references/update-rules.md) <br>
- [Workflows](references/workflows.md) <br>
- [Household Development Path Framework](references/development-path-framework.md) <br>
- [Templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files, local workspace files, shell command output, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores user household data in the configured local workspace rather than the skill package.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
