## Description:

Check for co-authorship conflicts between authors and suggested reviewers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Editors, journal staff, and researchers use this skill to compare proposed reviewers against manuscript authors using supplied names and optional publication CSV records before making peer-review assignments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes reviewer, author, and publication data in a local workspace.

Mitigation: Run it in a controlled workspace and avoid sharing generated conflict reports in public or collaborative locations.

Risk: Conflict results are advisory and may be affected by documented reliability issues in the demo path and unused institutional check.

Mitigation: Have an editor or reviewer verify flagged and unflagged conflicts against authoritative publication and institutional records before making decisions.

Risk: The publications option reads a user-supplied local CSV path.

Mitigation: Use a controlled CSV path and review input files before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain-text CLI report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory conflict findings and reviewer recommendations based on provided author, reviewer, and publication inputs.]

## Skill Version(s):

0.1.4 (source: server release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
