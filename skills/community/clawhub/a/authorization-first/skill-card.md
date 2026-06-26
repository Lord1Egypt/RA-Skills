## Description: <br>
Requires an agent to explain proposed changes, risks, and impact, then obtain explicit user authorization before modifying files, running state-changing commands, changing configuration, or making external calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pikaqiuyaya](https://clawhub.ai/user/pikaqiuyaya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to make an assistant pause before impactful operations, present the intended action and risks, and wait for explicit approval. It is most useful where an agent may edit files, run commands, update configuration, or call external services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users who cannot read the Chinese instructions may misunderstand when authorization is required. <br>
Mitigation: Install only after reading the instructions directly or translating them accurately. <br>
Risk: The skill encourages asking before impactful operations, but an approved command or file change could still be harmful if the user does not review it. <br>
Mitigation: Review proposed commands, file paths, diffs, external calls, and stated risks before approving execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pikaqiuyaya/authorization-first) <br>
- [Publisher profile](https://clawhub.ai/user/pikaqiuyaya) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with command, diff, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides authorization request templates, approval levels, error-handling guidance, and a pre-execution checklist.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
