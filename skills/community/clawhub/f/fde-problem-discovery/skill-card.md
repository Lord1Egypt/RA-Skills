## Description:

Stage 1 of FDE Delivery Loop: turns customer interviews, frontline observations, tickets, meeting notes, and business data into an evidence-backed customer problem-discovery package for uncovering needs, reconstructing workflows, designing interview guides, validating problems, and screening POC candidates without committing to a solution, PRD, or prototype.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xukun0821](https://clawhub.ai/user/xukun0821)

### License/Terms of Use:

MIT-0

## Use Case:

External teams, field engineers, product leads, and customer-facing delivery teams use this skill to turn raw customer evidence into a bounded problem-discovery package, interview guide, or POC readiness screen. It is suited for discovery before delivery scope is committed, especially when the team needs to separate facts, hypotheses, workflow pain, constraints, and next-decision criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended for discovery documents and interview guides, not PRDs, implementation plans, or delivery commitments.

Mitigation: Review outputs for accidental solution commitments and route scope, schedule, pricing, and technical decisions to downstream engagement-charter or delivery workflows.

Risk: Discovery outputs can overstate customer needs if sales narratives, opinions, or generated interview prompts are treated as facts.

Mitigation: Require behavioral, observational, ticket, log, sample, or owner-confirmed evidence before recommending a POC decision.

Risk: The local interview-guide helper writes to a user-provided output path.

Mitigation: Choose the output path deliberately and review generated Markdown before sharing or using it as project evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xukun0821/skills/fde-problem-discovery)
- [Problem discovery pack](references/problem-discovery-pack.md)
- [Discovery rules](references/discovery-rules.md)
- [Discovery input guide](references/discovery-input-guide.md)
- [Discovery quality rubric](references/discovery-quality-rubric.md)
- [Discovery field handbook](references/discovery-field-handbook.md)
- [Industry discovery overlays](references/industry-discovery-overlays.md)
- [User research](references/user-research.md)
- [Requirement analysis](references/requirement-analysis.md)
- [Discovery worked example](references/discovery-worked-example.md)
- [Public method sources](references/public-sources.md)
- [GOV.UK: How the discovery phase works](https://www.gov.uk/service-manual/agile-delivery/how-the-discovery-phase-works)
- [GOV.UK: User research in the discovery phase](https://www.gov.uk/service-manual/user-research/user-research-in-discovery)
- [Atlassian Project Poster](https://www.atlassian.com/team-playbook/plays/project-poster)
- [OpenAI: Practical Guide to Building Agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown discovery packages, interview guides, readiness screens, evidence logs, and optional shell commands for local guide generation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script reads a project JSON file and writes a Markdown interview guide to the output path selected by the user.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and TRUST-CARD.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
