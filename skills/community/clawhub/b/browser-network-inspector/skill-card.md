## Description: <br>
Browser-side request inspection and reporting for user-authorized web debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dougzl](https://clawhub.ai/user/dougzl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect browser-side fetch, XMLHttpRequest, and basic WebSocket activity for web pages they are authorized to debug, then produce redacted JSON and Markdown reports for analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can capture and save sensitive browser traffic. <br>
Mitigation: Use it only on sites and sessions the user is authorized to inspect, prefer isolated or throwaway browser sessions, review reports before sharing, and delete report files when finished. <br>
Risk: Captured browser activity may include more hosts or messages than intended. <br>
Mitigation: Configure include and exclude host filters before capture and disable WebSocket capture when it is not needed. <br>
Risk: Redaction and truncation reduce exposure but may not remove every sensitive value. <br>
Mitigation: Treat generated JSON and Markdown reports as sensitive artifacts and avoid committing or echoing raw logs into chat. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dougzl/browser-network-inspector) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON capture files, Markdown reports, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Request and response content is truncated and sensitive fields are redacted before export.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
