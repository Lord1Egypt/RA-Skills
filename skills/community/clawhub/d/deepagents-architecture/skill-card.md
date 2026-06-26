## Description: <br>
Guides architectural decisions for Deep Agents applications. Use when deciding between Deep Agents vs alternatives, choosing backend strategies, designing subagent systems, or selecting middleware approaches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose whether Deep Agents fits an application and to document backend, subagent, middleware, human-in-the-loop, context, and checkpointing decisions before implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deep Agents implementations can expose broad filesystem roots, command execution, subagent tool access, or persistent memory if architecture choices are not scoped before implementation. <br>
Mitigation: Use the skill's decision gates and the security guidance to explicitly scope filesystem roots, command approvals, subagent tool access, and memory retention before building. <br>
Risk: Documentation-only architecture guidance may be applied incorrectly or become outdated as Deep Agents behavior changes. <br>
Mitigation: Review the generated architecture decisions against current project requirements and scan the skill before deployment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with tables, decision gates, and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only architecture guidance; no code execution, credential access, or installation actions are performed by the skill itself.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
