## Description:

Geepers Llm sends requests to the dr.eamer.dev LLM API for chat completions, vision analysis, image generation, text-to-speech, and video generation across 12 model providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukeslp](https://clawhub.ai/user/lukeslp)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to call a unified external LLM API for chat, vision, image generation, text-to-speech, video generation, and provider comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, and text-to-speech content are sent to api.dr.eamer.dev and may be routed to downstream model providers.

Mitigation: Avoid sending secrets, credentials, regulated data, or sensitive images unless that data flow has been approved.

Risk: The skill depends on an external LLM API service and API-key authentication.

Mitigation: Confirm service availability, provider terms, and DREAMER_API_KEY handling before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lukeslp/skills/geepers-llm)
- [Dreamer LLM service](https://dr.eamer.dev)
- [Dreamer LLM API](https://api.dr.eamer.dev)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with HTTP examples and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DREAMER_API_KEY; requests may include prompts, image URLs, and text-to-speech content sent to an external API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
