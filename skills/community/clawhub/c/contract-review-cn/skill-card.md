## Description:

Reviews Chinese contracts by extracting text from PDF, Word, or TXT files, identifying legal risks, proposing revisions, and producing a Markdown comparison report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingmoon96-dev](https://clawhub.ai/user/lingmoon96-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users, legal reviewers, and business teams use this skill to perform an initial Chinese-language contract risk review and prepare draft revision guidance for contracts they are authorized to process.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential contract text may be sent to the configured AI provider.

Mitigation: Use only contracts approved for provider processing, redact sensitive terms before review, and avoid broad auto-trigger use for confidential documents.

Risk: AI-generated contract analysis may be incomplete or legally unreliable.

Mitigation: Have a qualified human review the output before relying on it for legal or commercial decisions.

Risk: Untrusted configuration files may change provider, model, or credential behavior.

Mitigation: Use trusted configuration files and keep API keys in protected local configuration rather than shared artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lingmoon96-dev/skills/contract-review-cn)
- [Artifact README](artifact/README.md)
- [Artifact QUICKSTART](artifact/QUICKSTART.md)
- [Artifact SKILL](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown report with a risk summary, revision suggestions, and an original/proposed/reason comparison table.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save a *_review.md file or print the report with --show-only; default generation cap is 4096 tokens.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
