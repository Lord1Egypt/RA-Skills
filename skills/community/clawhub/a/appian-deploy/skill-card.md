## Description: <br>
Deploy (import) an Appian package ZIP into an Appian environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solarspiker](https://clawhub.ai/user/solarspiker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to deploy a selected Appian package ZIP to a configured Appian environment and monitor the deployment until a terminal status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can deploy packages to the configured Appian environment using sensitive credentials. <br>
Mitigation: Use a least-privilege Appian API key, verify APPIAN_BASE_URL before running, and rely on Appian approval or review controls for production deployments. <br>
Risk: An unintended package or customization file could be uploaded if the local inputs are wrong. <br>
Mitigation: Inspect the ZIP first, confirm any customization file path, and validate packages before deployment. <br>
Risk: If environment variables are not injected, nearby appian.json files can supply credentials. <br>
Mitigation: Check the working directory and parent directories for appian.json before running in sensitive environments. <br>


## Reference(s): <br>
- [Appian v2 Deployment Management API](https://docs.appian.com/suite/help/25.4/Deploy_Package_API.html) <br>
- [ClawHub Appian Deploy skill page](https://clawhub.ai/solarspiker/appian-deploy) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text status logs and deployment summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APPIAN_BASE_URL and APPIAN_API_KEY; accepts a ZIP path, deployment name, optional description, and optional customization file path.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release metadata and script @version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
