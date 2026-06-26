## Description: <br>
A free web search skill that queries Bing and returns structured search results without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ipdoctor961051-cyber](https://clawhub.ai/user/ipdoctor961051-cyber) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to run ordinary public web searches, find current information, and retrieve title, URL, and snippet results as JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Bing and may expose sensitive content if users include secrets or private records. <br>
Mitigation: Use the skill only for ordinary public web searches and do not include passwords, tokens, private records, or sensitive personal details in queries. <br>
Risk: The helper depends on a local Python script and third-party Python packages. <br>
Mitigation: Verify the installed script path and install any missing Python dependencies from trusted sources before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ipdoctor961051-cyber/ddg-free) <br>
- [Bing Search](https://www.bing.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [JSON printed to stdout, with errors printed to stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results include the original query and an array of title, URL, and snippet objects.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
