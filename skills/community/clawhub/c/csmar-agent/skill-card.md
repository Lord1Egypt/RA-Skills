## Description: <br>
csmar-agent queries financial report information for A-share companies through a CSMAR-related service and streams the returned content without an added summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xmpx8](https://clawhub.ai/user/xmpx8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to ask for A-share company financial report information and receive streamed text output from the configured backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User queries are forwarded to an undisclosed plain-HTTP private-IP service. <br>
Mitigation: Use only when the endpoint and network are trusted, controlled, and approved; avoid confidential or proprietary prompts otherwise. <br>
Risk: Financial research responses are streamed from the backend without local validation. <br>
Mitigation: Review returned content before relying on it for business, investment, or reporting decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xmpx8/csmar-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands] <br>
**Output Format:** [Plain text streamed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Streams content chunks and omits wrapping summary text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
