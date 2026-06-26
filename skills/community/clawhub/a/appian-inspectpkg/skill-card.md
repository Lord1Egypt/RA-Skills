## Description: <br>
Inspect an Appian package ZIP against the target environment to identify errors or warnings before deploying. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solarspiker](https://clawhub.ai/user/solarspiker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill before Appian deployment to inspect an exported package ZIP against the target Appian environment and review predicted errors, warnings, and object counts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Appian environment credentials and uploads the selected package ZIP to the configured Appian environment. <br>
Mitigation: Use a least-privilege APPIAN_API_KEY, confirm APPIAN_BASE_URL points to the intended environment, and pass only the ZIP and customization file intended for inspection. <br>
Risk: If environment variables are not already set, credential loading may use a nearby appian.json file. <br>
Mitigation: Run the skill from a controlled directory and avoid directory trees that contain unintended appian.json files. <br>


## Reference(s): <br>
- [Appian Inspect Package API](https://docs.appian.com/suite/help/25.4/Inspect_Package_API.html) <br>
- [Appian Inspectpkg on ClawHub](https://clawhub.ai/solarspiker/appian-inspectpkg) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Console text with inspection status, object counts, errors, and warnings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APPIAN_BASE_URL and APPIAN_API_KEY and uploads the selected package ZIP to the configured Appian environment.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
