## Description:

Helps agents research current US law for legality, permits, zoning, licensing, compliance, and filing requirements by using Corpus live law search instead of training data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teakesdev](https://clawhub.ai/user/teakesdev)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to answer US legal research questions with current Corpus search results, verbatim citations, jurisdiction context, and full provision checks before relying on a result.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Legal research queries are sent to Corpus through a remote service.

Mitigation: Confirm the user is comfortable sending legal research queries to Corpus before installation or use.

Risk: Users may overread cited research as legal advice or ask the agent to file, pay, submit forms, or collect Social Security Numbers.

Mitigation: Keep use limited to cited research support; do not file, pay, submit anything, collect SSNs, or present the output as legal advice.

Risk: The optional Hermes plugin installation path may change behavior if installed from an unreviewed moving revision.

Mitigation: Prefer a pinned or reviewed plugin revision when using the optional Hermes plugin route.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/teakesdev/skills/corpus-legal-research)
- [Corpus Agent Guide](https://corpuslaw.us/agents)
- [Corpus MCP Protocol Reference](https://corpuslaw.us/docs/mcp)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with citations, jurisdiction labels, and inline shell commands for connector setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to the Corpus MCP server; no API key is required for initial use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
