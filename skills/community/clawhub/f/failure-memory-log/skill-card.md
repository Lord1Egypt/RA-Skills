## Description: <br>
Records agent failures in a searchable local Markdown log and supports recall and reporting so repeated mistakes can be avoided. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VoidLight00](https://clawhub.ai/user/VoidLight00) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to record command, API, configuration, and task failures with context, root cause, resolution, and prevention notes. Before related work, they can search the log to recall known pitfalls and generate summaries of repeated failure patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive error details, credentials, customer data, private paths, or confidential operational details could be saved in the local failure log. <br>
Mitigation: Keep the memory directory in an appropriate project location, review it periodically, and avoid logging secrets or confidential data. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown records and reports with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates a local memory/failures.md file when initialized and used by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
