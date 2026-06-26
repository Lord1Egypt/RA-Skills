## Description: <br>
PipelineGate chains Green Helix tools into multi-step pipelines for scanning text and skills, checking scope and environment readiness, validating JSON, diffing text, and converting JSON or YAML. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use PipelineGate to run configured sequences of Green Helix checks and utility steps through a local pipeline API. It is suited for composing repeatable security, validation, diff, environment-readiness, and JSON/YAML conversion workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes a local pipeline service that executes submitted pipeline steps. <br>
Mitigation: Keep the uvicorn server bound to localhost and use it only with trusted callers. <br>
Risk: The check-env step can reveal whether requested environment variables are present or missing. <br>
Mitigation: Use check-env only with variable names you are comfortable revealing as present or absent. <br>
Risk: Pipeline execution depends on Green Helix modules imported by the runtime. <br>
Mitigation: Confirm the Green Helix modules are supplied by a trusted runtime before deployment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Analysis] <br>
**Output Format:** [JSON API responses with per-step result objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Pipelines accept 1 to 20 ordered steps; stop_on_error controls whether execution halts on the first failed step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
