## Description:

LLM/Agent application testing toolkit covering L0-L4 checks, prompt security auditing, RAG evaluation, stress and regression testing, and LLM-as-judge review with runnable scripts and test cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shylamb-token](https://clawhub.ai/user/shylamb-token)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to evaluate LLM, agent, tool-calling, MCP, RAG, prompt-security, stress, and regression behavior before release or during CI quality gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Online test modes may send prompts, conversation content, or evaluation cases to configured LLM, RAG, or tool endpoints.

Mitigation: Use local or trusted endpoints, avoid production prompts and customer data, and redact sensitive fixtures before running online modes.

Risk: The MCP audit includes a default check against https://httpbin.org/get, which creates external network egress.

Mitigation: Remove, disable, or replace that endpoint when external egress is not intended.

Risk: The security evidence states that MCP compliance scoring is partial or simulated unless real protocol checks are added.

Mitigation: Treat MCP scores as advisory and add real protocol checks before using them as release gates.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shylamb-token/skills/ai-app-testing)
- [AI App Testing Skill Documentation](artifact/SKILL.md)
- [Pricing and License Notes](artifact/PRICING.md)
- [Bundled Test Summary](artifact/ai-app-test/reports/test_summary.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples plus JSON/YAML test artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces runnable Python testing workflows and reports; online modes require trusted endpoints.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
