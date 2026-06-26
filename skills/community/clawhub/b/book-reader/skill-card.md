## Description: <br>
Read EPUB, PDF, and TXT books from Project Gutenberg, direct URLs, or local files with progress tracking and chunked reading for agent learning workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[josharsh](https://clawhub.ai/user/josharsh) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents and developers use this skill to search public-domain books, download readable book files, read local EPUB/PDF/TXT files in chunks, and resume reading from saved progress. It is suited to learning, research preparation, summarization, and knowledge extraction workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download book files from Project Gutenberg IDs or direct URLs. <br>
Mitigation: Review direct URLs before use and keep downloads in the OpenClaw workspace or another non-sensitive books folder. <br>
Risk: The skill reads local book files selected by the user and saves reading progress locally. <br>
Mitigation: Point it only at intended EPUB, PDF, or TXT files and avoid using sensitive directories for book storage or progress state. <br>
Risk: Some sources or books may have copyright or local-law restrictions. <br>
Mitigation: Prefer public-domain Project Gutenberg sources and verify rights before using copyrighted or non-public-domain material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/josharsh/book-reader) <br>
- [Publisher profile](https://clawhub.ai/user/josharsh) <br>
- [Project Gutenberg](https://www.gutenberg.org/) <br>
- [Gutendex Project Gutenberg API](https://gutendex.com/) <br>
- [artifact/README.md](artifact/README.md) <br>
- [artifact/SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Terminal text and Markdown-style command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads book content in configurable chunks and stores progress in a local reading-state JSON file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
