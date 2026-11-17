## Description:

Generates competitor patent analysis reports from PatSnap professional search queries against patent and literature data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, patent analysts, and competitive-intelligence teams use this skill to run PatSnap search expressions, retrieve patent and literature results, and produce competitor patent reports for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API keys through local configuration files.

Mitigation: Use a dedicated low-privilege PatSnap API key and avoid sharing credentials with other skills.

Risk: The server security summary flags review-worthy risk in credential flow, dependency installation, title sanitization, endpoint allowlisting, and HTML escaping.

Mitigation: Review and preferably fix those areas before installation or deployment.

Risk: Generated HTML reports may include untrusted report content.

Mitigation: Treat generated HTML reports as untrusted until escaping is confirmed or corrected.

Risk: Configurable service endpoints can affect where requests are sent.

Mitigation: Allowlist expected PatSnap endpoints before use in shared or production environments.

## Reference(s):

- [Artifact skill definition](artifact/SKILL.md)
- [Sample patent report](artifact/reports/report_20260416_152606.md)
- [PatSnap Open Platform](https://open.zhihuiya.com/)
- [PatSnap Connect API base](https://connect.zhihuiya.com)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration]

**Output Format:** [Markdown report text saved to files, with a partial report returned in conversation and optional HTML report generation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided PatSnap API key; optional literature and ARK keys affect literature retrieval and summarization.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
