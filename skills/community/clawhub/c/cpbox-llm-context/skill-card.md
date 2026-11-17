## Description:

Provides RAG and LLM grounding by returning pre-extracted, relevance-ranked web content through GET and POST API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sprintmint](https://clawhub.ai/user/sprintmint)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI builders use this skill to retrieve web-grounding context for agents, RAG pipelines, assistants, fact checking, and content research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic x402 payment execution through an unpinned payment client may make paid requests without enough guardrails.

Mitigation: Pin and vet the x402 payment client, and use spending limits or explicit confirmation before paid calls.

Risk: Location-aware recall can send precise coordinates when local headers are used.

Mitigation: Avoid sending exact coordinates unless the user specifically requests location-aware results; prefer coarse location fields when sufficient.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sprintmint/skills/cpbox-llm-context)
- [CPBox API provider](https://www.cpbox.io)
- [CPPay x402 facilitator](https://www.cppay.finance)
- [LLM Context GET endpoint](https://www.cpbox.io/api/x402/llm-context)
- [LLM Context POST endpoint](https://www.cpbox.io/api/x402/llm-context/post)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with HTTP and bash examples; API responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports token, URL, snippet, ranking, Goggles, and optional location parameters; paid requests use x402 payment middleware.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
