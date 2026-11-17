## Description:

Iteratively densifies text summaries using the Chain-of-Density technique for compressing verbose documentation, condensing requirements, or creating executive summaries while preserving information density.

This skill is ready for commercial/non-commercial use.

## Publisher:

[killerapp](https://clawhub.ai/user/killerapp)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers, analysts, and other external users use this skill to turn verbose source text into denser summaries through iterative entity injection while tracking added entities and preserving a target word count.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The summarization workflow can change meaning if used where exact wording must be preserved.

Mitigation: Avoid using it for legal, compliance, specification, or other precision-critical text; review the final summary against the source before use.

Risk: Source text may be sent through a serial subagent process during summarization.

Mitigation: Do not provide sensitive or restricted text unless the agent environment and subagent handling are approved for that data.

## Reference(s):

- [From Sparse to Dense: GPT-4 Summarization with Chain of Density Prompting](https://arxiv.org/abs/2309.04269)
- [HuggingFace griffin/chain_of_density dataset](https://huggingface.co/datasets/griffin/chain_of_density)
- [Chain of Density ClawHub page](https://clawhub.ai/killerapp/skills/chain-of-density)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain text or Markdown summary, with optional YAML history and inline shell commands for text metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final summaries are intended to preserve a target word count across iterative densification passes; the helper script can return word, character, byte, or JSON metrics.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
