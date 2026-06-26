## Description: <br>
Cuihua Logger helps agents analyze JavaScript and TypeScript logging coverage and propose structured logging with levels, context, timing, and error details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[supermario11](https://clawhub.ai/user/supermario11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to check logging coverage, add structured logs to functions and API endpoints, and produce logging patterns for Winston, Pino, or Bunyan-style workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated logging examples may capture sensitive values such as passwords, tokens, session IDs, auth headers, request bodies, payment details, emails, IPs, or stack traces. <br>
Mitigation: Review generated logging before committing it, prefer allowlisted fields, and apply redaction middleware for secrets and personal data. <br>
Risk: The local CLI reads project source files to produce logging coverage reports. <br>
Mitigation: Run it only against intended project paths and review any generated report before sharing it outside the project. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/supermario11/cuihua-logger) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript code blocks and CLI output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node; analyzes JavaScript and TypeScript files for logging coverage.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
