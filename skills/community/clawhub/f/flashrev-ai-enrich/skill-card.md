## Description: <br>
Enrich CSV lead lists through the flashrev-ai-enrich CLI with dry-run estimates, sample previews, token checks, and mapped outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flashlabs-ai](https://clawhub.ai/user/flashlabs-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, sales operations teams, and agents use this skill to enrich CSV lead lists with FlashRev data while confirming credentials, token balance, input mappings, cost estimates, and sample output before live runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI uses a sensitive FlashRev API key and processes CSV contact or business data. <br>
Mitigation: Use the FLASHREV_API_KEY environment variable, avoid printing or storing the key in generated artifacts, and confirm which CSV columns will be sent before live enrichment. <br>
Risk: Paid enrichment can consume FlashRev tokens, especially when prompt routing or unlock capabilities are used. <br>
Mitigation: Check token balance, run dry-run estimates, review the sample preview, and avoid --yes unless the user has already approved the cost and output path. <br>
Risk: The customer_api capability can send mapped CSV fields to user-selected third-party URLs. <br>
Mitigation: Confirm the destination domain with the user, avoid mapping credentials or unrelated PII into headers or bodies, and prefer first-party FlashRev capabilities when they cover the requested data. <br>


## Reference(s): <br>
- [FlashRev AI Enrich API Contract](references/api_contract.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/flashlabs-ai/flashrev-ai-enrich) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, CSV files] <br>
**Output Format:** [Markdown guidance with CLI commands, JSON-capable status output, and enriched CSV output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a FlashRev API key and available tokens; live runs should follow dry-run and sample-preview confirmation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
