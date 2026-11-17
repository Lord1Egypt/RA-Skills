## Description:

AI-powered bidirectional Word-to-LaTeX converter supporting multiple AI providers, with Word-to-LaTeX refinement and LaTeX-to-Word conversion that can preserve original document styles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinzhengxu](https://clawhub.ai/user/jinzhengxu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document authors use this skill to convert Word documents to LaTeX, refine converted LaTeX with a selected AI provider, edit documents through LaTeX, and convert LaTeX back to Word while reusing the original document as a style reference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document contents can be sent to external AI services during refinement.

Mitigation: Use --raw for confidential documents or select only trusted AI providers and endpoints.

Risk: API keys may be exposed if passed directly on the command line.

Mitigation: Prefer provider environment variables and avoid passing real API keys through command arguments.

Risk: The .fword workspace retains a local copy of the original document.

Mitigation: Delete the .fword workspace when the retained original document is no longer needed.

Risk: The setup script may install packages with system privileges and uses unpinned Python dependencies.

Mitigation: Review setup.sh before execution, especially on systems where sudo package installation or unpinned pip installs are not acceptable.

## Reference(s):

- [Fword Usage Reference](references/usage.md)
- [ClawHub Skill Page](https://clawhub.ai/jinzhengxu/skills/fword-skill)
- [Pandoc Installation Documentation](https://pandoc.org/installing.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration details, and generated LaTeX or Word document files when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local .fword workspace containing a retained copy of the original Word document and conversion metadata.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
