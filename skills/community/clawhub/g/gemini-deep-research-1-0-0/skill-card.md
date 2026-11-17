## Description:

Performs complex, long-running research tasks using Gemini Deep Research Agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lion504](https://clawhub.ai/user/lion504)

### License/Terms of Use:


## Use Case:

Developers, analysts, and researchers use this skill to launch Gemini Deep Research investigations that gather web sources and produce comprehensive reports for market, technical, or competitive research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research prompts and optional file-search context are sent to Google Gemini.

Mitigation: Use only approved inputs, avoid secrets or regulated data in queries, and confirm that Google Gemini use is acceptable for the task.

Risk: Generated JSON metadata may include prompt, response, and interaction details.

Mitigation: Choose an output directory outside shared repositories when needed, and review or delete generated metadata after use.

Risk: Supplying an API key on the command line can expose it through shell history or process inspection.

Mitigation: Prefer GEMINI_API_KEY from the environment over the --api-key argument.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lion504/skills/gemini-deep-research-1-0-0)
- [Google AI Studio API keys](https://aistudio.google.com/apikey)
- [Gemini Generative Language API endpoint](https://generativelanguage.googleapis.com/v1beta/interactions)

## Skill Output:

**Output Type(s):** [markdown, json, shell commands, guidance]

**Output Format:** [Markdown report plus JSON interaction metadata; progress updates may stream to stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GEMINI_API_KEY; saves timestamped report and metadata files to the selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
