## Description: <br>
Search the web using Gemini with Google Search grounding through a local script, with model routing and quota fallback across Gemini Flash-Lite / Flash variants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jas0n1ee](https://clawhub.ai/user/jas0n1ee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent needs Gemini-only web research with Google Search grounding, model routing, quota-aware fallback, and structured JSON results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Google/Gemini for grounded search. <br>
Mitigation: Use the skill only for queries approved for third-party processing, and avoid confidential or regulated data unless that disclosure is authorized. <br>
Risk: The skill requires a Gemini API key and can load it from local environment configuration. <br>
Mitigation: Use `SMART_SEARCH_GEMINI_API_KEY` for this skill, keep `.env.local` gitignored, and avoid storing unrelated secrets in the same file. <br>
Risk: Grounding citations may be Google or Vertex redirect URLs rather than canonical publisher URLs. <br>
Mitigation: Review citation targets before relying on them in final research or downstream reports. <br>
Risk: Quota or model availability can cause fallback to a different Gemini model than the preferred display label. <br>
Mitigation: Inspect `model_used`, `fallback_chain`, and `display_chain` in the JSON output when reproducibility or model choice matters. <br>


## Reference(s): <br>
- [Config Notes](references/config.md) <br>
- [Example Output](assets/example-output.json) <br>
- [Model ID Reconnaissance](references/model-id-recon.md) <br>
- [Escalation Design](references/escalation-design.md) <br>
- [QA Test Plan](references/qa-test-plan.md) <br>
- [QA Results 2026-03-12](references/qa-results-2026-03-12.md) <br>
- [Release Notes v0.1.1](references/release-notes-v0.1.1.md) <br>
- [Gemini Developer API models endpoint](https://generativelanguage.googleapis.com/v1beta/models) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Structured JSON search result, or plain text answer with sources when JSON output is not requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON includes ok, query, mode, model_used, fallback_chain, display_chain, answer, citations, usage, error, and escalation fields.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
