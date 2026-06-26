## Description: <br>
Generates structured monthly internal-control compliance reports from complaint counts, risk events, supplier scores, exception handling data, and major incident notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nic-yuan](https://clawhub.ai/user/nic-yuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Internal-control and compliance teams use this skill to turn monthly operations metrics into a management-ready compliance report covering complaints, logistics exceptions, supplier risk, major events, and next-month priorities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monthly compliance reports may include sensitive case, supplier, legal, regulatory, or contact details. <br>
Mitigation: Use aggregated metrics where possible and redact unnecessary identifiers before sharing or storing the generated report. <br>
Risk: The skill's Alibaba-style role language could be mistaken for official Alibaba approval. <br>
Mitigation: Treat the output as a drafting template and verify branding, authorization, conclusions, and recommendations with an authorized reviewer. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nic-yuan/05-monthly-report) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only; uses user-provided monthly metrics and does not access systems or execute code.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 1.7.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
