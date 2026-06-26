## Description: <br>
Convert PDFs and documents to markdown, index them locally for RAG retrieval, and analyze them token-efficiently. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chiefsegundo](https://clawhub.ai/user/chiefsegundo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Boof to convert local PDFs or documents into markdown, index them for local semantic retrieval, and analyze focused excerpts without placing entire documents in the model context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports a path-injection flaw in the script. <br>
Mitigation: Review before installing, use only trusted files with simple filenames, and avoid unusual paths until path handling is fixed. <br>
Risk: The security evidence reports that indexing can include more markdown files than expected. <br>
Mitigation: Use a dedicated output directory and verify that only intended files are indexed. <br>
Risk: The skill processes local documents through document-conversion and retrieval tooling. <br>
Mitigation: Avoid processing untrusted documents unless the environment and dependencies are reviewed. <br>


## Reference(s): <br>
- [Boof Skill Page](https://clawhub.ai/chiefsegundo/boof) <br>
- [Setup Guide](references/setup-guide.md) <br>
- [Advanced Usage](references/advanced-usage.md) <br>
- [opendataloader-pdf](https://github.com/opendataloader-project/opendataloader-pdf) <br>
- [QMD](https://github.com/tobi/qmd) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces converted markdown files and QMD collection names for later retrieval.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
