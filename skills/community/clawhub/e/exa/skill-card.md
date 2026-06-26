## Description: <br>
Neural web search and code context via Exa AI API. Requires EXA_API_KEY. Use for finding documentation, code examples, research papers, or company info. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fardeenxyz](https://clawhub.ai/user/fardeenxyz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and researchers use this skill to run Exa web searches, retrieve code and documentation context, and extract page content from URLs through the Exa API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, URLs, and requested page content are sent to Exa. <br>
Mitigation: Avoid submitting internal, confidential, or sensitive URLs or queries unless that data may be shared with Exa. <br>
Risk: The skill depends on an EXA_API_KEY in the local environment. <br>
Mitigation: Keep the API key private, rotate it if exposed, and avoid logging or committing environment values. <br>
Risk: The shell scripts rely on local jq and curl binaries. <br>
Mitigation: Use trusted local installations of jq and curl before running the skill. <br>


## Reference(s): <br>
- [ClawHub Exa skill page](https://clawhub.ai/fardeenxyz/exa) <br>
- [Exa API key dashboard](https://dashboard.exa.ai/api-keys) <br>
- [Exa search API endpoint](https://api.exa.ai/search) <br>
- [Exa contents API endpoint](https://api.exa.ai/contents) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EXA_API_KEY and local jq and curl installations.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
