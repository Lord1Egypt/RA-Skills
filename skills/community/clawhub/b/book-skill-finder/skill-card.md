## Description: <br>
Searches a local Heardly-derived catalog of 5904 nonfiction books and returns ratings, summaries, links, and suggested agent knowledge-base additions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaysonmeng](https://clawhub.ai/user/jaysonmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to find nonfiction books by title, author, concept, or recommendation request and to draft SOUL, MEMORY, or SKILL snippets from selected book summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested SOUL, MEMORY, or SKILL markdown can influence future agent behavior if copied into an agent knowledge base. <br>
Mitigation: Review and scan generated snippets before adding them to agent knowledge files. <br>
Risk: Recommendations come from a bundled local book database and may be incomplete or stale. <br>
Mitigation: Validate important recommendations against current external sources before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/jaysonmeng/book-skill-finder) <br>
- [Heardly book pages](https://heardly.app/book) <br>
- [Artifact README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [JavaScript object results with Markdown snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes book metadata and suggested SOUL, MEMORY, and SKILL additions; security evidence reports local reads only, with no network calls, credentials, or file changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
