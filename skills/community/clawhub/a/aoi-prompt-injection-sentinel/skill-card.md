## Description: <br>
Detects and scores prompt injection attempts in text, outputting severity, action, and matched rules without external calls or secret handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edmonddantesj](https://clawhub.ai/user/edmonddantesj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security teams use this skill to locally screen user-provided text for prompt-injection patterns before passing content into agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner uses lightweight heuristic rules and may miss new prompt-injection variants or flag benign text. <br>
Mitigation: Use the result as a screening signal alongside review, policy checks, and other security controls rather than as a complete security boundary. <br>
Risk: The JSON output may be sensitive when it describes or fingerprints confidential input text. <br>
Mitigation: Keep analysis local and avoid sharing output externally when the analyzed input contains sensitive information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/edmonddantesj/aoi-prompt-injection-sentinel) <br>
- [AOI skills issue tracker](https://github.com/edmonddantesj/aoi-skills/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes severity, action, reasons, matched rule ids, and an input fingerprint.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata, artifact _meta.json, artifact package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
