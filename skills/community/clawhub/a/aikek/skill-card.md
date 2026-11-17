## Description:

Access AIKEK APIs for crypto/DeFi research and image generation. Authenticate with a Solana wallet, query the knowledge engine for real-time market data and news, generate images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vvsotnikov](https://clawhub.ai/user/vvsotnikov)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to authenticate with AIKEK, query crypto and DeFi market intelligence, generate image assets, and manage API credits through documented endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can store and print long-lived API credentials.

Mitigation: Use an OS keychain, secret manager, or encrypted vault when possible; avoid printing or pasting tokens into shell history; rotate or revoke exposed credentials.

Risk: The generated Solana wallet is used for API authentication.

Mitigation: Do not put funds in the generated wallet.

Risk: API tokens do not expire automatically.

Mitigation: Store tokens securely, restrict where they are sent, and revoke or rotate them if exposure is suspected.

## Reference(s):

- [AIKEK Developer API Documentation](https://docs.alphakek.ai/developers/developer-api.md)
- [AIKEK API Base URL](https://api.alphakek.ai)
- [ClawHub Skill Page](https://clawhub.ai/vvsotnikov/skills/aikek)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell, Python, curl, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API endpoint usage, credential setup guidance, and examples of expected external API responses.]

## Skill Version(s):

1.3.1 (source: server release metadata; artifact frontmatter reports 1.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
