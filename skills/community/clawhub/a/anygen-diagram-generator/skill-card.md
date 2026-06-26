## Description: <br>
Use this skill when an agent needs to create diagrams, flowcharts, or visual structures such as architecture diagrams, mind maps, org charts, user journeys, ER diagrams, sequence diagrams, process flows, decision trees, network topologies, class diagrams, Gantt charts, SWOT analysis diagrams, wireframes, or sitemaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[logictortoise](https://clawhub.ai/user/logictortoise) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and other agent users can use this skill to route diagram requests through the AnyGen CLI and generate visual charts server-side. It is suited for creating common technical and planning diagrams from natural-language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagram content is sent to AnyGen's servers. <br>
Mitigation: Avoid sending confidential diagrams unless AnyGen is approved for that data. <br>
Risk: The skill can ask the agent to install an additional helper skill. <br>
Mitigation: Manually inspect and approve the helper-skill installation instead of allowing an automatic install. <br>
Risk: The skill requires an AnyGen API key. <br>
Mitigation: Use a dedicated, revocable API key and rotate or revoke it when access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/logictortoise/anygen-diagram-generator) <br>
- [AnyGen website](https://www.anygen.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the anygen CLI and ANYGEN_API_KEY; diagram content is sent to AnyGen's servers.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
