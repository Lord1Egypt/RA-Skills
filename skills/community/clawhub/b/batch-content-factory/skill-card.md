## Description:

Batch Content Factory helps agents create platform-specific content outlines, publishing calendars, and SEO recommendations for bulk content workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, self-media operators, and brand content teams use this skill to draft platform-specific content frameworks, plan weekly publishing calendars, and review article SEO.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation overstates the automation scope relative to the local helper script.

Mitigation: Treat generated outputs as templates and guidance; verify facts, claims, and platform fit before publication.

Risk: The documented pip install command recommends unnecessary dependencies for the bundled script.

Mitigation: Run the script with standard Python unless the publisher adds real dependency usage.

Risk: Using an output path can replace content at the selected file path.

Mitigation: Use explicit output paths in a working directory and review target filenames before running commands.

## Reference(s):

- [ClawHub Release Page](https://clawhub.ai/openlark/skills/batch-content-factory)
- [Content Marketing Institute Strategy Guide](https://contentmarketinginstitute.com/developing-a-strategy/)
- [Content Templates](references/content_templates.md)
- [Platform Content Guidelines Reference](references/platform_guidelines.md)
- [Content Factory Agent Full Use Case](https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/content-factory.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain text, with optional files written to a user-provided output path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI commands cover content drafting, calendar generation, and SEO review; generated material should be reviewed before publication.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
