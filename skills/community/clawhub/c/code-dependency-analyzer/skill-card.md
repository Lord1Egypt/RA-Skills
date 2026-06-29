## Description: <br>
Free tier: Code Dependency Analyzer - scan project dependencies, find outdated packages, and check dependency status with npm and pip commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingaiwork](https://clawhub.ai/user/kingaiwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to quickly inspect JavaScript and Python project dependencies, including outdated packages, npm audit output, and basic dependency summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running npm audit, npm outdated, or pip outdated may send dependency metadata to package registries. <br>
Mitigation: Review the project and registry privacy expectations before running the commands, especially in private or sensitive codebases. <br>
Risk: The free tier advertises circular-import detection, but the artifact only provides basic dependency-checking commands. <br>
Mitigation: Use the skill for npm and pip dependency checks and verify circular imports with a separate tool when that analysis is required. <br>
Risk: The skill includes sponsored service links unrelated to dependency analysis. <br>
Mitigation: Treat those links as advertising and evaluate them independently before using any promoted service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingaiwork/skills/code-dependency-analyzer) <br>
- [King AI Works homepage](https://kingai.work/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Analysis] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs proposed command sequences for npm and pip dependency checks; command results depend on the user's local project and package registries.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
