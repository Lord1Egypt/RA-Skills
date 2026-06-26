## Description: <br>
Add, extend, fix, or document the Subagents panel inside the OpenClaw Control UI Agents page, including editable subagent settings, config save wiring, fallback settings, and alignment with runtime subagent model precedence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement or maintain the OpenClaw Agents-page Subagents tab, including model override controls, shared subagent defaults, config save wiring, and focused UI tests aligned with runtime precedence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated edits may change shared subagent defaults or limits that affect multiple OpenClaw agents. <br>
Mitigation: Review diffs for agents.defaults.subagents and per-agent subagent overrides before saving or deploying. <br>
Risk: Suggested pnpm validation commands execute project tooling in the target repository. <br>
Mitigation: Run the suggested checks only in a trusted OpenClaw checkout. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maverick-software/agent-subagents-ui) <br>
- [File map](references/file-map.md) <br>
- [Runtime precedence](references/runtime-precedence.md) <br>
- [Implementation notes](references/implementation-notes.txt) <br>
- [Subagents panel reference implementation](references/agents-panel-subagents.ts.txt) <br>
- [Agents page integration reference](references/agents.ts.txt) <br>
- [App render wiring reference](references/app-render.subagents.txt) <br>
- [Agents UI tests reference](references/agents.test.ts.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline code paths and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for review before applying changes to an OpenClaw repository.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
