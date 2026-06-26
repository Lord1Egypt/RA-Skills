## Description: <br>
Provides production-ready, privacy-first decentralized search for AI agents through Presearch's distributed node infrastructure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NosytLabs](https://clawhub.ai/user/NosytLabs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to send web search queries to the Presearch API and receive structured search results for downstream reasoning or retrieval tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to an external Presearch service and may expose sensitive terms. <br>
Mitigation: Use only when sharing queries with Presearch is acceptable, and avoid secrets, private identifiers, or sensitive internal details in search terms. <br>
Risk: The skill requires a Presearch API key. <br>
Mitigation: Store the API key securely and do not paste it into prompts, logs, or checked-in files. <br>


## Reference(s): <br>
- [Presearch Search API endpoint](https://na-us-1.presearch.com/v1/search) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown with HTTP, JSON, Python, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Presearch API key; search responses are JSON result objects.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
