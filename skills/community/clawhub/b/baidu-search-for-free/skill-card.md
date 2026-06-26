## Description: <br>
Searches Baidu for Chinese web results and can fetch and parse content from result pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoking](https://clawhub.ai/user/chaoking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Baidu searches for Chinese web information, inspect titles, summaries, and links, and optionally parse result pages into readable text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The webpage fetcher disables HTTPS certificate verification, which can expose fetched content to interception or tampering. <br>
Mitigation: Review or patch the fetcher to keep certificate verification enabled before using it with sensitive content or untrusted networks. <br>
Risk: The skill's triggers are broader than its Baidu-specific purpose. <br>
Mitigation: Use it only for explicit Baidu or Chinese-web search tasks and review fetched URLs before relying on the results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chaoking/baidu-search-for-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text or JSON search results with optional parsed webpage text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search result count and parsed webpage length can be limited with command-line options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
