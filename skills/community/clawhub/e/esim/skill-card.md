## Description: <br>
Implement and troubleshoot eSIM across consumer activation, carrier integration, and RSP development. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, carrier integration teams, and support engineers use this skill as a concise reference for eSIM activation formats, platform API restrictions, certification requirements, and troubleshooting decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Following profile deletion troubleshooting without a replacement activation path can temporarily interrupt mobile service. <br>
Mitigation: Confirm carrier support or a replacement activation code before deleting an eSIM profile. <br>
Risk: Applying consumer RSP guidance to M2M RSP, or the reverse, can lead to incorrect implementation decisions. <br>
Mitigation: Verify whether SGP.22 consumer RSP or SGP.02 M2M RSP applies before planning the activation or integration flow. <br>
Risk: Assuming public mobile APIs can provision arbitrary eSIMs may lead to rejected apps or blocked integrations. <br>
Mitigation: Confirm Apple carrier entitlements, Android carrier privilege requirements, and carrier partnership status before designing provisioning features. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/esim) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown reference guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only guidance with no executable behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
