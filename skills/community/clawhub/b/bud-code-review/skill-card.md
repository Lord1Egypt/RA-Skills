## Description:

AI-powered code review using Gemini. Reviews entire projects, catches bugs, suggests fixes, and helps debug.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stigg86](https://clawhub.ai/user/stigg86)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review Python projects, individual files, or inline snippets with Gemini, then receive prioritized findings, debugging guidance, and suggested fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewed code may be sent to Gemini during analysis.

Mitigation: Avoid using the skill on private, regulated, or secret-bearing repositories unless that data sharing is acceptable.

Risk: The release includes a hardcoded Gemini API key fallback.

Mitigation: Require an explicit user-provided GEMINI_API_KEY and remove embedded credentials before use.

Risk: Security evidence reports weak disclosure and controls around external code sharing.

Mitigation: Add clear data-sharing warnings and align the implementation with the documented credential behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stigg86/skills/bud-code-review)
- [Google AI Studio](https://aistudio.google.com)
- [Gemini generateContent API endpoint](https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown-style text report with prioritized findings and suggested fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include review findings, debugging explanations, and code-oriented recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
