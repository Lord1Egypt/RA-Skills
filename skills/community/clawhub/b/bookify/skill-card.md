## Description: <br>
Convert Markdown files to styled PDF or EPUB ebook using md-bookify. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielefavi](https://clawhub.ai/user/danielefavi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and documentation maintainers use this skill to convert Markdown files into styled PDF documents or EPUB ebooks. It supports selecting output format, document metadata, PDF page settings, styles, and EPUB cover or description metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs pinned npm packages from the npm registry. <br>
Mitigation: Install only after verifying the md-bookify package or source, and run conversion in a trusted or sandboxed environment for sensitive documents. <br>
Risk: PDF generation may require Puppeteer to download Chrome if a compatible browser is not already available. <br>
Mitigation: Expect and review the browser installation step before running it in controlled or restricted environments. <br>


## Reference(s): <br>
- [Bookify Skill Page](https://clawhub.ai/danielefavi/bookify) <br>
- [md-bookify npm Package](https://www.npmjs.com/package/md-bookify) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, files] <br>
**Output Format:** [Markdown guidance with shell commands that produce PDF or EPUB files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses md-bookify 2.2.1 and may require Node >= 20 and a Puppeteer-managed Chrome installation for PDF generation.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
