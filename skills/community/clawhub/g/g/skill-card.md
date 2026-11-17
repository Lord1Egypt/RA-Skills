## Description:

Google全家桶入口 is a Chinese-language launcher that helps agents list, search, categorize, and open official Google and YouTube service links from a bundled product catalog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgta23](https://clawhub.ai/user/hgta23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ClawHub users can use this skill as a Chinese-language shortcut menu for quickly finding and opening common Google services across search, communication, office, maps, entertainment, and tools categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The short invocation name "g" may be triggered unintentionally.

Mitigation: Confirm intent before using the launcher or opening a selected service.

Risk: Opening a product navigates the user's browser to Google or YouTube services where normal account, session, and external-site behavior applies.

Mitigation: Review the destination URL before opening and use the relevant Google account and privacy settings for the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hgta23/skills/g)
- [Bundled product catalog](artifact/products.json)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Console text with product names, descriptions, categories, and URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May open selected official Google or YouTube URLs in the user's browser.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
