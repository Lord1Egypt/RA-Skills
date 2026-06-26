## Description: <br>
Baidu Skill Guard checks skill install, download, scan, and audit requests against Baidu's skill security service before an agent proceeds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jenics](https://clawhub.ai/user/jenics) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to evaluate skill install, download, scan, and audit requests before proceeding. It is intended for workflows that want Baidu's security service involved in skill acquisition or review decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can share skill slugs, versions, inventory counts, and content fingerprints with Baidu's security service during checks. <br>
Mitigation: Use it only where that sharing is acceptable, and avoid directory or batch scans on private or unreleased skill folders. <br>
Risk: The skill changes install and download workflows by requiring a security check before proceeding. <br>
Mitigation: Keep human approval and retry paths available when the service returns non-safe results or cannot complete a check. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jenics/baidu-skill-guard) <br>
- [Baidu skill security service](https://skill-sec.baidu.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON report fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Directs agents to display the security service's report text verbatim and choose next actions from structured result fields.] <br>

## Skill Version(s): <br>
1.0.9 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
