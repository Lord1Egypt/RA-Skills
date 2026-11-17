## Description:

Call 120+ AI models and read live web data (scrape, crawl, extract) through one OpenAI-compatible ApexApi key that agents can register and fund with card or USDC on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nitrotechinc](https://clawhub.ai/user/nitrotechinc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to register for ApexApi, manage account funding, call OpenAI-compatible model endpoints, and use web scrape, crawl, and extract APIs from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to persist an API key and claim token, including a recovery token that is sensitive.

Mitigation: Store credentials in a keychain or a 0600-permission secret file, never include them in logs or messages, and send the API key only to the expected ApexApi endpoint.

Risk: Funding and large jobs can spend prepaid account balance.

Mitigation: Require human confirmation before funding or large jobs, check account balance before broad usage, and set spend caps and model allowlists where available.

Risk: The optional local MCP path uses an unpinned `npx` package with an API key.

Mitigation: Prefer the remote ApexApi endpoint or pin and verify the local MCP package version before using it.

Risk: Scraped web content is untrusted data and may contain prompt-injection attempts.

Mitigation: Treat scraped page responses as data, not instructions, and review downstream actions before execution.

## Reference(s):

- [ApexApi Homepage](https://apexapi.dev)
- [ApexApi MCP Documentation](https://apexapi.dev/docs/mcp)
- [Machine-Readable Onboarding](https://apexapi.dev/auth.md)
- [OpenAPI 3.1 Specification](https://apexapi.dev/openapi.json)
- [llms.txt](https://apexapi.dev/llms.txt)
- [ApexApi Documentation](https://apexapi.dev/docs)
- [ClawHub Skill Page](https://clawhub.ai/nitrotechinc/skills/apexapi)
- [Publisher Profile](https://clawhub.ai/user/nitrotechinc)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON request examples, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API calls that require a funded ApexApi account and may return model, image, video, scrape, crawl, or extract results depending on the selected endpoint.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
