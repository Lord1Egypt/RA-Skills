## Description:

Arena Council runs multiple local LLMs in parallel and combines their responses with voting or consensus strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nerua1](https://clawhub.ai/user/nerua1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Arena Council to send prompts to multiple local LM Studio LLMs, collect responses in parallel, and return a majority or weighted consensus answer for analysis, coding, and Q&A workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may rewrite prompts to bypass model refusals and can interact with a sibling god-mode module.

Mitigation: Install only when that behavior is intended; review the sibling god-mode directory and remove or disable prompt rewriting before sensitive or policy-bound use.

Risk: Prompts can be sent to multiple locally loaded LM Studio models, increasing exposure of sensitive inputs within the local model environment.

Mitigation: Avoid sensitive prompts, or explicitly select and audit trusted local models before using the council.

Risk: The installation guidance does not pin dependencies.

Mitigation: Install in a controlled environment and pin reviewed dependency versions before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [String or Markdown, depending on the prompt and selected local models.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a single consensus response; raw per-model responses are available through the Python API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
