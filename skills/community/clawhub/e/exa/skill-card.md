## Description:

Neural web search and code context via Exa AI API. Requires EXA_API_KEY. Use for finding documentation, code examples, research papers, or company info.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fardeenxyz](https://clawhub.ai/user/fardeenxyz)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to query Exa for web search, code/documentation context, research papers, company information, and extracted URL content from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, code-search prompts, and requested URLs are sent to Exa.

Mitigation: Avoid submitting secrets, private source snippets, internal URLs, or confidential project details unless organizational policy permits Exa use.

Risk: The skill requires an EXA_API_KEY to make Exa API calls.

Mitigation: Configure the API key through the environment and rotate or revoke it according to normal credential handling practices.

## Reference(s):

- [ClawHub Exa Skill](https://clawhub.ai/fardeenxyz/skills/exa)
- [Exa API Keys Dashboard](https://dashboard.exa.ai/api-keys)
- [Exa Search API Endpoint](https://api.exa.ai/search)
- [Exa Contents API Endpoint](https://api.exa.ai/contents)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Shell commands, Configuration guidance]

**Output Format:** [JSON API responses and Markdown guidance with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EXA_API_KEY and sends user-provided queries or URLs to Exa.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
