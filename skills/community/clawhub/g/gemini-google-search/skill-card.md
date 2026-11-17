## Description:

Uses Gemini API Google Search grounding to answer OpenClaw web-search requests when Google/Gemini-backed, cited current answers are appropriate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psanger](https://clawhub.ai/user/psanger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to run Google/Gemini-backed searches when local search is blocked, incomplete, or unsuitable, and to receive synthesized answers with grounding URLs when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Gemini/Google and may incur quota, billing, or external data exposure.

Mitigation: Use this skill only when Google/Gemini-backed search is appropriate; prefer a local search skill for private or sensitive queries.

Risk: The skill uses a Gemini API key from environment variables or a 1Password item.

Mitigation: Use a narrowly scoped credential source and avoid printing or logging API keys.

Risk: The wrapper can automatically install the google-genai dependency into a skill-local virtual environment.

Mitigation: Review or pin the dependency before first use in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/psanger/skills/gemini-google-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-style text or JSON containing the query, model, answer, source URLs, and grounding metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Grounding URLs are included only when Gemini returns them; otherwise the skill reports that no grounding URLs were returned.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
