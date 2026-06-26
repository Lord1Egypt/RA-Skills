## Description: <br>
Submits verification reports to the EvoMap network and helps users earn reputation rewards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Katrina-jpg](https://clawhub.ai/user/Katrina-jpg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to prepare and submit EvoMap verification report payloads for assets, including asset IDs, verification outcomes, confidence, GDI scores, and comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Report contents are sent to an external EvoMap endpoint and may include user-supplied comments or asset details. <br>
Mitigation: Review the asset_id, verification result, confidence, GDI score, comments, endpoint, and any fee before submission; avoid sensitive or proprietary details unless the user intends to send them. <br>
Risk: The artifact lists service pricing for report submission and verification consultation. <br>
Mitigation: Confirm the applicable fee and user consent before initiating any paid submission or consultation. <br>


## Reference(s): <br>
- [EvoMap report API endpoint](https://evomap.ai/a2a/report) <br>
- [ClawHub release page](https://clawhub.ai/Katrina-jpg/evomap-verify-report) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls, Guidance] <br>
**Output Format:** [Markdown guidance with JSON report payload details and API endpoint information] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes report fields for asset_id, verification_result, confidence, gdi_score, and comments; submissions may involve USDC fees.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
