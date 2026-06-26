## Description: <br>
Check the status of an Appian deployment by UUID and optionally download its artifacts (log, package ZIP). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solarspiker](https://clawhub.ai/user/solarspiker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to monitor Appian deployment progress after export or deployment workflows and to retrieve deployment logs or package ZIP artifacts when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional artifact downloads may write outside the intended exports folder if the Appian response supplies a crafted filename. <br>
Mitigation: Avoid --download-log and --download-zip until filename handling is fixed, or use them only with a trusted Appian tenant and reviewed deployment responses. <br>
Risk: The skill requires an Appian API key and tenant URL. <br>
Mitigation: Use a least-privilege Appian API key and set APPIAN_BASE_URL only to a trusted Appian tenant. <br>


## Reference(s): <br>
- [Appian Deployment Results API](https://docs.appian.com/suite/help/25.4/Get_Deployment_Results_API.html) <br>
- [ClawHub skill page](https://clawhub.ai/solarspiker/appian-deploymtstatus) <br>
- [solarspiker publisher profile](https://clawhub.ai/user/solarspiker) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Console text with optional downloaded log or ZIP files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APPIAN_BASE_URL and APPIAN_API_KEY; optional wait and download flags control polling and artifact retrieval.] <br>

## Skill Version(s): <br>
1.2.0 (source: release evidence and script header) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
