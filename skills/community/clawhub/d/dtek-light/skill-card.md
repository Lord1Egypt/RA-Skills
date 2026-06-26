## Description: <br>
Checks current electricity availability for a fixed Odesa address through the DTEK Odesa power outage website. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kapishdima](https://clawhub.ai/user/kapishdima) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can ask an agent whether power is currently available and, when reported by the source site, when service may be restored for the configured Odesa address. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill launches a local Node.js Playwright script with Chromium and contacts DTEK's public outage page. <br>
Mitigation: Install only in environments where local browser automation and access to the DTEK public outage page are acceptable. <br>
Risk: Responses may be shared in user-facing or professional settings and the source skill includes informal wording. <br>
Mitigation: Review or edit the response wording before using the skill in shared, Ukrainian-language, or professional contexts. <br>
Risk: The result applies to one fixed Odesa address and may not represent other locations. <br>
Mitigation: Confirm that the configured address is the intended location before relying on the status. <br>


## Reference(s): <br>
- [DTEK Odesa power outage page](https://www.dtek-oem.com.ua/ua/shutdowns) <br>
- [ClawHub skill page](https://clawhub.ai/kapishdima/dtek-light) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and status-based response text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The local script returns JSON status values that the agent turns into a user-facing response.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
