## Description: <br>
Find Appian application objects that are missing a description by exporting the application, scanning object XML files, and reporting each object with an empty or absent description tag. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solarspiker](https://clawhub.ai/user/solarspiker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Appian application teams use this skill to audit application documentation coverage after changes by finding exported Appian objects with missing or blank descriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Appian credentials. <br>
Mitigation: Use a least-privileged Appian API key and rotate or revoke it if exposure is suspected. <br>
Risk: The skill may load Appian credentials from appian.json files in parent directories. <br>
Mitigation: Run it only from a trusted working directory and check parent directories for unintended appian.json files before execution. <br>
Risk: Exported Appian application ZIP files can remain on disk after the audit. <br>
Mitigation: Delete appian-exports files after use when exported application data should not persist locally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/solarspiker/appian-unnamedobjects) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/solarspiker) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command output with grouped object findings and object-type counts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports each matching object's type, name, and UUID; the skill asks the agent to relay the full printed output verbatim.] <br>

## Skill Version(s): <br>
1.3.0 (source: evidence.release.version and script header) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
