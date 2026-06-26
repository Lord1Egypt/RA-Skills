## Description: <br>
Query builder reputation data via Talent Protocol API. Get Builder Rank, verify humans, resolve identities (Twitter/Farcaster/GitHub/wallet), search by location/country, get credentials, and enrich with GitHub data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JuampiHernandez](https://clawhub.ai/user/JuampiHernandez) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to query Talent Protocol for builder reputation, identity resolution, location-based discovery, credentials, and project signals. It can also enrich resolved GitHub identities with public profile, repository, and activity data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries can send handles, wallet addresses, locations, and profile identifiers to Talent Protocol, and GitHub usernames to GitHub when enrichment is used. <br>
Mitigation: Use the skill only for appropriate profile lookups, avoid unnecessary broad searches, and be cautious when correlating identity, wallet, reputation, location, and public GitHub data. <br>
Risk: API tokens can be exposed if pasted into chats, commands, or logs. <br>
Mitigation: Keep TALENT_API_KEY and GITHUB_TOKEN in environment variables or a secret store, and use the GitHub token only when higher rate limits are needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JuampiHernandez/builder-data) <br>
- [Talent Protocol](https://talent.app) <br>
- [Talent API data issuers and credentials](https://docs.talentprotocol.com/docs/talent-api/api-reference/get-data-issuers-and-credentials-available) <br>
- [Endpoints](references/endpoints.md) <br>
- [Use Cases](references/use-cases.md) <br>
- [GitHub Enrichment](references/github-enrichment.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, JSON] <br>
**Output Format:** [Markdown with inline curl commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TALENT_API_KEY for Talent Protocol requests and optional GITHUB_TOKEN for higher GitHub rate limits.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
