## Description: <br>
Generate or refine agent-usable CLIs for existing software/codebases using the CLI-Anything methodology. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to assess whether CLI-Anything fits a target app or repository, reuse existing harness examples, and package generated or refined CLI workflows for OpenClaw-compatible agent use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested commands may be adapted to local tools or authenticated CLIs that can change state. <br>
Mitigation: Confirm the target, review the exact command, and use accounts or tokens with only the intended access before execution. <br>
Risk: Generated or third-party harness code may be incomplete, misleading, or unsafe if treated as trusted implementation. <br>
Mitigation: Review and scan harness code before deployment, then verify the entry point and real backend dependencies before claiming it works. <br>
Risk: Bundled harness examples are not all equally verified. <br>
Mitigation: Validate each selected harness independently; use the documented GIMP harness only as a first local demonstration target. <br>


## Reference(s): <br>
- [Bundled harnesses in CLI-Anything](references/bundled-harnesses.md) <br>
- [Adapting CLI-Anything into OpenClaw](references/openclaw-adaptation-notes.md) <br>
- [Validated example: gimp harness](references/validated-example-gimp.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON inspection output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated or refined harness files when the user asks to package or implement a CLI; review commands before execution.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
