## Description:

A bidding and tendering Q&A assistant that uses IMA knowledge bases to answer process, template, bid-risk, objection, and complaint questions with source-grounded guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External users and procurement teams use this skill to ask bidding and tendering questions, analyze uploaded bidding materials, route questions to IMA knowledge bases, and receive structured guidance with sources, risks, and next actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically trust newly discovered knowledge bases for sensitive procurement guidance.

Mitigation: Pin reviewed knowledge-base IDs or require approval before newly discovered libraries are used in production.

Risk: Retrieved knowledge-base text may be incomplete, stale, or unsuitable as final legal or procurement advice.

Mitigation: Treat retrieved content as evidence, require source-grounded answers, and verify outputs against official sources or counsel before relying on them.

Risk: Legal-case retrieval may be unavailable, which could otherwise lead to unsupported case comparisons.

Mitigation: Preserve the documented KB-L downgrade behavior: continue the main answer, mark case retrieval as unavailable, and avoid inventing cases or docket numbers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/bidding-qa-assistant)
- [README](README.md)
- [System prompt](references/system_prompt.md)
- [IMA knowledge-base catalog](references/ima_kb_catalog.md)
- [Knowledge-base routing](references/kb_routing.md)
- [Few-shot examples](references/few_shot.md)
- [Test cases](references/test_cases.md)
- [Knowledge-base enhancement plan](references/kb_enhancement_plan.md)
- [KB-A IMA share link](https://ima.qq.com/wiki/?shareId=6bd8e274955cb1493860613dbaed87ceb170158b2ac6ac32bbca7f9a4f534a6a)
- [KB-B IMA share link](https://ima.qq.com/wiki/?shareId=7b6f1d9a03b7537d56f7816a6b4cd3d034aaaa5db4648b9e5ee1efd235c2766e)
- [KB-C IMA share link](https://ima.qq.com/wiki/?shareId=d0e49f86f3cf6930e8340e4398fbf969209a46cd76700372587b131b26510601)
- [KB-X IMA share link](https://ima.qq.com/wiki/?shareId=a88b3a2942a40a10856c554fb95bd6043859b665456588d9df5e4c3d1eb4e2f2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with structured answer sections and source citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers are expected to include the main response, source basis, risk提示, and action suggestions; unsafe bidding requests are refused.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
