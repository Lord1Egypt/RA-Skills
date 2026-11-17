## Description:

APIDot Wan 2.2 Fast API helps agents route developers to APIDot documentation and async workflow guidance for Wan 2.2 Fast text-to-video and image-to-video integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this documentation-only skill to plan APIDot Wan 2.2 Fast integrations, find the right model and API documentation, and handle task IDs, polling, webhooks, and API-key safety.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys or private generation inputs could be exposed if copied into browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY in a backend secret store or server-side environment variable, and avoid logging API keys, private prompts, private media URLs, generated video URLs, or callback URLs.

Risk: Agents may produce stale or incorrect APIDot request details if they rely on memory or another Wan model family.

Mitigation: Use the live APIDot Wan 2.2 Fast docs and model page for current request fields, supported modes, limits, availability, and commercial terms.

Risk: Live paid API calls may be made before the integration environment and user intent are confirmed.

Mitigation: Do not make live APIDot calls unless the user explicitly asks and provides a safe server-side environment.

## Reference(s):

- [APIDot Wan 2.2 Fast Reference](references/api.md)
- [APIDot Documentation](https://apidot.ai/docs)
- [Wan 2.2 Fast Model Page](https://apidot.ai/models/wan-2-2-fast)
- [Wan 2.2 Fast API Docs](https://apidot.ai/docs/wan-2-2-fast)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with inline code or configuration examples when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no bundled executable files or automatic network calls.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
