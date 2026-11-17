## Description:

Use APIDot for Tripo H3.1 3D API workflows, including Tripo H3.1 API, text-to-3D API, image-to-3D API, multiview-to-3D API, 3D asset generation, async task submission, task_id handling, polling, task status, and webhook integration based on APIDot docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route APIDot Tripo H3.1 3D API questions to current docs, examples, async task handling patterns, and security guidance for text-to-3D, image-to-3D, and multiview-to-3D integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys, private prompts, source media URLs, callback URLs, or generated asset URLs could be exposed if copied into client code, logs, public repositories, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY and sensitive workflow data server-side, store secrets in a backend secret store, and avoid logging or echoing private values.

Risk: Live APIDot calls may create jobs or use account resources unintentionally.

Mitigation: Only make live API calls when the user explicitly asks and provides a safe server-side environment.

Risk: Model-specific request fields, limits, availability, and commercial terms may change outside the local reference notes.

Mitigation: Use current APIDot docs and model pages as the source of truth before preparing payloads or making product claims.

## Reference(s):

- [APIDot Tripo H3.1 Reference](references/api.md)
- [APIDot Documentation](https://apidot.ai/docs)
- [Tripo H3.1 Model Page](https://apidot.ai/models/tripo-h31-3d)
- [Tripo H3.1 3D API Docs](https://apidot.ai/docs/tripo-h31-3d)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown text with links, implementation guidance, and optional code or configuration snippets when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no executable payload, bundled client, stored credentials, or automatic network calls.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
