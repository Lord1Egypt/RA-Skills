## Description:

Analyzes the evolution memory graph for stagnation patterns, recurring failures, and success plateaus. Generates actionable insights to guide future evolution cycles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanng-ide](https://clawhub.ai/user/wanng-ide)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to analyze evolution memory graph data for stagnation, recurring failure causes, gene efficacy, and trend signals that can guide future evolution cycles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The analyzer can be pointed at any readable JSONL file and may access evolution-memory data outside the intended scope.

Mitigation: Constrain graphPath to an approved memory directory before exposing the skill in shared or untrusted environments.

Risk: The analyzer has no file-size, line-length, event-count, or timeout limits.

Mitigation: Add input size and execution limits before using the skill with untrusted or very large memory graph files.

## Reference(s):


## Skill Output:

**Output Type(s):** [analysis, guidance]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a memory_graph.jsonl file and returns cycle counts, success rates, stagnation signals, top genes, top failures, and recommendations.]

## Skill Version(s):

1.0.0 (source: package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
