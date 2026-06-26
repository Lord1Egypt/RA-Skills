## Description: <br>
Orchestrates an agent build workflow by parsing a request, coordinating research workers, delegating construction to Builder, and reporting the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DweikAnas](https://clawhub.ai/user/DweikAnas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to coordinate new agent builds and error-handling workflows. It turns an initial build request into parsed YAML, research worker outputs, Builder instructions, and a final build result report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow launches local research-worker and Builder agents that can create build files. <br>
Mitigation: Verify the dependent local worker and Builder skills before use, and review generated build outputs before deployment. <br>
Risk: Build prompts and research outputs are saved locally and may contain sensitive project details. <br>
Mitigation: Do not include secrets, tokens, private credentials, or other sensitive values in build prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DweikAnas/build-pipeline) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with YAML schemas, shell commands, progress events, and status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local YAML build, parse, research, and builder result files under the build workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
