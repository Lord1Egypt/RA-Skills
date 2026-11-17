## Description:

Analyzes paid-ad frequency, CTR, CVR, and reach trends against an early-flight baseline to diagnose creative fatigue or audience saturation and return Rotate-creative, Widen-audience, or Hold triggers per ad set.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators and paid-growth teams use this skill to decide whether scaled ad sets need creative rotation, audience expansion, or a hold based on frequency, CTR, CVR, reach, and baseline trend data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe ledger command examples can mishandle untrusted ad-set names.

Mitigation: Run ledger commands with structured arguments or properly quoted values; treat campaign names, ad-set names, CSV rows, and ad labels as data rather than executable instructions.

Risk: Campaign performance exports and saved summaries may retain sensitive account data.

Mitigation: Save outputs only when the user intends to keep campaign performance data in memory, and store only the minimum summary needed for follow-up decisions.

Risk: Single-day snapshots or learning-phase data can produce misleading fatigue recommendations.

Mitigation: Require a daily or weekly time series and a stable post-learning baseline before issuing Rotate-creative or Widen-audience guidance.

## Reference(s):

- [Fatigue Frequency Manager on ClawHub](https://clawhub.ai/aaron-he-zhu/skills/fatigue-frequency-manager)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown fatigue read with per-ad-set diagnosis, trigger, caveats, handoff summary, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should label figures as Measured, User-provided, or Estimated and avoid saving campaign performance data unless the user asks.]

## Skill Version(s):

19.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
