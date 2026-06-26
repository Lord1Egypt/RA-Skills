## Description: <br>
Alicloud Service Scenario-Based Skill for auto-deploying the Build AI Animation Story Creation App by creating an OSS bucket, provisioning a Bailian API key, deploying the FC application with a Devs template, and stopping at the experience page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud engineers use this skill to deploy Alibaba Cloud's AI Animation Story Creation App with scripted setup for OSS, Bailian, Function Compute, Devs project configuration, deployment polling, and access URL generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make broad, persistent changes to an Alibaba Cloud account, including creating cloud resources, roles, custom domains, API keys, and attaching full-access policies. <br>
Mitigation: Use a disposable or tightly scoped RAM user, review the scripts before execution, avoid production credentials, and delete created resources, roles, domains, API keys, and attached policies after use. <br>
Risk: The Bailian API key is created during the workflow and may be printed in command output. <br>
Mitigation: Do not allow the generated API key to be pasted into chat, stored in logs, or shared; rotate or delete the key after the deployment is no longer needed. <br>
Risk: The final application URL is publicly accessible and can consume Function Compute resources and Bailian API quota. <br>
Mitigation: Share the URL only with trusted users, monitor usage and costs, and remove the custom domain and deployed project when testing is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-tech-solution-animation-creation-auto-deploy) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related Commands](references/related-commands.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and script invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment steps, environment variable guidance, generated resource names, deployment status checks, cleanup commands, and a public access URL.] <br>

## Skill Version(s): <br>
0.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
