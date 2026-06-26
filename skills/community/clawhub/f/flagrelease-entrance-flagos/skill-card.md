## Description: <br>
Full FlagRelease pipeline orchestrator for LLM deployment, verification, and benchmarking on multi-chip GPU backends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wbavon](https://clawhub.ai/user/wbavon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to run a structured LLM deployment pipeline inside an existing GPU Docker container, verify model serving, and collect benchmark results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow runs Docker and package installation steps inside a GPU container. <br>
Mitigation: Run it only against a known, disposable or recoverable non-production container and confirm the container name before execution. <br>
Risk: Model downloads, serving checks, and benchmarks can consume GPU, disk, network, and runtime budget. <br>
Mitigation: Confirm the model path, expected tensor parallel settings, and available resources before starting the pipeline. <br>
Risk: The orchestrator delegates detailed install and test behavior to referenced sibling skills. <br>
Mitigation: Review the sibling skills before installation because they contain the package installation, model verification, and benchmarking logic. <br>


## Reference(s): <br>
- [Pipeline State Schema](references/pipeline-state.md) <br>
- [ClawHub skill page](https://clawhub.ai/wbavon/flagrelease-entrance-flagos) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summary with structured JSON report content and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports PASS, PARTIAL, or FAIL status with step diagnostics, package results, model verification details, errors, and benchmark tables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
