## Description:

Call Script Coach helps users prepare for difficult phone calls by building branching call scripts, objection-response trees, printable cheat sheets, and practice drills from a stated goal, leverage, and fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to prepare for high-stakes phone calls such as billing disputes, cancellations, landlord repair demands, collections responses, sales calls, and rate negotiations. It helps an agent produce structured scripts, objection handling, printable notes, and practice feedback for a specific call.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated scripts saved under ~/.call-scripts may contain account numbers, dispute details, or negotiation strategy.

Mitigation: Avoid entering unnecessary sensitive identifiers, keep saved files private, and delete generated scripts when they are no longer needed.

Risk: Collections, landlord, insurance, recording, and rights-based language can be legally sensitive and may vary by jurisdiction.

Mitigation: Verify local law or get qualified advice before relying on jurisdiction-specific language in an actual call.

## Reference(s):

- [Call Negotiation Playbook](references/negotiation-playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands; generated call scripts are saved as local text and JSON files when the bundled script is run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local stdlib Python commands and can save user-provided call details under ~/.call-scripts.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
