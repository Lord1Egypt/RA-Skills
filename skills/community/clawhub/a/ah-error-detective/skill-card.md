## Description:

Error Detective helps agents investigate software errors through root cause analysis, stack trace interpretation, error pattern recognition, memory leak analysis, and performance bottleneck identification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to investigate application errors, classify recurring patterns, analyze stack traces and system context, and produce evidence-based remediation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Debugging workflows can expose sensitive stack traces, source snippets, source maps, or host metadata.

Mitigation: Restrict file reads to the intended project directory and avoid sharing diagnostic data with third parties without consent.

Risk: The TypeScript example includes metrics endpoint behavior that could transmit diagnostic metadata.

Mitigation: Review any metrics endpoint before enabling telemetry and limit collected data to approved fields.

## Reference(s):

- [Error Detective Code Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/mtsatryan/skills/ah-error-detective)
- [Publisher Profile](https://clawhub.ai/user/mtsatryan)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown investigation reports with code examples, ranked fixes, evidence notes, and confidence scores]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic context, source snippets, stack traces, and remediation recommendations.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
