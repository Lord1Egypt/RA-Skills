## Description: <br>
Access AIKEK APIs for crypto and DeFi research, real-time market and news queries, Solana-wallet authentication, and image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vvsotnikov](https://clawhub.ai/user/vvsotnikov) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external agent users use this skill to authenticate with AIKEK, query crypto and DeFi knowledge endpoints, generate images, and manage credit-related API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a locally stored Solana private key and a non-expiring AIKEK API token. <br>
Mitigation: Store credentials in a private secrets store or a restricted local credentials file, avoid printing full tokens, and keep ~/.config/aikek/credentials private. <br>
Risk: Some API calls consume AIKEK credits or submit referral verification data. <br>
Mitigation: Review and explicitly approve credit-spending requests and referral submissions before running them. <br>
Risk: Credentials could be exposed if sent to a non-AIKEK domain. <br>
Mitigation: Send AIKEK credentials only to api.alphakek.ai and verify endpoint URLs before execution. <br>


## Reference(s): <br>
- [AIKEK Developer API Documentation](https://docs.alphakek.ai/developers/developer-api.md) <br>
- [AIKEK API Base URL](https://api.alphakek.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, Python, JSON, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes authenticated API request examples that may consume AIKEK credits.] <br>

## Skill Version(s): <br>
1.3.1 (source: release metadata; SKILL.md frontmatter reports 1.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
