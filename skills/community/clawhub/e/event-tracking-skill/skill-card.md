## Description: <br>
Coordinates GA4 and Google Tag Manager tracking work from site discovery through schema review, GTM sync, preview QA, and publish readiness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jtrackingai](https://clawhub.ai/user/jtrackingai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analytics engineers, and implementation teams use this skill to plan, configure, validate, and prepare GA4/GTM event tracking for websites. It is especially useful when the right workflow phase is unclear or when an existing artifact directory needs to be resumed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GTM-scoped OAuth access can modify tracking configuration when sync or publish steps are run. <br>
Mitigation: Grant access only for intended GA4/GTM work, confirm the account, container, and workspace before sync, and require explicit publish approval. <br>
Risk: Local credentials and refresh tokens are stored in the workflow artifact directory. <br>
Mitigation: Keep credentials.json and artifact directories out of source control and restrict access to users who need to operate the tracking workflow. <br>
Risk: Analytics parameters may expose full URLs, referrers, link destinations, form destinations, tokens, personal data, or private paths. <br>
Mitigation: Sanitize event parameters and review analytics privacy choices before publishing tracking changes. <br>


## Reference(s): <br>
- [Architecture Reference](references/architecture.md) <br>
- [Output Contract](references/output-contract.md) <br>
- [Event Schema Generation Guide](references/event-schema-guide.md) <br>
- [GA4 Event Guidelines](references/ga4-event-guidelines.md) <br>
- [GTM Troubleshooting](references/gtm-troubleshooting.md) <br>
- [Telemetry Consent](references/telemetry-consent.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with shell commands plus JSON and configuration artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces checkpoint-driven workflow artifacts and reports for review before GTM publishing.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
