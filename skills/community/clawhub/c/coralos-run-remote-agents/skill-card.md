## Description: <br>
End-to-end Coral Cloud workflow - discover registry remote agents, compose and launch a session of agents, then monitor and close it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omni-georgio](https://clawhub.ai/user/omni-georgio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to discover Coral Cloud registry agents, prepare a session payload, launch remote agents, and monitor session state through the Coral Cloud workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Creating Coral Cloud sessions can launch remote agents with selected payloads, namespaces, permissions, or costs. <br>
Mitigation: Before creating a session, review the selected agent, payload, namespace, and expected permissions or costs. <br>
Risk: Helper scripts or templates referenced by the workflow may come from outside the reviewed artifact. <br>
Mitigation: Treat separately downloaded helper scripts or templates as unreviewed until they are inspected and scanned. <br>


## Reference(s): <br>
- [Coral Cloud API guide](https://docs.coralos.ai/cloud/using-api) <br>
- [CoralOS ClawHub skill page](https://clawhub.ai/omni-georgio/coralos-run-remote-agents) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and API endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
