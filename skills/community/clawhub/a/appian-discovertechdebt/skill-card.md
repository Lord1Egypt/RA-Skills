## Description: <br>
Scan an Appian application for tech debt by finding objects whose SAIL definitions reference outdated versioned functions marked by Appian with a _v suffix. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solarspiker](https://clawhub.ai/user/solarspiker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Appian application maintainers use this skill to export an Appian application and identify SAIL objects that reference deprecated versioned functions before releases or periodic maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Appian credentials and can load them from an appian.json file in the working tree or parent directories. <br>
Mitigation: Run it only in trusted workspaces, prefer injected APPIAN_BASE_URL and APPIAN_API_KEY, and remove or tightly control appian.json files before execution. <br>
Risk: The skill stores exported Appian application ZIPs locally. <br>
Mitigation: Treat appian-exports directories as sensitive artifacts and delete or secure exported ZIPs according to the Appian environment's data handling policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/solarspiker/appian-discovertechdebt) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, text, shell commands] <br>
**Output Format:** [Plain text report from a Node.js command, including per-object findings and a deduplicated summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APPIAN_BASE_URL and APPIAN_API_KEY; writes exported Appian ZIPs to local appian-exports directories.] <br>

## Skill Version(s): <br>
1.7.0 (source: server-resolved release metadata and script header) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
