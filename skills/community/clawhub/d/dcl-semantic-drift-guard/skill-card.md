## Description:

Detects semantic hallucinations and context drift by comparing an LLM-generated response against an inline source document or configured knowledge-base query, then returns a grounding verdict and audit-oriented drift details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daririnch](https://clawhub.ai/user/daririnch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, evaluation teams, and agent operators use this skill to check whether generated answers remain grounded in a trusted source before committing, publishing, or escalating the output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional kb_query mode sends query text to a configured remote RAG endpoint.

Mitigation: Use context mode for confidential or regulated material; when kb_query is needed, use only trusted HTTPS endpoints under the user's control.

Risk: The optional paid MCP pre-check can send llm_output text externally and write audit metadata outside the agent context.

Mitigation: Run the optional pre-check only after confirming that external processing and audit metadata writing are acceptable for the content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daririnch/skills/dcl-semantic-drift-guard)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON verdict record with drift items, confidence, strictness, source mode, timestamp, and audit hash; explanatory text may accompany reviewer guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default context mode is local to the agent context; kb_query and the optional MCP pre-check can send selected text or query data externally.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
