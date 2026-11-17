## Description:

Search and explore Are.na for curated channels, references, and visual inspiration by analyzing connections and identifying key curators across any topic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[givenness](https://clawhub.ai/user/givenness)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to research Are.na collections, follow channel and block connections, identify relevant curators, and synthesize sourced briefs from curated material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to load a broad global shell environment file, which may expose unrelated secrets or execute local shell content.

Mitigation: Provide only ARENA_ACCESS_TOKEN through a skill-specific environment file or per-command environment before use.

Risk: The artifact references CLI and API files that are not included in the submitted artifact.

Mitigation: Verify the missing referenced CLI files are present and reviewed before relying on the skill's command workflows.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON output from the referenced CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save markdown research drafts when the skill's save workflow is available.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
