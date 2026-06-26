## Description: <br>
Books is a CLI skill for AI agents to search and look up book and author metadata using the Open Library API without authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffaf](https://clawhub.ai/user/jeffaf) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this agent skill to search Open Library for books by title, author, or subject, then retrieve work details, author biographies, and bibliography entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed package is documentation-only and points to external CLI scripts that were not included in the reviewed artifact. <br>
Mitigation: Review and pin the external repository before installing or executing the CLI files. <br>
Risk: The skill may run network lookups against Open Library when invoked for broad book-related conversations. <br>
Mitigation: Invoke it only for explicit search, work, or author lookup requests and inspect returned metadata before relying on it. <br>


## Reference(s): <br>
- [Open Library](https://openlibrary.org) <br>
- [Open Library API](https://openlibrary.org/developers/api) <br>
- [Books on ClawHub](https://clawhub.ai/jeffaf/books) <br>
- [jeffaf ClawHub Profile](https://clawhub.ai/user/jeffaf) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text CLI output with book and author metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes titles, publication dates, ratings, subjects, descriptions, work IDs, author IDs, and cover links when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
