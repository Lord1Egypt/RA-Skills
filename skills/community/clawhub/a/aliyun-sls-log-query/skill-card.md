## Description: <br>
Use when querying or troubleshooting logs in Alibaba Cloud Log Service (SLS) with query|analysis syntax and the Python SDK for time-bounded search, error investigation, and root-cause analysis workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to query Alibaba Cloud SLS logstores, troubleshoot errors, and summarize operational evidence over bounded time ranges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud log access can expose secrets, personal data, or operationally sensitive information. <br>
Mitigation: Use dedicated least-privileged read-only SLS credentials, redact saved outputs, and avoid retaining sensitive log contents. <br>
Risk: Broad or long-running log queries can return excessive data or increase operational cost. <br>
Mitigation: Keep queries time-bounded, use limits, and narrow filters before expanding scope. <br>
Risk: Unpinned SDK dependencies can change behavior across installs. <br>
Mitigation: Install in a virtual environment and pin the Alibaba Cloud Log Service SDK version for repeatable deployments. <br>


## Reference(s): <br>
- [SLS Query and Analysis Syntax Notes](references/query-syntax.md) <br>
- [Python SDK Basic Calls](references/python-sdk.md) <br>
- [SLS Troubleshooting Query Templates](references/templates.md) <br>
- [Source List](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline Python and bash examples; helper scripts emit newline-delimited JSON log rows.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries should be time-bounded and limited; helper scripts may report partial failures for individual logstores.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
