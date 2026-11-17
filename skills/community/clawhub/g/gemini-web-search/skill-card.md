## Description:

Use Gemini CLI (@google/gemini-cli) to do web search and fact-finding, then return a concise sourced summary for up-to-date information requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengjiajie](https://clawhub.ai/user/fengjiajie)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill when they need current web search, news triage, source links, or fact-finding summaries produced through Gemini CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt text passed through the bundled shell wrapper may be interpreted as local shell syntax.

Mitigation: Avoid the wrapper until it is changed to pass Gemini arguments without shell interpretation; review command execution before use.

Risk: Web-search prompts or Gemini CLI activity may use an existing local Gemini login or session.

Mitigation: Use only non-sensitive prompts and confirm the active Gemini account/session before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fengjiajie/skills/gemini-web-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with concise bullets, links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces sourced summaries and may provide Gemini CLI prompts or troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
