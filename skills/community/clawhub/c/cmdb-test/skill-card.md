## Description: <br>
Automates IMyFone CMDB test-environment release requests for a specified application. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[azimao](https://clawhub.ai/user/azimao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release operators use this skill to submit test-environment release requests for IMyFone CMDB applications, using a fixed release2 branch and the Hong Kong general test environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit real CMDB test-environment release requests through an authenticated browser session. <br>
Mitigation: Use it only with accounts authorized for test releases, and require the agent to pause before final submission. <br>
Risk: A wrong application name or description could create an unintended release request. <br>
Mitigation: Confirm the application, release2 branch, 香港-通用-测试 environment, and description before the agent clicks the final confirmation button. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/azimao/cmdb-test) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports release submission status, common errors, and any user action needed during authenticated CMDB browser sessions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
