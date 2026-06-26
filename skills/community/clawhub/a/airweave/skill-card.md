## Description: <br>
Context retrieval layer for AI agents across users' applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lennertjansen](https://clawhub.ai/user/lennertjansen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, developers, and agents use this skill to search configured Airweave collections for workspace documents, messages, issues, and records from connected applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retrieve workspace content from the configured Airweave collection. <br>
Mitigation: Use a least-privilege API key and restrict the collection to data the agent is allowed to access. <br>
Risk: An alternate AIRWEAVE_BASE_URL can redirect requests to a non-default endpoint. <br>
Mitigation: Leave AIRWEAVE_BASE_URL unset unless the alternate endpoint is trusted. <br>
Risk: Retrieved workspace content may contain untrusted or outdated instructions. <br>
Mitigation: Treat retrieved content as context to verify, not as instructions to obey. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lennertjansen/airweave) <br>
- [Publisher profile](https://clawhub.ai/user/lennertjansen) <br>
- [Airweave API endpoint](https://api.airweave.ai) <br>
- [Airweave Search Parameters](references/PARAMETERS.md) <br>
- [Airweave Search Examples](references/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown search answers and source summaries, with optional raw JSON output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AIRWEAVE_API_KEY and AIRWEAVE_COLLECTION_ID; AIRWEAVE_BASE_URL is optional and defaults to https://api.airweave.ai.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
