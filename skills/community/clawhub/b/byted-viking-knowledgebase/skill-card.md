## Description: <br>
Searches a configured Viking knowledge base for query keywords and returns relevant knowledge content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to turn a Viking knowledge-base search request into a Python command that queries a configured knowledge service and returns matching text results. <br>

### Deployment Geography for Use: <br>
Global, subject to the configured Volcengine/Viking service region. <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and an API token may be sent to the external knowledge service over unencrypted HTTP. <br>
Mitigation: Review before use, switch requests to HTTPS where possible, and treat both queries and credentials as sensitive. <br>
Risk: The skill may activate too broadly for general knowledge-base mentions. <br>
Mitigation: Invoke it only for explicit Viking knowledge-base search requests and confirm the search query before sending it to the service. <br>
Risk: Unpinned Python dependencies can change behavior across installations. <br>
Mitigation: Pin and review dependencies in the deployment environment before installing or running the skill. <br>


## Reference(s): <br>
- [Byted Viking Knowledgebase on ClawHub](https://clawhub.ai/volcengine-skills/byted-viking-knowledgebase) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration guidance] <br>
**Output Format:** [Plain text results and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Viking knowledge-base service credentials and Python dependencies before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
