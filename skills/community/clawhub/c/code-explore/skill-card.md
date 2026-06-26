## Description: <br>
Analyze a local codebase to explain directory structure, entrypoints, dependencies, call chains, and data flow without modifying code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sf0799](https://clawhub.ai/user/sf0799) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect a local codebase, locate entrypoints and core files, and explain dependencies, call paths, and data flow without changing project behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read and summarize project files relevant to the user's question. <br>
Mitigation: Use it only in repositories whose contents are appropriate to analyze in the agent conversation. <br>
Risk: Codebase explanations can be incomplete or misleading when relevant files have not been inspected. <br>
Mitigation: Require conclusions to cite code evidence and mark uninspected areas or assumptions as uncertain. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sf0799/code-explore) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown analysis with concise summaries and code-grounded findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only codebase analysis; no executable code or install hooks are included in the skill artifact.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
