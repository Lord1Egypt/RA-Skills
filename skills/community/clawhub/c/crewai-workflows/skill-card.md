## Description: <br>
Executes remote AI crew workflows for marketing content, customer support responses, business data analysis, and social media calendar generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Rita5fr](https://clawhub.ai/user/Rita5fr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to call hosted CrewAI workflows that draft marketing copy, support responses, data-analysis summaries, and social media plans from user-provided JSON inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contains a real-looking API key in its instructions. <br>
Mitigation: Rotate or replace the key before use and provide credentials through a trusted environment variable or secret manager. <br>
Risk: User-provided business or customer content is sent to the remote crew.iclautomation.me service and its model providers. <br>
Mitigation: Use only with approved data, avoid secrets and regulated content unless authorized, and verify that the service and providers are trusted for the intended use case. <br>
Risk: The helper script saves full service responses under /tmp, which can expose sensitive generated output on shared systems. <br>
Mitigation: Disable or remove automatic response saving when outputs may contain confidential information, or clean up the saved files immediately after review. <br>


## Reference(s): <br>
- [CrewAI workflow service](https://crew.iclautomation.me) <br>
- [CrewAI service health check](https://crew.iclautomation.me/health) <br>
- [ClawHub skill page](https://clawhub.ai/Rita5fr/crewai-workflows) <br>
- [Publisher profile](https://clawhub.ai/user/Rita5fr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calls a remote service with JSON input, extracts result.output, and may save the full JSON response to /tmp for inspection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
