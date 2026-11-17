## Description: <br>
Guides agents through purchasing and applying DV, OV, and EV SSL certificates with Alibaba Cloud Certificate Authority Service across China and International sites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud operators, and certificate administrators use this skill to acquire reusable or newly purchased Alibaba Cloud CAS certificate instances, fill certificate application details, and submit or verify SSL certificate applications with explicit confirmation gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate billable Alibaba Cloud certificate orders. <br>
Mitigation: Use a least-privilege RAM profile and approve purchase prompts only after verifying domain, CA brand, duration, site, region, account profile, and expected cost. <br>
Risk: Certificate application actions can affect public domain validation and issuance workflows. <br>
Mitigation: Require explicit confirmation before submission and verify the target domain, contact, company information, validation method, and certificate type. <br>
Risk: Cloud credentials could be exposed if copied into chat or echoed in commands. <br>
Mitigation: Check credential status without printing secrets and configure credentials outside the agent conversation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-cas-ssl-cert-purchase) <br>
- [Publisher profile](https://clawhub.ai/user/sdk-team) <br>
- [API command reference](references/api-commands.md) <br>
- [CLI installation guide](references/cli-installation-guide.md) <br>
- [RAM policies](references/ram-policies.md) <br>
- [Error handling](references/error-handling.md) <br>
- [Verification method](references/verification-method.md) <br>
- [Related commands](references/related-commands.md) <br>
- [Acceptance criteria](references/acceptance-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash command blocks, parameter summaries, confirmation prompts, and environment variable exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are interactive and gated before billable purchases or certificate submissions.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
