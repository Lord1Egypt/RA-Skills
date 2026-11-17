## Description:

AI agent cybersecurity skill implementing MITRE ATLAS, OWASP Top 10 for LLM and Agentic Applications, CSA MAESTRO, NIST AI RMF, and Gray Swan frameworks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crevita](https://clawhub.ai/user/crevita)

### License/Terms of Use:

MIT-0

## Use Case:

Security teams, CISO agents, and developers use this skill to run structured AI-agent patrols, vulnerability assessments, posture scoring, and patch recommendations across MITRE ATLAS, OWASP, CSA MAESTRO, NIST AI RMF, and Gray Swan guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unscoped quarantine instructions could cause an autonomous agent to isolate systems without defined approval, scope, or rollback controls.

Mitigation: Require explicit human approval before quarantine, define affected systems and authority, and document rollback steps before deployment.

Risk: An unpinned npx install path can introduce supply-chain uncertainty if the package source and version are not verified.

Mitigation: Prefer the ClawHub or manual installation path, or pin and verify the package source and version before use.

## Reference(s):

- [CISO Agent Security on ClawHub](https://clawhub.ai/crevita/skills/ciso-agent-security)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)
- [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [CSA MAESTRO](https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro)
- [NIST AI Risk Management Framework](https://www.nist.gov/artificial-intelligence/executive-order-safe-secure-and-trustworthy-artificial-intelligence)
- [Gray Swan AI Research](https://grayswan.ai/research)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown or plain text reports with framework mappings, posture scores, and patch recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PASS/WARNING/FAIL scores, quarantine recommendations, and mitigation guidance.]

## Skill Version(s):

1.0.0 (source: release metadata, frontmatter, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
