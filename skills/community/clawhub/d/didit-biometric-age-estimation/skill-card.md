## Description: <br>
Estimates a person's age from a facial image via the Didit standalone API, with passive liveness checking and configurable thresholds for age-gating workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rosasalberto](https://clawhub.ai/user/rosasalberto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and compliance teams use this skill to add biometric age-estimation and liveness checks to age-gated flows, including over-18 or over-21 checks and fallback paths for borderline cases. <br>

### Deployment Geography for Use: <br>
Global, with per-country age restrictions configured by the implementing service. <br>

## Known Risks and Mitigations: <br>
Risk: Facial images are sent to Didit for biometric age estimation, which creates privacy, consent, and retention obligations. <br>
Mitigation: Confirm user consent and legal basis before use, disclose Didit processing, and configure request saving or retention deliberately. <br>
Risk: DIDIT_API_KEY exposure or personal identifiers in vendor_data could leak access or user information. <br>
Mitigation: Store DIDIT_API_KEY in a secret manager, avoid logging it, and use non-identifying vendor_data values. <br>
Risk: The sample CLI alone is not sufficient for regulated age-gating decisions. <br>
Mitigation: Implement threshold, liveness, fallback, regional policy, and response-schema checks before relying on it in production. <br>


## Reference(s): <br>
- [Didit documentation](https://docs.didit.me) <br>
- [Didit Age Estimation API reference](https://docs.didit.me/standalone-apis/age-estimation) <br>
- [Didit Age Estimation feature guide](https://docs.didit.me/core-technology/age-estimation/overview) <br>
- [ClawHub skill page](https://clawhub.ai/rosasalberto/didit-biometric-age-estimation) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with API examples, shell commands, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DIDIT_API_KEY; CLI usage returns JSON API responses from user-selected facial images.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
