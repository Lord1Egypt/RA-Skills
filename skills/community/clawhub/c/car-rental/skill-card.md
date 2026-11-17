## Description:

Find the best car rental deals with price comparison, alerts, and lease vs rent analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to compare car rental, lease, subscription, and buy options; track preferences; and monitor price or availability alerts with permission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and maintain local preference, search, alert, and rental-history files.

Mitigation: Create or update files under ~/car-rental/ only after user permission, and keep the files reviewable and removable by the user.

Risk: Price monitoring or broad travel-triggered help could create ongoing assistant behavior the user does not want.

Mitigation: Enable alerts only when explicitly requested, confirm alert frequency and thresholds, and allow the user to disable alerts at any time.

Risk: Rental searches send trip criteria such as location, dates, and car type to rental sites as part of normal comparison.

Mitigation: Use only the search criteria needed for comparison and avoid account credentials, payment information, or personal identifiers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/car-rental)
- [Skill homepage](https://clawic.com/skills/car-rental)
- [setup.md](artifact/setup.md)
- [memory-template.md](artifact/memory-template.md)
- [sites.md](artifact/sites.md)
- [comparison.md](artifact/comparison.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with optional local memory and saved-search file structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can propose local files under ~/car-rental/ and periodic alert settings only with user permission.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
