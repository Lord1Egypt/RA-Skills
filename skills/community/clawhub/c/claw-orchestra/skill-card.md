## Description: <br>
OpenClaw native multi-agent orchestrator based on the AOrchestra 4-tuple (I, C, T, M) abstraction, with dynamic sub-agent creation, parallel execution, smart routing, an experience store, and cost tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zcyynl](https://clawhub.ai/user/zcyynl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to break complex work into specialized sub-agent tasks, route context, select models and tools, and integrate the resulting outputs into a final report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic multi-agent delegation can expand task scope and tool access beyond what a user expected. <br>
Mitigation: Enable the skill only for tasks where delegation is intended, review activation triggers, and restrict sub-agent tools to the minimum needed for the task. <br>
Risk: Sub-agent outputs may be integrated into a final report before the user reviews each intermediate result. <br>
Mitigation: Require review of sub-agent summaries and final report files before relying on the output for decisions or publication. <br>
Risk: Experience and cost tracking can persist task text, model usage, token counts, and session-related metadata. <br>
Mitigation: Configure storage locations and retention before use, and avoid sensitive tasks unless persistence can be disabled or scoped appropriately. <br>
Risk: The skill targets OpenClaw integration and named internal models, so behavior may degrade in environments without those tools or models. <br>
Mitigation: Validate model and tool availability in a controlled workspace before using the skill in routine workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zcyynl/claw-orchestra) <br>
- [AOrchestra paper](https://arxiv.org/abs/2602.03786) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [ClawOrchestra repository link listed in artifact](https://github.com/zcyynl/claw-orchestra) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with optional code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include execution statistics, token usage estimates, sub-agent summaries, and generated report files.] <br>

## Skill Version(s): <br>
0.1.0 (source: target metadata and pyproject.toml; package.json lists 0.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
