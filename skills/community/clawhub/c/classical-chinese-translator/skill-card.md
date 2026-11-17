## Description:

Translates Classical Chinese text into modern vernacular Chinese while preserving supported e-book and XHTML/HTML structure and adding specialized terminology explanations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrfengcn](https://clawhub.ai/user/mrfengcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and language-focused users use this skill to translate Classical Chinese source texts, especially philosophical or e-book material, into modern Chinese with terminology explanations and preserved document structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted EPUB or XHTML document may cause local file contents to appear in generated output.

Mitigation: Use the skill only with trusted input files, or run it in a sandbox without sensitive local files.

Risk: The documentation overstates safety relative to the server security summary.

Mitigation: Review the skill before installation and rely on the server security guidance when deciding deployment controls.

Risk: Unpinned runtime dependencies can change behavior across environments.

Mitigation: Pin and review dependencies before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrfengcn/skills/classical-chinese-translator)
- [English documentation](artifact/classical-chinese-translator/README-en.md)
- [Daoist terminology reference](artifact/classical-chinese-translator/references/daoist_terminology.json)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples and generated EPUB, XHTML, or HTML output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes local files and terminology dictionaries; review generated translations and formatted outputs before release.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
