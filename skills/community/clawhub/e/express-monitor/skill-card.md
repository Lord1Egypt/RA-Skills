## Description: <br>
Tracks package delivery status, queries logistics updates by tracking number, stores local delivery history, and supports phone-number binding for express monitoring workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to query package tracking numbers, review recent delivery history, and manage locally stored phone bindings for delivery monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Phone numbers and delivery history are stored locally in readable JSON despite documentation claiming encrypted phone storage. <br>
Mitigation: Review the local data directory before use, avoid storing sensitive phone numbers on shared systems, and require implementation updates before relying on encrypted storage claims. <br>
Risk: Tracking numbers are sent to Kuaidi100 endpoints for company detection and logistics lookup. <br>
Mitigation: Use the skill only when users consent to sending tracking identifiers to Kuaidi100 and when that service is acceptable for the deployment environment. <br>
Risk: Advertised automatic phone-based monitoring and Feishu synchronization are not fully supported by the artifact behavior. <br>
Mitigation: Treat phone-based monitoring and Feishu sync as unavailable unless the maintainer updates the implementation and documentation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hongjiahao371-pixel/express-monitor) <br>
- [Kuaidi100 mobile site](https://m.kuaidi100.com/) <br>
- [Kuaidi100 query endpoint](https://m.kuaidi100.com/query) <br>
- [Kuaidi100 auto-detect endpoint](https://m.kuaidi100.com/apicenter/kdquerytools.do?method=autoComNum) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command output and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local JSON files for phone bindings and delivery history under ~/.openclaw/workspace/data/express/.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
