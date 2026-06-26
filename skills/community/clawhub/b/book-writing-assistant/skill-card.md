## Description: <br>
A conversational writing companion for book authors that tracks manuscript continuity and helps brainstorm, outline, draft, and unblock fiction or nonfiction projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris-openclaw](https://clawhub.ai/user/chris-openclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External authors and writing-focused agent users use this skill to organize book projects, maintain continuity, track research and story structure, brainstorm ideas, draft passages, and work through writer's block. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores manuscript continuity data, research notes, character details, and book ideas in a local book-data.json file. <br>
Mitigation: Review or delete book-data.json when older book ideas, research notes, or character details should not persist or be reused. <br>
Risk: The skill may activate on broad or casual book-writing phrases. <br>
Mitigation: Confirm the active project and intent when a writing-related prompt could be casual or ambiguous. <br>


## Reference(s): <br>
- [Book Writing Assistant README](artifact/README.md) <br>
- [Book Writing Assistant release page](https://clawhub.ai/chris-openclaw/book-writing-assistant) <br>
- [chris-openclaw publisher profile](https://clawhub.ai/user/chris-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Conversational Markdown responses, drafted prose passages, structured outlines, and local JSON project data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local book-data.json file containing manuscript continuity, research notes, characters, plot threads, chapter outlines, and related project details.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter, changelog, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
