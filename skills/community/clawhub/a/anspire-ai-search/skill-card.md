## Description: <br>
Anspire Search provides real-time web search for news, events, and time-sensitive facts through the Anspire Search API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anspire-ai](https://clawhub.ai/user/anspire-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill when an agent needs current web information, including recent news, market updates, policy changes, research checks, and other time-sensitive facts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security assessment says the skill pushes the agent to collect and permanently save the user's Anspire API key in local startup files. <br>
Mitigation: Prefer setting ANSPIRE_API_KEY through a secure secret manager or a temporary session variable, and do not paste the full key into chat for an agent to write into shell startup files. <br>
Risk: The security guidance warns against installing from an unpinned raw GitHub main-branch URL. <br>
Mitigation: Install from the reviewed ClawHub release or pin any source-based installation to a reviewed revision. <br>
Risk: Search queries and API credentials are sent to Anspire's service. <br>
Mitigation: Install only if the user trusts Anspire with search queries and is comfortable managing an Anspire API key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anspire-ai/anspire-ai-search) <br>
- [Publisher profile](https://clawhub.ai/user/anspire-ai) <br>
- [Anspire Search](https://aisearch.anspire.cn) <br>
- [Anspire Search API endpoint](https://plugin.anspire.cn/api/ntsearch/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ANSPIRE_API_KEY and either python3 or curl.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
