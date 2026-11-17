## Description:

Step-by-step SEO blog writing workflow for teams who want full control over keyword strategy, competitive research, content structure, internal linking, AI writing pattern avoidance, link verification, and QA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justinbao19](https://clawhub.ai/user/justinbao19)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, content teams, and SEO practitioners use this skill to plan, draft, optimize, verify, and hand off long-form blog articles for any website or blog.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run with full execution privileges and bypass normal approval gates for link verification and QA.

Mitigation: Run it only in a constrained workspace, confirm which files it may read and write, and grant full execution privileges only when the referenced QA scripts and network requests are trusted.

Risk: The workflow depends on external link checks and QA scripts that may make network requests.

Mitigation: Review requested network activity and script behavior before execution, then verify the generated article and QA report before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justinbao19/skills/blog-writing)
- [Publisher profile](https://clawhub.ai/user/justinbao19)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and structured review handoff notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces research briefs, article drafts, link-verification notes, QA report references, and review handoff guidance.]

## Skill Version(s):

2.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
