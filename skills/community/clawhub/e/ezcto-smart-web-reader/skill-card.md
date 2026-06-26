## Description: <br>
Agent web access acceleration layer that reads URLs as structured JSON with a cache-first path as an alternative to raw web_fetch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[takahashigy](https://clawhub.ai/user/takahashigy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and OpenClaw users use this skill to turn URL access into structured page data, cached summaries, and next-action guidance for downstream agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically process arbitrary user-provided URLs. <br>
Mitigation: Use it only for intended public HTTP or HTTPS pages and avoid login-protected, internal, private, signed, or token-bearing URLs unless contribution is disabled and cache retention has been reviewed. <br>
Risk: Extracted page data and URLs may be shared with api.ezcto.fun. <br>
Mitigation: Review the data-sharing posture before deployment and disable contribution to the shared asset library when handling sensitive or restricted content. <br>
Risk: Local cache files may retain page-derived data. <br>
Mitigation: Review cache location, retention, and cleanup practices for the deployment environment. <br>
Risk: Generated next actions or chained-skill suggestions may lead the agent to follow unreviewed actions. <br>
Mitigation: Require confirmation before following generated next actions or chained-skill suggestions. <br>


## Reference(s): <br>
- [Output JSON Schema](references/output-schema.md) <br>
- [OpenClaw Integration Guide](references/openclaw-integration.md) <br>
- [Site Type Detection](references/site-type-detection.md) <br>
- [Translation Prompt](references/translate-prompt.md) <br>
- [Crypto Extension Fields](references/extensions/crypto-fields.md) <br>
- [E-commerce Extension Fields](references/extensions/ecommerce-fields.md) <br>
- [Restaurant Extension Fields](references/extensions/restaurant-fields.md) <br>
- [EZCTO API Documentation](https://ezcto.fun/api-docs) <br>
- [ClawHub Release Page](https://clawhub.ai/takahashigy/ezcto-smart-web-reader) <br>


## Skill Output: <br>
**Output Type(s):** [json, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [OpenClaw wrapper JSON with cached Markdown summaries and structured error objects.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cache hits can return zero-token structured data; cache misses may fetch HTML, call an LLM parser, write local cache files, and contribute extracted page data to the EZCTO service.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
