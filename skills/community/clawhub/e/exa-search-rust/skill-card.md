## Description:

Exa Search (Rust) lets agents run Exa AI web search, similar-page discovery, and URL content retrieval through a Rust command-line binary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prompt-surfer](https://clawhub.ai/user/prompt-surfer)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agents use this skill to search the web, find pages similar to a known URL, and fetch page contents through Exa when a task needs current or indexed web information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and requested URLs are sent to Exa using the user's EXA_API_KEY.

Mitigation: Avoid secrets, internal-only URLs, and regulated data unless third-party sharing with Exa is approved.

Risk: Fetched page text can contain untrusted web content that attempts to steer the agent.

Mitigation: Treat fetched content as data for review and summarization, not as instructions for the agent to follow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/prompt-surfer/skills/exa-search-rust)
- [Exa AI](https://exa.ai)
- [Official Exa Python SDK](https://github.com/exa-labs/exa-py)
- [OpenClaw Exa plugin](https://github.com/Prompt-Surfer/openclaw-exa-plugin)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [JSON on stdout, including result objects and a formatted markdown field for search-style actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EXA_API_KEY and sends search terms or requested URLs to Exa.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
