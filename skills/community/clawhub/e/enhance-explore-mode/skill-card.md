## Description: <br>
探索模式 (Explore Mode) guides an agent through read-only, systematic exploration of a codebase, system, or topic before answering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jobzhao15](https://clawhub.ai/user/jobzhao15) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to understand unfamiliar repositories, trace feature implementations, investigate bugs, and produce a structured exploration report without modifying files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read and summarize repository contents, including sensitive code or business context present in the workspace. <br>
Mitigation: Use normal care with private repositories and remove secrets or confidential material before asking an agent to explore them. <br>
Risk: Exploration findings can be incomplete or mistaken if the agent samples too narrowly or fails to distinguish evidence from inference. <br>
Mitigation: Review cited file paths and line references, and ask for follow-up verification before acting on high-impact findings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jobzhao15/enhance-explore-mode) <br>
- [Project homepage](https://github.com/jobzhao15/openclaw-enhance) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown exploration report with findings, direct answers, and optional recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only workflow; no files are modified by the skill itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
