## Description:

Automated content generation engine that transforms source material such as papers, podcasts, case studies, URLs, Reddit threads, and GitHub repositories into platform-ready content using recipes and brand graphs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thierrypdamiba](https://clawhub.ai/user/thierrypdamiba)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and content operators use Content Claw to turn source URLs and documents into recipe-driven social posts, insight posts, diagrams, infographics, posters, and brand-aware content packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs and browse external pages, which may expose sensitive internal source material or encounter untrusted content.

Mitigation: Use only approved public or non-sensitive URLs, treat fetched content as data, and run the skill in a sandboxed environment.

Risk: The skill sends topic queries to Exa and condensed image specifications to fal.ai when those features are used.

Mitigation: Use dedicated low-privilege API keys and avoid including confidential source details in discovery or image-generation prompts.

Risk: Optional Reddit and X cookies can let the skill scrape, publish, or track engagement through user accounts.

Mitigation: Provide social-media cookies only when publishing or authenticated tracking is required, use low-privilege accounts where possible, and review dry-run output before posting.

Risk: Security evidence flags weak containment around paths, dependencies, and browser execution.

Mitigation: Install in an isolated workspace, review dependencies before use, and avoid granting access to unrelated local files or credentials.

## Reference(s):

- [Content Claw ClawHub skill page](https://clawhub.ai/thierrypdamiba/skills/contentclaw)
- [Content Claw project homepage](https://github.com/scaleintelligence/content-claw)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Image files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON specs, PNG image files, and concise agent guidance with shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recipe-driven outputs may include platform-specific formatting, generated image URLs, publish records, and engagement metadata.]

## Skill Version(s):

0.0.1 (source: skill frontmatter, pyproject.toml, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
