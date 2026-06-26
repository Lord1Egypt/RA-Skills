## Description: <br>
Tracks intent drift across multi-turn tasks and advises whether an agent should patch, replan, or abort when a user's instruction changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deepseek609609-collab](https://clawhub.ai/user/deepseek609609-collab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill during multi-step work to compare prior constraints with a new user instruction and decide whether to continue, roll back to an affected anchor, or stop for confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The patch, replan, or abort result is heuristic and could recommend the wrong continuation path for important work. <br>
Mitigation: Treat the result as advisory and keep explicit user confirmation for significant restarts, abandoned tasks, or high-impact changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deepseek609609-collab/daf-intent-guard) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [JSON decision output from a Python command-line helper, with Markdown usage guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs patch, replan, or abort with semantic distance, anchor drift, first affected anchor, and a short reason.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
