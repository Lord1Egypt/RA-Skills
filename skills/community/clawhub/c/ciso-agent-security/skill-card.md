## Description: <br>
AI agent cybersecurity skill for autonomous agent systems that implements MITRE ATLAS, OWASP Top 10 for LLM and Agentic Applications, CSA MAESTRO, NIST AI RMF, and Gray Swan frameworks for red team patrols, posture scoring, quarantine workflows, and patch standards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crevita](https://clawhub.ai/user/crevita) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security engineers, CISO teams, and agent developers use this skill to guide AI agent red team patrols, vulnerability assessments, posture scoring, quarantine decisions, and patch recommendations against named AI security frameworks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: If the receiving agent has real quarantine or patch authority, following this skill could affect active agents or prompts. <br>
Mitigation: Keep quarantine and patch actions scoped, logged, reversible, and subject to human approval. <br>
Risk: Framework-based security guidance can become stale as MITRE, OWASP, CSA, NIST, and Gray Swan materials change. <br>
Mitigation: Review updates against the official framework URLs on a regular schedule before relying on assessment results. <br>


## Reference(s): <br>
- [CISO Agent Security on ClawHub](https://clawhub.ai/crevita/ciso-agent-security) <br>
- [MITRE ATLAS](https://atlas.mitre.org/) <br>
- [MITRE ATLAS Techniques Matrix](https://atlas.mitre.org/matrices/ATLAS) <br>
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) <br>
- [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/) <br>
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) <br>
- [CSA MAESTRO Framework](https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro) <br>
- [CSA MAESTRO GitHub](https://github.com/CloudSecurityAlliance/MAESTRO) <br>
- [NIST AI Risk Management Framework](https://www.nist.gov/artificial-intelligence/executive-order-safe-secure-and-trustworthy-artificial-intelligence) <br>
- [NIST AI RMF 1.0](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf) <br>
- [Gray Swan AI Research](https://grayswan.ai/research) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-style security assessment guidance, scoring notes, and patch recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include quarantine recommendations and patch proposals that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
