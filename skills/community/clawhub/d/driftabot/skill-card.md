## Description: <br>
Query the DriftaBot Registry for API spec drifts, breaking changes, and provider information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pgomes13](https://clawhub.ai/user/pgomes13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and API maintainers use DriftaBot to check tracked API providers for spec drift, breaking changes, provider coverage, and current spec types from the public DriftaBot Registry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may make outbound requests to GitHub-hosted public registry files while answering API drift questions. <br>
Mitigation: Use it for public API drift checks only, avoid sending secrets or proprietary details in queries, and review fetched registry results before relying on them. <br>
Risk: Registry drift reports can be absent or empty for a provider, which means no breaking changes were detected by the registry rather than a guarantee that the API has no risk. <br>
Mitigation: State that missing reports mean no detected breaking changes and verify critical API changes against the provider's canonical documentation. <br>


## Reference(s): <br>
- [ClawHub DriftaBot release](https://clawhub.ai/pgomes13/driftabot) <br>
- [DriftaBot Registry](https://driftabot.github.io/registry/) <br>
- [DriftaBot Registry raw data base](https://raw.githubusercontent.com/DriftaBot/registry/main) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text responses summarizing public registry data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public registry lookups; no credentials are requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
