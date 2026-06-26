## Description: <br>
Multi-Agent Memory + Dispatch System. 4-tier memory (HOT/WARM/COLD/ARCHIVE), cross-channel sharing, dispatch loop with auto-learning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenshuangl](https://clawhub.ai/user/wenshuangl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent-system builders use this skill to add local multi-agent memory, cross-channel recall, dispatch logging, and memory lifecycle workflows to agent projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cross-agent and cross-channel memory sharing can expose stored context beyond the expected agent or channel. <br>
Mitigation: Configure explicit sharing rules and limit which ~/.agent-mem agent folders are indexed before using the skill with sensitive work. <br>
Risk: A background process hook in engine_v2.py may run behavior users have not reviewed. <br>
Mitigation: Review or disable the dbridge launcher before installation or deployment. <br>
Risk: Forgetting and cache-clear paths can delete stored memory. <br>
Mitigation: Keep backups of important memory stores and test cleanup behavior before relying on it in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wenshuangl/agent-mem) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory and dispatch guidance; runtime behavior stores and indexes data under local agent memory directories.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
