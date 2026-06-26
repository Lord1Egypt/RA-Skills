## Description: <br>
Article2Book helps an agent evaluate existing writing assets and reorganize them into a book, booklet, course, article series, practical handbook, knowledge base, or a recommendation not to productize. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cat-xierluo](https://clawhub.ai/user/cat-xierluo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and content teams use this skill when they have a folder of existing text materials and need an agent to assess the best content product shape, produce a planning opinion, and, after confirmation, draft the chosen deliverable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and summarizes a selected folder of writing materials, which may include client, personal, or sensitive content. <br>
Mitigation: Use a dedicated folder containing only intended documents, redact sensitive information first, and review or delete generated output files that contain sensitive summaries or snippets. <br>
Risk: Published capability metadata includes unsupported crypto and purchase tags, although the supplied artifacts do not show that behavior. <br>
Mitigation: Do not treat this as a crypto or purchasing automation skill; rely on the artifact behavior and ask the publisher to correct the metadata. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cat-xierluo/article2book) <br>
- [Project homepage](https://github.com/cat-xierluo/legal-skills) <br>
- [Agent reading protocol](references/agent-reading-protocol.md) <br>
- [Book viability rubric](references/book-viability-rubric.md) <br>
- [Content productization models](references/content-productization-models.md) <br>
- [Content screening rubric](references/content-screening-rubric.md) <br>
- [Output template](references/output-template.md) <br>
- [Source type handling](references/source-type-handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, guidance] <br>
**Output Format:** [Markdown planning documents and optional local draft files, with shell commands only for optional inventory support.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default outputs are written under a local source-directory output folder; optional processed notes and inventory files may be created for large or complex material sets.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and CHANGELOG, released 2026-05-17) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
