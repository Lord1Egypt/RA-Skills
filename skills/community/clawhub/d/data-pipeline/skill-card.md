## Description: <br>
Lightweight JavaScript ETL pipeline helper for composing data transformation, validation, analysis, lifecycle hooks, retries, timeouts, and built-in transformers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pagoda111king](https://clawhub.ai/user/pagoda111king) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build local JavaScript data-processing pipelines for data cleaning, ETL workflows, validation, grouping, aggregation, and API data shaping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided stages, validators, aggregations, and callbacks execute as normal JavaScript in the local process. <br>
Mitigation: Review custom functions before running them and avoid processing sensitive data with untrusted callback code. <br>
Risk: This is an unvetted third-party helper. <br>
Mitigation: Install it only when the publisher and local data-processing behavior match your requirements. <br>


## Reference(s): <br>
- [ClawHub Data Pipeline release page](https://clawhub.ai/pagoda111king/data-pipeline) <br>
- [Artifact usage guide](artifact/SKILL.md) <br>
- [Basic usage examples](artifact/examples/basic-usage.js) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with JavaScript code snippets and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for local JavaScript data transformation workflows.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
