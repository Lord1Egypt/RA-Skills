## Description: <br>
Adversarial pre-build architecture review where a structurally independent agent reviews proposed builds before any code is written and returns APPROVE, REVISE, or REJECT with specific itemized findings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jfulmines-star](https://clawhub.ai/user/jfulmines-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill as a pre-build gate for new features, endpoints, schema changes, payment or auth work, external integrations, and other architecture decisions that need adversarial review before implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task briefs, repository metadata, and architecture details are sent to Anthropic using the user's API key. <br>
Mitigation: Review briefs and repository metadata before running; omit secrets, customer data, sensitive incident details, and confidential content that is not needed for the review. <br>
Risk: Provider usage is billed to the user's Anthropic account. <br>
Mitigation: Run the critic only for qualifying architecture changes and keep account billing limits aligned with expected usage. <br>
Risk: Saved verdict files may contain confidential architecture or security findings. <br>
Mitigation: Store verdicts in an appropriate local workspace and periodically remove or restrict access to sensitive verdict files. <br>


## Reference(s): <br>
- [Architecture Critic README](README.md) <br>
- [Security & Privacy](SECURITY.md) <br>
- [Web / API Architecture Critic Checklist](references/checklist-web.md) <br>
- [General Architecture Critic Checklist](references/checklist-general.md) <br>
- [Security Checklist](references/security.md) <br>
- [Payment Flows Checklist](references/payment-flows.md) <br>
- [AI/LLM Builds Checklist](references/ai-builds.md) <br>
- [ClaWHub Skill Page](https://clawhub.ai/jfulmines-star/architecture-critic) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown verdict file with command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns APPROVE, REVISE, REJECT, or ERROR and writes a local verdict file under specialists/critic-verdicts.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence; artifact frontmatter and clawhub.yaml list 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
