## Description: <br>
Looks up the generic name for a provided drug name using a local SearXNG search service and returns structured results for agent analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dddwinter](https://clawhub.ai/user/dddwinter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to query drug names and receive search context that helps identify a likely generic name. It is intended for lookup assistance, not medical advice or clinical decision-making. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Drug name searches can reveal sensitive health interests to the configured local SearXNG service. <br>
Mitigation: Use only a trusted local SearXNG instance and avoid entering identifying medical details unless logging and retention are understood. <br>
Risk: Search results and agent interpretation may produce an incorrect generic-name match. <br>
Mitigation: Treat results as lookup assistance and verify drug information against authoritative medical or pharmacy sources before use. <br>


## Reference(s): <br>
- [Generic Drug ClawHub release](https://clawhub.ai/dddwinter/generic-drug) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Guidance] <br>
**Output Format:** [JSON with optional plain-text analysis prompt] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, curl, jq, python3, and a trusted local SearXNG service at http://localhost:8080.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
