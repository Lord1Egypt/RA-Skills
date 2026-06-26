## Description: <br>
Professional market data and AI APIs via x402 micropayments with pay-per-call USDC access to crypto, equities, forex, global time-series, and AI inference endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tinkle-community](https://clawhub.ai/user/tinkle-community) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to query paid market-data and AI endpoints through a Base wallet, then format returned data into summaries, tables, analysis, or follow-up commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend USDC from a configured Base wallet for API calls. <br>
Mitigation: Use a dedicated low-balance wallet and require confirmation before paid or multi-call workflows. <br>
Risk: The skill depends on an external SDK/package for paid API access. <br>
Mitigation: Verify the package source before installation and review updates before use. <br>
Risk: Prompts or request bodies may be sent to paid AI endpoints. <br>
Mitigation: Do not send secrets, private wallet data, personal data, or confidential trading information to the AI endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tinkle-community/claw402) <br>
- [claw402 homepage](https://claw402.ai) <br>
- [claw402 API catalog](https://claw402.ai/api/v1/catalog) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and formatted JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WALLET_PRIVATE_KEY for paid calls and prints status, url, and data fields as JSON.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
