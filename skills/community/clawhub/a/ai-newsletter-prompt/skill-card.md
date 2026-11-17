## Description:

Generates a curated daily AI news digest from fresh web sources, covering recent AI and machine learning developments such as model releases, research papers, funding, product launches, regulation, and benchmark results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to request a curated AI news briefing from live web sources. It filters, ranks, verifies, and summarizes relevant AI news for practitioner-oriented daily or recent digests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on live web search and page fetching, so digest quality can be affected by stale snippets, inaccessible pages, paywalls, duplicate stories, or source errors.

Mitigation: The artifact directs the agent to verify page relevance, skip login walls and low-content pages, retry failed fetches, remove duplicates, cite sources, and report shortfalls or warnings.

Risk: The skill can write a dated markdown newsletter file when file output is requested.

Mitigation: Use inline output unless a saved digest is desired, and choose file or both only when writing under the outputs directory is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j3ffyang/skills/ai-newsletter-prompt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, JSON]

**Output Format:** [Markdown digest, optional markdown file, or JSON object when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can optionally create a dated markdown newsletter file when file output is requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
