## Description:

Hex grid spatial utilities for offset coordinate systems. Use when working with hexagonal grids, calculating distances, finding neighbors, or spatial queries on hex maps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and map-tooling agents use this skill to reason about odd-r offset hex grids, including neighbor lookup, direction lookup, distance calculation, adjacency checks, and range queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect coordinate convention could produce wrong neighbors, distances, or spatial queries.

Mitigation: Confirm the project uses odd-r offset coordinates with odd rows shifted right before relying on results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/civ6-adjacency-optimizer-hex-grid-spatial)

## Skill Output:

**Output Type(s):** [Guidance, Code]

**Output Format:** [Markdown with Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces coordinate tuples, direction indices, integer distances, and boolean adjacency results when used as Python helpers.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
