## Description:

Use APIDot for Gemini 3.5 Flash API workflows, including stable Gemini Native generateContent, streamGenerateContent, long-context chat, coding iteration, knowledge-base Q&A, streaming planning, usage tracking, API key safety guidance, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan APIDot Gemini 3.5 Flash integrations, route users to current APIDot documentation, and handle API-key and streaming guidance safely.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys could be exposed if placed in browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Provide APIDOT_API_KEY only through server-side environment variables or a backend secret manager.

Risk: Unintended live APIDot requests could send prompts, documents, customer data, or tool inputs outside the local environment.

Mitigation: Make live API calls only when the user explicitly asks and a safe server-side environment is available.

Risk: Model fields, limits, pricing, or availability can change after this documentation-only skill is released.

Mitigation: Check the live APIDot docs and model page before preparing requests or making product claims.

## Reference(s):

- [APIDot Gemini 3.5 Flash Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [APIDot Gemini 3.5 Flash Model Page](https://apidot.ai/models/gemini-3-5-flash)
- [APIDot Gemini 3.5 Flash API Docs](https://apidot.ai/docs/gemini-3-5-flash)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with optional code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no bundled executable behavior or automatic network calls.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
