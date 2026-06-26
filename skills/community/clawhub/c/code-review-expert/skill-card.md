## Description: <br>
Multi-agent code review system using Manager-Worker pattern. Provides comprehensive code analysis from syntax, logic, security, and performance perspectives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[banxian87](https://clawhub.ai/user/banxian87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to run multi-perspective LLM-assisted code reviews covering syntax and style, logic defects, security issues, and performance concerns before merging or deploying code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted code and review artifacts may be processed through configured LLM steps without a clear data-handling notice. <br>
Mitigation: Use only on repositories whose data may be shared with the configured LLM provider, and avoid secrets, regulated data, or proprietary code unless provider, retention, redaction, and local-model options have been confirmed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Structured Markdown report and ReviewReport object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include severity ratings, line-level findings, an overall score, recommendations, and code examples for fixes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
