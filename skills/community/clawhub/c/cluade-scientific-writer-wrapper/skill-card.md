## Description:

AI-powered scientific writing tool. Generate publication-ready papers, grant proposals, posters, and more with real-time research and verified citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josephyb97](https://clawhub.ai/user/josephyb97)

### License/Terms of Use:


## Use Case:

External users, developers, and research teams use this skill to generate scientific manuscripts, grant proposals, posters, literature reviews, and clinical reports from prompts and optional data files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install mutable external Python code.

Mitigation: Install in an isolated virtual environment, pin and verify the package where possible, and review the package before production use.

Risk: The skill requires API credentials and may encourage storing them in environment files.

Mitigation: Use a keychain or securely permissioned environment variables, avoid production credentials, and keep any .env file out of version control.

Risk: Prompts and selected data files may be sent to Anthropic, OpenRouter, or other research services.

Mitigation: Do not use sensitive clinical, proprietary, or unpublished data unless those providers are approved for that data.

Risk: Generated scientific content, citations, and clinical-style reports may be incomplete or misleading.

Mitigation: Have qualified reviewers verify claims, citations, and domain-specific conclusions before publication or operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/josephyb97/skills/cluade-scientific-writer-wrapper)
- [Package source link from artifact metadata](https://github.com/K-Dense-AI/claude-scientific-writer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code examples, plus generated scientific writing files from the installed package]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill describes outputs saved under writing_outputs/ and may produce papers, proposals, posters, literature reviews, and clinical reports.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
