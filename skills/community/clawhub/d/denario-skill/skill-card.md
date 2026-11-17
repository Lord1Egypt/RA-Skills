## Description:

Automates scientific research workflows by generating ideas, methodology, results, papers, and citations using the Denario framework with Z.ai-compatible model access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jmanhype](https://clawhub.ai/user/jmanhype)

### License/Terms of Use:

ISC

## Use Case:

Researchers, developers, and research automation teams use this skill to run staged scientific research workflows, including idea generation, methodology drafting, results generation, paper compilation, and citation management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The citations workflow embeds an undisclosed third-party API key.

Mitigation: Do not run the citations path until the publisher removes and rotates the embedded key.

Risk: First run installs unpinned packages into a persistent user environment.

Mitigation: Run in a sandboxed environment and review or pin dependencies before operational use.

Risk: Research prompts, generated project content, and citation queries may be sent to external model or citation providers.

Mitigation: Use only approved API keys and avoid submitting sensitive or confidential research content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jmanhype/skills/denario-skill)
- [Publisher profile](https://clawhub.ai/user/jmanhype)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Files, Guidance]

**Output Format:** [Console output, generated research prose, Markdown-like reports, LaTeX paper files, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates a local Denario project directory and can emit paper artifacts when the paper workflow is run.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
