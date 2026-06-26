## Description: <br>
China Express Query helps users look up shipment status for major Chinese courier companies and can auto-detect the carrier from a tracking number. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hyqdq888](https://clawhub.ai/user/hyqdq888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Chinese package tracking numbers from the command line, optionally selecting a carrier and writing results to a file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tracking numbers are sent to Kuaidi100 and Baidu during lookup. <br>
Mitigation: Use only when sharing tracking numbers with those third-party services is acceptable. <br>
Risk: Lookup failures may be displayed as successful tracking-like results. <br>
Mitigation: Treat returned tracking data as unverified when source lookups fail and confirm important shipments with the courier or an official tracking page. <br>


## Reference(s): <br>
- [China Express Query on ClawHub](https://clawhub.ai/hyqdq888/china-express-query) <br>
- [Kuaidi100](https://www.kuaidi100.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Console text with optional file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and network access to third-party courier lookup services; no API key is declared.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
