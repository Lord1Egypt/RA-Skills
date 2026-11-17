## Description:

Ai Poison Guard is a local heuristic text scanner that flags GEO-style AI-poisoning patterns, assigns risk scores, and produces filtering guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[testmtcode](https://clawhub.ai/user/testmtcode)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to screen suspicious text or files for common AI-poisoning persuasion patterns and receive a risk score, findings, and practical review guidance. Treat the output as heuristic triage rather than proof that a source or website is trustworthy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation overstates source or website verification capabilities.

Mitigation: Use the skill as a local heuristic text scanner and confirm source trust with independent authoritative checks.

Risk: Risk scores may produce false positives or false negatives because detection is based on fixed text patterns.

Mitigation: Review matched phrases and compare claims against multiple reliable sources before acting on the score.

Risk: The documentation recommends dependency installation that may be unnecessary or unpinned for the current local scanner behavior.

Mitigation: Install only reviewed, pinned dependencies that are actually required in the deployment environment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/testmtcode/skills/ai-poison-guard)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Plain text or Markdown-style reports, with optional JSON output from guard.py --json and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local heuristic pattern matching; no API keys, MCP tools, or external service calls were detected.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
