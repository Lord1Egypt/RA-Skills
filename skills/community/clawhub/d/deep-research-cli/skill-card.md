## Description:

Deep Research guides an agent through iterative web search, page reading, gap analysis, and synthesis to produce comprehensive, well-sourced Markdown reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangsjt](https://clawhub.ai/user/yangsjt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and other external users can use this skill to structure deep web research, evaluate sources, resolve gaps, and produce citation-rich Markdown briefings in the user's language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The standalone script can run Gemini with broad unattended authority.

Mitigation: Review the script before use and prefer configurations that keep tool approval interactive or tightly scoped.

Risk: Background mode has unsafe command handling when task names or prompts are untrusted or free-form.

Mitigation: Avoid background mode for untrusted inputs and use simple, trusted task names when the script is run.

Risk: The fallback search path may start a local SearXNG Docker container.

Mitigation: Do not run the Docker fallback unless a local SearXNG container is explicitly intended.

## Reference(s):

- [Research Methodology Reference](references/research-methodology.md)
- [ClawHub skill page](https://clawhub.ai/yangsjt/skills/deep-research-cli)
- [OpenClaw](https://github.com/anthropics/openclaw)
- [Gemini CLI](https://github.com/google-gemini/gemini-cli)
- [SearXNG](https://github.com/searxng/searxng)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with inline citations and a numbered source list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Matches the user's prompt language and includes executive summary, key findings, detailed analysis, contradictions, limitations, and sources.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
