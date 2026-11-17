## Description:

Enterprise AI Agent Security Scanner detects prompt injection, credential theft, data exfiltration, supply-chain abuse, and attack-chain indicators using rule-based and optional LLM-assisted analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caidongyun](https://clawhub.ai/user/caidongyun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to scan AI agent skill packages and source trees before release or deployment. It helps triage risky patterns such as prompt injection, credential theft, data exfiltration, suspicious curl usage, and attack-chain behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanner results are heuristic and can understate risk, especially when context-based downgrades are applied.

Mitigation: Use results as triage input, manually review important findings, include SKILL.md and other instruction files in scan scope, and avoid relying only on downgraded classifications.

Risk: Optional LLM analysis may disclose scanned source snippets to a third-party model endpoint.

Mitigation: Keep LLM analysis disabled for private code unless third-party disclosure is acceptable, or route analysis through an approved model path.

Risk: File-count limits, timeouts, or circuit-breaker behavior can leave parts of large or complex skill packages insufficiently reviewed.

Mitigation: Review skipped and timed-out files separately and tune scan limits for high-value or unusually large reviews.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caidongyun/skills/agent-security-skill-scanner)
- [GitHub repository link declared in artifact](https://github.com/caidongyun/agent-security-skill-scanner)
- [Gitee repository link declared in artifact](https://gitee.com/caidongyun/agent-security-skill-scanner)
- [Gitee package repository link declared in artifact](https://gitee.com/caidongyun/agent-security-skill-scanner-master)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [CLI scan summaries in text form or JSON report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include detected findings, severity/risk tiers, scan scope, timeout information, optional LLM statistics, and output file path when JSON output is requested.]

## Skill Version(s):

6.2.0 (source: server release metadata, SKILL.md frontmatter, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
