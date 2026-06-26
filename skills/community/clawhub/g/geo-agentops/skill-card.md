## Description: <br>
GEO AgentOps helps B2B export, independent-site, and DTC teams plan GEO market research, competitive analysis, localized content strategy, multi-channel distribution, and AI citation optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketing and export-operations teams use this skill to generate GEO-oriented topics, articles, FAQs, social posts, citation reports, and operating guidance for global B2B and DTC market expansion. The skill may call third-party AI, search, and social APIs when users configure credentials and approve publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Brand, market, draft-content, and citation-analysis context may be sent to third-party AI or search providers. <br>
Mitigation: Use only approved data, avoid secrets or sensitive customer information in prompts, and review provider policies before configuring API keys. <br>
Risk: Social publishing features can expose public content through OAuth-connected platforms. <br>
Mitigation: Grant the narrowest OAuth scopes available and manually approve every public post before publishing. <br>
Risk: Broad activation phrases can trigger the skill in ordinary marketing conversations. <br>
Mitigation: Confirm the intended GEO workflow and target market before generating or distributing content. <br>


## Reference(s): <br>
- [GEO AgentOps Homepage](https://geoagentops.ai) <br>
- [GEO Methodology](artifact/references/GEO-METHODOLOGY.md) <br>
- [LLMs.txt Configuration Guide](artifact/references/LLMs-TXT-GUIDE.md) <br>
- [Schema Markup Guide](artifact/references/SCHEMA-GUIDE.md) <br>
- [OpenAI API](https://api.openai.com) <br>
- [Anthropic API](https://api.anthropic.com) <br>
- [Perplexity API](https://api.perplexity.ai) <br>
- [LinkedIn API](https://api.linkedin.com) <br>
- [Twitter/X API](https://api.twitter.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with structured text, inline code blocks, templates, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce content drafts, reports, platform-specific post copy, scoring guidance, and local script commands.] <br>

## Skill Version(s): <br>
2.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
