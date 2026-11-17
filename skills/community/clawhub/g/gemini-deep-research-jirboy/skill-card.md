## Description:

Runs Gemini Deep Research for complex, long-running research tasks and synthesizes findings into reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and external users can use this skill to run Gemini-backed deep research on a topic and receive a synthesized report with saved interaction metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research prompts and generated results are sent to Google's Gemini API and may include sensitive topics.

Mitigation: Use a restricted Gemini API key, avoid submitting sensitive data unless approved, and review the provider's data handling terms before use.

Risk: The skill saves markdown reports and full JSON interaction metadata locally.

Mitigation: Choose an output directory appropriate for the sensitivity of the research topic and apply local access controls where needed.

Risk: Supplying an API key as a command-line argument can expose it through shell history or process listings.

Mitigation: Prefer the GEMINI_API_KEY environment variable instead of the --api-key option.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, JSON, files]

**Output Format:** [Markdown report, JSON metadata file, and terminal progress output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Gemini API key; results are saved locally in the selected output directory.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
