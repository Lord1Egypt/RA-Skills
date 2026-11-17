## Description:

Chief is an HR organizational diagnosis skill that uses a seven-step method, Socratic audit, and iceberg model to turn ambiguous team, culture, compensation, attrition, and talent questions into structured diagnostic reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

HR leaders, HRBPs, and organizational consultants use Chief to analyze complex people and organization issues such as team dysfunction, attrition, culture adoption, change readiness, talent review, and compensation benchmarking. The skill produces prioritized recommendations with confidence checks, adversarial review, and citation validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may store sensitive HR case, compensation, investigation, or legal-risk details in local knowledge-base files.

Mitigation: Use a dedicated knowledge-base path, redact personal or confidential data before analysis, and require explicit approval before writing case or taxonomy records.

Risk: External search or imported skill use may expose sensitive organizational context or return unsupported guidance.

Mitigation: Disable or gate external searches for confidential matters and review all retrieved evidence before using it in employee-facing or legal-risk decisions.

Risk: The initializer supports overwrite behavior that can replace existing knowledge-base files.

Mitigation: Avoid the overwrite option unless replacement is intended, and back up the knowledge base before initialization or migration.

Risk: Citation validation is part of the workflow but was called out for review in the security guidance.

Mitigation: Review or fix the citation checker before relying on it for policy, legal, compensation, or investigation reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tuobadaidai/skills/chief)
- [Publisher profile](https://clawhub.ai/user/tuobadaidai)
- [Step 1 Define](references/step-1-define.md)
- [Step 2 Decompose](references/step-2-decompose.md)
- [Step 3 Prioritize](references/step-3-prioritize.md)
- [Step 4 Plan](references/step-4-plan.md)
- [Step 5 Analyze](references/step-5-analyze.md)
- [Step 6 Synthesize](references/step-6-synthesize.md)
- [Step 7 Communicate](references/step-7-communicate.md)
- [Evaluator Specification](references/evaluator-spec.md)
- [XML Scaffold Specification](references/xml-scaffold-spec.md)
- [State Pruning Specification](references/state-pruning-spec.md)
- [Multi-Agent Aggregation](references/multi-agent-aggregation.md)
- [Enhanced Frameworks](references/enhanced-frameworks.md)
- [V6 Architecture Validation](references/v6-architecture-validation.md)
- [Few-Shot Examples](references/few-shot-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown diagnostic reports, structured XML state, JSONL case records, and optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initialize local HR knowledge-base files and validate report citations against a configured knowledge-base path.]

## Skill Version(s):

5.0.1 (source: ClawHub release evidence; bundled frontmatter reports 5.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
