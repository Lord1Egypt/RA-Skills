## Description: <br>
Generates professional EPUB ebooks from Markdown, text, or structured content with chapters, a table of contents, cover image support, and metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, authors, and content teams use this skill to create EPUB 3.0 ebooks from Markdown or structured chapter content, including generated chapters, navigation, a table of contents, optional cover images, and book metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and uses the third-party `ebooklib` Python package. <br>
Mitigation: Install `ebooklib` in a trusted Python environment before using the generated EPUB workflow. <br>
Risk: Cover image and output paths are local file paths, so an incorrect path could read the wrong image or overwrite an existing EPUB. <br>
Mitigation: Provide explicit cover and output paths and confirm before overwriting existing EPUB files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobewin/epub-studio) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance and Python code that can produce EPUB files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses python3 and the ebooklib package; generated EPUB output depends on supplied chapter text, metadata, cover image path, and output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
