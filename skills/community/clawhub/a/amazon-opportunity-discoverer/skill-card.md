## Description:

Automated product opportunity scanner for Amazon sellers that scans categories with preset selection strategies, validates candidates with ZooData signals, and ranks opportunities by composite score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apiclaw](https://clawhub.ai/user/apiclaw)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and commerce analysts use this skill to discover product opportunities from broad keywords or categories, score candidates against seller profile constraints, and receive ranked next-step guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API-key handling and configurable endpoint trust can expose credentials if users point requests at an untrusted destination.

Mitigation: Review configuration before use, avoid ZOODATA_BASE_URL unless the destination is fully trusted, and do not use HTTP or localhost with a production API key.

Risk: Broad opportunity scans can consume paid ZooData API credits.

Mitigation: Confirm broad or multi-call scans before running them and use quick or granular scans when credit budget is limited.

Risk: A mutable install source can change after review.

Mitigation: Pin the repository or release before installing or deploying the skill.

## Reference(s):

- [ZooData API Field Reference](references/reference.md)
- [ZooData CLI Contract](references/cli-contract.md)
- [ZooData-Skills project homepage](https://github.com/SerendipityOneInc/ZooData-Skills)
- [ClawHub skill listing](https://clawhub.ai/apiclaw/skills/amazon-opportunity-discoverer)
- [ZooData](https://zoodata.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with tables, ranked candidates, data provenance, and API usage details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZOODATA_API_KEY and may consume ZooData API credits during scans.]

## Skill Version(s):

1.0.9 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
