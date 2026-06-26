## Description: <br>
Audit-first frontend-backend contract analyzer for static API compatibility checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlawnsdk](https://clawhub.ai/user/dlawnsdk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to compare frontend API calls with backend endpoint contracts before release, refactors, or regression review. It produces prioritized contract-audit findings for missing endpoints, method or path drift, and query, body, response, or auth mismatches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional live helper can use credentials and may delete API data even when generated as read-only. <br>
Mitigation: Use the static audit workflow as the default path. Run live helpers only against disposable dev or staging systems with non-production credentials, inspect generated files before execution, and do not rely on --read-only as a strict safety boundary. <br>
Risk: Static extraction is pattern-dependent and may miss API behavior hidden behind dynamic URL construction, generated clients, or unsupported framework conventions. <br>
Mitigation: Treat findings as engineering review inputs, verify high-risk paths against source code and existing QA tests, and rerun the audit after fixes. <br>


## Reference(s): <br>
- [Audit Scope](references/AUDIT-SCOPE.md) <br>
- [Audit Examples](references/EXAMPLES.md) <br>
- [Limitations](references/LIMITATIONS.md) <br>
- [Live Mode](references/LIVE-MODE.md) <br>
- [MVP Spec](references/MVP-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown and JSON audit reports with shell command guidance and optional generated helper code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The primary audit writes audit-report.md and audit-report.json to a user-selected output directory; optional live helper generation is secondary and should be reviewed before execution.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
