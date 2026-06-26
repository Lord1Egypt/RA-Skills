## Description: <br>
Retrieves Google Analytics 4 data for akku-alle.de, including page views, users, sessions, top pages, and traffic sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akkualle](https://clawhub.ai/user/akkualle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site operators, and analytics users use this skill to request recent Google Analytics 4 traffic metrics for akku-alle.de, including visitor counts, top pages, and traffic sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a local ga4-analytics executable that is not included in artifact/ for review. <br>
Mitigation: Review or obtain the executable before installation or execution, and deploy only a trusted copy. <br>
Risk: The skill uses Google Analytics credentials and a GA4 property identifier. <br>
Mitigation: Use read-only credentials scoped to the intended akku-alle.de GA4 property and rotate credentials if exposure is suspected. <br>
Risk: Always-on activation could run the analytics command for unrelated analytics requests. <br>
Mitigation: Disable always-on activation or narrow activation triggers to explicit GA4 requests for this property. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/akkualle/akkualle-ga4-analytics) <br>
- [Akkualle Publisher Profile](https://clawhub.ai/user/akkualle) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with shell command examples and tabular analytics summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GOOGLE_APPLICATION_CREDENTIALS and GA4_PROPERTY_ID environment variables; examples show a 7-day traffic overview and top-page table.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
