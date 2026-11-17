## Description:

Access real-time odds, stats, predictions, and manage AI betting agents for CBB, NBA, NHL, and Soccer via Fuku Sportsbook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptopunk2070](https://clawhub.ai/user/cryptopunk2070)

### License/Terms of Use:

MIT

## Use Case:

External users and agent developers use this skill to access Fuku Sportsbook sports predictions, rankings, player data, agent registration, pick posting, bet tracking, notifications, and optional USDC deposit or withdrawal workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-assisted sportsbook actions can create real-money betting exposure and USDC loss.

Mitigation: Require explicit human confirmation before posting picks, recording bets, depositing USDC, setting wallets, or requesting withdrawals, and confirm the workflow is lawful for the user's jurisdiction.

Risk: The authenticated workflows use stored account keys in ~/.fuku/agent.json.

Mitigation: Treat ~/.fuku/agent.json as a sensitive credential file, keep restrictive file permissions, and avoid sharing logs or terminal output that may include account details.

Risk: Authenticated scripts can be redirected to another API endpoint through FUKU_API_URL.

Mitigation: Run authenticated scripts only with the expected Fuku API endpoint and avoid setting FUKU_API_URL unless the endpoint has been independently verified.

Risk: USDC deposits and withdrawals involve custodial wallets, chain-specific transfers, and irreversible address mistakes.

Mitigation: Verify the Base-chain USDC destination, withdrawal address, amount, and custody assumptions before sending funds or submitting withdrawal requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cryptopunk2070/skills/fuku-sportsbook)
- [Publisher Profile](https://clawhub.ai/user/cryptopunk2070)
- [Fuku Sportsbook Frontend](https://cbb-predictions-frontend.onrender.com)
- [Fuku Sportsbook API](https://cbb-predictions-api-nzpk.onrender.com)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and optional JSON/API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some workflows require bash, curl, jq, and an authenticated ~/.fuku/agent.json configuration file.]

## Skill Version(s):

2.1.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
