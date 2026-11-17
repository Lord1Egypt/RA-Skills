## Description:

Crypto Genie helps agents assess cryptocurrency addresses for scam risk using local database checks and Etherscan-backed analysis for uncached addresses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[princedoss77](https://clawhub.ai/user/princedoss77)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to check cryptocurrency addresses before interacting with them, receiving risk scores, scam indicators, and suggested next steps. The results are heuristic safety signals and should not be treated as proof that an address is safe or unsafe.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uncached address checks can contact Etherscan with the user's API key.

Mitigation: Review network and API-key behavior before installation, configure keys through setup or environment variables, and avoid storing real keys in shell history, crontab lines, or broadly readable files.

Risk: The tool keeps local wallet-analysis history and background sync state.

Mitigation: Protect the local configuration and database directory with appropriate file permissions and review retention expectations before use.

Risk: Cron or systemd background sync can run repeatedly and make external API calls.

Mitigation: Bound sync jobs with maximum job counts and delays, protect scheduled tasks with locks, and monitor rate-limit or failure behavior.

Risk: Risk scores and scam labels are heuristic signals.

Mitigation: Use results as one input in a broader review and verify with additional sources before sending funds or making trust decisions.

## Reference(s):

- [Crypto Genie ClawHub Listing](https://clawhub.ai/princedoss77/skills/crypto-genie)
- [README](README.md)
- [Skill Usage Guide](SKILL.md)
- [Database Architecture](DATABASE_ARCHITECTURE.md)
- [Security Guidance](SECURITY.md)
- [Etherscan API Key Setup](https://etherscan.io/myapikey)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON risk analysis with command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include address validity, risk score, risk level, scam indicators, transaction summaries, and recommendations; uncached address analysis may require an Etherscan API key.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
