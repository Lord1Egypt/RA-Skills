## Description:

Conduct evidence-based research with exact, accurate APA citations using the Gemini API's 'scientific citation' (Google Search grounding) feature.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoxh](https://clawhub.ai/user/guoxh)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, research assistants, developers, and writers use this skill to run grounded Gemini research queries and receive cited summaries, literature-review support, fact-checking output, or structured source lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries are sent to Gemini and Google Search grounding.

Mitigation: Use the skill only where sharing the query with Gemini and Google Search grounding is acceptable.

Risk: The GEMINI_API_KEY environment variable is required for API access.

Mitigation: Keep the key private, scope it appropriately, and avoid committing it to skill files or logs.

Risk: The google-genai dependency may change behavior over time.

Mitigation: Pin or review the dependency before deployment.

Risk: Grounded citations improve traceability but do not guarantee factual correctness.

Mitigation: Manually verify important citations and source claims before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guoxh/skills/gemini-citation)
- [Google AI Studio API keys](https://aistudio.google.com/app/apikey)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON from a Python CLI, with grounded source titles and URLs when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, google-genai, and GEMINI_API_KEY; supports model selection and text or JSON output.]

## Skill Version(s):

1.0.3 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
