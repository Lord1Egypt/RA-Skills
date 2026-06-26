## Description: <br>
Chinese Compliance Checker helps agents assess global privacy, data transfer, app store, payment, content moderation, and AI Act readiness for Chinese products expanding overseas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lm203688](https://clawhub.ai/user/lm203688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, and compliance reviewers use this skill to triage overseas-launch requirements for Chinese apps, SaaS, e-commerce, content, AI, or payment products and to produce a compliance audit report with gaps and remediation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compliance findings may be incomplete, outdated, or mistaken legal guidance. <br>
Mitigation: Treat outputs as an initial checklist and verify current requirements with qualified counsel in each target market. <br>
Risk: Optional API and web app paths may send user-submitted product, compliance, or marketing details to an external Tencent-hosted service with limited data-handling disclosure. <br>
Mitigation: Do not submit confidential product plans, customer data, legal drafts, unpublished marketing copy, or sensitive data-flow details unless the service operator, privacy terms, retention, and jurisdictional handling have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lm203688/chinese-compliance-checker) <br>
- [Compliance regulations API endpoint](https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com) <br>
- [Compliance web app](https://1341839497-jv04655vcs.ap-shanghai.tencentscf.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown compliance audit report with tables, checklists, and a remediation roadmap; optional CLI output from regulations.sh.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Informational compliance support only; optional API and web app paths may send submitted content to an external service.] <br>

## Skill Version(s): <br>
2.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
