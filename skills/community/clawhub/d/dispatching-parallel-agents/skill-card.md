## Description: <br>
Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlc000190](https://clawhub.ai/user/zlc000190) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to split independent coding, debugging, or test-failure investigations across parallel sub-agents, then review and integrate the returned work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated prompts may expose unnecessary secrets or unrelated private context. <br>
Mitigation: Provide only the context needed for each independent task and avoid including secrets in delegated prompts. <br>
Risk: Parallel agents may make conflicting or incorrect changes when tasks are not truly independent. <br>
Mitigation: Use parallel dispatch only for independent problem domains, review each summary, check file conflicts, and run the full relevant test suite before accepting changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zlc000190/dispatching-parallel-agents) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code] <br>
**Output Format:** [Markdown guidance with example agent prompts and task dispatch snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review each parallel-agent summary, check for conflicts, and run the relevant test suite before accepting integrated changes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
