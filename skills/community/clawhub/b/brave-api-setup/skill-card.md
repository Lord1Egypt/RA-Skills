## Description: <br>
Set up Brave Search API for OpenClaw web_search. Use when user needs to configure Brave API, get Brave API key, enable web search, or fix "missing_brave_api_key" error. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[garibong-labs](https://clawhub.ai/user/garibong-labs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure Brave Search API access, apply an existing Brave API key to OpenClaw web search, or repair a missing Brave API key configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reveal and store a live Brave API key while configuring OpenClaw web search. <br>
Mitigation: Use it only for explicit Brave API setup or missing-key repair tasks, and confirm key values are redacted in output and logs. <br>
Risk: The helper script writes the supplied API key into the user's OpenClaw configuration. <br>
Mitigation: Run the script only after confirming the target OpenClaw configuration and the exact key source. <br>


## Reference(s): <br>
- [Brave Search API Dashboard](https://api-dashboard.search.brave.com) <br>
- [Brave Search API Keys Page](https://api-dashboard.search.brave.com/app/keys) <br>
- [ClawHub Skill Page](https://clawhub.ai/garibong-labs/brave-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with browser actions and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write the supplied Brave API key into the user's OpenClaw configuration.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
