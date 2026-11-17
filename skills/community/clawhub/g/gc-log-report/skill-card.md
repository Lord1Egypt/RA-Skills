## Description:

Analyzes JDK GC logs and produces professional HTML reports and Markdown executive summaries with risk highlights, charts, and JVM tuning guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ranenwang](https://clawhub.ai/user/ranenwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, performance engineers, and JVM operators use this skill to turn one or more gc.log files into readable reports for incident review, leadership updates, and architecture tuning decisions. It is especially suited for identifying Full GC, frequent Young GC, long pauses, old-generation pressure, incomplete rolling-log windows, and practical JVM or application-side follow-up actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad GC, JVM tuning, or reporting prompts where the user expects a narrower answer or a different language.

Mitigation: Ask for the desired scope, language, and report format when the request is ambiguous.

Risk: Incomplete rolling GC log sets can make a partial time window look like a complete historical analysis.

Mitigation: State the analyzed files, covered time window, missing rolling logs, and conclusion boundaries in every report.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [HTML report and Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include embedded charts, risk labels, key metrics, tuning rationale, and explicit data-boundary notes when rolling GC logs are incomplete.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
