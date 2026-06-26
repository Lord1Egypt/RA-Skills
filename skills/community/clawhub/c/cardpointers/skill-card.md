## Description: <br>
Query CardPointers card recommendations, wallet cards, and offers via the CardPointers CLI for credit card rewards optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emcro](https://clawhub.ai/user/emcro) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to choose cards for purchases, inspect wallet cards, search and filter offers, check expiring offers, and compare recommendations across linked CardPointers profiles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: After login, the CardPointers CLI can query wallet cards, offers, profiles, and recommendations. <br>
Mitigation: Install only if the CardPointers CLI and Homebrew tap are trusted, treat ~/.cardpointers/config as a secret, and run cardpointers logout when the stored token is no longer needed. <br>
Risk: CARDPOINTERS_API can point the CLI at a non-default service endpoint. <br>
Mitigation: Keep CARDPOINTERS_API pointed at the official endpoint unless the user intentionally trusts another server. <br>


## Reference(s): <br>
- [CardPointers CLI](https://cardpointers.com/cli/) <br>
- [CardPointers MCP API endpoint](https://mcp.cardpointers.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON output from the CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the CardPointers CLI, jq, authentication with CardPointers, and a CardPointers+ subscription.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
