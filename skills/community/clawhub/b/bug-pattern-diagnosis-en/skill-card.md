## Description:

Diagnoses intermittent or environment-specific bugs by comparing reported symptoms with curated past cases, while requiring independent project-specific verification before recommending fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgvgfgvh](https://clawhub.ai/user/hgvgfgvh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to triage intermittent, environment-specific, or log-inconsistent bugs by structuring symptoms, consulting prior case notes as hypotheses, and planning verification steps before code changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic examples may lead agents to test live systems or expose sensitive tokens and logs.

Mitigation: Use non-production or low-risk requests where possible, redact real tokens and sensitive logs, and confirm potentially impactful commands before execution.

Risk: Past case notes can bias diagnosis toward a similar-looking root cause.

Mitigation: Treat case files only as hypotheses and require current-project verification before recommending code changes.

Risk: Optional case accumulation could persist sensitive incident details.

Mitigation: Ask before saving new BUGxx notes and remove secrets, customer data, and unnecessary production details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hgvgfgvh/skills/bug-pattern-diagnosis-en)
- [BUG01 case library entry](artifact/experience/BUG01.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, code]

**Output Format:** [Markdown responses with structured symptom summaries, hypothesis checks, and optional shell command or code snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose creation of new BUGxx.md case notes only after user consent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
