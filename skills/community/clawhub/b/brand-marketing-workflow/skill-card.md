## Description:

Plans brand marketing workflows by normalizing brand inputs, drafting channel content, analyzing public competitor signals, scoring performance, and preparing iteration guidance with human approval gates for sensitive actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halfmoon82](https://clawhub.ai/user/halfmoon82)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators, brand teams, and developers use this skill to turn brand inputs into briefs, content plans, competitor summaries, performance reviews, and iteration notes for public or authorized-only marketing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package is presented as documentation-only while server security evidence reports runnable workflow code.

Mitigation: Review it as operational code before installation and run it only in an environment intended for marketing workflow execution.

Risk: The workflow can read local OpenClaw configuration and use configured LLM and search services.

Mitigation: Use least-privilege configuration values and confirm that outbound LLM and search services are approved for the brand data being processed.

Risk: Brand briefs or strategy data may be sent externally before the current authorization check runs.

Mitigation: Avoid sensitive brand inputs unless external processing is approved, and review outbound service settings before use.

Risk: Competitor content may be cached during workflow runs.

Mitigation: Treat cached competitor data as retained marketing intelligence and clear caches when persistence is not acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/halfmoon82/skills/brand-marketing-workflow)
- [Structural Reference](artifact/SKILL.md)
- [Workflow Optimization Notes](artifact/autoresearch.md)
- [Integration Test Result](artifact/evidence/integration_test_result.txt)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [JSON workflow result plus Markdown-ready planning artifacts and approval prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit human-assist requests for login, captcha, publishing, payment, or authorization boundaries.]

## Skill Version(s):

3.0.1 (source: server release metadata and clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
