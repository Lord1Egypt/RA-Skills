## Description:

Recommend the next book to read by combining the user's current request with relevant conversation context, available long-term memory, reading history, and verified book information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fov6363](https://clawhub.ai/user/fov6363)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to get a single timely book recommendation grounded in their current request, relevant memory, reading history when available, and verified book facts. It is intended for personalized reading guidance rather than generic book lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use relevant long-term memory or reading-history data when available.

Mitigation: Use only the minimum relevant memory signal, avoid exposing unrelated memories, and treat stale or ambiguous memory as uncertain.

Risk: Book facts, availability, or edition-specific claims may be outdated or incorrect if not verified.

Mitigation: Verify title, author, premise, availability, and edition-sensitive claims with reliable current sources before recommending a book.

Risk: The default prompt and response contract may lead to Chinese-language output.

Mitigation: Match the user's requested language or make the language choice explicit when needed.

## Reference(s):

- [Recommendation Rubric](references/recommendation-rubric.md)
- [ClawHub Skill Page](https://clawhub.ai/fov6363/skills/find-next-book)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown response with a primary recommendation, compact rationale, reading approach, and cited uncertainty]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include up to two alternatives when they represent meaningful tradeoffs.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
