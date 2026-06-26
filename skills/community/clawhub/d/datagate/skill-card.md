## Description: <br>
DataGate validates JSON data against JSON Schema Draft 2020-12 through a local API and returns validity, error counts, field paths, and violation messages for agent pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use DataGate to validate JSON payloads against JSON Schema before agents or services pass data downstream. It exposes language-agnostic validation through a local API that returns validity, error counts, paths, and messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local validation service exposure or resource use from untrusted payloads. <br>
Mitigation: Run in an isolated Python environment, keep the service bound to localhost unless network access is intentional, and avoid validating secrets or very large untrusted payloads. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mirni/datagate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local API usage guidance and validation response details including valid, error_count, and errors.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
