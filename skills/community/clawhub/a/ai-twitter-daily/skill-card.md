## Description: <br>
Generate daily AI Twitter report from top AI researchers and companies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danetteceola](https://clawhub.ai/user/danetteceola) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and AI watchers use this skill to produce a daily Chinese-language summary of recent Twitter/X activity from selected AI researchers and organizations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends report prompts and a bearer token to a configurable external AI API endpoint. <br>
Mitigation: Use only a vetted provider URL, avoid sensitive private data in prompts, and do not set GROK_API_URL to an untrusted host. <br>
Risk: The configured API key is used as a bearer token for the outbound request. <br>
Mitigation: Store GROK_API_KEY securely, scope or rotate the credential where possible, and avoid sharing logs that may expose request failures or configuration. <br>


## Reference(s): <br>
- [Monitored Twitter/X accounts](references/users.txt) <br>
- [Skill page](https://clawhub.ai/danetteceola/ai-twitter-daily) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Chinese Markdown-style report with tables and bullet points printed to standard output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GROK_API_KEY and can use configurable GROK_API_URL and GROK_MODEL environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
