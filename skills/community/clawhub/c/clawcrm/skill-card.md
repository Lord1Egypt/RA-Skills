## Description: <br>
Agent-native CRM built for AI agents to manage sales pipelines autonomously. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[giorgallidis](https://clawhub.ai/user/giorgallidis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to configure a ClawCRM workspace, create and enrich sales leads, send delayed email sequences, track proposal engagement, and analyze pipeline health through the ClawCRM API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent administrator-like authority over CRM records and sales workflows. <br>
Mitigation: Use a dedicated scoped key where available, test first in a sandbox workspace, and limit access to data and actions the agent actually needs. <br>
Risk: Lead enrichment may process personal or professional contact data without sufficient consent or retention review. <br>
Mitigation: Require explicit human approval before enrichment and confirm consent, retention, deletion, and audit-log controls before using real contacts. <br>
Risk: Delayed outbound email sequences could be sent without clear approval, opt-out, rate-limit, or cancellation safeguards. <br>
Mitigation: Require human approval before any outbound sequence and verify opt-out, rate-limit, audit-log, and cancellation controls in the ClawCRM service. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/giorgallidis/clawcrm) <br>
- [ClawCRM Homepage](https://clawcrm.ai) <br>
- [ReadyCRM Service](https://readycrm.netlify.app) <br>
- [ReadyCRM Repository](https://github.com/Protosome-Inc/ReadyCRM) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON request/response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a CLAWCRM_API_KEY or administrator token for authenticated ClawCRM API operations.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
