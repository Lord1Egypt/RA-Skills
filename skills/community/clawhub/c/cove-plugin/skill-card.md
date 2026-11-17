## Description:

Chain of Verification (CoVe) fact-checks responses against the user's knowledge base, memory, and web search before they are presented.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bhawanakatiyar](https://clawhub.ai/user/bhawanakatiyar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to check factual claims in agent responses against local OpenClaw memory, workspace files, optional vector stores, and optional web search. It is intended for responses that include business facts, dates, numbers, policies, customer information, or other claims that should be verified before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads private OpenClaw workspace and memory content by default and may include selected context in verification prompts.

Mitigation: Install only where that access is acceptable, and disable system memory or custom document sources in sensitive environments unless they are explicitly needed.

Risk: Verification may send claim text and selected context to configured model, search, or vector services.

Mitigation: Use approved providers and API keys, disable web or vector sources unless needed, and avoid ambient generic API keys in shared environments.

Risk: Auto-correction can change an agent response after verification.

Mitigation: Disable auto-correction for high-sensitivity workflows and review verification reports before sending corrected text.

Risk: Structured verification logs may contain sensitive claim text or correction details.

Mitigation: Review stdout and session logs in environments where customer, policy, or private workspace details may be included.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bhawanakatiyar/skills/cove-plugin)
- [OpenClaw](https://openclaw.sh)
- [Qdrant documentation](https://qdrant.tech/documentation/)
- [Chroma documentation](https://docs.trychroma.com/)
- [Weaviate documentation](https://weaviate.io/developers/weaviate)
- [Milvus documentation](https://milvus.io/docs/)
- [Redis vector search documentation](https://redis.io/docs/interact/search-and-query/)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text or JSON verification report with optional corrected response text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include verified, inaccurate, and unverifiable claim counts, source snippets, corrections, and exit codes for command-line use.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
