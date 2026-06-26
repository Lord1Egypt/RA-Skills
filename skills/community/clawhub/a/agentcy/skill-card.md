## Description: <br>
Agentcy helps OpenClaw agents query marketing analytics, advertising, search, ecommerce, and web research sources to produce synthesized insights and recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twchase](https://clawhub.ai/user/twchase) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing analysts and agency operators use this skill to query client marketing performance, inspect configured data sources, and run competitive research through Agentcy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The AGENTCY_API_KEY can query marketing data sources connected in the Agentcy portal. <br>
Mitigation: Use a limited-scope key or test account where possible and review connected domains before running queries. <br>
Risk: Queries and client domain context are sent to Agentcy API endpoints for analysis and research. <br>
Mitigation: Install only if you trust Agentcy and avoid sending client data that should not be processed by the Agentcy service. <br>


## Reference(s): <br>
- [Agentcy homepage](https://www.goagentcy.com) <br>
- [ClawHub skill page](https://clawhub.ai/twchase/agentcy) <br>
- [Publisher profile](https://clawhub.ai/user/twchase) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text responses from shell commands, with markdown examples in documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENTCY_API_KEY and the curl and jq command-line tools.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
