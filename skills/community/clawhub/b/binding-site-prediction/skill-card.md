## Description:

Binding-site and pocket prediction workflows using P2Rank, AF2BIND, and fpocket through SciMiner.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sciminer](https://clawhub.ai/user/sciminer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, computational biologists, and structure-based drug discovery teams use this skill to predict, rank, and cross-check candidate ligand-binding pockets from protein structures or supported identifiers before docking, virtual screening, or focused analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote SciMiner Markdown can affect credential-bearing API calls and protein file uploads.

Mitigation: Install only if SciMiner's hosted documentation and infrastructure are trusted; prefer reviewed, pinned API schemas and destination validation before attaching credentials.

Risk: Incorrect or divergent pocket predictions could lead users to overcommit to a single binding-site hypothesis.

Mitigation: Cross-check complementary methods and inspect uncertain or disagreeing candidate pockets before using results for docking, screening, or design decisions.

## Reference(s):

- [P2Rank SciMiner API documentation](https://sciminer.tech/tool_api_files/p2rank_api_doc.md)
- [AF2BIND SciMiner API documentation](https://sciminer.tech/tool_api_files/af2bind_api_doc.md)
- [fpocket SciMiner API documentation](https://sciminer.tech/tool_api_files/fpocket_api_doc.md)
- [Binding site prediction on ClawHub](https://clawhub.ai/sciminer/skills/binding-site-prediction)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration, markdown]

**Output Format:** [Markdown with API invocation code, parameter guidance, status summaries, and SciMiner share URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SciMiner task results and share URLs; avoids printing or persisting the configured API key.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
