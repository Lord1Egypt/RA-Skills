## Description:

Search the web using Gemini with Google Search grounding through a local script, with model routing and quota fallback across Gemini Flash-Lite / Flash variants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jas0n1ee](https://clawhub.ai/user/jas0n1ee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Gemini-only web research with Google Search grounding, selectable cheap/balanced/deep routing, quota-aware fallback, and structured JSON for orchestration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Google's Gemini API with Google Search grounding.

Mitigation: Use this skill only for queries that may be shared with the Gemini API and avoid sensitive or confidential search content unless approved.

Risk: The shell wrapper can execute a local .env.local file as shell code, and the Python entrypoint imports variables from that file.

Mitigation: Prefer the Python entrypoint, keep .env.local under your control with only SMART_SEARCH_GEMINI_API_KEY or GEMINI_API_KEY, and avoid the shell wrapper unless the env file is trusted and simple key-value data.

Risk: Grounding citations may be Google or Vertex redirect URLs rather than canonical publisher URLs.

Mitigation: Review citations before reuse or downstream fetching, and preserve source context when consuming search results.

Risk: Gemini model display labels and callable API IDs can drift, causing fallback to a different model than the selected mode implies.

Mitigation: Inspect model_used, display_chain, fallback_chain, and usage.attempted_models in JSON output when cost, latency, or model selection matters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jas0n1ee/skills/gemini-smart-search)
- [Config Notes](references/config.md)
- [Release Checklist](references/release-checklist.md)
- [Release Notes v0.1.1](references/release-notes-v0.1.1.md)
- [QA Results 2026-03-12](references/qa-results-2026-03-12.md)
- [Model ID Reconnaissance](references/model-id-recon.md)
- [Escalation Design](references/escalation-design.md)
- [Example Output](assets/example-output.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON with answer text, citations, model routing metadata, error details, and escalation metadata; optional plain text output without --json.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SMART_SEARCH_GEMINI_API_KEY or GEMINI_API_KEY; supports cheap, balanced, and deep modes with retryable Gemini model fallback.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
