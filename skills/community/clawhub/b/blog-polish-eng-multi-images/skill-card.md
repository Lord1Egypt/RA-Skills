## Description:

Polishes a technical blog draft into a 1000-1200 word en-US article while preserving technical terms and generating consistent hero and section image prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and content teams use this skill to polish technical blog drafts, restructure them for clarity, and prepare a matching set of image prompts for publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a configured draft file and saves durable outputs in the OpenClaw workspace.

Mitigation: Use trusted draft and output paths, and avoid custom subject values that contain path characters.

Risk: Security evidence reports that the runnable workflow may not fully match the advertised polishing behavior.

Mitigation: Review the generated article and image prompts before publication, especially when relying on the runnable workflow output.

Risk: Security evidence reports under-scoped file-writing behavior.

Mitigation: Run the skill in a workspace with appropriate file permissions and review written files after execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j3ffyang/skills/blog-polish-eng-multi-images)
- [Publisher profile](https://clawhub.ai/user/j3ffyang)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown file plus structured output fields for polishedPath, imagePaths, and imagePrompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces timestamped markdown output and hero plus per-section image prompts; image paths may be intended filenames when image generation is unavailable.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; artifact frontmatter states 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
