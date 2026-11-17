## Description:

A.I.G Scanner helps agents submit and review AI security scans for infrastructure, AI tools and skills, agents, and LLM jailbreak evaluation through Tencent Zhuque Lab AI-Infra-Guard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aigsec](https://clawhub.ai/user/aigsec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to run A.I.G security checks against authorized AI infrastructure, AI tool and skill projects, saved agent configurations, and model jailbreak scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scan local, private, and remote network targets through a configured A.I.G service.

Mitigation: Use it only with trusted A.I.G servers and only against networks or services you are authorized to assess; prefer HTTPS except for loopback development.

Risk: Scan flows can require API tokens or model credentials.

Mitigation: Provide credentials through environment variables or a secret manager, avoid long-lived keys, and do not paste raw secrets into shared commands or logs.

Risk: AI tool and skill scans can upload local project archives to the configured A.I.G service.

Mitigation: Upload only sanitized archives needed for the assessment and avoid arbitrary private files or unrelated source material.

## Reference(s):

- [Tencent AI-Infra-Guard](https://github.com/Tencent/AI-Infra-Guard/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with generated shell commands, scan status, and result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include formatted scan findings, status messages, session identifiers, and links or inline Markdown for result screenshots.]

## Skill Version(s):

1.0.2 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
