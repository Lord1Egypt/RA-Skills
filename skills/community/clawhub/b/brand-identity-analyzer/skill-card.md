## Description:

Brand Identity Analyzer researches brands with Gemini and Google Search grounding to generate reusable structured JSON brand identity profiles for ad generation and creative workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pauldelavallaz](https://clawhub.ai/user/pauldelavallaz)

### License/Terms of Use:


## Use Case:

Developers and creative operators use this skill to create, refresh, and reuse structured brand profiles for Ad-Ready, Morpheus, and other creative workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to commit and push generated brand profiles to GitHub without a clear confirmation step.

Mitigation: Use local output unless publishing is explicitly intended, confirm the target remote before pushing, and inspect generated JSON before publication.

Risk: Brand analysis may involve sensitive brand material or credentials when run in an agent environment.

Mitigation: Prefer GEMINI_API_KEY over command-line API keys and review the skill before installing it in environments with Git credentials or sensitive brand assets.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [JSON brand profile files, stdout JSON, and Markdown command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Profiles may be written to a user-specified path or auto-saved to the Ad-Ready brand catalog.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
