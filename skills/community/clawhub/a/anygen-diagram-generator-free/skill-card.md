## Description: <br>
Generates basic diagrams such as flowcharts, architecture diagrams, and sequence diagrams from text descriptions by using AnyGen CLI and the AnyGen server-side smart_draw workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, product teams, and operations teams use this skill to turn written process, system, or workflow descriptions into basic visual diagrams for documentation and review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagram descriptions are processed by AnyGen's external service and may contain sensitive system, architecture, or business details. <br>
Mitigation: Avoid submitting secrets, credentials, private architecture details, or confidential business data unless the AnyGen account and data-handling terms are acceptable. <br>
Risk: The workflow requires command execution and dependency installation for the AnyGen toolchain. <br>
Mitigation: Review the skill and commands before installation, use a controlled agent environment, and grant only the execution access needed for the diagram generation workflow. <br>
Risk: API keys may be exposed if pasted into prompts, logs, generated files, or version control. <br>
Mitigation: Store API keys in environment variables or approved secret storage, avoid hard-coding credentials, and rotate keys if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/anygen-diagram-generator-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return links or generated image outputs from the AnyGen service, along with execution logs or error guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
