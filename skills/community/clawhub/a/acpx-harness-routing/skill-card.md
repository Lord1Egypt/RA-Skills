## Description: <br>
Routes harness tasks to Claude, Codex, or Gemini via ACPX with explicit approval, non-interactive execution, session, working-directory, and timeout rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoyang78](https://clawhub.ai/user/chaoyang78) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to route one-shot and multi-turn harness work across Claude, Codex, and Gemini while preserving session continuity and explicit execution boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Blanket approval and persistent ACPX sessions can allow delegated agents to make unattended file changes. <br>
Mitigation: Use disposable or tightly scoped workspaces, set explicit task boundaries, and avoid sensitive files, credentials, production systems, or important repositories. <br>
Risk: Non-interactive harness runs may complete without case-by-case review. <br>
Mitigation: Review generated commands, changed files, and final outputs before relying on or deploying results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chaoyang78/acpx-harness-routing) <br>
- [Publisher profile](https://clawhub.ai/user/chaoyang78) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with command templates and decision rules] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes routing choices, required ACPX flags, session naming, working-directory rules, timeout guidance, and task-brief structure.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
