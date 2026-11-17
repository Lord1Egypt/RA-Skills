## Description:

AgentSafe Scan helps agents gate remote skill installs, re-fetches, and allowlist promotions by calling a hosted heuristic static red-flag scanner for suspicious skill patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albin-holmgren](https://clawhub.ai/user/albin-holmgren)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent maintainers use this skill before remote skill lifecycle events to submit skill URLs or markdown to AgentSafe for static risk-band findings, decision guidance, fingerprints, and drift checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Skill URLs, skill markdown, agent IDs, watch entries, and payment transaction hashes are shared with the third-party AgentSafe hosted scanner.

Mitigation: Use the service only when that data sharing is acceptable, and do not submit secrets, credentials, private repository URLs with tokens, signing material, personal data, or other sensitive payloads.

Risk: The scanner is heuristic static analysis and is not a formal audit, certification, penetration test, insurance, or guarantee of safety.

Mitigation: Treat deny and review decisions as gates for refusal or human review, and never auto-install a skill solely because the score is low.

Risk: Remote skill content can drift after an initial scan or allowlist decision.

Mitigation: Re-scan when the content fingerprint changes, and use the watch/rescan workflow for monitored URLs where ongoing drift detection is needed.

## Reference(s):

- [AgentSafe Scan ClawHub Listing](https://clawhub.ai/albin-holmgren/skills/agentsafe-scan)
- [AgentSafe API Home](https://agentsafe.up.railway.app)
- [AgentSafe OpenAPI Docs](https://agentsafe.up.railway.app/docs)
- [AgentSafe Agent Brief](https://agentsafe.up.railway.app/llms.txt)
- [API quick map](references/api-quick.md)
- [Free to paid flow](references/payment.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl and optional AGENTSAPE_BASE_URL and AGENTSAPE_AGENT_ID environment variables; hosted scan responses include risk bands, findings, decision actions, content fingerprints, capability signals, quota status, and next actions.]

## Skill Version(s):

0.1.8 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
