## Description: <br>
Reviews Deep Agents code for bugs, anti-patterns, and improvements, including create_deep_agent, backend, subagent, middleware, and human-in-the-loop patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Deep Agents implementations for configuration bugs, unsafe backend choices, subagent and middleware mistakes, prompt issues, and performance concerns. It guides reviews to cite current file evidence before making findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reviews user-selected repositories and may quote file snippets in findings. <br>
Mitigation: Use it only on codebases whose contents may be summarized in agent output, and avoid repositories containing secrets or sensitive private material. <br>
Risk: Review guidance can be misleading if findings are made from memory or unstated assumptions. <br>
Mitigation: Require each finding to cite same-turn file and line evidence, and stop when required files or searches are unavailable. <br>


## Reference(s): <br>
- [Code Review Checklist](references/checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/anderskev/deepagents-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown review findings with file and line references, quoted code snippets, checklist results, and concise remediation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are evidence-bound and should stop rather than infer when relevant files or searches are missing.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
