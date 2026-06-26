## Description: <br>
Finds and ranks MCP server directories and registries for publication, backlinks, and discovery using the ServiceGraph product_directory dataset. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nostrband](https://clawhub.ai/user/nostrband) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent builders, and growth teams use this skill to shortlist MCP registries, rank them by authority or reach, and plan submissions for MCP server discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a ServiceGraph credential. <br>
Mitigation: Keep the API key out of chat transcripts and logs; route authenticated calls through the harness or a local environment wrapper. <br>
Risk: Unlocking ServiceGraph detail rows can spend paid credits. <br>
Mitigation: Review the selected registry apexes and expected credit cost before running unlock requests. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nostrband/find-mcp-directories) <br>
- [ServiceGraph API](https://api.servicegraph.co) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with ranked recommendations, inline shell commands, and API endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require a ServiceGraph API key and user approval before paid detail unlocks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
