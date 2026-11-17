## Description:

Polish AI-written replies, emails, articles, and documentation for smoother flow and better human readability while preserving meaning and factual accuracy; when requested, test revisions with GPTZero or another detector and work toward lower AI-detection scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dexhunter](https://clawhub.ai/user/dexhunter)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to revise AI-assisted prose for clarity, tone, factual preservation, and publication readiness. When explicitly requested, it can measure detector-score changes while reporting limitations and avoiding claims that a score proves human authorship.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may overstate detector-score changes as proof of human authorship or permission to publish.

Mitigation: Report detector scores as limited measurements, follow destination-site rules and disclosure requirements, and review public posts before authorizing them.

Risk: Optimizing for a lower detector score can degrade factual accuracy, technical correctness, or readability.

Mitigation: Preserve a claim inventory, review correctness before interpreting scores, and reject lower-scoring text when it introduces errors or removes needed qualifications.

Risk: Detector measurements can be stale, incomparable, or unauthenticated.

Mitigation: Use fresh completed scans with the same service, mode, and displayed model; keep exact inputs and receipt records; state that local receipts do not authenticate the detector service.

## Reference(s):

- [Evidence Limits](references/evidence.md)
- [Optional Detector Measurement](references/measurement.md)
- [Strict Receipt Format](references/receipt-format.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown or plain text with optional local receipt-check commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include claim inventories, reviewer notes, detector-score observations, warnings, and receipt-validation results when requested.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
