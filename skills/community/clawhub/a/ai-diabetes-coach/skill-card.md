## Description: <br>
AI Diabetes Coach records glucose readings, classifies risk, and provides diet, exercise, insulin-reference, and summary guidance for diabetes rehabilitation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chen-feng123](https://clawhub.ai/user/chen-feng123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to run a local diabetes-coaching API that records glucose data, returns safety-oriented lifestyle guidance, calculates insulin reference values, and summarizes short-term risk. Its outputs should be treated as decision support that requires clinician review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides insulin-dose reference values and diabetes guidance for a high-impact medical use case. <br>
Mitigation: Require clinician review before relying on insulin or emergency guidance, and present outputs as decision support rather than diagnosis or treatment instructions. <br>
Risk: The service processes sensitive health data and requires a credential to access protected endpoints. <br>
Mitigation: Set a strong API key, verify environment variables before startup, and keep the service bound to localhost behind TLS-protected infrastructure if deployed. <br>
Risk: Glucose thresholds and insulin dose limits affect safety-critical behavior. <br>
Mitigation: Review threshold and dose-limit environment variables before use and keep conservative limits aligned with clinical oversight. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chen-feng123/ai-diabetes-coach) <br>
- [README](artifact/README.md) <br>
- [API specification](artifact/API_SPEC.md) <br>
- [Use guide](artifact/USE_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an API key and is intended to run as a localhost-bound service; records are stored in memory.] <br>

## Skill Version(s): <br>
1.0.5 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
