## Description:

Generates bilingual dialectical business analysis by coordinating constructive, critical, and arbitrator perspectives to produce structured feasibility and recommendation reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philonis](https://clawhub.ai/user/philonis)

### License/Terms of Use:

MIT-0

## Use Case:

Business analysts, founders, strategy teams, and agents use this skill to stress-test a business topic through pro/con debate, optional knowledge enhancement, multi-dimensional scoring, and a synthesized recommendation report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External search can disclose business topics, constraints, or other sensitive planning context to search providers.

Mitigation: Disable search by default in confidential environments and require explicit user consent before sending analysis inputs to Tavily, Brave, or DuckDuckGo.

Risk: A crafted session ID can cause workspace files to be written outside the intended skill workspace.

Mitigation: Validate session IDs against a strict safe-character pattern and enforce that resolved output paths remain under the skill workspace.

Risk: The security verdict is suspicious for confidential business use.

Mitigation: Review and patch the search and session-path behaviors before installing the skill in business environments that handle non-public information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/philonis/skills/dialectical-analysis)
- [Publisher profile](https://clawhub.ai/user/philonis)

## Skill Output:

**Output Type(s):** [text, markdown, json, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and JSON debate state, with CLI commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Matches the user's input language and may include optional search-derived context when enabled.]

## Skill Version(s):

3.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
