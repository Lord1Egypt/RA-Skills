## Description: <br>
Standardized ClearML metrics logging patterns for PDEBench experiment scripts, covering train loss, validation metrics, competition scores, PDE residuals, and TensorBoardX integration for dist/expflow compatibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diamond2nv](https://clawhub.ai/user/diamond2nv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when creating or modifying PDEBench training and evaluation scripts that need consistent ClearML metric logging. It provides naming conventions and code patterns for training loss, validation metrics, competition scores, PDE residuals, system metrics, k-fold summaries, and TensorBoardX plus ClearML dual logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ClearML metric logging may report validation scores, competition results, experiment metadata, GPU telemetry, or other system values that are sensitive in some environments. <br>
Mitigation: Review the metrics and system values your scripts report before enabling ClearML logging, and avoid logging sensitive experiment or telemetry data unless it is approved for your environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/diamond2nv/clearml-metrics-logging-pattern) <br>
- [expflow homepage](https://github.com/diamond2nv/expflow) <br>
- [Publisher profile](https://clawhub.ai/user/diamond2nv) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for ClearML metric logging patterns; no hidden execution behavior identified by the provided security evidence.] <br>

## Skill Version(s): <br>
0.5.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
