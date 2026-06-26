## Description: <br>
Provides OpenClaw agents with direct HTTP guidance for querying global financial market data, including equities, indices, funds, bonds, company fundamentals, and real-time or historical quotes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CZZLEGEND](https://clawhub.ai/user/CZZLEGEND) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to query Finloop market-data endpoints directly for market monitoring, instrument lookup, and basic company or asset research across equities, funds, bonds, commodities, foreign exchange, and virtual assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External Finloop API requests may expose confidential portfolio, customer, or internal business information. <br>
Mitigation: Use the skill only for intended market-data lookups and avoid sending confidential or internal data to the external API. <br>
Risk: The manifest lacks a repository or source URL, making package provenance harder to verify before installation. <br>
Mitigation: Verify the npm package name and publisher before installing or running the package. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CZZLEGEND/finloop-mktdata-skills) <br>
- [Publisher profile](https://clawhub.ai/user/CZZLEGEND) <br>
- [Finloop market-data interface reference](artifact/.agents/skills/finloop-mktdata-skill/references/REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with direct HTTP request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include curl, fetch, or axios request snippets and guidance to avoid creating wrapper files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
