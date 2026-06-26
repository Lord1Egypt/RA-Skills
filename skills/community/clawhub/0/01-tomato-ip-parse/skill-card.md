## Description: <br>
Analyzes Tomato novel IP content to extract worldbuilding, character details, core conflict, highlight points, and a basic compliance result for AI short-drama adaptation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ghwyever](https://clawhub.ai/user/ghwyever) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content adaptation teams and agents use this skill to turn Chinese web novel text into structured adaptation notes for short-drama development. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Full manuscript text is sent to the configured model API. <br>
Mitigation: Use only an API_BASE provider you trust and avoid sending sensitive or unauthorized manuscript content. <br>
Risk: The returned compliance_check is not a real compliance review and may mark unsafe content as safe. <br>
Mitigation: Treat compliance_check as non-authoritative and run a separate content, legal, or policy review before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ghwyever/01-tomato-ip-parse) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [JSON object with ip_info and compliance_check fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires API_KEY, API_BASE, and MODEL_NAME; sends novel text to the configured model API.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
