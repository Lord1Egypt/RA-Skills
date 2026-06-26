## Description: <br>
Integrates the Didit Face Search standalone API to perform 1:N facial search against previously verified sessions and return ranked matches with similarity percentages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rosasalberto](https://clawhub.ai/user/rosasalberto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and identity operations teams use this skill to integrate Didit's face-search API for duplicate-account detection, blocklist checks, and facial deduplication workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Face images and biometric match results are sent to Didit for processing. <br>
Mitigation: Use the skill only when authorized to process biometric data and when proper user consent and legal basis are in place. <br>
Risk: The DIDIT_API_KEY grants access to the Didit API. <br>
Mitigation: Store the API key in a secret manager or protected environment variable, avoid logging it, and rotate it if exposure is suspected. <br>
Risk: Face-search request saving and retention settings may affect privacy obligations. <br>
Mitigation: Review Didit's retention and request-saving settings before deployment and store only the minimum match metadata needed for the workflow. <br>


## Reference(s): <br>
- [Didit Face Search skill page](https://clawhub.ai/rosasalberto/didit-face-search) <br>
- [Didit documentation](https://docs.didit.me) <br>
- [Didit Face Search API reference](https://docs.didit.me/standalone-apis/face-search) <br>
- [Didit Face Search feature guide](https://docs.didit.me/core-technology/face-search/overview) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline code examples and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request examples, environment variable setup, response interpretation, and command-line usage.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
