## Description:

Consults multiple configured language models in parallel for complex questions and returns a structured Markdown report with consensus, differences, conflicts, and actionable synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pongpong990909-prog](https://clawhub.ai/user/pongpong990909-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent users use Ask-More to consult multiple configured language models on complex questions, compare their answers, and receive a structured synthesis of consensus, differences, conflicts, and next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Packed questions, and recent conversation context in full mode, may be sent to configured external model providers.

Mitigation: Review the packed question before sending, avoid highly sensitive information, and use the first-use privacy notice to confirm provider data-sharing expectations.

Risk: The security summary flags an exploitable config-validation helper on untrusted or unusual skill paths.

Mitigation: Review before installing and avoid running scripts/load-config.sh on untrusted or unusual skill paths until the path interpolation issue is fixed.

Risk: Multi-model consensus can still be incorrect or reflect shared model bias.

Mitigation: Treat consensus as advisory, review conflicts manually, and require human judgment for high-stakes decisions.

## Reference(s):

- [Prompt Templates](artifact/references/prompt-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/pongpong990909-prog/skills/ask-more)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown consultation report with optional raw comparison sections, progress messages, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include consensus, unique insights, conflicts, uncertainty labels, participating model status, and optional run logs when logging is enabled.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
