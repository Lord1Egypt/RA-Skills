## Description: <br>
Enables agents to check, open, bind, and unbind Alipay AI payment authorization through the alipay-bot CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alipay](https://clawhub.ai/user/alipay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and payment-enabled agents use this skill to manage Alipay AI payment authorization, including status checks, wallet binding, authorization-code handling, and wallet unbinding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill manages Alipay AI payment authorization and can bind or close wallet authorization. <br>
Mitigation: Install and run it only when the user deliberately wants agent-managed Alipay payment authorization, and treat bind-wallet or close-wallet requests as payment-authorization changes. <br>
Risk: The release installs a local alipay-bot CLI from npm that remains on PATH. <br>
Mitigation: Review the npm install prompt, require the pinned package and integrity check, and do not proceed if the package integrity check fails. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alipay/alipay-authenticate-wallet) <br>
- [Publisher profile](https://clawhub.ai/user/alipay) <br>
- [GitHub homepage](https://github.com/alipay/payment-skills) <br>
- [npm package](https://www.npmjs.com/package/@alipay/agent-payment) <br>
- [CLI setup](artifact/references/cli-setup.md) <br>
- [Environment variables](artifact/references/env-vars.md) <br>
- [Output rules](artifact/references/output-rules.md) <br>
- [Image output](artifact/references/image-output.md) <br>
- [Security notes](artifact/references/security.md) <br>
- [Feedback flow](artifact/references/feedback.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown text with CLI command execution and occasional image handoff instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI JSON responses are consumed internally; user-facing CLI Markdown and authorization URLs must be preserved exactly.] <br>

## Skill Version(s): <br>
1.0.11-beta.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
