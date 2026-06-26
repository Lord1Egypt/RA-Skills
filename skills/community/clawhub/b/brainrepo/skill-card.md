## Description: <br>
BrainRepo helps an agent capture, organize, and retrieve a personal markdown knowledge repository using PARA and Zettelkasten patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codezz](https://clawhub.ai/user/codezz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Individuals and teams use BrainRepo to let an AI agent create and maintain a local markdown knowledge base for notes, projects, people, tasks, journals, and reference material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores personal knowledge and notes in a local markdown repository, which may include sensitive information if the user captures it. <br>
Mitigation: Do not store secrets or highly sensitive personal details casually, and review captured content before syncing or sharing the repository. <br>
Risk: Daily and weekly cleanup workflows can move or delete notes during agent-assisted processing. <br>
Mitigation: Review proposed file changes before deletion, archiving, cleanup, or commit operations. <br>
Risk: Optional Git synchronization can publish the repository to the wrong remote or an unintended public location. <br>
Mitigation: Verify any Git remote is private and correct before allowing git push. <br>


## Reference(s): <br>
- [BrainRepo release page](https://clawhub.ai/codezz/brainrepo) <br>
- [BrainRepo Structure Guide](references/structure.md) <br>
- [BrainRepo Workflows](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown notes and instructions with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local markdown files under ~/Documents/brainrepo/ when used by an agent with filesystem access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
