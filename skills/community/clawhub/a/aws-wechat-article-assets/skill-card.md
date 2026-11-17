## Description:

公众号素材库 & 预设包 helps agents manage WeChat article business materials, product images, and .aws preset packages under .aws-article/.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiworkskills](https://clawhub.ai/user/aiworkskills)

### License/Terms of Use:

MIT-0

## Use Case:

External content operators, brand teams, and design-support users use this skill to store business descriptions and product images by product, then import .aws preset bundles for WeChat article production workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The preset importer can update aws.env with credential-like values from a bundle config.

Mitigation: Inspect the .aws bundle and run a dry run first; avoid running the importer in repositories containing real API keys or WeChat credentials until the user has confirmed the expected changes.

Risk: Configuration diffs printed to stdout may expose sensitive values in logs.

Mitigation: Run imports only in controlled terminals, redact captured logs, and avoid shared logging environments unless the config-diff output is fixed or redacted.

Risk: The importer can download .aws bundles and includes a debug flag that relaxes host validation.

Mitigation: Use only HTTPS aiworkskills.cn bundle URLs for normal use and avoid --allow-any-host outside controlled testing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiworkskills/skills/aws-wechat-article-assets)
- [Publisher profile](https://clawhub.ai/user/aiworkskills)
- [aiworkskills homepage](https://aiworkskills.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration diffs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide agents to write local Markdown/image asset files under .aws-article/ and run bundled Python scripts that may update .aws-article/ and aws.env.]

## Skill Version(s):

1.0.25 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
