## Description:

Set up Brave Search API for OpenClaw web_search. Use when user needs to configure Brave API, get Brave API key, enable web search, or fix "missing_brave_api_key" error.

This skill is ready for commercial/non-commercial use.

## Publisher:

[garibong-labs](https://clawhub.ai/user/garibong-labs)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to configure Brave Search API access for web_search or resolve missing_brave_api_key setup errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a live Brave API key, and passing the key through commands or transcripts can expose the credential.

Mitigation: Prefer a protected secret input or stdin-only path, avoid placing the key in shell commands, and rotate the key if it may have appeared in logs, transcripts, or process monitoring.

Risk: The helper script writes the API key into the OpenClaw configuration file.

Mitigation: Review the target configuration path and file permissions before running the helper script, and confirm the stored key is masked or protected according to local credential handling policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/garibong-labs/skills/brave-api-setup)
- [Publisher profile](https://clawhub.ai/user/garibong-labs)
- [Brave Search API dashboard](https://api-dashboard.search.brave.com)
- [Brave Search API keys dashboard](https://api-dashboard.search.brave.com/app/keys)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline browser actions and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and an existing Brave Search API account with an API key.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
