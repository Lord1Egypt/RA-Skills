## Description:

Computes suspect networks and crime probabilities using eigenforensic spectral analysis to support OSINT investigations and priority reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evezart](https://clawhub.ai/user/evezart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and investigators use this skill to run OSINT suspect-network analysis, generate JSON or Markdown reports, and review inferred crime-probability patterns. Outputs require lawful use, consent where applicable, and independent human review before any consequential action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run unaudited local Python code.

Mitigation: Independently verify the external evez-osint-engine code before installation or execution, and run it only in a controlled environment.

Risk: The skill can produce high-impact crime-probability reports about named suspects.

Mitigation: Use outputs only in lawful, consented, human-reviewed contexts and never as the sole basis for accusations, prioritization, employment, legal, policing, or other consequential decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/evezart/skills/evez-osint-skill)
- [Publisher Profile](https://clawhub.ai/user/evezart)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python code blocks; downstream reports may be JSON or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report outputs concern suspect-network analysis and should be treated as speculative until independently reviewed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
