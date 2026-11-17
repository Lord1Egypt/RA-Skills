## Description:

Checks Audible promotions against Goodreads ratings and optional reading history and taste notes to recommend relevant audiobook deals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lenpr](https://clawhub.ai/user/lenpr)

### License/Terms of Use:

MIT

## Use Case:

Readers and OpenClaw users check Audible daily promotions or scan their Goodreads Want-to-Read shelf for discounts, with optional personalized recommendations and configured delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal Goodreads exports and reading notes may be used in recommendation writing.

Mitigation: Provide only files you intend to share; select privacyMode "minimal" to exclude personal reading data from model-facing fit writing.

Risk: Optional Audible authentication stores sensitive account tokens locally.

Mitigation: Keep the auth file private, and never paste or publish its contents.

Risk: Optional scheduled runs and message delivery can send recommendations without a manual check each time.

Mitigation: Enable automation or external delivery only on a trusted OpenClaw host with delivery targets you control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lenpr/skills/audible-goodreads-deal-scout)
- [Project homepage (release metadata)](https://github.com/lenpr/audible-goodreads-deal-scout)
- [Trust and data access](artifact/TRUST.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Recommendation cards and optional Markdown discount reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional configured delivery; Want-to-Read discount scans support Audible US only; no purchases.]

## Skill Version(s):

0.1.19 (source: ClawHub release metadata and CHANGELOG, 2026-10-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
