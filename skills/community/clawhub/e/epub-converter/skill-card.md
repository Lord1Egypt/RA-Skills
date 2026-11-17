## Description:

Converts EPUB ebooks between Traditional and Simplified Chinese, including text content, metadata, and table-of-contents repair.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnzhaoxiao](https://clawhub.ai/user/johnzhaoxiao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert authorized Chinese EPUB ebooks between Traditional and Simplified Chinese while preserving the original file and producing a new EPUB.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First run may install unpinned Python packages into a persistent local virtual environment.

Mitigation: Install dependencies from reviewed, pinned versions or run the conversion in an isolated environment before using it with valuable ebooks.

Risk: Artifact guidance mentions removing DRM before conversion.

Mitigation: Use the skill only with EPUB files the user is authorized to convert and avoid following DRM-removal guidance.

Risk: Conversion can alter ebook text, metadata, or table-of-contents structure.

Mitigation: Keep original EPUB files backed up and inspect converted output in an ebook reader before distribution or archival use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnzhaoxiao/skills/epub-converter)
- [OpenCC project](https://github.com/BYVoid/OpenCC)
- [ebooklib project](https://github.com/aerkalov/ebooklib)
- [EPUB specification](http://idpf.org/epub)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Markdown, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and generated EPUB files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a new converted EPUB file and prints conversion status, output path, and file size comparison.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
