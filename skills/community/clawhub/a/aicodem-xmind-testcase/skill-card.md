## Description:

Generates XMind test-case mind map files from structured test case data, including modules, test points, cases, prerequisites, steps, expected results, and priority.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aicodem](https://clawhub.ai/user/aicodem)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and test teams use this skill to convert structured test case data into XMind-compatible mind maps for test planning and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be directed to overwrite arbitrary writable files through an underdocumented output path.

Mitigation: Run it in a dedicated output directory and validate or constrain the requested output_file path before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aicodem/skills/aicodem-xmind-testcase)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON input guidance and generated .xmind files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an XMind-compatible ZIP workbook and returns the output file path plus module, test point, and test case counts.]

## Skill Version(s):

1.0.0 (source: server release evidence, SKILL.md frontmatter, skill.yaml, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
