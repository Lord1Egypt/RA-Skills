## Description: <br>
Intelligent skill router that analyzes the current problem statement and context, scores available skills for applicability, and recommends the most relevant ones in priority order. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[science-prof-robot](https://clawhub.ai/user/science-prof-robot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use autoskill to identify which available agent skills are relevant to a task, review a scored execution plan, and choose whether any recommended or high-risk skills should run. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A downstream skill selected through autoskill may perform high-risk actions such as deployment, billing, account operations, database changes, or external communications. <br>
Mitigation: Review the execution plan before confirmation, decline any downstream skill you do not trust, and treat skills marked high-risk as requiring separate scrutiny. <br>
Risk: Skill recommendations can be incomplete or misleading if the task context or available skill inventory is ambiguous. <br>
Mitigation: Use the scored table and reasons as decision support, then confirm only the skills that match the actual task. <br>
Risk: Installing the artifact creates a persistent /autoskill command in the local Claude configuration. <br>
Mitigation: Install only when persistent routing behavior is desired, and review install.sh before running it. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/science-prof-robot/autoskill) <br>
- [Project homepage](https://github.com/Science-Prof-Robot/autoskill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown decision tables, execution previews, confirmation prompts, and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local git and language-detection shell commands in its preamble; downstream skill execution requires explicit user confirmation.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
