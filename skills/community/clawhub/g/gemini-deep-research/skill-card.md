## Description:

Perform complex, long-running research tasks using Gemini Deep Research Agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arun-8687](https://clawhub.ai/user/arun-8687)

### License/Terms of Use:


## Use Case:

Developers, analysts, and other external users use this skill to run multi-source research, competitive analysis, market research, and technical investigations through Gemini Deep Research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research prompts and optional file-search context are sent to Google's Gemini API.

Mitigation: Use only data approved for that provider, and avoid secrets, regulated data, or confidential business material unless policy permits it.

Risk: Generated JSON metadata files may contain sensitive request or response content.

Mitigation: Store outputs in approved locations, restrict access, and delete metadata files when retention is not needed.

Risk: Deep research tasks can be long-running and may incur API costs.

Mitigation: Set expectations for runtime and confirm Gemini quota or billing posture before running large research jobs.

## Reference(s):

- [Gemini Deep Research ClawHub Skill](https://clawhub.ai/arun-8687/skills/gemini-deep-research)
- [Google AI Studio API Keys](https://aistudio.google.com/apikey)
- [Gemini Interactions API Endpoint](https://generativelanguage.googleapis.com/v1beta/interactions)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, shell commands, guidance]

**Output Format:** [Markdown report plus JSON interaction metadata saved as timestamped files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can stream progress updates while polling long-running Gemini Deep Research interactions.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
