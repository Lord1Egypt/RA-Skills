## Description: <br>
Perform web searches using Alibaba Cloud UnifiedSearch API with configurable search parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leowing](https://clawhub.ai/user/leowing) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to query Alibaba Cloud UnifiedSearch/OpenSearch for web results with optional engine type, time range, category, city, or IP filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Alibaba Cloud access keys may be exposed or over-permissioned if handled carelessly. <br>
Mitigation: Use least-privilege credentials limited to UnifiedSearch/OpenSearch, keep secrets out of chats and committed files, and rotate keys periodically. <br>
Risk: Search result links and snippets may contain untrusted or misleading web content. <br>
Mitigation: Treat returned links and snippets as untrusted and verify them before opening, citing, or acting on the results. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/leowing/aliyun-search-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration instructions] <br>
**Output Format:** [Plain text search results with setup and command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Alibaba Cloud credentials in environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
