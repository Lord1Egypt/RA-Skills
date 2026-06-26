## Description: <br>
万向传动轴CAD图纸生成。当用户说"万向传动轴"、"生成万向传动轴图纸"、"做一个万向传动轴"、"driveshaft"时使用此 skill。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liv09370](https://clawhub.ai/user/liv09370) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and mechanical-design practitioners use this skill to collect driveshaft parameters, call the JXT mechanical-parts API, review calculated values, and create a guest production sheet for CAD drawing generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends driveshaft design parameters to jixietools.com. <br>
Mitigation: Use the skill only for designs that can be shared with that third-party service, or confirm the service's access controls and retention terms before use. <br>
Risk: The workflow creates guest-access production-sheet links. <br>
Mitigation: Avoid entering confidential or proprietary mechanical designs unless the link sharing and access behavior is acceptable for the project. <br>


## Reference(s): <br>
- [Driveshaft skill page](https://clawhub.ai/liv09370/driveshaft) <br>
- [JXT mechanical tools API base URL](https://jixietools.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Chinese Markdown guidance with curl commands, JSON responses, tables, and production-sheet links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides step-by-step user input, sends driveshaft parameters to jixietools.com, stores returned filenames and guest codes during the workflow, and polls production status.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
