## Description: <br>
Routes user requests to specialist agents using configured intent-matching rules, then integrates the results with retry, fallback, logging, and limited parallel dispatch support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daxiangnaoyang](https://clawhub.ai/user/daxiangnaoyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users and builders can use this skill to classify incoming requests, route work to coding, research, writing, design, or management agents, and combine the returned results into a single response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts may be forwarded to routed specialist agents and recorded as dispatch metadata. <br>
Mitigation: Avoid secrets, private business data, and regulated personal information unless that content is approved for routed agent processing and logging. <br>
Risk: Broad routing rules may send a request to an unintended specialist agent. <br>
Mitigation: Review routing patterns and test representative prompts before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daxiangnaoyang/daxiang-agent-dispatch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with code and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May route prompts to specialist agents, retry failed dispatches, fall back to the main agent, and log dispatch metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
