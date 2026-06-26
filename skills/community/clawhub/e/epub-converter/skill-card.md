## Description: <br>
Convert EPUB ebooks between Traditional and Simplified Chinese, including text content, metadata, table of contents repair, and a newly written EPUB output file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnzhaoxiao](https://clawhub.ai/user/johnzhaoxiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert Chinese-language EPUB files between Traditional and Simplified Chinese while preserving ebook structure and producing a converted EPUB file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review notes guidance involving DRM removal. <br>
Mitigation: Use only on EPUB files the user is authorized to modify and avoid DRM-circumvention workflows. <br>
Risk: The security review notes first-run installation of unpinned Python packages. <br>
Mitigation: Preinstall or pin dependencies in a controlled environment before using the skill in production. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/johnzhaoxiao/epub-converter) <br>
- [OpenCC project](https://github.com/BYVoid/OpenCC) <br>
- [ebooklib project](https://github.com/aerkalov/ebooklib) <br>
- [EPUB specification](http://idpf.org/epub) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [EPUB file output with Markdown and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a converted EPUB file; default output names add a Simplified or Traditional Chinese suffix unless an output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
