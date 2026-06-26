## Description: <br>
Generate or refine agent-usable CLIs for existing software/codebases using the CLI-Anything methodology. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JasonChenJC](https://clawhub.ai/user/JasonChenJC) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to assess whether existing software can be exposed through agent-usable CLIs, inspect CLI-Anything harnesses, and adapt validated harness workflows into OpenClaw-compatible skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect a local CLI-Anything workspace through helper scripts and hardcoded workspace paths. <br>
Mitigation: Use it in a sandbox or with a reviewed project workspace when local code or private files may be present. <br>
Risk: Generated or adapted CLI harnesses may not match their claimed backend behavior until individually validated. <br>
Mitigation: Verify dependencies, CLI entry points, and minimal real-backend commands before treating a harness as usable. <br>


## Reference(s): <br>
- [Bundled Harnesses](references/bundled-harnesses.md) <br>
- [OpenClaw Adaptation Notes](references/openclaw-adaptation-notes.md) <br>
- [Validated Example: GIMP Harness](references/validated-example-gimp.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; helper scripts may print JSON summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is grounded in local CLI-Anything workspace inspection and bundled reference files.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
