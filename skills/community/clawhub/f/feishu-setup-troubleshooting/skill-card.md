## Description: <br>
Set up and troubleshoot Feishu or Lark messaging integration with Hermes Agent, including connection checks, access control, and common failure modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuxuclassmate](https://clawhub.ai/user/xuxuclassmate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up and troubleshoot Hermes Agent Feishu or Lark messaging integrations, including gateway health, access control, connection settings, and common failure modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill works with Feishu/Lark app secrets, encrypt keys, verification tokens, and access-control settings. <br>
Mitigation: Store credentials securely, never commit them, and prefer explicit user allowlists for production deployments. <br>
Risk: Troubleshooting logs may contain sensitive integration details or user data. <br>
Mitigation: Review and redact logs before sharing them outside the deployment team. <br>
Risk: Misconfigured Feishu or gateway allow rules can unintentionally block or broaden user access. <br>
Mitigation: Verify both Feishu-level and gateway-level access-control settings after configuration changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuxuclassmate/feishu-setup-troubleshooting) <br>
- [Publisher profile](https://clawhub.ai/user/xuxuclassmate) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [References Hermes CLI diagnostics and Feishu/Lark environment variables.] <br>

## Skill Version(s): <br>
1.2.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
