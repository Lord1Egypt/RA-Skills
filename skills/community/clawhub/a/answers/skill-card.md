## Description:

Provides AI-grounded answers through Brave's OpenAI-compatible chat completions API, with fast single-search and deeper research modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xrichyrich](https://clawhub.ai/user/0xrichyrich)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to call Brave Answers for cited, web-grounded responses in chat interfaces, research workflows, or OpenAI SDK-compatible integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to Brave when the skill is used.

Mitigation: Use only prompts and source material that policy allows sending to Brave; avoid secrets, private internal documents, personal data, and regulated data unless approved.

Risk: Research mode can increase usage and cost because it performs iterative searches.

Mitigation: Set query, iteration, token, and time limits, and monitor usage data returned by the API.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0xrichyrich/skills/answers)
- [Brave Search API](https://api.search.brave.com)
- [Brave Answers Chat Completions Endpoint](https://api.search.brave.com/res/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with cURL examples, Python code blocks, API parameters, and response format guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documents single-search and research modes, streaming constraints, citation behavior, and usage reporting.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
