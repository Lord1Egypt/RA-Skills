## Description: <br>
Guides agents through submitting, monitoring, canceling, deleting, and retrieving results for FaMou evolution experiments with famou-ctl. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoM0](https://clawhub.ai/user/zhaoM0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and experiment operators use this skill to manage FaMou evolution experiments from a config.yaml file, including submission, status polling, logs, results, and lifecycle actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store a FaMou API key at ~/.famou-ctl/settings.json. <br>
Mitigation: Use a limited-scope key, run the SDK in an isolated environment, and require explicit approval before writing or overwriting credentials. <br>
Risk: The skill can cancel, delete, or resubmit experiments. <br>
Mitigation: Require explicit user confirmation before canceling, deleting, editing experiment files, or resubmitting experiments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaoM0/famou-experiment-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide installation, local API configuration, experiment submission, status checks, logs, results, cancellation, deletion, and resubmission.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
