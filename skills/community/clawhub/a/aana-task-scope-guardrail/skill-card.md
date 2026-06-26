## Description: <br>
Ensures agents only perform requested tasks using relevant data, ask before expanding scope, and stop when the request is complete. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this instruction-only skill to keep OpenClaw-style agents within the current user request, limit data use to task-relevant context, and require approval before broader work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may expand a narrow request into broader work, access unrelated private data, or continue after the requested task is complete. <br>
Mitigation: Use the skill's scope gate to classify each next action, narrow or ask when scope is ambiguous, and stop once the completion target is satisfied. <br>
Risk: Marketplace capability tags may mislead users about the skill's purpose. <br>
Mitigation: Review the release metadata before deployment and correct unrelated capability tags so the listing matches the instruction-only guardrail behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindbomber/aana-task-scope-guardrail) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [Task scope gate schema](schemas/task-scope-gate.schema.json) <br>
- [Redacted task scope gate example](examples/redacted-task-scope-gate.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown instructions with an optional redacted JSON-compatible scope gate payload] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; does not install dependencies, execute commands, call services, write files, or persist memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact manifest lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
