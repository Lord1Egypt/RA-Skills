## Description:

Creates a five-section pre-earnings equity research draft with claims and figures tied to source quotes and anchors, excluding ratings, target prices, and share-price forecasts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

Equity researchers and analysts use this skill to draft pre-earnings, single-company research from supplied or retrieved source material. It structures the note around business, competition, drivers, risks, and key figures, with traceable evidence for each claim.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports unexplained network requests.

Mitigation: Review the request destinations and confirm they are expected before using the optional retrieval path.

Risk: The security guidance reports gaps in calculation and recommendation safeguards in the note checker.

Mitigation: Manually verify cited text, anchors, calculations, and the absence of recommendation language; do not rely on the checker alone to validate financial content.

Risk: The security evidence is incomplete because a local reference could not be resolved.

Mitigation: Resolve and review that reference when assessing the skill's security evidence.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huhoo/skills/cue-cn-equity-research-note)
- [CUE MCP catalog](https://cuecue.cn/api/mcp-catalog)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown structured as a five-section equity research note with source quotes, anchors, and source IDs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pre-earnings research draft; no ratings, target prices, or share-price forecasts.]

## Skill Version(s):

0.2.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
