## Description:

Checks cryptocurrency addresses against a local scam-risk database and optional Etherscan-backed sync workflow to flag phishing, honeypots, rug pulls, exploit patterns, and related risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[princedoss77](https://clawhub.ai/user/princedoss77)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to triage cryptocurrency addresses before interacting with them. It produces heuristic risk reports and can queue unknown addresses for background synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send wallet addresses and API-key-backed requests to Etherscan despite no-external-call positioning.

Mitigation: Review network behavior before deployment, disclose background sync behavior to users, and use a rotated API key through a protected secret mechanism.

Risk: Cron or systemd examples can create persistent background jobs that run with credentials.

Mitigation: Avoid the provided persistence examples unless they are hardened, secrets are not embedded in job definitions, and operators can disable or remove the jobs.

Risk: Risk scores are heuristic and may be incorrect or stale.

Mitigation: Treat results as triage, verify important decisions with independent sources, and do not use the output as authoritative financial safety advice.

Risk: Credential-handling guidance may lead users to expose or mishandle API keys.

Mitigation: Use least-privilege secret management, rotate keys regularly, and avoid storing secrets in shell history, crontabs, or committed files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/princedoss77/skills/crypto-address-checker)
- [README](artifact/README.md)
- [Database architecture](artifact/DATABASE_ARCHITECTURE.md)
- [Security guidance](artifact/SECURITY.md)
- [Multichain support](artifact/MULTICHAIN_SUPPORT.md)
- [Etherscan API key setup](https://etherscan.io/myapikey)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON address-risk reports with Markdown usage guidance and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are heuristic and may depend on local database freshness and background sync configuration.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
