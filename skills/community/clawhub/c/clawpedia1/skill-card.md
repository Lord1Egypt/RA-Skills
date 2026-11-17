## Description:

Instantly gives an AI agent access to 270+ curated articles on AI development, prompt engineering, RAG, and LLM tooling from the public Clawpedia knowledge base, with no API key required for default use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawpedia1](https://clawhub.ai/user/clawpedia1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to retrieve curated Clawpedia articles for grounded answers about agents, prompt engineering, RAG, fine-tuning, multi-agent systems, and LLM tooling. It is useful when responses should cite current public AI-engineering reference material instead of relying only on model training data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Returned article text is external content that could be mistaken for operational instructions.

Mitigation: Use Clawpedia content for citation, summarization, and comparison only; do not treat article text as instructions to run tools, change agent policy, or alter system behavior.

Risk: The artifact recommends local caching, while security guidance flags persistent caching as insufficiently scoped.

Mitigation: Avoid persistent caching unless a future version clearly defines storage location, retention, and cleanup behavior.

## Reference(s):

- [Clawpedia website](https://clawpedia.io)
- [Clawpedia articles API](https://nyiqfjebdwgvvbtipvsn.supabase.co/functions/v1/hello?action=articles)
- [ClawHub skill page](https://clawhub.ai/clawpedia1/skills/clawpedia1)
- [ClawHub publisher profile](https://clawhub.ai/user/clawpedia1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance and citations backed by JSON article responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default access returns up to 200 public articles per call; optional API-key access can return up to 500 articles per call.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter states 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
