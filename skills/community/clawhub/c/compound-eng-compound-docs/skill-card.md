## Description:

Capture solved problem write-ups for team reuse, including context gathering, YAML validation, categorized Markdown files, and follow-up cross-references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iliaal](https://clawhub.ai/user/iliaal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this workflow after non-trivial debugging, resolved issues, or post-mortems to document root cause, failed attempts, solution details, prevention notes, and related links for future reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad auto-trigger behavior may create or modify repository documentation after ordinary success phrases without a clear write-approval checkpoint.

Mitigation: Use explicit documentation requests such as 'document this solution' or require the agent to show the target path and wait for approval before creating or changing files.

Risk: Follow-up menu options can lead to additional documentation or skill changes beyond the initial solution write-up.

Mitigation: Review the selected option and target files before allowing changes, especially for actions that promote patterns or add knowledge to existing or new skills.

Risk: Missing or invalid context can produce incomplete or misleading troubleshooting documentation.

Mitigation: Require the documented critical context and block creation until YAML frontmatter validates against the bundled schema.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iliaal/skills/compound-eng-compound-docs)
- [Documentation capture process](artifact/references/documentation-process.md)
- [YAML frontmatter schema](artifact/references/yaml-schema.md)
- [Quality guidelines](artifact/references/quality-guidelines.md)
- [Example scenario](artifact/references/example-scenario.md)
- [Resolution template](artifact/assets/resolution-template.md)
- [Critical pattern template](artifact/assets/critical-pattern-template.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files with YAML frontmatter, command snippets, and follow-up guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates documentation under docs/solutions/ and validates frontmatter with Python 3 and PyYAML when available.]

## Skill Version(s):

4.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
