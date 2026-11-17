## Description:

Daozheji Grill Skill helps an agent answer customer questions about Daozheji Grill locations, hours, dishes, prices, delivery, group-buying packages, membership benefits, parking, Wi-Fi, reservations, and food-safety topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liubuq-sys](https://clawhub.ai/user/liubuq-sys)

### License/Terms of Use:

MIT-0

## Use Case:

External customer-service agents use this skill to answer restaurant guest questions with a warm, conversational style while grounding operational details in the bundled reference files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installers recommend direct remote script execution and configure unattended daily updates from a mutable branch.

Mitigation: Review the installer before use, prefer a pinned release or reviewed local copy, and avoid or remove the default cron job or Windows Scheduled Task unless unattended future updates are acceptable.

Risk: Restaurant details such as prices, promotions, allergens, delivery terms, and hours can become stale or be answered incorrectly if the reference files are unavailable.

Mitigation: Keep the bundled reference files current and readable at query time, and confirm time-sensitive promotions or safety questions with the restaurant when accuracy matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liubuq-sys/skills/daozheji-grill-skill)
- [Business information](artifact/references/business-info.md)
- [Menu and services](artifact/references/services.md)
- [Promotions](artifact/references/promotions.md)
- [FAQ](artifact/references/faq.md)
- [Brand information](artifact/references/brand.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Natural-language Markdown responses grounded in bundled reference files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the restaurant reference files to be readable at query time.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact CHANGELOG.md and version.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
