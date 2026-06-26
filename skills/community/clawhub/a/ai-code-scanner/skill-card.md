## Description: <br>
ai-code-scanner helps agents review code by combining an external API scan for security and quality patterns with deeper AI analysis and a Markdown review report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lm203688](https://clawhub.ai/user/lm203688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill during code review, security audits, PR checks, and code quality assessments for Python, JavaScript, TypeScript, Go, Java, and Rust. It is most appropriate when the reviewed source code and filenames may be sent to the external review service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reviewed source code and filenames can be uploaded to an external API without a clear consent step. <br>
Mitigation: Use only when the service operator, retention policy, and consent controls are acceptable; avoid private repositories, customer data, regulated code, and files that may contain secrets. <br>
Risk: API scan findings may be incomplete or may miss context-specific security and quality issues. <br>
Mitigation: Treat API results as a first-pass review and require human review before accepting, rejecting, or merging code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lm203688/ai-code-scanner) <br>
- [External code review API endpoint](https://1341839497-kvq7g9wk8p.ap-guangzhou.tencentscf.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review report with CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include score, approval status, issue counts, severity buckets, and prioritized recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
