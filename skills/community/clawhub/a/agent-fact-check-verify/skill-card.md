## Description: <br>
Agent Fact Check Verify helps AI agents extract verifiable claims, cross-check public sources, and return neutral fact-check conclusions without exposing internal scoring details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NHZallen](https://clawhub.ai/user/NHZallen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external-facing AI agents use this skill to verify user claims against public sources and compose neutral, integrated fact-check responses with related links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private messages, confidential drafts, secrets, or sensitive allegations may be exposed to external search or social-media providers during verification. <br>
Mitigation: Use this skill for public fact-checking workflows and avoid submitting private or confidential text unless external searches are acceptable. <br>
Risk: Optional X or Reddit CLI credentials and cookies could be mishandled in shared environments. <br>
Mitigation: Configure optional social-media credentials deliberately, use low-privilege accounts, store cookies with restricted permissions, and avoid committing them. <br>
Risk: Public-source verification can miss paywalled, private, closed-community, or newly changed information. <br>
Mitigation: Prioritize official and primary sources, cross-check independent sources, and keep the public-information limitation visible in final responses. <br>


## Reference(s): <br>
- [Agent Fact Check Verify on ClawHub](https://clawhub.ai/NHZallen/agent-fact-check-verify) <br>
- [Source Policy](references/source-policy.md) <br>
- [Internal Scoring Rubric](references/scoring-rubric.md) <br>
- [English README](docs/README.en.md) <br>
- [twitter-cli](https://github.com/jackwener/twitter-cli) <br>
- [rdt-cli](https://github.com/jackwener/rdt-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown responses with related links, plus JSON intermediate files and shell command examples for extract, score, and compose workflows.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Final responses use a fixed four-part structure and up to five related links; internal scores are not exposed.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
