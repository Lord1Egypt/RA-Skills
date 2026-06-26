## Description: <br>
Empire Builder helps agents work with SmartVault treasuries, leaderboards, boosters, distribution preparation and storage, burns, airdrops, and Clanker-backed Empire launches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cryptorabble](https://clawhub.ai/user/cryptorabble) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide Empire Builder integrations that read Empire state, prepare and store treasury distributions, register burns and airdrops, configure boosters, and connect Clanker token deployments to Empire records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mainnet write flows can move treasury assets or persist distribution and burn records when signed and broadcast. <br>
Mitigation: Use the skill only for intended live Base or Arbitrum workflows; manually verify chain ID, vault address, Empire ID, recipients, amounts, calldata, and transaction simulation before signing or broadcasting. <br>
Risk: API keys and wallet-signing material are sensitive credentials. <br>
Mitigation: Send API keys with x-api-key headers, avoid putting secrets in URLs, use narrowly scoped credentials, and keep signing authority limited to the required operator wallet. <br>
Risk: Co-signers cannot replace the vault owner on the documented API distribution path. <br>
Mitigation: Use the vault owner wallet for prepare-to-executeBatch integration flows, or use the official web-app UserOperation path when operating as a co-signer. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/cryptorabble/empire-builder) <br>
- [Empire Builder Skill Guide](artifact/SKILL.md) <br>
- [Empire Builder Homepage](https://empirebuilder.world/skill/SKILL.md) <br>
- [HTTP API Reference](artifact/references/http-api.md) <br>
- [End-to-End Workflows](artifact/references/workflows.md) <br>
- [SmartVault Contract Reference](artifact/references/contracts.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with HTTP payloads, curl examples, JavaScript or TypeScript snippets, and transaction checklists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include live-mainnet operation checks, API authentication notes, wallet-signing guidance, and route-specific request or response shapes.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
