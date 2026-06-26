## Description: <br>
Run GitHub Copilot CLI from OpenClaw for coding tasks in a target project directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cecwxf](https://clawhub.ai/user/cecwxf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to delegate implementation, debugging, refactoring, review, and scripted coding workflows to GitHub Copilot CLI from an OpenClaw session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copilot CLI execution can run commands, edit files, and affect GitHub repositories. <br>
Mitigation: Run the skill only in the intended repository and branch, review resulting changes before pushing or opening pull requests, and avoid broad GitHub tokens. <br>
Risk: Unrestricted --allow-all-tools use can grant broader command access than a task needs. <br>
Mitigation: Prefer scoped --allow-tool permissions, add deny rules for destructive commands when appropriate, and reserve --allow-all-tools for tasks that require full autonomy. <br>
Risk: Long-running delegated sessions can continue beyond the intended task window. <br>
Mitigation: Track session IDs, poll logs for completion, and stop background sessions when the task is done. <br>


## Reference(s): <br>
- [Copilot CLI Skill on ClawHub](https://clawhub.ai/cecwxf/copilot-cli-skill) <br>
- [Copilot CLI documentation summary](references/copilot-doc-summary.md) <br>
- [Copilot CLI usage recipes](references/copilot-usage-recipes.md) <br>
- [About GitHub Copilot CLI](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-copilot-cli) <br>
- [Install GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli) <br>
- [Use GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands and execution notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed and authenticated GitHub Copilot CLI in the target repository.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
