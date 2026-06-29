## Description: <br>
Generates Chinese-language HTML book research reports and Markdown conversation kits from a book title, using public web sources and optional text-based PDF extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alzero-t](https://clawhub.ai/user/alzero-t) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create structured reading material for books, especially Chinese and English classics. It produces a self-study HTML report and a Markdown conversation kit with source-aware caveats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-supplied PDFs are read locally, and cached source data plus generated reports are stored under the skill directory. <br>
Mitigation: Invoke the skill explicitly, avoid sensitive PDFs unless local storage is acceptable, and review generated files before sharing. <br>
Risk: Public book sources can be incomplete, unstable, or blocked, which may leave generated report sections sparse or unverified. <br>
Mitigation: Keep unsupported details omitted or marked as unverified, and verify important claims against primary sources before reuse. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alzero-t/book-report) <br>
- [Publisher Profile](https://clawhub.ai/user/alzero-t) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, guidance] <br>
**Output Format:** [HTML report file plus Markdown conversation kit, with concise file-path guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports are written under the skill's reports directory; optional PDF input is limited to text-based PDFs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
