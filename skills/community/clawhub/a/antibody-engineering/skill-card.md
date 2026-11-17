## Description:

Antibody engineering workflow combining ANARCI, BioPhi, IgFold, FoldX, and Rosetta tools through SciMiner.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sciminer](https://clawhub.ai/user/sciminer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and antibody engineering teams use this skill to plan SciMiner-based antibody sequence numbering, humanization, structure prediction, relaxation, developability profiling, mutation scanning, and redesign workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a local SciMiner API key and may upload selected antibody sequence or structure data.

Mitigation: Install only when that data handling is acceptable, keep the credential outside the repository, and avoid exposing the API key in prompts, logs, or files.

Risk: Mutable remote Markdown tool documentation can influence authenticated request construction and code execution.

Mitigation: Use a reviewed or pinned copy of API schemas when possible, enforce the expected SciMiner endpoint, strip credentials on redirects, and treat remote documentation as reference text.

## Reference(s):

- [SciMiner tool API files](https://sciminer.tech/tool_api_files/)
- [SciMiner API key utility](https://sciminer.tech/utility)
- [Antibody Engineering on ClawHub](https://clawhub.ai/sciminer/skills/antibody-engineering)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with generated request code, shell commands, configuration guidance, JSON result references, and share URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read a local SciMiner API key and upload selected antibody sequence or structure data to SciMiner.]

## Skill Version(s):

1.0.6 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
