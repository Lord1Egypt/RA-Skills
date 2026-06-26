## Description: <br>
Deep Coding coordinates an Orchestrator, Builders, and Reviewers to decompose complex software projects, implement modules, review changes, and verify work with end-to-end tests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[extraterrest](https://clawhub.ai/user/extraterrest) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to coordinate multi-agent implementation of complex coding projects, including module decomposition, builder assignment, reviewer testing, progress tracking, and final smoke testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local dashboard can expose project files and logs when run from a workspace that contains credentials, private logs, or unrelated projects. <br>
Mitigation: Run it only in a dedicated trusted project workspace, keep it bound to localhost, avoid storing secrets in that workspace, and review the log path handling before use. <br>
Risk: Builder and Reviewer workflows may execute generated project code, tests, browsers, and local shell commands. <br>
Mitigation: Use containers or virtual machines for untrusted projects, review generated changes before relying on them, and restrict tool access to the minimum needed for the project. <br>


## Reference(s): <br>
- [Deep Coding on ClawHub](https://clawhub.ai/extraterrest/deep-coding) <br>
- [Architecture Reference](references/architecture.md) <br>
- [Orchestrator Rules](references/orchestrator-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, JSON, Shell commands, Code, Markdown] <br>
**Output Format:** [Markdown guidance with JSON request snippets, shell commands, project files, review notes, and progress updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Project-specific outputs may include generated code, local dashboard files, agent logs, and end-to-end test results.] <br>

## Skill Version(s): <br>
0.0.3 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
