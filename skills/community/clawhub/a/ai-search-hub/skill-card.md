## Description:

Run the AI Search Hub browser automation scripts for Yuanbao, LongCat, Doubao, Qwen, Gemini, and Grok.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peanuts62](https://clawhub.ai/user/peanuts62)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to send a prompt to supported AI chat and search sites through a common browser automation entrypoint, collect the response, and optionally save it to a text file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill opens or attaches to a local Chromium browser and sends prompts to selected external AI providers.

Mitigation: Use a dedicated browser profile and avoid submitting secrets, regulated data, or confidential prompts.

Risk: The skill can copy signed-in browser profile data into a persistent debug directory.

Mitigation: Prefer a fresh profile, disable implicit invocation for sensitive environments, and delete the debug profile after use.

Risk: Browser automation may fail or produce incomplete results when a provider requires login, blocks access, changes its UI, or is region unavailable.

Mitigation: Review saved outputs before relying on them and rerun with an explicit provider, profile, and output path when results are incomplete.

## Reference(s):

- [AI-Search-Hub ClawHub release](https://clawhub.ai/peanuts62/skills/ai-search-hub)
- [Publisher profile](https://clawhub.ai/user/peanuts62)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and text-file outputs from browser automation runs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the selected external AI provider, login state, browser availability, and target site behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
