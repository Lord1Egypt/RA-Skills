## Description:

Helps writers research article images, build traceable candidate pools, evaluate content fit, and record source, license, attribution, risk, and recommended use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zacktian89](https://clawhub.ai/user/zacktian89)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and content teams use this skill to identify image needs for articles, search appropriate image sources, score candidates for factual fit and license safety, and hand off recommended, backup, and rejected images with attribution notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image lookup may send article topics or draft details to external search and image-provider services.

Mitigation: Confirm the search plan before querying, use non-sensitive search terms where possible, and avoid submitting private drafts unless the user accepts the provider exposure.

Risk: Candidate image licenses, attribution, or source metadata may be incomplete or stale.

Mitigation: Verify each selected image on its original landing page before publication and retain creator, license, license URL, landing URL, retrieval date, and attribution.

Risk: Search results, stock photos, or AI-generated images can misrepresent facts, events, people, products, or timelines.

Mitigation: Use official or primary sources for evidence images, reject images with subject or context mismatches, and mark AI-generated images so they are not treated as factual evidence.

## Reference(s):

- [License policy](artifact/references/license-policy.md)
- [Provider matrix](artifact/references/provider-matrix.md)
- [Query playbook](artifact/references/query-playbook.md)
- [Scoring rubric](artifact/references/scoring-rubric.md)
- [Tool-assisted search rules](artifact/references/tool-assisted-search.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with structured JSON image candidate records and optional HTML figure snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Candidate records include image needs, use/backup/reject decisions, source URLs, license details, attribution, risk flags, scores, and usage notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
