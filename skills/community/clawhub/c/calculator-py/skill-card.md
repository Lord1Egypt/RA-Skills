## Description: <br>
A local Python calculator skill that lets agents delegate arithmetic, matrix, statistics, high-precision, optimization, integration, and signal-processing tasks to numerical computing libraries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leonardo-lb](https://clawhub.ai/user/leonardo-lb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run local numerical computations when model-only arithmetic may be unreliable, including matrix operations, statistics, arbitrary precision, optimization, integration, and signal processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted expressions passed to the calculator may execute local shell commands. <br>
Mitigation: Use only with trusted expressions in an isolated environment; replace eval-style parsing with a strict math parser or AST allowlist and add runtime limits before accepting untrusted input. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leonardo-lb/calculator-py) <br>
- [README_EN.md](README_EN.md) <br>
- [README.md](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text stdout with section headers; errors are written to stderr.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local numerical results through Python command invocations and returns nonzero exit codes for errors.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
