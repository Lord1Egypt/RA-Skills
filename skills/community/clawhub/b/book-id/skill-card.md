## Description: <br>
Catalog books from photos or text. Trigger on: book photo, catalog book, log book, add to library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gabebac](https://clawhub.ai/user/gabebac) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to identify a book from a cover photo or text prompt, gather bibliographic details from web sources, and create a structured book note with a saved cover photo. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create book notes and photos in the workspace after broad trigger phrases. <br>
Mitigation: Confirm the target book and output path before allowing file creation. <br>
Risk: The workflow includes running a local fix-md.sh script that is not provided in the artifact. <br>
Mitigation: Review or remove the fix-md.sh step before installation or execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gabebac/book-id) <br>
- [Publisher Profile](https://clawhub.ai/user/gabebac) <br>
- [OpenLibrary Search API](https://openlibrary.org/search.json) <br>
- [OpenLibrary Covers API](https://covers.openlibrary.org/) <br>
- [Wikipedia](https://www.wikipedia.org/) <br>
- [Goodreads](https://www.goodreads.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files] <br>
**Output Format:** [Markdown note with YAML frontmatter, workspace file paths, and shell command execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a 32-property book note and may save a related book photo when a readable cover or sufficient text is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
