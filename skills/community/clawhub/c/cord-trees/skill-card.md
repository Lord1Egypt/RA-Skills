## Description: <br>
Cord Trees helps agents build dynamic coordination trees at runtime, decomposing complex goals into spawn, fork, ask, and serial tasks with explicit dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moltenbot000](https://clawhub.ai/user/moltenbot000) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to plan and execute complex, decomposable work by deciding parallel research, dependency ordering, human checkpoints, and synthesis steps at runtime. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous multi-agent orchestration can spawn subagents and keep updating local state with too few built-in limits. <br>
Mitigation: Set explicit limits for subagent count, runtime, retries, file locations, and approval checkpoints before use. <br>
Risk: Subagent results may be stored in cord-state.json and reused in later prompts, which can expose sensitive work if used on secrets or confidential tasks. <br>
Mitigation: Avoid running the skill over secrets or sensitive work unless state file locations and reuse are acceptable and reviewed. <br>
Risk: Forked synthesis can carry incorrect or incomplete child-agent outputs into later decisions. <br>
Mitigation: Review child results and require human checkpoints before final synthesis, implementation, or high-impact decisions. <br>


## Reference(s): <br>
- [Cord protocol](https://github.com/kimjune01/cord) <br>
- [State Management Helpers](references/state-helpers.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with pseudocode and JSON state examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and update cord-state.json and spawn subagent sessions when used in a compatible agent environment.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
