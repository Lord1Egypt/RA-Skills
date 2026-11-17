## Description:

Multi-perspective academic manuscript review agent that configures role-separated reviewer personas, produces peer-review reports, and synthesizes editorial decisions, revision roadmaps, verification reviews, guided review, and calibration reports.

This skill is for research and development only.

## Publisher:

[sedey999](https://clawhub.ai/user/sedey999)

### License/Terms of Use:

CC BY-NC 4.0

## Use Case:

Researchers, authors, editors, and reviewers use this skill to simulate structured journal-style review, compare multiple reviewer perspectives, assess revisions, and produce actionable review and decision artifacts for academic manuscripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manuscripts and review materials may contain private or sensitive academic data.

Mitigation: Treat submitted materials as private, use restricted credentials, and avoid sharing manuscripts with external providers unless the user explicitly opts in.

Risk: Optional cross-model verification can send manuscript content to an external provider.

Mitigation: Leave cross-model verification off unless external-provider use is intended and approved for the specific manuscript.

Risk: API-key or request details may be exposed when shell commands place secrets in process arguments or logged URLs.

Mitigation: Use dedicated restricted API keys and avoid command patterns that expose credentials through process lists, logs, or URLs.

Risk: Role-separated reviewer personas can be mistaken for independent error processes.

Mitigation: Disclose actual execution provenance and describe the outputs as role-separated perspectives rather than independent reviews.

Risk: The skill may generate incorrect, unsupported, or fabricated academic claims if evidence discipline is not enforced.

Mitigation: Require source-backed findings, label unsupported speculation, and manually verify citations, computations, and editorial conclusions before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sedey999/skills/ars-academic-reviewer)
- [README](artifact/README.md)
- [Attribution](artifact/ATTRIBUTION.md)
- [License](artifact/LICENSE)
- [Review criteria framework](artifact/references/guides/review_criteria_framework.md)
- [Editorial decision standards](artifact/references/guides/editorial_decision_standards.md)
- [Re-review mode protocol](artifact/references/guides/re_review_mode_protocol.md)
- [Review panel provenance protocol](artifact/references/guides/review_panel_provenance_protocol.md)
- [Peer review report template](artifact/references/templates/peer_review_report_template.md)
- [Editorial decision template](artifact/references/templates/editorial_decision_template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration, JSON]

**Output Format:** [Markdown reports and structured sidecar artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include role-specific review reports, editorial decision letters, revision roadmaps, verification matrices, calibration summaries, and reviewer configuration cards.]

## Skill Version(s):

1.11.2 (source: server release and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
