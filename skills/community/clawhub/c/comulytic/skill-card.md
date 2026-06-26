## Description: <br>
Query meetings, contacts, action items, and conversations from Comulytic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenbaochao](https://clawhub.ai/user/chenbaochao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and teams with Comulytic accounts use this skill to search meeting records, retrieve summaries or transcripts, inspect contact history, and review pending action items through Comulytic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Comulytic login credentials and can retrieve sensitive meeting summaries, transcripts, contacts, conversation snippets, and action items. <br>
Mitigation: Install only if you trust the Comulytic service and publisher with that data, and avoid broad searches or full transcript requests unless they are necessary. <br>
Risk: The login helper stores an access token at ~/.comulytic/mcp-token.json for later API access. <br>
Mitigation: Keep the token file private, remove or revoke it when access is no longer needed, and rerun login only in trusted environments. <br>


## Reference(s): <br>
- [Comulytic MCP API endpoint](https://api.comulytic.ai/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/chenbaochao/comulytic) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, python3, and a Comulytic access token; responses may include private meeting, transcript, contact, conversation, and action item data.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
